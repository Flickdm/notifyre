from flask import Flask

app = None
hw = None

def create_app(hardware, app_name):
    app = Flask(app_name)
    hw = hardware

    from . import views
    app.register_blueprint(views.main)

    return app
