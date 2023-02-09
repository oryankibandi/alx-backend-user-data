#!/usr/bin/env
"""Session auth views"""

import os
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from flask import abort, jsonify, request


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth(request):
    """handles post"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400

    userInstance = User({'email': email, '_password': password})
    user = userInstance.search(userInstance, {'email': email})

    if user is None:
        return jsonify({"error": "no user found for this email"}), 404
    if userInstance._password != user[0]._password:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(userInstance.id)

    res = jsonify(state=0, msg=userInstance.__dict__())
    res.set_cookie(os.getenv('SESSION_NAME'), session_id)

    return res
