#!/bin/bash

# Deployment script for Google Cloud Run
# Make sure you have gcloud CLI installed and authenticated

# Set your project variables
PROJECT_ID="nifty-bindery-461113-t6"
SERVICE_NAME="pycube-solver"
REGION="us-central1"

echo "Deploying PyCube Solver to Google Cloud Run..."

# Build and deploy in one command
gcloud run deploy $SERVICE_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 10 \
    --timeout 300 \
    --project $PROJECT_ID

echo "Deployment complete!"
echo "Your service should be available at the URL provided above."
