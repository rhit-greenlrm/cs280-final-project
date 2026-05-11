import os
import json
import flask
import functools
import dataservice
from flask import jsonify
from flask import request
#from flask_jwt_extended import JWTManager TODO
#from flask_jwt_extended import jwt_required TODO
#from flask_jwt_extended import get_jwt_identity TODO
#from flask_jwt_extended import create_access_token TODO
#from flask_jwt_extended import verify_jwt_in_request TODO

#code referenced from securityintro livecoding 
from werkzeug.utils import secure_filename
IMAGE_FOLDER = 'public/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = flask.Flask(__name__,
            static_url_path='',
            static_folder='public',)

app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

@app.get("/shutdown")
def shutdown():
    os._exit(0)


#TODO remove unused imports
#TODO replace commented lines/functions with versions for animal profiles
#TODO reference rest api plan for accuracy 

#TODO set up employee vs regular user logins 
def require_basic_auth(f):
    @functools.wraps(f)
    def wrap(**kwargs):
        auth = flask.request.authorization

#         if auth is not None and auth.get("username") == "abc" and auth.get("password") == '1234':
#             return f(**kwargs)
#         else:
#             return flask.Response(status="401 Unauthorized", 
#                               headers={"WWW-Authenticate": "Basic realm='Shopping cart'"})
    return wrap

@app.get("/list")
@require_basic_auth 
def get_profiles():
    return flask.Response(status="200 OK", 
                            headers={"Content-Type": "application/json"}, 
                            response = json.dumps(dataservice.get_profile_list()))


#TODO create get function to get statistics

#TODO make this the main upload for image and data
@app.post("/list/profile")
@require_basic_auth
def add_profile_to_list():
#     item = flask.request.form['itemWithImageName']
    filepath = process_image_file(flask.request)
#     if filepath is None: TODO  remove since imag eis required?
#         dataservice.add_item_to_list(item)
#     else:
#         # need to replace public/ because the final serving path is relative
#         # to the html file, not the server. 
#         dataservice.add_item_with_image(item, filepath.replace("public/",""))
    return flask.redirect("/employee_action.html")


#TODO change to allow editing of animal data
@app.patch("/list/<profile>")  #TODO check format?
@require_basic_auth
def update_profile(profile):
    dataservice.update_profile_data(profile)
    return flask.Response(status="200 OK",
                          headers={"Content-Type": "application/json"},
                          response = json.dumps(dataservice.get_profile_list()))


#TODO complete patch function to allow user prefernce changing
@app.patch("") #TODO ??? need to settle list/db place for user preferences
@require_basic_auth
def update_user_preferences(): #TODO determine correct parameter (user data/profile?)
    #TODO complete
    return flask.Response(status="200 OK",
                          headers={"Content-Type": "application/json"},
                          response = json.dumps(dataservice.get_profile_list())) #TODO change response????


@app.delete("/list/<profile>")
@require_basic_auth 
def delete_profile(profile):
    dataservice.remove_profile(profile)
    return flask.Response(status="200 OK",
                          headers={"Content-Type": "application/json"},
                          response = json.dumps(dataservice.get_profile_list()))

# File Processing Code (referenced from securityintro)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image_file(request):
    # check if the post request has the file part
    if 'imageData' not in request.files:
        return None
    file = request.files['imageData']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['IMAGE_FOLDER'], filename)
        print(os.getcwd())
        file.save(filepath)
        return filepath


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
