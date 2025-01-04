from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance/market.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications to suppress warnings
app.config['SECRET_KEY'] = 'abddb702bfdef0f238c0023e'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Define CLI commands
@app.cli.command("reset-db")
def reset_db():
    """Drops all tables and recreates them."""
    with app.app_context():
        db.drop_all()
        print("All tables dropped!")
        db.create_all()
        print("Database and tables recreated!")

# Ensure database and tables are created at startup
if not os.path.exists("instance/market.db"):
    with app.app_context():
        db.create_all()
        print("Database and tables created!")

from market import routes


if __name__ == "__main__":
    app.run(debug=True)