from flask import Flask
from Controllers.GameController import *
from database import db, DatabaseInit

app = Flask(__name__)

# Config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'

# Database
db.init_app(app)
database_init = DatabaseInit(db)

# Controllers
game_controller = GameController(db)


# Routes
@app.route('/')
def index():
    return game_controller.index_action()


@app.route('/new', methods=['GET', 'POST'])
def new():
    return game_controller.new_action()


@app.route('/play', methods=['GET', 'POST'])
def play():
    return game_controller.play_action()


@app.route('/statistics')
def statistics():
    return game_controller.statistics_action()


# Database
with app.app_context():
    database_init.create_database()

# Startup
if __name__ == '__main__':
    app.run()
