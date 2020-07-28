from flask import Blueprint ,request,render_template
from bl.wrap import checkUser

plugin = Blueprint('setting', __name__)