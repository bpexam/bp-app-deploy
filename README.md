# bp-app-deploy

This is my exam for BP

### Prerequisites
This deploy has been tested under:
* Python 2.7.14
* Pip (18.1) modules:
* requests==2.21.0

### Configuration
* s3FilePath = 'https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz'
* imageFolder = './public/images' 
* healthCheckUrl = 'http://localhost:3000/health'
* warmUptime = 15 #This value might need tweak on slow connection to retrive the container images


### Running Instructions
This repo holds the deployment files only.
in order to setup the deploy process, add the files into the root directory of ops-exercise available in git repo https://github.com/bigpandaio/ops-exercise

Once the files has been copied to the root directory
start the deployment process by running:

```
python main.py
```

