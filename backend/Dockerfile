# Use the official Python image
FROM python:3.13-alpine

# Set the working directory
WORKDIR /app

# Copy only the requirements file to my working dir
COPY requirements.txt .

# Updgrade pip to lastest version
RUN python -m pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend code
COPY . .

# Command to run the application with production environment
CMD ["python", "main.py", "--env", "production"]