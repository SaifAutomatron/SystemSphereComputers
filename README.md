# Cloud-Based Retail Web Application

This repository contains a **Django web application** named **System Sphere Computers**, a computer retail webapplication. The application leverages **AWS Cloud Services** to provide a **scalable, secure, and cost-effective Software as a Service (SaaS)** solution for managing products, customers, and orders.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [AWS Services Used](#aws-services-used)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the App](#running-the-app)
- [Deployment](#deployment)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Project Overview

This cloud-based solution for **System Sphere Computers** is built to manage computer products, provide a product catalog for customers, and enable secure online purchases. The app uses **AWS Cloud Services** for **scalability**, **security**, and **cost efficiency**. Developed with **Python** and **Django**, it integrates AWS services like **RDS**, **S3**, **SNS**, **CloudFront**, and **Elastic Beanstalk** for high availability, secure data storage, and rapid scaling.

## Features

### User Features:
- **User Authentication**: Secure registration, login, and logout using Django’s authentication system.
- **Product Catalog**: Allows users to browse products and view details.
- **Shopping Cart**: Customers can add products to their cart and manage quantities.
- **Payment Gateway**: Integrated with **Stripe** for secure payments.
- **Order Confirmation**: Sends email notifications upon successful order placement.
- **Store Locations**: Users can view the nearest stores for in-store purchases.
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices.

### Admin Features:
- **Admin Panel**: Admins can manage users, products, and orders from a user-friendly interface.
- **Inventory Management**: Retailers can add, update, or remove products from the catalog.

## Architecture

<img width="508" alt="image" src="https://github.com/user-attachments/assets/537d2573-deea-4c7e-bc17-6d77d2eecfe6">
                                              
High level Architecture



The application is designed with a cloud-first approach using **Django** for the backend and **AWS services** for infrastructure. The architecture consists of the following components:

1. **Frontend**: HTML, CSS, and JavaScript for the user interface.
2. **Backend**: Django-powered REST API for handling business logic.
3. **Database**: **Amazon RDS (MySQL)** for storing user, product, and order data.
4. **Static and Media Files**: Stored in **Amazon S3** for high availability.
5. **Email Notifications**: Handled by **Amazon SNS** for sending email updates to users.
6. **Content Delivery**: Static assets are served globally through **Amazon CloudFront**.
7. **Deployment**: Hosted on **AWS Elastic Beanstalk**.

## AWS Services Used

- **Amazon RDS (MySQL)**: Managed relational database for storing user, product, and order data.
- **Amazon S3**: Object storage for product images, invoices, and static files.
- **Amazon CloudFront**: Content Delivery Network (CDN) for low-latency delivery of static assets.
- **Amazon SNS**: Simple Notification Service for sending email notifications to users.
- **Amazon Secrets Manager**: Secure storage for database credentials and API keys.
- **Amazon Elastic Beanstalk**: Hosting service for deploying and managing the application.
- **Amazon CloudWatch**: Monitoring and logging service for application health and performance.

## Installation

To set up and run this project locally, follow these steps:

### Prerequisites

- **Python 3.8+**
- **Django 3.x**
- **AWS CLI** installed and configured.
- **Stripe Account** for payment processing.
- **AWS Account** with the necessary services set up (RDS, S3, SNS, etc.).

### Clone the Repository

```bash
git clone https://github.com/your-repo/your-project.git
cd your-project
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

You will need to configure environment variables to run this project. Create a `.env` file in the root directory with the following keys:

```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name

# Stripe API Keys
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLIC_KEY=your_stripe_public_key

# Django Settings
DJANGO_SECRET_KEY=your_django_secret_key

# RDS Database Settings
DB_HOST=your_rds_host
DB_PORT=3306
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password

# SNS Topic ARN
SNS_TOPIC_ARN=your_sns_topic_arn
```

## Running the App

1. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```

2. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

3. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

4. Open your browser and navigate to `http://127.0.0.1:8000`.

## Deployment

### AWS Elastic Beanstalk

The application is deployed using **AWS Elastic Beanstalk**. Follow these steps to deploy:

1. **Install the AWS EB CLI**:
   ```bash
   pip install awsebcli
   ```

2. **Initialize Elastic Beanstalk**:
   ```bash
   eb init
   ```

3. **Create and Deploy an Environment**:
   ```bash
   eb create
   eb deploy
   ```

4. **Set Environment Variables** in AWS Elastic Beanstalk through the console or using the EB CLI.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project was developed as part of the **Master's in Cloud Computing** program at **National College of Ireland**. Special thanks to my supervisor **Adriana Chis** for her guidance throughout this project.
