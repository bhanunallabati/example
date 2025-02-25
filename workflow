name: Terraform Deployment

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Choose the environment (e.g., dev, prod, staging)'
        required: true
        default: 'dev'
        type: string
      runner:
        description: 'Choose the runner (e.g., ubuntu-latest, windows-latest, macos-latest)'
        required: true
        default: 'ubuntu-latest'
        type: string
      terraform_folder:
        description: 'Specify the Terraform folder (e.g., terraform/dev, terraform/prod)'
        required: true
        default: 'terraform/dev'
        type: string

jobs:
  deploy:
    runs-on: ${{ github.event.inputs.runner }}  # Use the selected runner

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Terraform
        uses: hashicorp/setup-terraform@v1
        with:
          terraform_version: '1.0.0'  # Set the Terraform version you need

      - name: Initialize Terraform
        run: |
          cd ${{ github.event.inputs.terraform_folder }}
          terraform init

      - name: Validate Terraform configuration
        run: |
          cd ${{ github.event.inputs.terraform_folder }}
          terraform validate

      - name: Plan Terraform
        run: |
          cd ${{ github.event.inputs.terraform_folder }}
          terraform plan -var="environment=${{ github.event.inputs.environment }}"

      - name: Apply Terraform
        run: |
          cd ${{ github.event.inputs.terraform_folder }}
          terraform apply -auto-approve -var="environment=${{ github.event.inputs.environment }}"
