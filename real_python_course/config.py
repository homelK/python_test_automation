import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# get path to base dir of the project
basedir = pathlib.Path(__file__).parent.resolve()

# get FlaskApp instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# get Flask app instance
app = connex_app.app

# configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'people.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)