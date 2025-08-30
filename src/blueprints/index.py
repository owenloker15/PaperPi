from flask import render_template, Blueprint

from config.configuration import get_configuration_helper

main_bp = Blueprint("main", __name__)

@main_bp.route('/')
def index():
    configuration = get_configuration_helper()
    return render_template("index.html", plugins=configuration.get_plugins())
    
