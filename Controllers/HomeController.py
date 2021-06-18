from flask import request, render_template, redirect, url_for

from database import Player, db, Game, Pin


class HomeController:
    def __init__(self, db):
        self.db = db

    def index_action(self):
        return render_template('home/index.html')
