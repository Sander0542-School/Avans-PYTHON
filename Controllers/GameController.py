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

            if int(positions) > int(colors):
                positions = colors

            ingame_pins = self.get_pins('', int(colors))

            player = Player(username)
            db.session.add(player)
            db.session.commit()

            game = Game(player.id, positions, colors, code, pins)

            db.session.add(game)
            db.session.commit()

            return redirect(url_for('play', player_id=player.id, game_id=game.id))

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
