import sys
import os
import requests
import time
import tarfile
import logging

#### Configuration
s3FilePath = 'https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz'
imageFolder = './public/images'
healthCheckUrl = 'http://localhost:3000/health'
warmUptime = 15 #This value might need tweak on slow connection to retrive the images
logging.basicConfig(filename='deploy.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

def getImages(s3FilePath,imageFolder):
    print('Starting image download from S3')
    try:
        r = requests.get(s3FilePath)
        with open('pandapics.tar.gz', 'wb') as f:
            f.write(r.content)
        if r.status_code == 200:
            print "Succesfully downloaded images"
            print "Extracting images into image folder"
            tar = tarfile.open("pandapics.tar.gz")
            tar.extractall(path=imageFolder)
            tar.close()
            print "Clean up archive"
            os.remove("pandapics.tar.gz")
        else:
            msg="There was an error downloading images error" + r.status_code
            print msg
            logger.error(msg)
    except requests.exceptions.RequestException as e:
        print e
        logger.error(e)
        sys.exit(1)

def startContainers():
    try:
        os.system('docker-compose up -d')
    except OSError as e:
        print e
        logger.error(e)
        sys.exit(1)

def healthCheck(healthCheckUrl):
    print "Checking app health status"
    try:
        r = requests.get(healthCheckUrl)
        if r.status_code == 200:
            print "App & DB deployed Succesfully"
        else:
            msg="App failed to start"+r.status_code
            print msg
            logger.error(msg)
    except requests.exceptions.RequestException as e:
        msg="App failed the healthcheck "+str(e)+"\n Removing containers"
        os.system('docker-compose down -d')
        print msg
        logger.error(msg)
        sys.exit(1)

def main():
    print "Starting deployment procedure"
    logger.info("-------- \n Starting deployment procedure\n--------")
    getImages(s3FilePath,imageFolder)
    print "Starting Docker containers"
    startContainers()
    print "Waiting for container warmup ( "+str(warmUptime)+" seconds)"
    time.sleep(warmUptime)
    print "Checking container health"
    healthCheck(healthCheckUrl)

if __name__ == '__main__':
    main()
