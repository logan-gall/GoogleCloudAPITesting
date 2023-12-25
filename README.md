# Google Cloud API Endpoint Demo

## Goal
This repository is designed to serve as a demo for a re-designed workflow to share data using Google Cloud Endpoints.
This README file will be a tutorial for the repo, giving an overview of the files utilized in the Google Cloud Process.

## Tutorial Outline
- Data Flow Diagram
- Pre-Tutorial
- Required Files
- Initial Set Up
- Programming for Endpoints
- Creating Tests
- Docker
- Google Cloud Build
- Google Cloud Run
- Google Cloud API Gateway

## Data Flow
![](Cloud_API_DFD.jpg)

## Required Files
Here are the files that are needed in order to successfully work through this data pipeline.

### app.py
* A Python application that provides a service
* Needs to have a web socket open with port 8080

### requirements.txt
* List of all required python packages and versions for app.py

### dockerfile
* Defines how to build docker container
* Builds container for app.py
* Installs required packages in requirements.txt

### cloudbuild.yaml
* Defines how to pull files, call docker building, and deploy into google cloud run

## Pre-Tutorial
I followed this youtube tutorial to create the initial implementation of this application. Credits here:

https://www.youtube.com/watch?v=0mfng-vih_I

## Overview Set Up
There are a number of steps to initally set up the Google Cloud Instance. We will assume this project will be started with a fresh Google Cloud Instance and empty Github Repo. Below gives an overview, and later steps will go into more detail of their importance.

### Download docker locally for testing
   * Optional but recommended

### Application
   * Have an application created in Python or any other type of web interface.
   * This demo has *app.py* which is a Python application buit utilizing Flask as a web gateway.
   * Have port 8080 open for interaction.

### Requirements.txt
   * Add any Python packages that are necessary.

### Dockerfile
   * Create a dockerfile that will create a deplloyable docker container of the above application.
   * Open this on port 80 for web interface.

### Test docker container locally (optional)
   * Test if docker builds locally using a terminal.
   * ```docker build -t clouddemoname .```
   * ```docker run -name clouddemoname -p 5001:8080 -d clouddemoname```
   * Go to ```localhost:5001``` and see if demo works properly

### Cloud Build YAML
   * Create a YAML file that will test, build, push, and deploy code.
   * The current demo has 3 steps. Testing to be implemented soon.
   * More details on YAML files in section below.

### Github setup
   * Create a new GitHub Repo.
   * Upload and create an initial push.

### Cloud Console
   * Enable google cloud run API service
   * Enable google build API service

### Cloud Run Service
This is a long section, refrence linked video if necessary.
   * Find cloud run tab (left menu)
   * Create service
   * Continuously deploy from source repository
   * Set up with Cloud Build
   * Link GitHub, select repo
   * Build configuration
     * Build type /dockerfile
   * Configure other settings as needed, this demo leaves them default.
   * Create.

### Edit Continuous Deployment
   * Give a name ```RTGS-CloudAPI-Demo```
   * Scroll down and change 'Location'
     * Repository (*cloudbuild.yaml* is with our github repo)
   * Edit Substitution variables
     * Add ```_GCR_HOSTNAME``` and set the value to ```us.gcr.io```


## Programming for Endpoints
Our typical research workflows focus on getting single results and moving on. This will not work in this case. We need to create user-focused methodology. Data endpoints are the way to do this!

In Python, Flask is an easy and powerful web interface toolkit. *app.py* has a simple web interface built on flask. It takes user input of a date, and returns values created in a dataframe of given data on the 2022 Becker UMN farms.

## Creating Tests
Testing is incredibly important for any workflow. Given we are working on public-facing code, it is impartive to have a robust testing scheme before publishing. *todo*

## Docker
Docker is a way to make our code easily run anywhere with little worry of environment errors.

## YAML
YAML files are a way to execute terminal commands easily.

## Google Cloud Build
Google cloud build is an environment to execute our docker container build.

## Google Cloud Run
Google cloud run is the place where we can create web access for our build.

## Google API Gateway
Google cloud API gateway provides a robust service to interact with our code in a headless environment.