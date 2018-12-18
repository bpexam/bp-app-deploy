import requests
import os
import time

#### Configuration
s3FilePath = 'https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz'
imageFolder = './public/images'
healthCheckUrl = 'http://localhost:3000/health'

def getImages(s3FilePath,imageFolder):
    print('Beginning image download from S3')
    r = requests.get(s3FilePath)
    with open('pandapics.tar.gz', 'wb') as f:
        f.write(r.content)
    if r.status_code == 200:
        print "Succesfully downloaded images"
        print "Checking if images directory exists and creating it if not"
        if not os.path.exists(imageFolder):
            os.makedirs(imageFolder)
            print "Image folder created"
        else:
            print "Image folder already exists"
        print "Untar our downloaded images to the image folder"
        os.system("tar -xf pandapics.tar.gz -C " + imageFolder)
        print "Cleanup the archive file"
        os.system("rm -f pandapics.tar.gz")
    else:
        print "There was an error downloading images"

def healthCheck(healthCheckUrl):
    print "Checking app health status"
    r = requests.get(healthCheckUrl)
    if r.status_code == 200:
        print "App & DB deployed Succesfully"
    elif r.status_code == 500:
        print "Issue with DB or Disk connectivity"
    else:
        print "Unknown error has occured"



### deployment procedure
print "Starting deployment procedure"
getImages(s3FilePath,imageFolder)
print "Starting Docker containers"
os.system('docker-compose up -d')
print "Waiting for container warmup ( 5 seconds)"
time.sleep(5)
print "Checking container health"
healthCheck(healthCheckUrl)
