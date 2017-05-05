import json
import os
import requests

import cgi
from jose import jwt
from flask_api import status
from flask import Flask, Response, jsonify, request, json, url_for, make_response, redirect, render_template
from werkzeug.exceptions import NotFound, Unauthorized

from . import app

form = cgi.FieldStorage()
auth_server_base = "https://pcs-sam-auth.mybluemix.net"
vault_server_base = "http://pcs-sam-vault.mybluemix.net"

@app.route('/')
def index():
  return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return app.send_static_file('register.html')
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        conf_password = request.form['password_2']

        user_info = {'email': email, 'first_name': first_name, 'last_name': last_name }
        data = { 'user_info': user_info, 'password':password }

        # Create a user
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(auth_server_base + "/users", json = data)

        if response.status_code == status.HTTP_201_CREATED:
            response_data = response.json()
            # Create a vault for the new user
            token = ('bearer ' + login_helper(email, password)).encode('utf-8')
            headers = {'Content-type': 'application/json',
                       'Accept': 'text/plain',
                       'Authorization': token}
            data = {'user_id'.encode('utf-8'): response_data['id']}
            response = requests.post(vault_server_base + "/vault", data=json.dumps(data), headers=headers)
            response_body = response.json()
            return render_template(vault.html, response_body['data'])

        return  make_response(jsonify({'uhoh':'Something went wrong with your registration.'}))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return app.send_static_file('login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        token = login_helper(email, password)
        token_data = jwt.get_unverified_claims(token)
        token = ('bearer ' + token).encode('utf-8')
        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain',
                   'Authorization': token}
        response = requests.get(vault_server_base + "/vault/" + str(token_data['user_id']), headers=headers)
        response_body = response.json()
        return render_template('vault.html', vault=response_body['data'])

def login_helper(email, password):
    data = {'email':email, 'password':password}
    response = requests.post(auth_server_base + '/auth/token', json=data)
    if response.status_code != status.HTTP_200_OK:
        raise Unauthorized('Invalid login credentials.')
    token = response.text
    return token.encode('utf-8')

@app.route('/dashboard', methods=['GET'])

def init():
    return
