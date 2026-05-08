import flask
import json
import dataservice
import os
from flask import jsonify
from flask import request

#from flask_jwt_extended import create_access_token
#from flask_jwt_extended import verify_jwt_in_request
#from flask_jwt_extended import get_jwt_identity
#from flask_jwt_extended import jwt_required
#from flask_jwt_extended import JWTManager



#old code referenced from securityintro livecoding 
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

import functools

def require_basic_auth(f):
    @functools.wraps(f)
    def wrap(**kwargs):
        auth = flask.request.authorization

        if auth is not None and auth.get("username") == "abc" and auth.get("password") == '1234':
            return f(**kwargs)
        else:
            return flask.Response(status="401 Unauthorized", 
                              headers={"WWW-Authenticate": "Basic realm='Shopping cart'"})
    return wrap

@app.get("/list")
@require_basic_auth
def get_list():
    return flask.Response(status="200 OK", 
                            headers={"Content-Type": "application/json"}, 
                            response = json.dumps(dataservice.get_shopping_list()))


     
@app.post("/list/<item>")
@require_basic_auth
def post_list_item(item):
    dataservice.add_item_to_list(item)
    return flask.Response(status="201 Created",
                          headers={"Content-Type": "application/json"},
                          response = json.dumps(dataservice.get_shopping_list()))


@app.post("/list/image")
@require_basic_auth
def add_image_to_item():
    item = flask.request.form['itemWithImageName']
    filepath = process_image_file(flask.request)
    if filepath is None:
        dataservice.add_item_to_list(item)
    else:
        # need to replace public/ because the final serving path is relative
        # to the html file, not the server. 
        dataservice.add_item_with_image(item, filepath.replace("public/",""))
    return flask.redirect("/shopping.html")


@app.patch("/list/<item>")
@require_basic_auth
def patch_list_item(item):
    dataservice.move_item_between_lists(item)
    return flask.Response(status="200 OK",
                          headers={"Content-Type": "application/json"},
                          response = json.dumps(dataservice.get_shopping_list()))


@app.delete("/list/<item>")
@require_basic_auth
def delete_list_item(item):
    dataservice.remove_item(item)
    return flask.Response(status="200 OK",
                          headers={"Content-Type": "application/json"},
                          response = json.dumps(dataservice.get_shopping_list()))



# File Processing Code Below

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
