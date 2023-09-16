from flask import Blueprint,Request,request,jsonify
import validators
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import get_jwt_identity
from scr.database import Bookmark,db
from scr.constants.http_status import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_201_CREATED,HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED,HTTP_200_OK,HTTP_404_NOT_FOUND
bookmarks =Blueprint("bookmarks",__name__,url_prefix="/api/vi/bookmarks")

@bookmarks.route('/',methods=['POST','GET'])
@jwt_required()
def  get_them():
    '''jwt required runs this function to only the current user'''
    currentuser =get_jwt_identity()

    if request.method == 'POST':
        body = request.get_json().get('body','')
        url = request.get_json().get('url','')
        '''to check if the url is valid, we use validator'''
        if not validators.url(url):
           return jsonify({
            "ERROR":"not a valid url"
        }),HTTP_400_BAD_REQUEST
        '''check if the url aready exist in the database'''

        if Bookmark.query.filter_by(url=url).first():
               return jsonify({
            "ERROR":"this is an already existing url"
        }),HTTP_409_CONFLICT
        '''to get the current user ogged in, 
        we use the get_jwt_identity()
        '''
        boom=Bookmark(body=body,url=url,user_id=currentuser)
        db.session.add(boom)
        db.session.commit()
        return jsonify({
                "ID":boom.id,
                "URL": boom.url,

                "SHORTURI":boom.shorturl,
                "BODY":boom.body,
                "VISITS":boom.visits,
                "CREATED-AT":boom.created_at,
                "UPDATED_AT":boom.updated_at
            }),HTTP_201_CREATED
    else:
        '''implement pagination'''
        page  = request.args.get('page',1,type=int)
        per_page =request.args.get('per_page',2,type=int)

        booms = Bookmark.query.filter_by(user_id=currentuser).paginate(page=page,per_page=per_page)
        data=[]
        for boom in booms.items:
            data.append({
                   
                "ID":boom.id,
                "URL": boom.url,

                "SHORTURI":boom.shorturl,
                "BODY":boom.body,
                "VISITS":boom.visits,
                "CREATED-AT":boom.created_at,
                "UPDATED_AT":boom.updated_at
                  })
            
        meta = {
                 "page": booms.page,
                  "pages": booms.pages,
                   "totale": booms.total,
                    "prevPage": booms.prev_num,
                     "nextPage": booms.next_num,
                      "has prev": booms.has_prev,
                       "has next": booms.has_next,

            }    

    return {"DATA" :data ,"Meta":meta}


"""
creating how to rerieve singe item in a page
and we'll be getting it by the /id  so we are using <int/id> in the endpoint
    """
@bookmarks.get('<int:id>')
@jwt_required()
def  me(id):
    currentuser =get_jwt_identity()
    ''' lets querry the database to certify the current user is the one logged in'''
    bookm =Bookmark.query.filter_by(user_id=currentuser, id=id).first()
    if not bookm:
        return jsonify({
            "Message":" Not Found"
        }),HTTP_404_NOT_FOUND
    
    return jsonify({
                "ID":bookm.id,
                "URL": bookm.url,

                "SHORTURI":bookm.shorturl,
                "BODY":bookm.body,
                "VISITS":bookm.visits,
                "CREATED-AT":bookm.created_at,
                "UPDATED_AT":bookm.updated_at
            }),HTTP_200_OK
'''to edit and perform changes in the dtatbase'''
@bookmarks.put('<int:id>')
@bookmarks.patch('<int:id>')
@jwt_required()
def worm(id):
    currentuser =get_jwt_identity()
    ''' lets querry the database to certify the current user is the one logged in'''
    bookm =Bookmark.query.filter_by(user_id=currentuser, id=id).first()
    if not bookm:
        return jsonify({
            "Message":"  Not Found"
        }),HTTP_404_NOT_FOUND
    body = request.get_json().get('body','')
    url = request.get_json().get('url','')
    '''to check if the url is valid, we use validator'''
    if not validators.url(url):
           return jsonify({
            "ERROR":"not a valid url"
        }),HTTP_400_BAD_REQUEST
    bookm.body=body
    bookm.url=url
    db.session.commit()
    return jsonify({
            "Body":bookm.body,
            "url" :bookm.url
        }),HTTP_200_OK

@bookmarks.delete('<int:id>')
@jwt_required()
def remove(id):
    currentuser =get_jwt_identity()
    ''' lets querry the database to certify the current user is the one logged in'''
    bookm =Bookmark.query.filter_by(user_id=currentuser, id=id).first()
    if not bookm:
        return jsonify({
            "Message":"  Not Found"
        }),HTTP_404_NOT_FOUND
    db.session.delete(bookm)
    db.session.commit()

    return jsonify({}),HTTP_204_NO_CONTENT


@bookmarks.get('/stats')
@jwt_required()
def  statistics():
    currentUser= get_jwt_identity()
    data=[]
    items = Bookmark.query.filter_by(user_id=currentUser).all()
    for item in items:
        trackLink={
            #"USER":item.email,
            "url": item.url,
            "Site checkouts":item.visits,
            "Short Url": item. shorturl,
            "ID":item.id
        }
        data.append(trackLink)
    return jsonify({"Data":data}),HTTP_200_OK