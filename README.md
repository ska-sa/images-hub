# Image Hub

The Image Hub is a web application designed to address the challenges of managing SARAO's growing image repository. This application provides a comprehensive solution for effective image management and controlled access.

## Key Goals

- Allow the general public (guest users) to browse and search a repository of low-resolution images.
- Enable guest users to request access to the original high-resolution versions of the images, providing a valid reason for the request.
- Empower SARAO administrators, such as department heads, to review and approve or disapprove these access requests based on the provided justification.

## Project File Structure

<ul>
    <li>
        /images-hub
        <ul>
            <li>
                /backend
                <ul>
                    <li>/classes</li>
                    <li>/databases (excluded)</li>
                    <li>/endpoints</li>
                    <li>/outputs</li>
                    <li>/tests</li>
                    <li>/tmp</li>
                    <li>/venv (excluded)</li>
                </ul>
            </li>
            <li>/configuration</li>
            <li>/design</li>
            <li>
                /frontend
                <ul>
                    <li>/node_modules (excluded)</li>
                    <li>
                        /src
                        <ul>
                            <li>/app</li>
                            <li>/assets</li>
                            <li>/environments (excluded)</li>
                            <li>favicon.icoo</li>
                            <li>index.html</li>
                            <li>main.ts</li>
                            <li>style.css</li>
                        </ul>
                    </li>
                    <li>.dockerignore</li>
                    <li>.editorconfig</li>
                    <li>angular.json</li>
                    <li>Dockerfile</li>
                    <li>nginx.conf</li>
                    <li>package-lock.json</li>
                    <li>tsconfig.app.json</li>
                    <li>tsconfig.json</li>
                    <li>tsconfig.spec.json</li>
                </ul>
            </li>
            <li>.gitignore</li>
            <li>docker-compose.yaml</li>
            <li>Makefile</li>
            <li>README.md</li>
        </ul>
    </li>
</ul>

## Backend

The backend for this application was built using Python packages Flask, Boto3, etc. And is responsible for inserting, selecting, updating and deleting data on our database and interacting with S3 bucket. This backend provides various Restful APIs for managing users, emails, images, requests, and links.

### Application Program Interface Endpoints

#### Email Endpoints
- `POST /api/v1/emails`: <br/>&emsp; Input (json with receiver_email_address subject and body), Patamaters (none), Output (json with status message).

#### User Endpoints
- `GET /api/v1/users`: <br/>&emsp; Input (none), Patamaters (optional path paramater min_id: int and max_id: int), Output (list of json of user objects).
- `GET /api/v1/users/<int:id>`: <br/>&emsp; Input (none), Patamaters (path paramater id: int), Output (json of user object with that id).
- `POST /api/v1/users`: <br/>&emsp; Input (json of user object), Patamaters (none), Output (json of user object of posted user).
- `PUT /api/v1/users`: <br/>&emsp; Input (json of user object), Patamaters (none), Output (updated json of user object).
- `DELETE /api/v1/users`: <br/>&emsp; Input (json of user object), Patamaters (none), Output (json of user object of deleted user).
- `POST /api/v1/users/auth`: <br/>&emsp; Input (json with email_address), Patamaters (none), Output (json of user object with that email_address).

#### Image Endpoints
- `GET /api/v1/images`: <br/>&emsp; Input (none), Patamaters (optional path paramater min_id: int and max_id: int), Output (list of json of image objects).
- `GET /api/v1/images/<int:id>`: <br/>&emsp; Input (none), Patamaters (path paramater id: int), Output (json of image object with that id).
- `GET /api/v1/images/<string:filename>`: <br/>&emsp; Input (none), Patamaters (path paramater filename: string), Output (json of with image id and its S3 url).
- `POST /api/v1/images`: <br/>&emsp; Input (json of image object), Patamaters (none), Output (json of image object of posted user).
- `PUT /api/v1/images`: <br/>&emsp; Input (json of image object), Patamaters (none), Output (updated json of image object).
- `DELETE /api/v1/images`: <br/>&emsp; Input (json of image object), Patamaters (none), Output (json of image object of deleted image).

#### Request Endpoints
- `GET /api/v1/requests`: <br/>&emsp; Input (none), Patamaters (optional path paramater min_id: int and max_id: int), Output (list of json of request objects).
- `GET /api/v1/requests/<int:id>`: <br/>&emsp; Input (none), Patamaters (path paramater id: int), Output (json of request object with that id).
- `POST /api/v1/requests`: <br/>&emsp; Input (json of request object), Patamaters (none), Output (json of request object of posted request).
- `PUT /api/v1/requests`: <br/>&emsp; Input (json of request object), Patamaters (none), Output (updated json of request object).
- `DELETE /api/v1/requests`: <br/>&emsp; Input (json of request object), Patamaters (none), Output (json of request object of deleted request).

#### Link Endpoints
- `GET /api/v1/links`: <br/>&emsp; Input (none), Patamaters (optional path paramater min_id: int and max_id: int), Output (list of json of link objects).
- `GET /api/v1/links/<int:id>`: <br/>&emsp; Input (none), Patamaters (path paramater id: int), Output (json of link object with that id).
- `POST /api/v1/links`: <br/>&emsp; Input (json of link object), Patamaters (none), Output (json of link object of posted link).
- `PUT /api/v1/links`: <br/>&emsp; Input (json of link object), Patamaters (none), Output (updated json of link object).
- `DELETE /api/v1/links`: <br/>&emsp; Input (json of link object), Patamaters (none), Output (json of link object of deleted link).

## Frontend

The frontend of this application is built using Angular 16, which incorporates Hypertext Markup Language (HTML), Cascading Style Sheets (CSS), and TypeScript. This combination provides a user-friendly interface for interacting with the application's features. Also, it leverages advanced Angular capabilities, such as lazy loading, to enhance performance and efficiency.

### Angular Building Blocks

<ul>
    <li>app</li>
    <ul>
        <li>components:</li>
        <ul>
            <li>sign-in</li>
        </ul>
        <li>interfaces:</li>
        <ul>
            <li>user</li>
            <li>email</li>
            <li>image</li>
            <li>request</li>
            <li>link</li>
        </ul>
        <li>modules:</li>
        <ul>
            <li>administrator:</li>
            <ul>
                <li>components:</li>
                <ul>
                    <li>table</li>
                    <li>row</li>
                </ul>
                <li>guard</li>
            </ul>
            <li>guest</li>
            <ul>
                <li>components:</li>
                <ul>
                    <li>request-details</li>
                </ul>
                <li>guard</li>
            </ul>
            <li>shared</li>
            <ul>
                <li>components:</li>
                <ul>
                    <li>header</li>
                    <li>grid</li>
                    <li>image-card</li>
                    <li>image-details</li>
                </ul>
                <li>services:</li>
                <ul>
                    <li>user</li>
                    <li>email</li>
                    <li>image</li>
                    <li>request</li>
                    <li>link</li>
                </ul>
            </ul>
        </ul>
    </ul>
</ul>

## Getting Started
To clone and run this project, follow these steps:

`git clone https://github.com/ska-sa/images-hub.git`
`cd images-hub`

### Running the Application with Virtual Environments\
Now split our terminal, and ensure that both are point at the project (images-hub).

Setup the backend:
Navigate to the backend folder:

`cd backend`
Create a Python virtual environment and activate it:

`python3 -m virtualenv venv`
`. venv/bin/activate`
Install the required packages:

`venv/bin/python -m pip install -r requirements.txt`
Running the backend application:

`venv/bin/python -m main.py --env production`
Setup the frontend:
On the other terminal, navigate to the frontend folder:

`cd frontend`
Install the required packages:

`npm install`
Running the fontend application:

`ng serve --port 3000`


### Running the Application with Docker
Download our images from dockerhub:

`docker image pull images-hub-backend`
`docker image pull images-hub-frontend`
Start the application using Docker Compose:
After cloning our repo, navigate to our project directory and run docker-compose, makesure you have you own .env file on our project directory:

`docker-compose up`
This command will build the necessary containers and start the application.

Conclusion
The Image Hub provides a robust solution for managing SARAO's image repository, facilitating easy access and effective management. For any questions or contributions, feel free to reach out!