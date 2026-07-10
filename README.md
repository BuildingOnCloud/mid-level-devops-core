# Mid-Level DevOps Core Monorepo

Welcome to the backend service core. This repository houses our production-grade, highly optimized microservice architecture.

## 🚀 Quick Start (Local Run)

### Prerequisites
* Docker Desktop (Latest)

### Building the Image
Our container utilizes a secure, multi-stage architecture designed to isolate compilation dependencies and minimize overall image footprint.

```bash
cd app
docker build -t devops-backend-app:senior-v1 .
