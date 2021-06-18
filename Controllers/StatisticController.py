from flask import render_template

from database import db, Game


class StatisticController:
    def __init__(self, db):
        self.db = db

    def index_action(self):
        with db.engine.connect() as conn:
            games_won = Game.query.filter_by(winner=True).count()
            games_lost = Game.query.filter_by(winner=False).count()
            games_playing = Game.query.filter_by(winner=None).count()

            top_five_players = conn.execute('SELECT player.username, COUNT(game.id) as wins FROM player INNER JOIN game on player.id = game.player_id WHERE game.winner is true GROUP BY game.player_id ORDER BY wins DESC LIMIT 5;')
            top_five_most_games = conn.execute('SELECT player.username, COUNT(game.id) as games FROM player INNER JOIN game on player.id = game.player_id GROUP BY game.player_id ORDER BY games DESC LIMIT 5;')
            top_five_fastest_wins = conn.execute('SELECT player.username, MAX(game_pin.turn) + 1 as turns FROM game INNER JOIN game_pin ON game.id = game_pin.game_id INNER JOIN player ON game.player_id = player.id WHERE game.winner is true GROUP BY game.id ORDER BY turns LIMIT 5;');

            return render_template('statistics/index.html', games_won=games_won,
                                   games_lost=games_lost,
                                   games_playing=games_playing,
                                   top_five_players=top_five_players,
                                   top_five_most_games=top_five_most_games,
                                   top_five_fastest_wins=top_five_fastest_wins
                                   )
