from flask import request, jsonify, send_from_directory, abort # type: ignore
from classes.image import Image as Im
from classes.database import Database
import os
import random
from dotenv import load_dotenv
from PIL import Image # type: ignore
import boto3
import botocore
import boto3.session
from botocore.exceptions import ClientError
import tempfile

# Specify the bucket names
root_bucket = 'images'
low_res_bucket = "low-res"
high_res_bucket = "high-res"
tmp_dir = "/tmp"  # Base temp directory


# Load environmental variables
load_dotenv()

def get_s3():
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    sarao_endpoint_url = os.getenv('SARAO_S3_ENDPOINT_URL')
    sarao_region = 'us-east-1'  # Update this with the correct region

    # Create an S3 client
    s3 = boto3.client('s3', 
                      aws_access_key_id=aws_access_key_id, 
                      aws_secret_access_key=aws_secret_access_key, 
                      region_name=sarao_region, 
                      endpoint_url=sarao_endpoint_url)
    return s3

def generate_low_res_image(img):
    """Generate a low-resolution image with predefined size."""
    target_size = (200, 150)  # Set your desired low resolution size here
    low_res_img = img.resize(target_size, Image.BICUBIC)
    return low_res_img

def upload_file(file_path, bucket_name, object_name):
    s3 = get_s3()
    try:
        s3.upload_file(file_path, root_bucket, f"{bucket_name}/{object_name}")
    except ClientError as e:
        print(f"An error occurred while uploading the file: {e}")
        return False
    return True

def generate_presigned_url(bucket_name, object_name, expiration=60 * 60 * 2):
    """Generate a presigned URL for an S3 object."""
    s3 = get_s3()
    try:
        response = s3.generate_presigned_url('get_object',
                                              Params={'Bucket': root_bucket, 'Key': f"{bucket_name}/{object_name}"},
                                              ExpiresIn=expiration)
    except ClientError as e:
        print(f"An error occurred while generating the presigned URL: {e}")
        return None
    return response

def recommend(images, num_of_images: int = 3) -> list[tuple[int, str, str]]:
    """
    Description: Using random packeage to recommend images.
    Input:  Integer num_of_image for number of output images.
    Output: List of Image tupple.
    """
    unique_random_image_indexes: list[int] = []
    recommended_images_list: list[tuple[int, str, str]] = []
    while len(unique_random_image_indexes) != num_of_images and len(unique_random_image_indexes) < len(images):
        random_index = random.randint(0, len(images) - 1)
        if random_index not in unique_random_image_indexes:
            unique_random_image_indexes.append(random_index)

    for index in unique_random_image_indexes:
        recommended_images_list.append(Image(*images[index]))
    return recommended_images_list

def get_images() -> tuple:
    """
    Description: Handling the GET /api/v2/images endpoint.
    Input: Query parameters ('min_id', 'max_id', 'limit', or 'model'), or nothing.
    Output: JSON of list of Image objects or 'message' key describing reason for process failure.
    """

    load_dotenv()
    db = Database()   
    table_name = 'image'

    # Get query parameters
    min_id = request.args.get('min_id', type=int)
    max_id = request.args.get('max_id', type=int)
    limit = request.args.get('limit', type=int)
    model = request.args.get('model', type=int)


    try:
        images = None
        if min_id is not None and max_id is not None:
            images = db.read_range(table_name, min_id, max_id)
        elif limit is not None:
            images = db.read(table_name, limit=limit)
        elif model is not None:
            images = db.read(table_name)
            images = recommend(images, len(images))
        else:
            images = db.read(table_name)
        
        imgs = [Im(*image).toJSON() for image in images]
        
        return jsonify(imgs), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


def get_image(id) -> tuple:
    """
    Description: Handling the GET /api/v2/images<int:id> endpoint.
    Input: Parameter id.
    Output: JSON of Image object or 'message' key describing reason for process failure.
    """

    load_dotenv()
    db = Database()
    table_name = 'image'

    try:
        images_list = db.read(table_name, criteria={'id': id})
        
        if images_list:
            img = images_list[0]
            image = Im(*img).toJSON()
            return jsonify(image), 200
        else:
            return jsonify({"message": "Image not found."}), 404
            
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

def get_image_s3_url(filename: str) -> tuple:
    """
    Description: Handling the GET /api/v2/images/<string:filename> endpoint.
    Input: Parameter filename and resolution.
    Output: JSON containing Image id and its S3 download url.
    """

    load_dotenv()
    db = Database()
    table_name = 'image'
    resolution = request.args.get('resolution', type=str)
    try:
        images_list = db.read(table_name, criteria={'low_res_image_filename': filename})
        
        if images_list:
            img = images_list[0]
            image = Im(*img)
            #
            low_res_download_url = generate_presigned_url(low_res_bucket, filename)
            high_res_download_url = generate_presigned_url(high_res_bucket, filename)
            url: str = low_res_download_url if resolution == "low" else high_res_download_url
            return jsonify({"id": image.id, "url": url}), 200
        else:
            return jsonify({"message": "Image not found."}), 404
            
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
"""
def serve_image(filename) -> tuple:
    "
    Description: Handling the GET /api/v2/images/<string:filename> endpoint.
    Input: Parameter filename.
    Output: Serves the image file directly.
    "

    load_dotenv()
    db = Database()
    table_name = 'image' 

    try:
        return send_from_directory(SERVER_DIRECTORY, filename)
    except FileNotFoundError:
        abort(404)  # Return a 404 error if the file is not found

def post_image() -> tuple:
    "
    Description: Handling the POST /api/v2/images endpoint.
    Input: JSON with 'img_path'.
    Output: JSON with 'message' key indicating success or failure.
    "

    load_dotenv()
    db = Database()
    table_name = 'image'

    data = request.json

    try:
        if 'img_path' not in data.keys():
            return jsonify({"message": "Missing required fields: 'img_path'"}), 400
        img_path = data['img_path']

        metadata = '{}'
        if 'metadata' in data.keys():
            metadata = data['metadata']

        if not os.path.isfile(img_path):
            return jsonify({"message": "Invalid image path"}), 401

        with Image.open(img_path) as img:
            low_res_img = img.resize((100, int(img.height * 100.0 / img.width)), Image.BICUBIC)
        
        filename = os.path.basename(img_path)
        low_res_destination_path = os.path.join(SERVER_DIRECTORY, "low_res_" + filename)
        low_res_img.save(low_res_destination_path)
        
        high_res_destination_path = os.path.join(SERVER_DIRECTORY, "high_res_" + filename)
        copyfile(img_path, high_res_destination_path)
        
       
        high_res_image_filename = f"high_res_{filename}"
        low_res_image_filename = f"low_res_{filename}"
        image_dict = {
            'high_res_image_filename': high_res_image_filename,
            'low_res_image_filename': low_res_image_filename,
            'metadata': metadata
        }
        if not db.insert(table_name, image_dict):
            return jsonify({"message": "Image failed to insert."}), 401
        
        image_data = dict(Im(*db.read(table_name, image_dict)[0]).toJSON())
        image_data.update({"message": "Image successfully inserted."})
        return jsonify(image_data), 200
    
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

"""
    
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Generate unique filenames for both high-res and low-res images
    high_res_filename = file.filename
    low_res_filename = file.filename

    # Save high-res image
    high_res_path = os.path.join(tmp_dir, 'high-res', high_res_filename)
    os.makedirs(os.path.dirname(high_res_path), exist_ok=True)
    file.save(high_res_path)

    # Generate and save low-res image
    with Image.open(high_res_path) as img:
        low_res_img = generate_low_res_image(img)
        low_res_path = os.path.join(tmp_dir, 'low-res', low_res_filename)
        os.makedirs(os.path.dirname(low_res_path), exist_ok=True)
        low_res_img.save(low_res_path)

    # Upload images to S3
    upload_file(high_res_path, high_res_bucket, high_res_filename)
    upload_file(low_res_path, low_res_bucket, low_res_filename)

    # Delete the files after uploading
    os.remove(high_res_path)
    os.remove(low_res_path)

    # Generate presigned URLs
    #high_res_url = generate_presigned_url(high_res_bucket, high_res_filename)
    #low_res_url = generate_presigned_url(low_res_bucket, low_res_filename)

    load_dotenv()
    db = Database()
    table_name = 'image'
    image_dict = {
        'low_res_image_filename': file.filename,
        'high_res_image_filename': file.filename
    }

    if db.insert(table_name=table_name, data=image_dict):
        image_data = dict(Im(*db.read(table_name, image_dict)[0]).toJSON())
        image_data.update({"message": "Image inserted successfully!"})
        return jsonify(image_data), 200
    else:
        return jsonify({"message": "Image insertion failed!"}), 402

def put_image() -> str:
    """
    Description: Handling the PUT /api/v2/images endpoint.
    Input: JSON with ('id', 'low_res_image_filename', 'high_res_image_filename', 'metadata', 'created_at').
    Output: JSON of Image object with 'message' key indicating success or failure.
    """

    load_dotenv()
    db = Database()
    table_name = 'image'

    data = request.json
    try:
        if all(key in data for key in ['id', 'low_res_image_filename', 'high_res_image_filename', 'metadata', 'created_at']):
            image_dict = {
                'id': data['id'],
                'low_res_image_filename': data['low_res_image_filename'],
                'high_res_image_filename': data['high_res_image_filename'],
                'metadata': data['metadata'],
                'created_at': data['created_at']
            }
            if db.update(table_name, image_dict,{'id': image_dict['id']}):
                image_data = dict(Im(*db.read(table_name, image_dict)[0]).toJSON())
                image_data.update({"message": "Image updated successfully!"})
                return jsonify(image_data), 200
            else:
                return jsonify({"message": "Image update failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'id', 'low_res_image_filename', 'high_res_image_filename', 'metadata', created_at"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500

def delete_image() -> str:
    """
    Description: Handling the DELETE /api/v2/images endpoint.
    Input: JSON with ('id', 'low_res_image_filename', 'high_res_image_filename', 'metadata', 'created_at').
    Output: JSON of Image object with 'message' key indicating success or failure.
    """

    load_dotenv()
    db = Database()
    table_name = 'image'

    data = request.json
    
    try:
        if all(key in data for key in ['id', 'low_res_image_filename', 'high_res_image_filename', 'metadata', 'created_at']):
            image_dict = {
                'id': data['id'],
                'low_res_image_filename': data['low_res_image_filename'],
                'high_res_image_filename': data['high_res_image_filename'],
                'metadata': data['metadata'],
                'created_at': data['created_at']
            }
            if db.delete(table_name, image_dict):
                image_data = dict()
                image_data.update(image_dict)
                image_data.update({"message": "Image deleted successfully!"})
                return jsonify(image_data), 200
            else:
                return jsonify({"message": "Image deleted failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'id', 'low_res_image_filename', 'high_res_image_filename', 'metadata', 'created_at'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500