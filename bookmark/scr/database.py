from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
db = SQLAlchemy()




class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(99), nullable=False,unique=True)
    email = db.Column(db.String(50), nullable=False   ,unique=True)
    sex = db.Column(db.String(50), nullable=False)
    password =  db.Column(db.Text(), nullable=False )
    created_at=db.Column(db.DateTime,default=datetime.now())
    updated_at=db.Column(db.DateTime,onupdate=datetime.now())

    def __repr__(self)->str:
        return f'USER---- {self.username}'
    
class  Bookmark(db.Model):
    """cass that generates a tabe in the Bookmark data base 
    """
    


    id= db.Column(db.Integer, primary_key=True)
    body= db.Column(db.Text, nullable=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    url= db.Column(db.Text,nullable =False)
    shorturl= db.Column(db.Text, nullable=True)
    visits= db.Column(db.Integer, default=0)
    created_at=db.Column(db.DateTime,default=datetime.now())
    updated_at=db.Column(db.DateTime,onupdate=datetime.now())
    
    def generate_character(self):
       """a function that generates random number from 0-9
       and aphabets from a-z using the random and the string module imported
       string.digits returns 0-9
       random dot choices generates random chars accordding to the size characters
       passed as the arguments
       dot oin arguments convert it to a string

                   """
       characters= string.digits+string.ascii_letters
       picked_char= "".join(random.choices(characters, k=7))
       link=Bookmark.query.filter_by(shorturl=picked_char).first()

       if link:
           self.generate_character()
       else:
           return picked_char

    def __init__(self,**kwargs)->None:
        super().__init__(**kwargs)
        self.shorturl= self.generate_character()





    def __repr__(self)->str:
        return f'BOOKMARK---- {self.url}'
    
   


