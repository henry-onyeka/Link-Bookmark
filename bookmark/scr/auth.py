from flask import Blueprint,request,jsonify
from scr.constants.http_status import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_201_CREATED, HTTP_401_UNAUTHORIZED,HTTP_200_OK
from werkzeug.security import generate_password_hash , check_password_hash
import validators
from flasgger import Swagger,swag_from
from scr.database import User,db
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required,get_jwt_identity
'''the request modue is used to get what is sent in a post request''' 
"""the   generate_password_hash , check_password_hash module encrypts passwords"""


auth =Blueprint("auth",__name__,url_prefix="/api/vi/auth")

@auth.post('/register')
@swag_from('./docs/auth/register.yml')
def  register():
    '''creating a resource on the sever and instantiate our database
    creating a user account and storing the detais in the database
    '''
    Fex = request.json['sex']
    username=request.json['username']
    password=request.json['password']
    email=request.json['email']
    if not Fex:
        return jsonify({'Error': 'Enter your gender'}),HTTP_400_BAD_REQUEST


    if not username.isalnum() or " " in username:
        return jsonify({'Error': 'username must contain alphabets and also numbers but not whitespace'}),HTTP_400_BAD_REQUEST

    if len(password) < 6:
        return jsonify({'Error': 'password is too short'}),HTTP_400_BAD_REQUEST

    if len(email) < 3:
        return jsonify({'Error': 'email is too short'}),HTTP_400_BAD_REQUEST
    if not validators.email(email):
        return jsonify({'Error': 'email is invalid'}),HTTP_409_CONFLICT
    if User.query.filter_by(email=email).first() is not None:
         return jsonify({'Error': 'email  exists'}),HTTP_409_CONFLICT
    

    if User.query.filter_by(username=username).first() is not None:
         return jsonify({'Error': 'username exists'}),HTTP_409_CONFLICT
    pwd=generate_password_hash(password)
    user=User(username=username,password=pwd,email=email,sex=Fex)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'Message': 'Account Successfully Created',
        "user":{'USERNAME ': username ," EMAIL": email
        }
        }),HTTP_201_CREATED
        
    return 'USER CREATED'

@auth.post('/login')
@swag_from('./docs/auth/login.yml')
def login():
    '''to authenticate email and user password for access via the login '''
    password = request.json.get('password','') 
    '''add an empty string so it wont crash'''
    email= request.json.get('email','')

    ''' to check if the emai entered exists in the database'''
    fed = User.query.filter_by(email=email).first()
    #pad = User.query.filter_by(password=password)

    if fed :
        correctpass = check_password_hash(fed.password, password)
        if correctpass:
            refresh = create_refresh_token(identity=fed.id)
            access = create_access_token(identity=fed.id)
            '''here you can grant access to a home page hence the 
            user has been confirmed to exist in the database
            '''
            return jsonify({
                "user":{
                    "Refresh":refresh,
                    "Access": access,
                    "UserName": fed.username,
                    "Email": fed.email
                }


            }),HTTP_200_OK
    return     jsonify({
        "ERROR":"email or password incorrect"
    }), HTTP_401_UNAUTHORIZED

    


   
'''using  jwt_required  before the main end point denies access
to the endpoint without  token
'''
@auth.get('/me')
@jwt_required()
def  me():
    '''import pdb
    a debugger which enabes inspection of functions and 
    variabes after posting
    pdb.set_trace()
    '''
    userid = get_jwt_identity()
    USS = User.query.filter_by(id=userid).first()

    return jsonify({"USERNAME":USS.username,
          "EMAIL":USS.email         
                    }),HTTP_200_OK

@auth.get('/token/refresh')
@jwt_required(refresh=True)
def  refr():
    idd = get_jwt_identity()
    access = create_access_token(identity=idd)

    return jsonify({"ACCESS":access                 
                    }),HTTP_200_OK
