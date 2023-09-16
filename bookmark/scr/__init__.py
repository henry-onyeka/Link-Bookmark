from flask import Flask,redirect,jsonify
from scr.database import Bookmark,db
from scr.auth import auth
from scr.bookmark import bookmarks
import os
from scr.config.swagger import template, swagger_config
from flasgger import Swagger,swag_from
from scr.constants.http_status import HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND
from flask_jwt_extended import jwt_manager,JWTManager
'''swagfrom enables us create a yaml file'''
def create_app(test_config=None):
    """a function to set up our app,
    create some config 
    and return it to us

    """
    app=Flask(__name__,instance_relative_config=True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRETE_KEY"),
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQALCHEMY_DB_URI"),
             JWT_SECRET_KEY = os.environ.get('JWT_SECRETE_KEY'),
             SQLALCHEMY_TRACK_MODIFICATIONS =False,
             SWAGGER ={
                 'title':"Bookmark API",
                 'uiversion':3
             }
        )
    else:
         app.config.from_mapping(
            test_config
        )
         
    db.app=app
    db.init_app(app)
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    JWTManager(app)
    Swagger(app,config=swagger_config,template=template)
    @app.get("/")
    def index():
        """define the function of the action you want to do once the route is created"""
        return "HOW ARE YOU THIS MORNING "+ " " 
    """ s"""
 

   
    @app.get("/<shorturl>")
    @swag_from('./docs/shorturl.yml')
    def numberOfVisits(shorturl):
        '''implementing how may times a user visits a link'''
        bookmark= Bookmark.query.filter_by(shorturl=shorturl).first_or_404()
        if bookmark:
            bookmark.visits =bookmark.visits+1
            db.session.commit()

            return redirect(bookmark.url)
    
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def errhand(e):
        return jsonify({"error":"Not found"}),HTTP_404_NOT_FOUND

    return app

