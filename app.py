from flask import Flask, render_template, request, jsonify
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='Chainset',
    description='A Flask-based mind mapping project that allows users to create and interlink chains of connected sets.'
)
maps = []

# TODO: Add endpoint with @ns.route to return JSON response
ns = api.namespace('chainset', description='Chains of connected sets.')

@app.route('/warning')
def home():
    items = request.args.getlist('item')
    return render_template('list.html', sets=items)

@app.route('/maps', methods=['POST'])
def create_map():
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

    return jsonify({'mensagem': 'Map created!', 'Map': new_map}), 201


if __name__ == '__main__': # pragma: no cover
    app.run(port=8080)
