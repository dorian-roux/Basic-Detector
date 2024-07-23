# Basic Detector | Scripts 

> Made by [**_Dorian ROUX_**](https://rouxdorian.com), Data Scientist and Software Engineer.  
> Last Update: 2024-07-23  
> Version: 1.1.0


<!-- Demonstration -->
## I. Demonstration
<img src="../static/demonstration-scripts.gif" alt="Demonstration"/>     


<!-- Description -->
## II. Description
The **_scripts_** directory contains the source code of the **_Basic Detector_**. It is a Python script that allows you to detect objects in images, videos, or through a webcam. The script uses the **_YOLOv3_** model to perform the detection process. The script is divided into several modules, each of which is responsible for a specific task. 
- **_main.py_** file is the entry point of the script. It allows you to choose the type of detection you want to perform (image, video, or webcam). 
- **_detection.py_** file contains the main functions used to perform the detection process. 
- **_image.py_**, **_video.py_**, and **_webcam.py_** files contain the functions used to detect objects in images, videos, and through a webcam, respectively.

<!-- Structure -->
## III. Structure
The structure of the **_scripts_** directory is described below. It contains the source code as well as the Dockerfile used to build the Docker Image.

```
.
├── Dockerfile
├── README.md
├── main.py
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── detection.py
│   ├── image.py
│   ├── utils.py
│   ├── video.py
│   └── webcam.py
└── utils.py
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


#### **1) Build the Docker Image**
The first step is to build the Docker Image using the Dockerfile from the **_scripts_** directory. You can do this by running the following command:
```bash 
# cd scripts  # <- Navigate to the scripts directory where the Dockerfile is located
docker build -t ${TAG} .
```
<u>Note:</u> &nbsp; `{TAG}` is the name you want to give to your Docker Image. It is used to identify it later. 


#### **2) Create and Start the Docker Container**
The next step is to create and start the Docker Container using the following command:
```bash
docker run -d --name ${CONTAINER_NAME} ${TAG}
docker start ${CONTAINER_NAME}
```
<u>Note:</u> &nbsp; `{CONTAINER_NAME}` is the name you want to give to your Docker Container. It is used to identify it later.


#### **3 - Copy your _data_ to the Docker Container**
Copy your data to the Docker Container using the following command:
```bash
docker cp /path/to/data ${CONTAINER_NAME}:/app/path/to/data
```
<u>Note:</u> &nbsp; `/path/to/data` is the path to the data you want to copy to the Docker Container. It can be either a file or a directory.


#### **4) Run the _Basic Detector_**
Once you have finished the previous steps regarding the Docker container, and the copy of the data, you can now run the _Basic Detector_ using the following command:
```bash
docker exec -it ${CONTAINER_NAME} /bin/bash
python3 main.py
``` 
Once running the script, you can fill the requested inputs and let the script run the detection process.


#### **5) Export the Output**
After the detection process is completed, you will find an information regarding the **_path_** to the output folder. You can copy the output folder to your host machine using the following command:
```bash
docker cp ${CONTAINER_NAME}:/app/output /path/on/host
```


#### **6) Stop the Docker Container using the following command:** 
```bash
docker stop ${CONTAINER_NAME}
```


### Command Line

Below are the steps to run the **process** using the **_Command Line_**:

#### **0) Prerequisites**

You must have Python installed on your machine and install the required packages. The following commands display the python installation through a virtual environment.
```bash
# cd scripts  # <- Navigate to the scripts directory
python -m venv ${ENV_NAME} # Create a virtual environment
source ${ENV_NAME}/bin/activate # Activate the virtual environment  # Depending on your OS
pip install -r requirements.txt # Install the required packages
```

#### **1) Run the _Basic Detector_**
Once you have finished the previous steps regarding the virtual environment, you can now run the _Basic Detector_ using the following command:
```bash
python3 main.py
```

Once running the script, you can fill the requested inputs and let the script run the detection process.

After the detection process is completed, you will find an information regarding the **_path_** to the output folder.


