from flask import Flask
from flask_login import LoginManager
app = None

def create_app(app_name):
    app = Flask(
        app_name,
        template_folder='WEB/templates',
        static_folder='WEB/static'
        )

    from . import views
    app.register_blueprint(views.main)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.do_admin_login'

    return app
