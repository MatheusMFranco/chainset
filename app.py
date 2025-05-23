from flask import Flask, render_template
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='Chainset',
    description='A Flask-based mind mapping project that allows users to create and interlink chains of connected sets.'
)

# TODO: Add endpoint with @ns.route to return JSON response
ns = api.namespace('chainset', description='Chains of connected sets.')

@app.route('/warning')
def home():
    return render_template('list.html', sets=['Typescript', 'Lotlin', 'Python'])

app.run(port=8080)
