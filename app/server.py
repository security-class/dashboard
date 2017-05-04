from . import app

import os
import requests
import cgi
from redis import Redis
from redis import ConnectionError
from flask_api import status
from flask import Flask, Response, jsonify, request, json, url_for, make_response

HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

form = cgi.FieldStorage()

@app.route('/')
def index():
  return app.send_static_file('reg.html')


@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password_1']
    conf_password = request.form['password_2']
    message = {"Hello":"World"}
    user_info = {'email': email, 'first_name': first_name, 'last_name': last_name }
    data = { 'user_info': user_info, 'password':password }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    print(json.dumps(data))
    result = requests.post("https://pcs-sam-auth.mybluemix.net/users", json = data)
    # result = requests.post("https://pcs-sam-auth.mybluemix.net/users", data= { "user_info": user_info , "password":password })
    print(result.status_code, result.reason)
    return make_response(jsonify(message), HTTP_200_OK)


def init():
    return
