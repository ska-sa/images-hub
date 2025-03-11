import os
import argparse
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

import os
import argparse
from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS  # type: ignore
from dotenv import load_dotenv, set_key
from endpoints.emails import send_email
from endpoints.users import get_users, get_user, post_user, auth, google_auth, put_user, delete_user
from endpoints.images import get_images, get_image, get_image_s3_url, upload_image, put_image, delete_image
from endpoints.requests import get_requests, get_request, post_request, put_request, delete_request
from endpoints.links import get_links, get_link, download_image, post_link, put_link, delete_link

app = Flask(__name__)

# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Select the environment (production, development, testing).")
    parser.add_argument("--env", choices=["production", "development", "testing"], default="development", help="Set the environment (default is development)")
    return parser.parse_args()

args = parse_args()
print(f"{args.env} db selected.")
set_key('.env', 'FLASK_ENV', args.env)

load_dotenv()

# Set Flask configuration based on the environment
app.config['ENV'] = args.env
app.config['DEBUG'] = (args.env == "development")
app.config['TESTING'] = (args.env == "testing")

# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

class Back_End:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')

    def validate_api_key(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return self.forbidden_response()
        api_key = auth_header.split(" ")[1]
        
        if api_key != self.api_key:
            return self.forbidden_response()

    def forbidden_response(self):
        return jsonify({'error': 'Forbidden'}), 403

backend = Back_End()

@app.route('/api/v2/emails', methods=['POST'])
def send_email_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return send_email()


@app.route('/api/v2/users', methods=['GET'])
def get_users_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return get_users()

@app.route('/api/v2/users/<int:id>', methods=['GET'])
def get_user_route(id: int):
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return get_user(id)

@app.route('/api/v2/users', methods=['POST'])
def post_user_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return post_user()

@app.route('/api/v2/users', methods=['PUT'])
def put_user_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return put_user()

@app.route('/api/v2/users', methods=['DELETE'])
def delete_user_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return delete_user()

@app.route('/api/v2/users/auth', methods=['POST'])
def auth_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return auth()

@app.route('/api/v2/users/users/google_auth', methods=['POST'])
def goofle_auth_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return google_auth()


@app.route('/api/v2/images', methods=['GET'])
def get_images_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return get_images()

@app.route('/api/v2/images/<int:id>', methods=['GET'])
def get_image_route(id: int):
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return get_image(id)

@app.route('/api/v2/images/<string:filename>', methods=['GET'])
def get_s3_image_url_route(filename: str):
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return get_image_s3_url(filename)

"""
@app.route('/api/v2/images', methods=['POST'])
def post_images_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return post_image()
"""

@app.route('/api/v2/images', methods=['POST'])
def upload_image_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return upload_image()

@app.route('/api/v2/images', methods=['PUT'])
def put_image_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return put_image()

@app.route('/api/v2/images', methods=['DELETE'])
def delete_image_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return delete_image()


@app.route('/api/v2/requests', methods=['GET'])
def get_requests_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return get_requests()

@app.route('/api/v2/requests/<int:id>', methods=['GET'])
def get_request_route(id: int):
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return get_request(id)

@app.route('/api/v2/requests', methods=['POST'])
def post_request_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return post_request()

@app.route('/api/v2/requests', methods=['PUT'])
def put_request_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return put_request()

@app.route('/api/v2/requests', methods=['DELETE'])
def delete_request_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return delete_request()


@app.route('/api/v2/links', methods=['GET'])
def get_links_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return get_links()

@app.route('/api/v2/links/<int:id>', methods=['GET'])
def get_link_route(id: int):
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return get_link(id)

@app.route('/api/v2/links/<string:key>', methods=['GET'])
def download_link_route(key: str):
    return download_image(key)

@app.route('/api/v2/links', methods=['POST'])
def post_link_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return post_link()

@app.route('/api/v2/links', methods=['PUT'])
def put_link_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return put_link()

@app.route('/api/v2/links', methods=['DELETE'])
def delete_link_route():
    validation_response = backend.validate_api_key()
    if validation_response:
        return validation_response
    return delete_link()
 
if __name__ == '__main__':
    app.run(host='localhost', debug=True)
