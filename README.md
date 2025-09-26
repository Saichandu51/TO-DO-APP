# 📝 To-Do App Deployment with Docker & AWS ECS

A scalable, secure To-Do Web Application deployed on AWS ECS (Fargate) with Docker containers for Frontend, Backend, and MySQL Database.

This project demonstrates how to move from local development → production-ready cloud deployment on AWS.

---

## ⚙️ Tech Stack

- **Frontend:** Nginx (serving static files)
- **Backend:** Flask (Python, running on port 5000)
- **Database:** MySQL (official container)
- **Containerization:** Docker & Docker Compose
- **Cloud:** AWS ECS (Fargate), ECR, VPC, Subnets, Security Groups, NAT Gateway, Internet Gateway, CloudWatch

---

## 🐳 Local Development Setup

**Clone the repo:**
```bash
git clone https://github.com/your-username/todo-app.git
cd todo-app
```

**Run with Docker Compose:**
```bash
docker-compose up -d
```

---

## 🔐 AWS CLI & ECR Setup

**Configure AWS CLI:**
```bash
aws configure
```
Provide:
- Access Key ID
- Secret Access Key
- Region (`us-east-1`)

**Create ECR Repositories:**
```bash
aws ecr create-repository --repository-name todo
aws ecr create-repository --repository-name todo
aws ecr create-repository --repository-name todo
```

**Authenticate Docker with ECR:**
```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
```

**Build & Push Images:**
```bash
docker build -t todo-frontend ./frontend
docker build -t todo-backend ./backend
docker build -t todo-mysql ./mysql

docker tag todo-frontend:latest <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/todo-frontend:latest
docker tag todo-backend:latest <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/todo-backend:latest
docker tag todo-mysql:latest <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/todo-mysql:latest

docker push <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/todo-frontend:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/todo-backend:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/todo-mysql:latest
```

---

## 🌐 AWS Infrastructure Setup

### 1. VPC & Subnets
- Created custom VPC (`10.0.0.0/16`)
- **2 Public Subnets:** for Frontend (internet-facing)
- **2 Private Subnets:** for Backend & MySQL

**Route Tables:**
- Public RT → routes `0.0.0.0/0` to Internet Gateway
- Private RT → routes `0.0.0.0/0` to NAT Gateway

### 2. Gateways
- **Internet Gateway (IGW):** attached to VPC for public subnets
- **NAT Gateway:** in public subnet for outbound internet from private subnets

### 3. Security Groups
- **Frontend SG:** Allow HTTP (`80`) from `0.0.0.0/0`
- **Backend SG:** Allow port `5000` from Frontend SG only
- **MySQL SG:** Allow port `3306` from Backend SG only

### 4. IAM Roles
- `ecsTaskExecutionRole` with policies:
  - AmazonECSTaskExecutionRolePolicy
  - AmazonEC2ContainerServiceRole
  - AmazonECS_FullAccess
- Added `iam:PassRole` for user deploying ECS

---

## 🚀 ECS Deployment

1. **Create ECS Cluster (Fargate).**

2. **Define Task Definitions:**
    - `todo-frontend-task`
    - `todo-backend-task`
    - `todo-mysql-task`

    Each with:
    - Image from ECR
    - CPU & Memory
    - Environment variables (DB_HOST, DB_USER, DB_PASS, DB_NAME for backend)
    - Execution Role → `ecsTaskExecutionRole`

3. **Create Services in ECS Cluster:**
    - `todo-frontend-service` → runs in public subnet with public IP
    - `todo-backend-service` → runs in private subnet
    - `todo-mysql-service` → runs in private subnet

4. **Verify Deployment:**
    - Get frontend Public IP from ECS service → access web app.

---

## ✅ Architecture

- **Local Dev:** Docker Compose (Frontend + Backend + MySQL)
- **ECR:** Stores Docker images
- **VPC:** Public (frontend) + Private (backend & DB) subnets
- **Gateways:** IGW + NAT for internet routing
- **Security Groups:** Layered protection between services
- **ECS (Fargate):** Runs frontend, backend, MySQL as services

---

## 🛠️ Challenges Faced

- **ECS tasks stuck in Pending:** fixed IAM PassRole & NAT routing.
- **IAM Role errors:** updated trust relationships.
- **Service Communication:** resolved with correct env vars + SG connections.

---

## ✨ Takeaway

This project shows how to move from local Docker Compose to AWS production-ready architecture with ECS (Fargate), VPC networking, IAM, and secure service-to-service communication.
