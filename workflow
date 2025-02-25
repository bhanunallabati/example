name: Terraform Deployment

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Choose the environment'
        required: true
        type: choice
        options:
          - dev
          - uat
          - prod
          - sandbox
        default: dev
      runner:
        description: 'Choose the runner (e.g., ubuntu-latest, windows-latest, macos-latest)'
        required: true
        type: string
        default: ubuntu-latest
      terraform_folder:
        description: 'Specify the Terraform folder (e.g., terraform/dev, terraform/prod)'
        required: true
        type: string
        default: terraform/dev

jobs:
  deploy:
    runs-on: ${{ github
