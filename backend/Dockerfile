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

# Building this docker image
# docker build -t <image_name> <path/to/project>

# Running the built docker image
# docker run --env-file <path/to/.env> -p 5000:5000 <image_name>
