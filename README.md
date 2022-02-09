# Aziona-CLI Documentation

![](https://img.shields.io/badge/version-0.1-green.svg)

![](https://img.shields.io/badge/docker--compose-build-blue.svg)
![](https://img.shields.io/badge/docker-build-blue.svg)

![Python](https://img.shields.io/badge/-Python-fff?&logo=python)

Aziona CLI is a cross CI platform tool that enables the building, testing, releasing, and deploying, DevOps/GitOps process steps. 
Pipelines have two major problems, namely the setup of the environment with all the dependencies, environmental variables and the management and maintenance of scripts to be executed during the CI/CD process.
Aziona CLI tries to simplify the aforementioned aspects by allowing developers to create agnostic and platform-independent configurations.
The advantage of Aziona configurations is that you can declare in one or more YML / Json files the tasks, environment variables, and dependencies needed to run the pipeline.

![File](https://github.com/azionaventures/aziona-cli/tree/main/docs/images/aziona_process.png)

## Architecture

Aziona CLI is written in Python3 and can be used in various ways in both local and pipelined environments, such as a:

- Container image (Ubuntu 20.04)
- Python package
- GitHub action
 

**YML structure**

The YML structure is divided into targets that include multiple stages; on top of that, you can inject a custom environment and additional settings.
Each stage is defined as a single action that imports modules executed with optional arguments.

![File](https://github.com/azionaventures/aziona-cli/tree/main/docs/images/aziona_file.png)

**Modules**
Modules are actions executed by a stage; they have different types like Python or bash modules.
Each module has to have defined the type, module, and eventually additional arguments.

## Develop environment

**Requirements**

- python >= 3.6
- pip3
- docker and docker-compose

**Setup** 

    git clone https://github.com/azionaventures/aziona-cli.git
    sudo make setup-dev
    source ./venv/bin/active

## Local environment

**Requirements**

- python >= 3.6
- pip3
- docker and docker-compose

**Setup** 

    pip3 install aziona

    # or

    pip3 install aziona==VERSION

## GitHub pipeline environment

**Requirements**

Nothing 

**Setup**

    ...

    jobs:
        build:
            name: Push image on ECR
            runs-on: ubuntu-20.04

            steps:
            - name: Checkout
            uses: actions/checkout@v2

            - uses: actions/checkout@v2
            with:
                repository: azionaventures/aziona-cli
                ref:  main
                path: .github/actions/aziona

            - name: Use aziona cli
            uses: ./.github/actions/aziona
            id: action-lambda-consumer
            with:
                target: target-name-1 ... 
    ...

## Usage

**Example release docker image into Aws ECR**

Require: AWS account and Dockerfile

Create project folder, and create file `.aziona.yml` with the snippet below.

Create ECR repository in the AWS region where your profile is pointing. 

Edit `.aziona.yml and set env vars: AWS_PROFILE, AWS_ACCOUNT_ID, and AWS_ECR_REGION.

Create sample Dockerfile.

Finally, run:
```
aziona release
```

This aziona configuration file firstly makes login on Ecr service, nextly, build docker image, and endly push image to ecr repository

Snippet

```
version: "1"

targets:
  global:
    stages:
      login:
        module: aziona.packages.docker.login_aws_credentials
        args: 
          --region: ${AWS_ECR_REGION}
          --registry: ${AWS_ECR_REGISTRY}
          --profile: ${AWS_PROFILE}
      build: 
        module: aziona.packages.docker.build
        args: 
          --path: .
          --dockerfile: Dockerfile
          --tag: ${DOCKER_IMAGE}
      push: 
        module: aziona.packages.docker.push
        args: 
          --image: ${DOCKER_IMAGE}
  release:
    stages:
      login: global.login
      build: global.build
      push: global.push

env:
  AWS_PROFILE: %aws profile name%
  AWS_ACCOUNT_ID: %aws account id%
  AWS_ECR_REGION: %aws ecr region%
  AWS_ECR_REPOSITORY: %aws repository name%
  AWS_ECR_REGISTRY: ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_ECR_REGION}.amazonaws.com
  DOCKER_IMAGE: ${AWS_ECR_REGISTRY}/${AWS_ECR_REPOSITORY}:latest
```

GitHub action use case
A use case for GitHub action is a pipeline to build a container image, release it to ECR, deploy it to EKS, and finally create R53 or Cloudflare DNS records pointing to the ingress.


## Contributing
    
    1. Open issue 
    2. Use module `aziona.core` for I/O, logging, settings etc
    3. Formatting and fix code with `make lint`
    4. Merge request

## License

[GNU General Public License v3.0](https://github.com/azionaventures/aziona-cli/blob/main/LICENSE)