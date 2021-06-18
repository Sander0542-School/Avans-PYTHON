from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class DatabaseInit:
    def __init__(self, db):
        self.db = db

    def create_database(self):
        try:
            open('game.db')

        except IOError:
            self.db.create_all()

            pins = [
                'red',
                'blue',
                'green',
                'yellow',
                'white',
                'black',
                'orange',
                'brown',
                'magenta',
                'purple',
            ]

            for color in pins:
                self.db.session.add(Pin(color))

            self.db.session.commit()


class GamePin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    pin_id = db.Column(db.Integer, db.ForeignKey('pin.id'), nullable=False)
    turn = db.Column(db.Integer, nullable=False)
    pin = db.relationship('Pin')

    def __init__(self, game_id, pin_id, turn):
        self.game_id = game_id
        self.pin_id = pin_id
        self.turn = turn


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    positions = db.Column(db.Integer, nullable=False, default=6)
    colors = db.Column(db.Integer, nullable=False, default=6)
    double_colors = db.Column(db.Boolean, nullable=False, default=False)
    winner = db.Column(db.Boolean, nullable=True)
    code = db.Column(db.String(20), nullable=True)
    ingame_colors = db.Column(db.String(40), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    pins = db.relationship('GamePin')
    player = db.relationship('Player')

    def __init__(self, player_id, positions, double_colors, colors, code, ingame_colors):
        self.player_id = player_id
        self.positions = positions
        self.double_colors = double_colors
        self.colors = colors
        self.code = code
        self.ingame_colors = ingame_colors


class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    color = db.Column(db.String, nullable=False)

    def __init__(self, color):
        self.color = color


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.username = name
