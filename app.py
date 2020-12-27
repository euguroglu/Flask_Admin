from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
from flask_admin.contrib.fileadmin import FileAdmin


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

#If i want to adjust admin view
class UserView(ModelView):
    #if i want to delete one column from view
    column_exclude_list = ['password']
    #if i want to display primary key
    column_display_pk = True
    #if i want to export data
    can_export = True
    #if i want to be able to modify or create new comment using admin view
    inline_models = [Comment]
    #if we set below function false user view wont be there we can set some functionality to authenticate someone to see that panel
    def is_accessible(self):
        return True
    #This is comment when someone try to see admin/user page without authenticated.
    def inaccessible_callback(self,name,**kwargs):
        return '<h1>You are not logged in</h1>'

class CommentView(ModelView):
    #To change create model page as pop-up window
    create_modal = True

admin.add_view(UserView(User,db.session))
admin.add_view(CommentView(Comment,db.session))

#Flask admin file view
path = os.path.join(os.path.dirname(__file__),'uploads')
admin.add_view(FileAdmin(path,'/uploads/',name='Uploads'))

if __name__ == "__main__":
    app.run(debug=True)
