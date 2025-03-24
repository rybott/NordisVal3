# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Django project subfolder into the container at /usr/src/app
COPY NordisSite/ /usr/src/app/

# Install any needed packages specified in requirements.txt
# Adjust if your requirements.txt is located elsewhere within NordisSite
RUN pip install --no-cache-dir -r requirements.txt

# Install additional tools
RUN apt-get update && apt-get install -y poppler-utils tesseract-ocr libtesseract-dev

RUN apt-get update && apt-get install -y git

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run Django server when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

