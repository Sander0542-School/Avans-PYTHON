from flask import Flask
from Controllers.GameController import *
from Controllers.HomeController import *
from Controllers.StatisticController import *
from database import db, DatabaseInit

app = Flask(__name__)

# Config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://avans_python:kQNEYAeB2dLP3Cnn@10.10.11.20:3306/avans_python'

# Database
db.init_app(app)
database_init = DatabaseInit(db)

# Controllers
game_controller = GameController(db)
home_controller = HomeController(db)
statistic_controller = StatisticController(db)

# Routes
@app.route('/')
def index():
    return home_controller.index_action()


@app.route('/new', methods=['GET', 'POST'])
def new():
    return game_controller.new_action()


@app.route('/play', methods=['GET', 'POST'])
def play():
    return game_controller.play_action()


@app.route('/statistics')
def statistics():
    return statistic_controller.index_action()


# Database
with app.app_context():
    database_init.create_database()

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

# Startup
if __name__ == '__main__':
    app.run()
