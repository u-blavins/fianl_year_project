# Final Year Project

This project is aimed towards provisioning infrastructure within a cloud environment in a compliant state, and deploys resources with Infrastructure as Code templates.

## Aims

To make the deployment of infrastructure an easier process so that an end user does not need to worry about misconfiguring their resources, as well as spend time learning about cloud services, by developing a provisioner solution.

## Objectives

- To interpret config data (from user) and convert it into infrastructure as code.
- To deploy compliant infrastructure into the cloud.
- To minimise time having to manually configure infrastructure securely.
- To house resources that have been deployed in a Infrastructure as Code template.
- To construct an Infrastructure as Code template that is Cloud Service Provider independent.

## Branching
When adding a feature, branch off the develop branch by switching from `master` to `develop` and then creating a feature branch.

## Prerequisites
- Python 3.x
- Pip
- Virtualenv
- AWS Account

## Setup
```
> virutalenv -p Python3 venv
> source venv/bin/activate
> pip install -r requirements.txt
```
> This setup is for local testing, you will not need to setup a virtual enviornment if using a CICD pipeline.

## Testing
To run the pytests locally, enter the following command in a terminal:
```$xslt
> python -m pytest
```
To run a test coverage report, use this:
```$xslt
> python -m --cov-report html --cov {package/file}