# Use a official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for mysqlclient
RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  build-essential \
  pkg-config  # Add this line

# Copy the current directory contents into the container at /app
COPY ./app /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8888 available to the world outside this container
EXPOSE 8888

# Define environment variable
ENV MYSQL_HOST=35.239.85.126
ENV MYSQL_USER="root"
ENV MYSQL_PASSWORD="sony1208"
ENV MYSQL_DB="price_tracker"
ENV MODULE_NAME="main"
ENV VARIABLE_NAME="app"
ENV PORT="8888"

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]
