from flask import request, render_template, redirect, url_for
import sqlite3 as sqlite

from sqlalchemy import func

from database import Player, db, Game, Pin


class StatisticController:
    def __init__(self, db):
        self.db = db

    def index_action(self):
        number_of_games_won = Game.query.filter_by(winner=True).count()
        top_five_wins = Game.query.filter_by(winner=True).group_by(Game.player_id).limit(5).all()
        top_five_fastest_wins = db.session.query(Game.player_id, func.count(Game.player_id)).join(Game.pins).group_by(Game.player_id).all()

        return render_template('game/statistics.html', number_of_games_won=number_of_games_won,
                               top_five_wins=top_five_wins,
                               top_five_fastest_wins=top_five_fastest_wins)
