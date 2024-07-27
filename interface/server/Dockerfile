# server/Dockerfile

# Slim Image of Python 3.10
FROM python:3.10-slim

# # Install required System Packages
RUN apt-get update && \
    apt-get install -y \
        libglib2.0-0 \
        libgl1-mesa-glx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
# Set the Working Directory
WORKDIR /app

# Copy the Python Requirements into the Working Directory
COPY requirements.txt .

# Install the Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Application Files into the Working Directory
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Install Gunicorn
RUN pip install gunicorn

# Command to start the app with Gunicorn
CMD ["gunicorn", "-w", "4", "--timeout", "3600", "-b", "0.0.0.0:8080", "server:app"]
