from Database import db

class User(db.model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)

    def __init__(self, username):
        self.username = username
