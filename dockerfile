# Use the official Python image from the Docker Hub
FROM python:3.13.0b4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set build arguments
ARG NULLBOT_TOKEN

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV NULLBOT_TOKEN=${NULLBOT_TOKEN}

# Command to run the bot
CMD ["python", "main.py"]
