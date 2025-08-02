@echo off
REM Deployment script for Google Cloud Run (Windows)
REM Make sure you have gcloud CLI installed and authenticated

REM Set your project variables
set PROJECT_ID=nifty-bindery-461113-t6
set SERVICE_NAME=pycube-solver
set REGION=us-central1

echo Deploying PyCube Solver to Google Cloud Run...

REM Build and deploy in one command
gcloud run deploy %SERVICE_NAME% --source . --platform managed --region %REGION% --allow-unauthenticated --memory 512Mi --cpu 1 --max-instances 10 --timeout 300 --project %PROJECT_ID%

echo Deployment complete!
echo Your service should be available at the URL provided above.
pause
