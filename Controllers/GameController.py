from pprint import pprint
from urllib.parse import urlparse, parse_qs

from flask import request, render_template, redirect, url_for

from database import Player, db, Game, Pin, GamePin

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
            username = request.form.get('username')
            positions = request.form.get('positions')
            colors = request.form.get('colors')
            double_colors = False if request.form.get('double_colors') is None else True

            if int(positions) > int(colors) and not double_colors:
                positions = colors

            game_pins = self.get_pins('', int(colors))

            try:
                player = Player.query.filter_by(username=username).one()
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
        game_id = request.args.get('game_id')
        cheat_mode = False if request.args.get('cheat_mode') is None else True

        game = Game.query.get(game_id)

        current_turn = -1
        for pin in game.pins:
            if current_turn < pin.turn:
                current_turn = pin.turn
        current_turn = current_turn + 1

        code_pins = self.get_pins_from_array(game.code)

        if request.method == 'GET':
            placed_pins = {}
            for pin in game.pins:
                placed_pins.setdefault(pin.turn, []).append(pin)

            game_pins = self.get_pins(game.id, game.colors)

            turn_stats = {}
            for turn, pins in placed_pins.items():
                turn_stats.setdefault(turn, [])

                for position, code_pin in enumerate(code_pins):
                    if code_pin.color == pins[position].pin.color:
                        turn_stats[turn].append('black')
                    elif self.color_in_pins(pins, code_pin.color):
                        turn_stats[turn].append('white')

                turn_stats[turn].sort()

            return render_template('game/play.html', game=game, current_turn=current_turn, placed_pins=placed_pins,
                                   game_pins=game_pins, code_pins=code_pins, turn_stats=turn_stats,cheat_mode=cheat_mode)
        elif request.method == 'POST':
            pins = self.get_request_pins(game)

            for pin in pins:
                game_pin = GamePin(game.id, pin.id, current_turn)
                db.session.add(game_pin)

            db.session.commit()

            if self.pins_match(pins, code_pins):
                game.winner = True
                db.session.commit()
            elif current_turn >= 9:
                game.winner = False
                db.session.commit()

            return redirect(url_for('play', game_id=game.id))

    def statistics_action(self):
        return

    def get_pins(self, id, colors):
        if id != '':
            pins = []
            game = Game.query.get(id)
            for pin_id in game.ingame_colors.split(' '):
                pins.append(Pin.query.get(str(pin_id)))

            return pins
        else:
            all_pins = []
            for pin in db.session.query(Pin).all():
                all_pins.append(pin)
            return random.sample(all_pins, int(colors))

    def get_pins_from_array(self, pin_ids):
        pins = []
        for pin_id in pin_ids.split(' '):
            pins.append(Pin.query.get(str(pin_id)))

        return pins

    def color_in_pins(self, pins, color):
        for pin in pins:
            if pin.pin.color == color:
                return True

        return False

    def get_request_pins(self, game):
        pin_ids = []

        for position in range(0, game.positions):
            pin_ids.append(request.form[f'pins[{position}]'])

        return self.get_pins_from_array(' '.join(pin_ids))

    def pins_match(self, pins1, pins2):
        for index, pin1 in enumerate(pins1):
            if pin1.id != pins2[index].id:
                return False

        return True

