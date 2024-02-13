from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sides = db.Column(db.Integer)
    rolls = db.Column(db.String)
