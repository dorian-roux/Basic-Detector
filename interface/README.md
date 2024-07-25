# Basic Detector | Interface

> Made by [**_Dorian ROUX_**](https://rouxdorian.com), Data Scientist and Software Engineer.  
> Last Update: 2024-07-25  
> Version: 1.1.0

<!-- Demonstration -->
## I. Demonstration
<img src="../static/demonstration-interface.gif" alt="Demonstration"/>     


<!-- Description -->
## II. Description
The **__interface__** directory contains 

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

You can run the **Script Process** using either a  **_[Docker](https://www.docker.com/)_** container or the **_Command Line_**.

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
