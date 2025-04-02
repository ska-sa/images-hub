# Step 1: Build the Angular application
FROM node:20.12.2 AS builder

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the entire frontend code
COPY . .

# Create environment files with dummy values
RUN mkdir -p src/environments && \
    echo "export const environment = {" > src/environments/environment.ts && \
    echo "  production: false," >> src/environments/environment.ts && \
    echo "  apiKey: 'dummy_api_key'," >> src/environments/environment.ts && \
    echo "  host: 'dummy_host'," >> src/environments/environment.ts && \
    echo "  clientId: 'dummy_client_id'" >> src/environments/environment.ts && \
    echo "};" >> src/environments/environment.ts && \
    echo "export const environment = {" > src/environments/environment.prod.ts && \
    echo "  production: true," >> src/environments/environment.prod.ts && \
    echo "  apiKey: 'dummy_api_key'," >> src/environments/environment.prod.ts && \
    echo "  host: 'dummy_host'," >> src/environments/environment.prod.ts && \
    echo "  clientId: 'dummy_client_id'" >> src/environments/environment.prod.ts && \
    echo "};" >> src/environments/environment.prod.ts

# Build the Angular application
RUN npm run build --prod

# Step 2: Serve the application using Nginx
FROM nginx:alpine

# Copy the built application from the builder stage
COPY --from=builder /app/dist/frontend /usr/share/nginx/html

# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose the port the app runs on
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]

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
# docker run -d --env-file <path/to/.env> -p 80:3000 <image_name>

# Listing docker containers
# docker ps

# Opening docker container bash
# docker exec -it <container_id> bash

# Deleting a docker container
# docker rm <container_id>