from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
admin = Admin(app,template_mode='bootstrap3')

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    age = db.Column(db.Integer)
    birthday = db.Column(db.DateTime)
    comments = db.relationship('Comment',backref='user',lazy='dynamic')

    def __repr__(self):
        return 'User: {}'.format(self.username)

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    comment_text = db.Column(db.String(200))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Comment %r>' % (self.id)

admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Comment,db.session))

if __name__ == "__main__":
    app.run(debug=True)
