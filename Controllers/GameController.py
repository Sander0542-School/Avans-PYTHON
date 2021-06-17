import logging

from flask import request, render_template, redirect, url_for

from database import Player, db, Game, Pin

import random


class GameController:
    def __init__(self, db):
        self.db = db

    def index_action(self):
        return render_template('game/index.html')

    def new_action(self):
        if request.method == 'GET':
            return render_template('game/new.html')
        elif request.method == 'POST':
            username = request.form['username']
            positions = request.form['positions']
            colors = request.form['colors']
            double_colors = request.form.get('double_colors')

            if int(positions) > int(colors):
                positions = colors

            if int(positions) > int(colors) and not double_colors:
                positions = colors

            game_pins = self.get_pins('', int(colors))

            if double_colors:
                double_colors = 1

            try:
                player = Player.query.filter_by(username=username).one()

                logging.info(player)
            except:
                player = Player(username)
                db.session.add(player)
                db.session.commit()

            if double_colors:
                code_tuple = random.choices(game_pins, k=int(positions))
            else:
                code_tuple = random.sample(game_pins, int(positions))

            code_ids = []
            for pin in code_tuple:
                code_ids.append(str(pin.id))

            pin_ids = []
            for pin in game_pins:
                pin_ids.append(str(pin.id))

            code = ' '.join(code_ids)
            pins = ' '.join(pin_ids)

            game = Game(player.id, positions, double_colors, colors, code, pins)

            db.session.add(game)
            db.session.commit()

            return redirect(url_for('play', game_id=game.id))

    def play_action(self):
        return

    def statistics_action(self):
        return

    def get_pins(self, id, colors):
        if id != '':
            pins = []
            game = Game.query.get(id)
            for color in game.ingame_colors.split(' '):
                pins.append(Pin.query.get(str(color)))

            return pins
        else:
            all_pins = []
            for pin in db.session.query(Pin).all():
                all_pins.append(pin)
            return random.sample(all_pins, int(colors))
