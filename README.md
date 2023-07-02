# How to run locally

- `cd` to the project's root directory (where the `Dockerfile` is located)
- `sudo docker build -t blockmate_hw .`
- `sudo docker run -p 8000:8000 blockmate_hw`

# How to deploy on AWS

- Create AWS account
- Create ECR repository (private)
    - In next steps, the repository is named `danieloravec-blockmate-hw`
- Download AWS CLI 
- Authenticate Docker to registry (using AWS CLI `get-login-password` command)
    - Set your `$AWS_DEFAULT_REGION` and `$AWS_ACCOUNT_ID` variables
    - `sudo docker login -u AWS -p $(aws ecr get-login-password --region $AWS_DEFAULT_REGION) $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com`
- Build the image
    - `cd` to the directory where `Dockerfile` is located
    - `docker build -t danieloravec-blockmate-hw .`
- Tag the image
    - `docker tag danieloravec-blockmate-hw:latest $AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/danieloravec-blockmate-hw:latest`
- Push the container to the repository
    - `docker push $AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/danieloravec-blockmate-hw:latest`
- Now we need to pull the image from the registry to the production server (such as EC2) and run the container there
    - A simple guide for this is accessible at: https://aws.amazon.com/getting-started/hands-on/deploy-docker-containers/
- Make sure the respective EC2 target group's health checks are set up properly (mainly port correctness)
    - Otherwise the server might be stopping and you might be getting `503` 

A sample deployment (Swagger) is accessible at: http://ec2co-ecsel-1llwg1jebg0p5-1045308539.eu-central-1.elb.amazonaws.com:8000/docs

## Testing the API
Just run `pytest` from the root project directory.