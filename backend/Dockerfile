# Use the official Python image
FROM python:3.10.12

# Set the working directory
WORKDIR /app

# Copy only the requirements file to my working dir
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend code
COPY . .

# Command to run the application with production environment
CMD ["python", "main.py", "--env", "production"]



# ============================== #
#         Docker Images          #       
# ============================== #

# Building this docker image
# docker build -t <image_name> <path/to/project>

# Listing docker images
# docker images

# Deleting a docker image
# docker rmi <images_id>



# ============================== #
#       Docker Containers        #
# ============================== #

# Running the built docker image in a detached mode
# docker run -d --env-file <path/to/.env> -p 5000:5000 <image_name>

# Listing docker containers
# docker ps

# Opening docker container bash
# docker exec -it <container_id> bash

# Deleting a docker container
# docker rm <container_id>
