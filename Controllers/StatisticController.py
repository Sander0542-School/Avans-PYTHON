from flask import request, render_template, redirect, url_for
import sqlite3 as sqlite

from database import Player, db, Game, Pin


class StatisticController:
    def __init__(self, db):
        self.db = db

    def index_action(self):
        games = Game.query.all()
        topFiveWins = Game.query.filter_by(winner=True).group_by(Game.player_id).limit(5).all()

        return render_template('game/statistics.html', games=allWins)
