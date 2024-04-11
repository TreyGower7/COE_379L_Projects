# COE379L Project 3

This git repo contains the script ``api.py``. This script is a flask application that is used to predict whether a building is damaged or not. The data returned is explained in the sections below. An in-depth writeup about the project is located in the ``Project 3 Writeup.pdf`` file.

## Run Instructions

### Starting and Stopping the Inference Server
> Make sure that the repo is pulled before running everything!

One way to start the server is using the ``docker-compose.yml`` file by running this command:
```
docker-compose up
```

Another way is to pull the image down and then run it manually:
```
docker pull jaeestee/ml-buildings-api:latest
```

To run it manually, run this command:
```
docker run -it --rm -p 5000:5000 jaeestee/ml-buildings-api:latest
```

### Endpoints
|Route|Method|What it should do|
|---|---|---|
|``/models/buildings/v1``|GET|Gets information about the model.|
|``/models/buildings/v1``|POST|Using the model.|

There are two ways to make requests to the inference server once it is started:
1. Running it in a linux shell

To run in a linux shell use curl, for example:
```
curl http://172.17.0.1:5000/models/buildings/v1
```
> This is the POST method

Here is a sample of the GET method:
```
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://github.com/TreyGower7/COE_379L_Projects/blob/main/Project_3/cnn-split/test/damage/-93.578271_30.779923999999998.jpeg?raw=true"}' http://172.17.0.1:5000/models/buildings/v1
```
> The ``-X POST -H "Content-Type: application/json" -d`` is CRUCIAL to make this all work!

2. Running a python script

Here is the python script:
```
url = "https://github.com/TreyGower7/COE_379L_Projects/blob/main/Project_3/cnn-split/test/damage/-93.578271_30.779923999999998.jpeg?raw=true"
rsp = requests.post("http://172.17.0.1:5000/models", json={"url": url})
rsp.json()
```
