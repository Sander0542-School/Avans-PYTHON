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

            for pin in pins:
                self.db.session.add(Pin(color=pin))

            self.db.session.commit()


game_pin = db.Table('game_pin',
                    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                    db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
                    db.Column('pin_id', db.Integer, db.ForeignKey('pin.id')),
                    db.Column('turn', db.Integer, nullable=False),
                    db.Column('correct', db.String, nullable=False)
                    )


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer, nullable=False)
    positions = db.Column(db.Integer, nullable=False, default=6)
    colors = db.Column(db.Integer, nullable=False, default=6)
    winner = db.Column(db.Boolean, nullable=True)
    code = db.Column(db.String(20), nullable=True)
    ingame_colors = db.Column(db.String(40), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, player_id, positions, colors, code, ingame_colors):
        self.player_id = player_id
        self.positions = positions
        self.colors = colors
        self.code = code
        self.ingame_colors = ingame_colors


class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    color = db.Column(db.String, nullable=False)
    games = db.relationship('Game', secondary=game_pin, backref=db.backref('board_pins', lazy='dynamic'))

    def __init__(self, color):
        self.color = color


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    games = db.relationship('Game')

    def __init__(self, name):
        self.username = name
