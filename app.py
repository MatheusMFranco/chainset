import jwt
import os
import datetime

from flask import Flask, render_template, request, jsonify
from flask_restx import Api, Resource
from functools import wraps

from mocks.user_mock import users

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'Sésamo')

api = Api(
    app,
    version='1.0',
    title='Chainset',
    description='A Flask-based mind mapping project that allows users to create and interlink chains of connected sets.'
)

maps = []
ns = api.namespace('chainset', description='Chains of connected sets.')

def generate_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return {'message': 'Token is away!'}, 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user = data['user']
        except jwt.ExpiredSignatureError:
            return {'message': 'Token expired!'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token invalid!'}, 401
        return f(user, *args, **kwargs)
    return decorated

@app.route('/warning')
def home():
    items = request.args.getlist('item')
    return render_template('list.html', sets=items)

@ns.route('/maps')
class MapsResource(Resource):
    def post(self):
        data = request.get_json()

        fields = ['description', 'shape', 'border', 'text']
        for field in fields:
            if field not in data:
                return jsonify({'error': f'Field "{field}" is required.'}), 400

        new_map = {
            'id': len(maps) + 1,
            'description': data['description'],
            'shape': data['shape'],
            'border': data['border'],
            'text': data['text']
        }

        maps.append(new_map)

        return jsonify({'message': 'Map created!', 'map': new_map}), 201

@ns.route('/login')
class LoginResource(Resource):
    def post(self):
        data = request.json
        username = data.get('user')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'User and password are required!'}), 400

        if users.get(username) != password:
            return jsonify({'message': 'Data are invalid!'}), 401

        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token})

@ns.route('/welcome')
class WelcomeResource(Resource):
    @generate_token
    def get(self, user):
        return jsonify({'message': f'Welcome, {user}!'})

if __name__ == '__main__':  # pragma: no cover
    app.run(port=8080)
