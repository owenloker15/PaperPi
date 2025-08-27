from flask import current_app, render_template, Blueprint

main_bp = Blueprint("main", __name__)

@main_bp.route('/')
def index():
    return render_template("index.html")
