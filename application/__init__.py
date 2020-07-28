from flask import Flask


app=Flask(__name__,template_folder='../templates',static_folder="../static")

from config.db_config import SQLALCHEMY_DATABASE_URI,SQLALCHEMY_TRACK_MODIFICATIONS
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI']=SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)

from application.plugins import index_plugin,\
                                explore_plugin,\
                                query_plugin,\
                                plan_plugin,\
                                setting_plugin,\
                                review_plugin

app.register_blueprint(index_plugin.plugin)
app.register_blueprint(explore_plugin.plugin)
app.register_blueprint(query_plugin.plugin)
app.register_blueprint(plan_plugin.plugin)
app.register_blueprint(setting_plugin.plugin)
app.register_blueprint(review_plugin.plugin)