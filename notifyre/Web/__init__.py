from flask import Flask
from flask_login import LoginManager
app = None

def create_web_app(app_name):
    app = Flask(
        app_name,
        template_folder='notifyre/Web/templates',
        static_folder='notifyre/Web/static'
        )

    from . import views
    app.register_blueprint(views.main)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.do_admin_login'

    return app
