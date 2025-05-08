from flask import render_template
from flask_login import LoginManager
from config import app
from user.views import user_bp
from data_entry.views import data_entry_bp
from education.views import education_bp
from game.views import game_bp
from database.tables import User
from graph_analysis.views import graph_analysis_bp

# Blueprint registration
app.register_blueprint(user_bp)
app.register_blueprint(data_entry_bp)
app.register_blueprint(education_bp)
app.register_blueprint(game_bp)
app.register_blueprint(graph_analysis_bp)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"
login_manager.login_message = "You need to Login to Access this Page"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(ssl_context=("cert.pem", "key.pem"))
