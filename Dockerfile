# Use an official Python runtime as a base image
FROM python:3.11-slim-bullseye

# Set the working directory in the container to /app
WORKDIR /flask

# Copy the flask directory contents into the container at /app
ADD app /flask/app

COPY requirements.txt /flask

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]