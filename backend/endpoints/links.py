import os
from dotenv import load_dotenv
from flask import request, jsonify
from classes.link import Link
from classes.image import Image
from classes.database import Database
from endpoints.images import generate_presigned_url


def get_links() -> tuple:
    """
    Description: Handling the GET /api/v1/links endpoint.
    Input: Query parameters ('min_id', 'max_id', or 'limit'), or nothing.
    Output: JSON of list of Link objects or 'message' key describing reason for process failure.
    """
    load_dotenv()
    db = Database()
    table_name = 'link'

    # Get query parameters
    min_id = request.args.get('min_id', type=int)
    max_id = request.args.get('max_id', type=int)
    limit = request.args.get('limit', type=int)

    try:
        links = None
        if min_id is not None and max_id is not None:
            links = db.read_range(table_name, min_id, max_id)
        elif limit is not None:
            links = db.read(table_name,limit=limit)
        else:
            links = db.read(table_name)
        
        lnks = [Link(*lnk).toJSON() for lnk in links]

        return jsonify(lnks), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    

def get_link(id: int) -> tuple:
    """
    Description: Handling the GET /api/v1/links<int:id> endpoint.
    Input: Parameter id.
    Output: JSON of Link objects or 'message' key describing reason for process failure.
    """
    load_dotenv()
    db = Database()
    table_name = 'link'

    try:
        links_list = db.read(table_name, criteria={'id': id})
        
        if links_list:
            link = links_list[0]
            lnk = Link(*link).toJSON()
            return jsonify(lnk), 200
        else:
            return jsonify({"message": "Link not found."}), 404
            
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


def download_image(key: str) -> tuple:
    """
    Description: Handling the GET /api/v1/links<string:key> endpoint.
    Input: Parameter key.
    Output: Download image or JSON or 'message' key describing reason for process failure.
    """
    db = Database()
    table_name = 'link'
    load_dotenv()
    app_url = os.getenv("APP_URL")
    try:
        links_list = db.read(table_name, criteria={'key': key})
        
        if links_list:
            link = links_list[0]
            lnk = Link(*link)
            if lnk.limit == 0:
                # Display failed download image
                html = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <link rel="icon" type="image/x-icon" href="/static/images/nrf_logo.png">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" />
                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
                        <title>Images Hub</title>
                        <style>
                            body {{
                                margin: 0;
                                padding: 0;
                                font-family: Arial, sans-serif;
                                background-color: #f0f0f0;
                            }}
                            .failed-container {{
                                display: flex;
                                flex-direction: column;
                                justify-content: center;
                                align-items: center;
                                height: 100vh;
                            }}
                            .failed-image {{
                                max-width: 300px;
                                animation: pulse 2s infinite;
                            }}
                            .failed-message {{
                                margin-top: 20px;
                                font-size: 18px;
                                text-align: center;
                            }}
                            .redirect-link {{
                                margin-top: 20px;
                                color: #007bff;
                                text-decoration: none;
                            }}
                            .logo{{
                                margin: 20px;
                                height: 150px;
                            }}
                            @keyframes pulse {{
                                0% {{ transform: scale(1); }}
                                50% {{ transform: scale(1.2); }}
                                100% {{ transform: scale(1); }}
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="failed-container">
                            <img src="/static/images/sarao_logo.png" alt="SARAO Logo" class="logo">
                            <div>
                                <span class="fa-stack fa-lg">
                                    <i class="fa fa-download fa-stack-1x"></i>
                                    <i class="fa fa-ban fa-stack-2x text-danger"></i>
                                </span>
                            </div>
                            <div class="failed-message">
                                The download link has expired. Please go back to the app and request the image again.
                            </div>
                            <a href="{app_url}" class="redirect-link">Go to Sign In Page</a>
                        </div>
                    </body>
                    </html>
                """
                return html, 200
            
            images_list = db.read("image", criteria={'id': lnk.image_id})
            if images_list:
                image = images_list[0]
                img = Image(*image)
                filename = img.high_res_image_filename
                high_res_bucket = "high-res"
                lnk.limit = lnk.limit - 1
                if db.update(table_name, {'limit': lnk.limit},{'id': lnk.id}):
                    high_res_download_url = generate_presigned_url(high_res_bucket, filename)
                    
                    # Display custom HTML code snippet with a growing and shrinking download icon
                    html = f"""
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <link rel="icon" type="image/x-icon" href="/static/images/nrf_logo.png">
                            <title>Images Hub</title>
                            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" />
                            <style>
                                body {{
                                    margin: 0;
                                    padding: 0;
                                    font-family: Arial, sans-serif;
                                }}
                                .download-container {{
                                    display: flex;
                                    flex-direction: column;
                                    justify-content: center;
                                    align-items: center;
                                    height: 100vh;
                                }}
                                .download-link {{
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                    font-size: 4rem;
                                    color: #007bff;
                                    text-decoration: none;
                                    animation: pulse 2s infinite;
                                }}
                                .download-icon {{
                                    transform-origin: center center;
                                    animation: grow-shrink 2s infinite;
                                }}
                                .download-status {{
                                    margin-top: 20px;
                                    font-size: 18px;
                                }}
                                .redirect-link {{
                                    margin-top: 20px;
                                    color: #007bff;
                                    text-decoration: none;
                                }}
                                .logo{{
                                    margin: 20px;
                                    height: 150px;
                                }}
                                @keyframes pulse {{
                                    0% {{ transform: scale(1); }}
                                    50% {{ transform: scale(1.2); }}
                                    100% {{ transform: scale(1); }}
                                }}
                                @keyframes grow-shrink {{
                                    0% {{ transform: scale(1); }}
                                    50% {{ transform: scale(1.5); }}
                                    100% {{ transform: scale(1); }}
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="download-container">
                                <script>
                                    window.onload = function() {{
                                        window.location.href = '{ high_res_download_url }';
                                        document.querySelector('.download-status').textContent = "Download has already begun...";
                                    }}
                                </script>
                                <img src="/static/images/sarao_logo.png" alt="SARAO Logo" class="logo">
                                <a href="#" class="download-link" onclick="location.reload()">
                                    <i class="fa fa-download" aria-hidden="true"></i>
                                </a> 
                                <div class="download-status">
                                    Downloading image...
                                </div>
                                <a href="{app_url}" class="redirect-link">Go to Sign In Page</a>
                            </div>
                        </body>
                        </html>
                    """
                    return html, 200
                else:
                    return jsonify({"message": "Link update failed."}), 404
            else:
                return jsonify({"message": "Image not found."}), 404
        else:
            return jsonify({"message": "Link not found."}), 404
    except Exception as e:
        print(f"Error in download_image: {e}")
        return jsonify({"message": "An error occurred."}), 500


def post_link() -> tuple:
    """
    Description: Handling the POST /api/v1/links endpoint.
    Input: JSON with ('id', 'image_id', 'key', 'limit').
    Output: JSON of Link object with 'message' key indicating success or failure.
    """
    load_dotenv()
    db = Database()
    table_name = 'link'

    data = request.json
    try:
        if all(key in data for key in ['image_id', 'key', 'limit']):
            link_dict: dict = {
                'image_id': data['image_id'],
                'key': data['key'],
                'limit': data['limit']
            }
            if db.insert(table_name, link_dict):
                link_data = dict(Link(*db.read(table_name, link_dict)[0]).toJSON())
                link_data.update({"message": "Link inserted successfully!"})
                return jsonify(link_data), 200
            else:
                return jsonify({"message": "Link insertion failed!"}), 501
        else:    
            return jsonify({"message": "Missing key(s) 'image_id', 'key', 'limit'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
def put_link() -> tuple:
    """
    Description: Handling the PUT /api/v1/links endpoint.
    Input: JSON with ('id', 'image_id', 'key', 'limit', 'created_at').
    Output: JSON with 'message' key indicating success or failure.
    """
    load_dotenv()
    db = Database()
    table_name = 'link'

    data = request.json

    try:
        if all(key in data for key in ['id', 'image_id', 'key', 'limit', 'created_at']):
            link_dict = {
                'id': data['id'],
                'image_id': data['image_id'],
                'key': data['key'],
                'limit': data['limit'],
                'created_at': data['created_at']
            }
            if db.update(table_name, link_dict,{'id': link_dict['id']}):
                link_data = dict(Link(*db.read(table_name, link_dict)[0]).toJSON())
                link_data.update({"message": "Link updated successfully!"})
                return jsonify(link_data), 200
            else:
                return jsonify({"message": "Link update failed!"}), 501
        
        else:    
            return jsonify({"message": "Missing key(s) 'id', 'image_id', 'key', 'limit', 'created_at"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
def delete_link() -> tuple:
    """
    Description: Handling the DELETE /api/v1/links endpoint.
    Input: JSON with ('id', 'image_id', 'key', 'limit').
    Output: JSON of Link object with 'message' key indicating success or failure.
    """
    load_dotenv()
    db = Database()
    table_name = 'link'

    data = request.json
    try:
        if all(key in data for key in ['id', 'image_id', 'key', 'limit', 'created_at']):
            link_dict = {
                'id': data['id'],
                'image_id': data['image_id'],
                'key': data['key'],
                'limit': data['limit'],
                'created_at': data['created_at']
            }
            if db.delete(table_name, {'id': link_dict['id']}):
                link_data = dict()
                link_data.update(link_dict)
                link_data.update({"message": "Link deleted successfully!"})
                return jsonify(link_data), 200
            else:
                return jsonify({"message": "Link delete failed!"}), 501
            
        else:    
            return jsonify({"message": "Missing key(s) 'id', 'image_id', 'key', 'limit', 'created_at'"}), 400
    except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
