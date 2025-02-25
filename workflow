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
