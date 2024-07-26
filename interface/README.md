# Basic Detector | Interface

> Made by [**_Dorian ROUX_**](https://rouxdorian.com), Data Scientist and Software Engineer.  
> Last Update: 2024-07-25    
> Version: 1.1.0

<!-- Demonstration -->
## I. Demonstration
<img src="../static/demonstration-interface.gif" alt="Demonstration"/>     


<!-- Description -->
## II. Description
The **__interface__** directory contains the source code of the web interface used to interact with the **_Basic Detector_**. The interface is composed of two main parts: the **_frontend_** and the **_backend_**. 

The **_frontend_** is a Next.js React application that allows users to perform object detection on images or videos. It is divided in three main components:
1. Initialize the Variables: 
    - Choice of the **categories** to detect (example: person, vehicle, animal, etc.).
    - Choice of the **confidence** threshold.
    - Choice of the **intersection over union** threshold.
2. Upload the File(s):
    It allows the user to upload one or multiple files that can be either images or videos.
3. Display the Results:
    It displays the results of the detection process identified by the **_Basic Detector_**.

The **_backend_** is a Flask application that receives the inputs (file, weights, thresholds) from the frontend, processes them using the **_Basic Detector_**, and returns the results to the frontend. 


<!-- Structure -->
## III. Structure
The structure of the **__interface__** directory is described below. It contains the source code as well as the docker-compose and within the frontend and backend the respective Dockerfile used to build the services.
```
.
├── docker-compose.yml
├── README.md
├── client
│   ├── Dockerfile
│   ├── package.json
|   └── ...
├── server
│   ├── Dockerfile
│   ├── server.py
│   ├── requirements.txt
|   └── ...
└── storage
    └──  ...
```

<!-- Usage -->
## IV. Usage

You can run the **Interface** using **_[Docker](https://www.docker.com/)_**.

### Docker

Below are the steps to run the **process** using your Docker : 

#### **0) Prerequisites**
```bash
# Verify that Docker is installed
docker --version
```


#### **1) Build the Docker Services**
To build the Docker services, you need to run the following command:
```bash
docker-compose up --build
```

Once the services are built, you can access the web interface by opening the following URL in your browser: [http://localhost:3000](http://localhost:3000). (PORT 3000)
