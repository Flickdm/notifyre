from flask import Flask

app = None

def create_app(app_name):
    app = Flask(app_name, template_folder='WEB/templates')

    from . import views
    app.register_blueprint(views.main)

    return app
