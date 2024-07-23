# Slim Image of Python 3.10
FROM python:3.10-slim

# Install required System Packages
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

# Create a "Data" Directory within the Working Directory
RUN mkdir -p data

# Command to Run the Application
CMD ["python", "main.py"]
