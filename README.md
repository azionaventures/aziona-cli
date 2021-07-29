# aziona

## Develop

**dependencies library**

- python >=3.6
- pip 3
- docker and docker-compose
- awscli 2
- aws-iam-authenticator
- terraform 13.
- kubectl
- eksctl
- kustomize

**setup** 

    git clone https://github.com/gduegroup/aziona.git
    sudo make setup-dev
    source ./venv/bin/active

**release python package**

    1. change VERSION var into aziona.core.conf.const
    2. make build-wheel
    3. make deploy (push new tag to github repo and start workflow)

**docs**

    make build-docs

## Usage

**in progress**

## Contributing
    
    1. Open issue 
    2. Use module `aziona.core` for I/O, logging, settings etc
    3. Formatting and fix code with `make lint`
    4. Merge request