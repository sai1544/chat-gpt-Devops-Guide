# chat-gpt-Devops-Guide

# Devops Day 1 & Day 2 Notes
 
 
---
 
#📅 Day 1 — FastAPI + Docker Fundamentals
 
FastAPI Setup
 
Initialized minimal FastAPI project
 
Implemented /health endpoint
 
Tested locally via Uvicorn
 
 
Command:
```
uvicorn app.main:app --reload
 
 ```
---
 
Local Debugging Concepts
 
Understood app.main:app import path
 
Observed stack traces for debugging
 
Verified logs from terminal
 
 
 
---
 
Dockerization
 
Created Dockerfile with:
 ```
python:3.10-slim base image
 ```
Installed dependencies from requirements.txt
 
Copied application code
 
Set Uvicorn as entrypoint
 
 
 
Image Build:
 ```
docker build -t fastapi-app .
 ```
Run Container:
``` 
docker run -p 8000:8000 fastapi-app
 
 ```
---
 
Verification
 
Accessed service from EC2 public IP:
 
 ```
http://<EC2-PUBLIC-IP>:8000/health
 ```
Verified container logs using:
 
 
docker logs <container-id>
 
 
---
 
#📅 Day 2 — Logging + Config + PostgreSQL Integration
 
Project Structure Refactor
 
Refactored into modular architecture:
 
app/
  routes/
  core/
  db/
  utils/
 
 
---
 
Structured Logging
 
Implemented reusable logger via logging module
 
Logged startup events
 
Logs written to stdout (container friendly)
 
 
 
---
 
Environment-Based Configuration
 
Created core/config.py
 
Loaded DB configs via os.getenv()
 
Removed DB credentials from codebase
 
 
Example env keys:
 ```
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
``` 
 
---
 
PostgreSQL Integration (psycopg2)
 
Installed psycopg2-binary
 
Created DB connector:
 ```
get_db_connection()
 ```
 
Wrote helper functions:
 ```
insert_service_status()
 
fetch_latest_status()
 
 ```
 
 
---
 
Database Schema
 ```
Table created:
 
CREATE TABLE service_status (
  id SERIAL PRIMARY KEY,
  service_name VARCHAR(50),
  status VARCHAR(20),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
 
 ```
---
 
Fail-Fast Startup Logic
 
DB connection checked on startup event
 
If DB unavailable → application exits
 
Ensures no degraded operation
 
 
Flow:
 
App start → DB check → success OR crash
 
 
---
 
Docker Compose Orchestration
 
Created docker-compose.yml with:
 
db service (PostgreSQL)
 
app service (FastAPI)
 
 
Internal networking:
 
DB_HOST=db
 
Run:
 
docker-compose up --build
 
 
---
 
🧠 Core Concepts Learned
 
Containerization
 
Dockerfile
 
Image vs Container
 
Port mapping
 
Logs to stdout
 
 
Config & Secrets
 
Env vars replace hardcoding
 
12-factor config principle
 
 
DB Connectivity
 
psycopg2 usage
 
SQL inserts & reads
 
Connection lifecycle
 
 
Fail-Fast Architecture
 
Detect critical failures early
 
Break instead of running broken
 
 
Service Orchestration
 
Docker Compose networking
 
Internal DNS resolution
 
depends_on behavior
 
 
 
---
 
🎤 Interview Highlights
 
You can say:
 
Built containerized FastAPI service
 
Implemented health endpoint & structured logging
 
Externalized configuration using env vars
 
Verified PostgreSQL connectivity with psycopg2
 
Applied fail-fast startup checks
 
Used Docker Compose for multi-service orchestration
 
 
 
---
 
🎯 End State After Day 2
 
You now have: ✔ Containerized FastAPI App
✔ Logging system
✔ Env-driven config system
✔ PostgreSQL integration
✔ Fail-fast startup behavior
✔ Docker Compose orchestration
 
 
---


# Day 3 — Production-Grade Docker 🚀

This document captures everything from **Day 3** of the DevOps learning journey: making Docker images optimized, secure, reproducible, and production-ready.

---

## 🎯 Goal
By the end of Day 3, you should confidently say:

> “My Docker image is optimized, secure, reproducible, and production-ready.”

---

## 🛠 Why Dockerfile Quality Matters
Recruiters don’t care if Docker *just works*.  
They care if you understand:

- **Image size** → smaller images deploy faster and use less storage.
- **Build layers** → caching makes builds faster and reproducible.
- **Security** → don’t run as root, use slim images.
- **Reproducibility** → builds are consistent across environments.

❌ Bad Dockerfile:
- Runs as root
- Huge image
- Installs unnecessary tools
- No caching

✅ Good Dockerfile:
- Small
- Non-root user
- Cached layers
- Explicit dependencies

---

## 📝 Multi-Stage Dockerfile

dockerfile
```
# -------- Stage 1: Builder --------
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

# -------- Stage 2: Runtime --------
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

COPY --from=builder /install /usr/local
COPY app ./app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 
```

▶️ Build & Run Instructions
Build image
bash
```
docker build -t devops-python-app:prod .
```
Check image size
bash
docker images
📌 Expected: < 300 MB

Run container
bash
```
docker run -p 8000:8000 devops-python-app:prod
```
Verify health
Open in browser:
```
Code
http://localhost:8000/health
Expected response:

json
{"status": "ok"}
```
🔐 Security & Best Practices
Use non-root user (appuser) → prevents privilege escalation.

Use slim base image → fewer packages, smaller attack surface.

Remove apt cache after install → smaller image size.

Explicit CMD → predictable runtime.


---

Day 4 — AWS ECR + IAM + Real Image Push 🚀
---


Today marks the first cloud touchpoint in our DevOps journey.  
We will securely push our Docker image to **Amazon Elastic Container Registry (ECR)** using IAM permissions.

---

## 🎯 Goal

> **Build → Tag → Authenticate → Push image to ECR securely using IAM**

This ensures our container is production-ready and can later be deployed seamlessly into Kubernetes (EKS).

---

## ⏱ Time Plan (5 Hours)

| Time | Task |
|------|------|
| 1 hr | AWS ECR setup |
| 1 hr | IAM roles & permissions |
| 1 hr | Docker login + tagging |
| 1 hr | Push + verify image |
| 1 hr | Cleanup + notes |

---

## 1️⃣ Create ECR Repository

- Go to **AWS Console → ECR → Private → Create Repository**
- Settings:
  - Repository name: `devops-python-app`
  - Tag immutability: **Enabled**
  - Scan on push: **Enabled**
  - Encryption: **AES-256 (default)**

📌 **Why immutability?**  
Prevents accidental overrides of production images.

---

## 2️⃣ IAM Permissions

Create a dedicated IAM user for DevOps with **programmatic access**.  
Attach the following minimal policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:CompleteLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:InitiateLayerUpload",
        "ecr:PutImage"
      ],
      "Resource": "*"
    }
  ]
}
```
📌 Why minimal?  
Real DevOps avoids admin credentials — only required actions are allowed.

3️⃣ Configure AWS CLI
On your laptop/server:

bash
aws configure
Enter:

AWS Access Key

AWS Secret Key

Region (e.g. ap-south-1)

Output: json

4️⃣ Login to ECR
bash
aws ecr get-login-password --region ap-south-1 \
  | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com
✅ If login succeeds → you are authenticated.

5️⃣ Tag the Image
bash
docker tag devops-python-app:latest \
<AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/devops-python-app:latest
6️⃣ Push to ECR
bash
docker push <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/devops-python-app:latest
Expected output:

Code
Layer upload: complete
Pushed image on ECR
7️⃣ Verify in AWS Console
Go to AWS Console → ECR → devops-python-app → Images

Check:

✔ Tag: latest

✔ Scan status: IN_PROGRESS or COMPLETED

✔ Vulnerabilities report

🧂 Bonus (Interview Gold)
“Our CI pushed to ECR with scan-on-push enabled, to detect CVEs before deployment.”

This shows security-first thinking in DevOps interviews.

✅ Success Checklist
[x] IAM user created with minimal permissions

[x] AWS CLI configured

[x] Docker authenticated to ECR



Day 5 — EKS Cluster Setup (AWS Kubernetes)

## 🎯 Goal
Create an **EKS cluster** in `ap-south-1` with a managed node group, configure `kubectl`, and validate workloads.

By the end of this task you should be able to run:
bash
kubectl get nodes
kubectl get pods -A
kubectl get svc
⏱️ Time Plan (5 Hours)
Time	Task
1 hr	Install AWS tooling
2 hr	Create EKS cluster
1 hr	Node group setup
1 hr	Verification + cleanup
1️⃣ Prerequisites
AWS account

IAM user/role with EKS + EC2 permissions

AWS CLI configured with region ap-south-1

Verify:

bash
aws configure get region
aws sts get-caller-identity
```
2️⃣ Install Required Tools
AWS CLI
Already installed in Day 4. Check:

bash
aws --version

Bash
curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_Linux_amd64.tar.gz"
Step 3: Extract the binary
Copy code
Bash
tar -xzf eksctl_Linux_amd64.tar.gz
Step 4: Move to /usr/local/bin
Copy code
Bash
sudo mv eksctl /usr/local/bin/
Step 5: Verify installation
Copy code
Bash
eksctl version

kubectl
bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin/
kubectl version --client
3️⃣ Create EKS Cluster
bash
eksctl create cluster \
  --name devops-eks \
  --region ap-south-1 \
  --nodegroup-name devops-ng \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 2 \
  --nodes-max 3 \
  --managed
Control plane: managed by AWS

Node group: EC2 worker nodes

Networking: VPC + subnets

Auth: kubeconfig auto-updated

⏳ Takes ~10–20 minutes.

4️⃣ Verify Cluster
Check nodes:

bash
kubectl get nodes
Check system pods:

bash
kubectl get pods -A
Expected:

aws-node (CNI)

kube-proxy

coredns

Check services:

bash
kubectl get svc -A
5️⃣ IAM & Kubeconfig Check
Inspect kubeconfig:

bash
cat ~/.kube/config
Verify cluster endpoint:

bash
aws eks describe-cluster \
  --name devops-eks \
  --region ap-south-1 \
  --query "cluster.endpoint" \
  --output text
6️⃣ Optional — Node Lifecycle Drill
bash
kubectl cordon <node-name>
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
kubectl uncordon <node-name>
```
✅ Success Checklist
[x] Cluster created (devops-eks)

[x] Node group online

[x] kubectl get nodes shows Ready

[x] System pods running

[x] kubeconfig updated

[x] Region = ap-south-1

[x] Image tagged & pushed

[x] Image visible in AWS console

[x] Security scan triggered





Day 6 — AWS Load Balancer Controller + IRSA + Ingress

## 🎯 Goal
Configure **AWS ALB Load Balancer Controller** via **IRSA** so that Kubernetes can create AWS ALBs automatically.

This connects Kubernetes networking with AWS infrastructure securely.

---

## ⏱️ Time Plan (5 Hours)

| Time | Task                          |
|------|-------------------------------|
| 1 hr | Install Helm                  |
| 1 hr | Create IRSA                   |
| 2 hr | Deploy ALB Controller         |
| 1 hr | Verification                  |

---

## 1️⃣ Install Helm

Helm is the Kubernetes package manager used to install the ALB controller.

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```
2️⃣ Create IAM Role for Service Account (IRSA)
IRSA allows Kubernetes service accounts to assume IAM roles securely.

Step 1 — Download IAM Policy
```bash
curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.6.2/docs/install/iam_policy.json
```
Step 2 — Create IAM Policy
```bash
aws iam create-policy \
  --policy-name AWSLoadBalancerControllerIAMPolicy \
  --policy-document file://iam-policy.json
```
Step 3 — Associate OIDC Provider
```bash
eksctl utils associate-iam-oidc-provider \
  --cluster devops-eks \
  --region ap-south-1 \
  --approve
```
Step 4 — Create IAM Service Account
```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
POLICY_ARN=arn:aws:iam::$ACCOUNT_ID:policy/AWSLoadBalancerControllerIAMPolicy

eksctl create iamserviceaccount \
  --cluster devops-eks \
  --namespace kube-system \
  --name aws-load-balancer-controller \
  --attach-policy-arn $POLICY_ARN \
  --override-existing-serviceaccounts \
  --region ap-south-1 \
  --approve
```
3️⃣ Deploy ALB Load Balancer Controller
Step 1 — Add Helm Repo
```bash
helm repo add eks https://aws.github.io/eks-charts
helm repo update
```
Step 2 — Install Controller
```bash
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  --namespace kube-system \
  --set clusterName=devops-eks \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set region=ap-south-1 \
  --set vpcId=$(aws eks describe-cluster \
      --name devops-eks \
      --region ap-south-1 \
      --query "cluster.resourcesVpcConfig.vpcId" \
      --output text)
 ```
4️⃣ Verify Deployment
Check Controller Pod
```bash
kubectl get pods -n kube-system | grep aws-load-balancer-controller
```
Check Logs
```bash
kubectl logs -n kube-system deployment/aws-load-balancer-controller
```
Confirm CRDs
```bash
kubectl get crd | grep elbv2.k8s.aws
```
Expected CRDs:

ingressclassparams.elbv2.k8s.aws

targetgroupbindings.elbv2.k8s.aws

✅ Day 6 Success Checklist
[x] Helm installed

[x] IAM Policy created

[x] OIDC provider associated with cluster

[x] IRSA service account created in kube-system

[x] ALB Controller deployed via Helm

[x] Controller pod running

[x] CRDs present (ingressclassparams, targetgroupbindings)



🧠 Big Picture Analogy
Imagine Kubernetes is a city planner.

Ingress = road map (where traffic should go).

ALB Controller = construction company (builds actual highways).

IRSA = government permit (legal permission to build).

Helm = blueprint delivery system (hands over construction plans cleanly).

Without IRSA, the construction company would have no legal permit. Without the controller, the road map stays on paper. Together, they make traffic flow from the internet into your pods securely.




---

# 🚀 Day 7 — Deploy Python App to EKS + Public Access

Today we deploy our FastAPI app to **AWS EKS** and expose it publicly using **AWS ALB Ingress**.  
By the end, you’ll be able to open a public AWS URL and see the `/health` response.

---

## 🎯 Goal

> Deploy FastAPI app on EKS and access it via AWS ALB Ingress.

This is a **real production deployment**, not just practice.

---

## ⏱ Time Plan (5 Hours)

| Time | Task                |
|------|---------------------|
| 1 hr | Namespace + Secrets |
| 1 hr | Deployment YAML     |
| 1 hr | Service YAML        |
| 1 hr | Ingress (ALB)       |
| 1 hr | Debug + Verify      |

---

## 1️⃣ Create Namespace + Secrets (1 Hour)

Namespaces isolate resources. Secrets store sensitive data like DB credentials.

### Create Namespace
```bash
kubectl create namespace app
```

### Create Secret (DB creds)
```bash
kubectl create secret generic db-secret \
  --namespace app \
  --from-literal=DB_HOST=<RDS-ENDPOINT-or-temp-db> \
  --from-literal=DB_PORT=5432 \
  --from-literal=DB_NAME=appdb \
  --from-literal=DB_USER=appuser \
  --from-literal=DB_PASSWORD=apppassword
```

📌 For now, DB can be temporary or placeholder. RDS comes later (Day 8–9).

---

## 2️⃣ Deployment YAML (1 Hour)

Defines how Pods run inside the cluster.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devops-python-app
  namespace: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: devops-python-app
  template:
    metadata:
      labels:
        app: devops-python-app
    spec:
      containers:
        - name: app
          image: 345466045476.dkr.ecr.ap-south-1.amazonaws.com/devops-repo:v1
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: db-secret
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 15
            periodSeconds: 20
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
```

### Apply Deployment
```bash
kubectl apply -f deployment.yaml
```

### Verify Pods
```bash
kubectl get pods -n app
```

---

## 3️⃣ Service YAML (1 Hour)

Provides a stable internal endpoint for Pods.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: devops-python-service
  namespace: app
spec:
  selector:
    app: devops-python-app
  ports:
    - port: 80
      targetPort: 8000
  type: ClusterIP
```

### Apply Service
```bash
kubectl apply -f service.yaml
```

### Verify Service
```bash
kubectl get svc -n app
```

---

## 4️⃣ Ingress (ALB) YAML (1 Hour)

Ingress defines external routing rules. The AWS Load Balancer Controller provisions an ALB.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: devops-python-ingress
  namespace: app
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80}]'
spec:
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: devops-python-service
                port:
                  number: 80
```

### Apply Ingress
```bash
kubectl apply -f ingress.yaml
```

---

## 5️⃣ Get Public URL (Important)

Check Ingress for ALB DNS:

```bash
kubectl get ingress -n app
```

You will see something like:

```
ADDRESS: xyz.ap-south-1.elb.amazonaws.com
```

Open in browser:

```
http://<ALB-DNS>/health
```

🎉 Your app is now live on the internet!

---

## 🧠 Debugging (If Any Issue)

- **Pods not running?**
  ```bash
  kubectl describe pod <pod> -n app
  kubectl logs <pod> -n app
  ```

- **ALB not created?**
  ```bash
  kubectl describe ingress devops-python-ingress -n app
  kubectl logs -n kube-system deployment/aws-load-balancer-controller
  ```

- **Service mismatch?**
  - Ensure labels in Deployment and Service match (`app: devops-python-app`).

---

## 📌 Day 7 Success Checklist

✔ Pods running  
✔ Service created  
✔ Ingress created  
✔ ALB provisioned  
✔ Public URL accessible  
✔ `/health` works  

If all ✔ → you just deployed a **real production app**.

---

## 🧠 What You Achieved

You can now say (truthfully):

> “I deployed a Python microservice on AWS EKS with ALB ingress, IAM-secured controller, secrets, probes, and autoscaling-ready config.”

This is **2026 DevOps-ready language**.





Day 8 — Connect EKS App to AWS RDS PostgreSQL
🎯 Goal
Provision AWS RDS PostgreSQL and securely connect workloads running in EKS to it.

By the end, your FastAPI app will talk to a real production database inside AWS.

⏱ Time Plan (5 Hours)
Time	Task
1 hr	RDS basics + planning
2 hrs	Create PostgreSQL RDS
1 hr	Security Groups
1 hr	Connect app → RDS
1️⃣ RDS Design Decision
We will create:

Engine: PostgreSQL

Subnets: Private (no public access)

Security: SG-based access only

Connectivity: Same VPC as EKS

This matches enterprise standards.

2️⃣ Create RDS PostgreSQL (AWS Console)
Steps:

Go to AWS Console → RDS → Create database

Choose:

Engine: PostgreSQL

Template: Free tier

DB identifier: devops-postgres

Username: appuser

Password: (store safely)

Connectivity:

VPC: Same VPC as EKS

Public access: ❌ No

DB subnet group: Default

Security group: Create new → rds-sg

3️⃣ Security Group Config (Critical)
RDS Security Group (rds-sg):
```

Inbound rule:

Type: PostgreSQL

Port: 5432

Source: EKS Node Security Group
```

📌 This ensures only Kubernetes nodes can access the DB.

4️⃣ Update Kubernetes Secret
Delete old secret:

Code
```
"kubectl delete secret db-secret -n app"
```
Create new secret with RDS endpoint:

Code
```
"kubectl create secret generic db-secret \
  --namespace app \
  --from-literal=DB_HOST=<RDS-ENDPOINT> \
  --from-literal=DB_PORT=5432 \
  --from-literal=DB_NAME=postgres \
  --from-literal=DB_USER=appuser \
  --from-literal=DB_PASSWORD=<password>"
```
Restart pods to pick up new secrets:

Code
```
"kubectl rollout restart deployment devops-python-app -n app"
```
5️⃣ Verify Connection
Check logs:

Code
```
"kubectl logs -n app <pod-name>"
```
Expected output:

Code
```
PostgreSQL connection successful
```
Then test:

Code
```
"http://<ALB-DNS>/health"
```
If it responds → 🎉 FULLY PRODUCTION BACKEND

✅ Day 8 Success Checklist
[x] RDS created

[x] Private DB (no public access)

[x] SG allows EKS → RDS

[x] Secret updated

[x] Pods restarted

[x] App connects to RDS

[x] /health still works

🧠 What You Learned (Interview Gold)
How EKS talks to RDS

Why private DBs matter

How SGs enforce zero trust

How apps consume secrets

How to roll config without downtime

This is real DevOps + Cloud Engineering.


# Debugging EKS ↔ RDS Connectivity (Security Group Fix)

This document captures the main issue faced while deploying a FastAPI application on Amazon EKS with PostgreSQL hosted on Amazon RDS, and how it was resolved.

---

## Issue Summary
- **Problem:** Application pods on EKS were unable to connect to the RDS PostgreSQL instance.
- **Symptom:** Logs showed repeated `connection timed out` errors when trying to connect to RDS.
- **Root Cause:** Security group (SG) rules between EKS worker nodes and RDS were not configured.

---

## Debugging Journey
1. **Observed Errors**
   - Pods started but crashed with DB connection errors.
   - Manual socket tests (`nc` / Python `socket`) inside pods timed out.

2. **Verification**
   - Confirmed EKS and RDS were in the same VPC.
   - Checked RDS SG inbound rules — no allowance for EKS node group SG.

3. **Testing**
   - Deployed a debug pod (`postgres:15` image) inside the EKS cluster.
   - Attempted `psql` connection to RDS → timed out.

---

## Resolution
1. **Configured Security Group Rules**
   - Edited RDS security group to allow inbound traffic on port **5432**.
   - Source set to the EKS cluster/node group security group.

2. **Validation**
   - Re-ran `psql` from debug pod → successful login.
   - Application logs showed:
     ```
     PostgreSQL connection successful
     Database connection verified and closed
     ```
   - Health probes (`/health`) returned `200 OK` consistently.

---

## Lessons Learned
- EKS and RDS **must be in the same VPC** for private connectivity.
- They **do not need to be in the same subnet**, but routing must exist.
- RDS SG must explicitly allow inbound traffic from EKS SG on port 5432.
- Debug pods with `psql` are invaluable for testing DB connectivity inside the cluster.

---

## Next Steps
- Automate SG configuration during infrastructure setup (Terraform/CloudFormation).
- Add retry logic in FastAPI startup to handle temporary DB unavailability.
- Document networking dependencies clearly in deployment guides.





# Day 9 — Database Init, Failure & Recovery (SRE Mindset)

## 🎯 Goal
Initialize the database, verify read/write, simulate failure, and explain recovery.

This day shifts from DevOps to SRE — proving reliability under failure conditions.

---

## ✅ Success Checklist
- [x] DB table created
- [x] Write endpoint works
- [x] Read endpoint works
- [x] DB outage simulated
- [x] Failure observed
- [x] Recovery confirmed
- [x] Incident documented

---

## 1️⃣ Database Initialization

Inside a running pod:

```bash
kubectl exec -it -n app <pod-name> -- bash
apt-get update && apt-get install -y postgresql-client
psql -h $DB_HOST -U $DB_USER -d $DB_NAME
```
Create table:
```
sql
CREATE TABLE health_logs (
  id SERIAL PRIMARY KEY,
  status VARCHAR(50),
  checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
Exit with \q.

📌 Running inside the pod confirms network + secrets + IAM + SGs are correct.

2️⃣ Read / Write API
Endpoints added in app/routes/health.py:
```
python
@router.get("/write")
def write_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO health_logs (status) VALUES (%s)", ("OK",))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Data inserted"}

@router.get("/read")
def read_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, status, checked_at FROM health_logs ORDER BY id DESC LIMIT 5")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"data": rows}
```
Test via ALB:
```
Code
http://<ALB-DNS>/write
http://<ALB-DNS>/read
```
✅ /write → inserts a row
✅ /read → fetches last 5 rows

3️⃣ Failure Simulation
Stop RDS instance in AWS Console:

Go to RDS → Stop instance

Observe pod logs:

bash
kubectl logs -n app <pod-name>
Expected:

Connection errors

App fails readiness probe

ALB returns 503

📌 This is correct behavior.

4️⃣ Recovery Test
Start RDS again:

Pods reconnect automatically

Readiness probe passes

ALB resumes traffic

Test again:
```
Code
http://<ALB-DNS>/health
http://<ALB-DNS>/read
```
✅ Recovery confirmed.

5️⃣ Incident Documentation
```
Create INCIDENT.md:

markdown
# Incident: RDS PostgreSQL Outage

## Impact
- API returned 503
- Writes failed

## Root Cause
- Database instance stopped manually

## Detection
- ALB health checks failed
- Kubernetes readiness probe failed

## Resolution
- Restarted RDS
- Pods reconnected automatically

## Prevention
- Add RDS Multi-AZ
- Add retry logic in DB connection
- Add alerts for DB downtime
```
🧠 Interview Statement
“I’ve handled a backend outage, observed Kubernetes + ALB behavior, and validated automatic recovery.”

This demonstrates real SRE-level DevOps experience.









# Day 10 — CI/CD with GitHub Actions (Foundation)

## 🎯 Goal
On every Git push → Docker image builds → pushed to ECR → deployed to EKS automatically.

After today:
- ❌ No manual `docker build`
- ❌ No manual `kubectl apply`
- ✅ One git push = production update

---

## 🧠 CI/CD Flow

GitHub Push
↓
GitHub Actions Runner
↓
Build Docker Image
↓
Push to AWS ECR
↓
kubectl set image (EKS)
↓
Rolling Update

Code

Modern DevOps (2026‑ready) — no Jenkins, no self‑hosted runners.

---

## ⏱ Time Plan (5 Hours)

| Time | Task |
|------|------|
| 1 hr | Prepare AWS IAM for GitHub |
| 1 hr | Store GitHub Secrets |
| 2 hrs | GitHub Actions workflow |
| 1 hr | Test & debug |

---

## 1️⃣ Create IAM User for CI/CD

- IAM → Users → Create user  
- Name: `github-actions-ecr-eks`  
- Access type: Programmatic  

Attach policy:
json
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:CompleteLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:InitiateLayerUpload",
        "ecr:PutImage"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "eks:ListClusters",
        "eks:DescribeCluster",
        "eks:GetToken"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sts:GetCallerIdentity",
        "sts:AssumeRole"
      ],
      "Resource": "*"
    }
  ]
}
```
Save:

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

2️⃣ Add GitHub Secrets

Repo → Settings → Secrets and variables → Actions → New repository secret

Name	 
```
AWS_ACCESS_KEY_ID	from IAM
AWS_SECRET_ACCESS_KEY	from IAM
AWS_REGION	ap-south-1
AWS_ACCOUNT_ID	your AWS account ID
EKS_CLUSTER_NAME	devops-eks
```
3️⃣ GitHub Actions Workflow
Create file: .github/workflows/deploy.yml

yaml
```
name: CI-CD to EKS

on:
  push:
    branches:
      - main

env:
  ECR_REPO: devops-python-app
  IMAGE_TAG: ${{ github.sha }}

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Login to Amazon ECR
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build Docker image
        run: |
          docker build -t $ECR_REPO:${IMAGE_TAG} .

      - name: Tag Docker image
        run: |
          docker tag $ECR_REPO:${IMAGE_TAG} \
          ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.${{ secrets.AWS_REGION }}.amazonaws.com/$ECR_REPO:${IMAGE_TAG}

      - name: Push image to ECR
        run: |
          docker push \
          ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.${{ secrets.AWS_REGION }}.amazonaws.com/$ECR_REPO:${IMAGE_TAG}

      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig \
            --region ${{ secrets.AWS_REGION }} \
            --name ${{ secrets.EKS_CLUSTER_NAME }}

      - name: Deploy to EKS
        run: |
          kubectl set image deployment/devops-python-app \
            app=${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.${{ secrets.AWS_REGION }}.amazonaws.com/$ECR_REPO:${IMAGE_TAG} \
            -n app
```
4️⃣ Commit & Push
bash
```
git add .github/workflows/deploy.yml
git commit -m "ci: enable github actions deployment"
git push origin main
```
Check GitHub → Actions tab → workflow runs step by step.

5️⃣ Verify Deployment
bash
```
kubectl get pods -n app
kubectl describe deployment devops-python-app -n app
```
Test via ALB:
Code
```
http://<ALB-DNS>/health
http://<ALB-DNS>/read
```
✅ Automated deployment complete.

✅ Success Checklist
[x] IAM user created

[x] GitHub secrets added

[x] Workflow runs successfully

[x] Image pushed to ECR

[x] Deployment updated automatically

[x] App works after push

🧠 Interview Statement
“We use GitHub Actions to build Docker images, push to ECR, and deploy to EKS using rolling updates.”










# DevOps Guide — FastAPI App on Azure

## Project Overview
This project demonstrates end‑to‑end DevOps practices by deploying a Python FastAPI application into cloud infrastructure.  
Originally started on AWS (ECR + EKS), the project was rebuilt from scratch on **Azure** after Day 10 due to account suspension.  
From **Day 12 onward**, all workflows, deployments, and hygiene practices are implemented using **Azure Container Registry (ACR)** and **Azure Kubernetes Service (AKS)**.

---

---

# 🚀 Day 12 — Image Versioning, Retention & Safe Releases (Azure)

## 📌 Release Strategy
- **Dual Tagging**
  - Immutable tags using Git SHA (e.g., `devops-python-app:01de7f5…`)
  - Semantic version tags for releases (e.g., `devops-python-app:v1.0.0`)
- Ensures **traceability** and **human‑friendly rollbacks**.

---

## ⚙️ GitHub Actions Workflow

This workflow:
- Auto‑increments semantic version tags (`v1.0.0 → v1.0.1 → v1.0.2`) using `github-tag-action`.
- Builds and pushes images with both SHA and SemVer tags.
- Deploys directly to AKS with the new version.

```yaml
name: CI-CD to AKS (Azure)

on:
  push:
    branches: [ "main" ]

permissions:
  contents: write   # allow workflow to push new tags

env:
  IMAGE_NAME: devops-python-app

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      # Auto-increment semantic version tags
      - name: Bump Version and Create Tag
        id: bump
        uses: anothrNick/github-tag-action@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          DEFAULT_BUMP: patch   # increments patch version (v1.0.0 → v1.0.1)
          WITH_V: true          # ensures tags are prefixed with 'v'

      - name: Azure Login
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Login to ACR
        run: |
          az acr login --name $(echo ${{ secrets.ACR_LOGIN_SERVER }} | cut -d'.' -f1)

      - name: Build & Push Image (Auto Version)
        run: |
          VERSION=${{ steps.bump.outputs.new_tag }}
          echo "Building image with version: $VERSION"

          docker build -t ${{ secrets.ACR_LOGIN_SERVER }}/${{ env.IMAGE_NAME }}:$VERSION .
          docker push ${{ secrets.ACR_LOGIN_SERVER }}/${{ env.IMAGE_NAME }}:$VERSION

      - name: Get AKS Credentials
        run: |
          az aks get-credentials \
            --resource-group ${{ secrets.AKS_RG }} \
            --name ${{ secrets.AKS_NAME }} \
            --overwrite-existing

      - name: Deploy to AKS
        run: |
          VERSION=${{ steps.bump.outputs.new_tag }}
          kubectl set image deployment/devops-python-app \
            app=${{ secrets.ACR_LOGIN_SERVER }}/${{ env.IMAGE_NAME }}:$VERSION \
            -n app

          kubectl rollout status deployment/devops-python-app -n app --timeout=120s
```

---

## 📖 Release Discipline
- **Create a release tag manually (first time only):**
  ```bash
  git tag v1.0.0
  git push origin v1.0.0
  ```
- **Deploy explicitly by version:**
  ```bash
  kubectl set image deployment/devops-python-app \
    app=<ACR_LOGIN_SERVER>/devops-python-app:v1.0.0 -n app
  ```
- **Rollback cleanly:**
  ```bash
  kubectl set image deployment/devops-python-app \
    app=<ACR_LOGIN_SERVER>/devops-python-app:v0.9.0 -n app
  ```

---

## 🧹 ACR Retention Policy
- Enabled automatic cleanup of **untagged images after 30 days**:
  ```bash
  az acr config retention update \
    --registry devopsacr7295 \
    --status Enabled \
    --days 30 \
    --type UntaggedManifests
  ```
- Verified with:
  ```bash
  az acr config retention show --registry devopsacr7295 -o table
  ```

---

## 🔎 Version Discovery
- **List available tags:**
  ```bash
  az acr repository show-tags \
    --name devopsacr7295 \
    --repository devops-python-app -o table
  ```
- Deploy or rollback using specific tags.

---

## ✅ Day 12 Success Checklist
- No `latest` in deployments  
- CI/CD produces **versioned images**  
- Explicit deployment by release tag (`v1.0.0`)  
- Deterministic rollback by version (`v0.9.0`)  
- ACR retention policy enabled  
- README updated with release strategy  

---

## 📌 Key Takeaway
Day 12 adds **release discipline**:
- Traceable deployments  
- Deterministic rollbacks  
- Cost & security hygiene  
- Professional artifact lifecycle management  

This is where **DevOps becomes reliable engineering**.

---

## 🔮 Future Reference
- **Version bumping rules**:  
  - `patch` → bug fixes (`v1.0.1`)  
  - `minor` → new features (`v1.1.0`)  
  - `major` → breaking changes (`v2.0.0`)  
- **Automation**: integrate commit message conventions (`feat:`, `fix:`, `BREAKING CHANGE:`) to auto‑decide bump type.  
- **Safe releases**: always deploy by explicit version, never `latest`.  
- **Rollback strategy**: keep at least 2–3 stable tags in ACR for deterministic rollbacks.  
- **Retention hygiene**: monitor ACR cleanup policies to avoid cost/security issues.  

---




## 🚀 Day 13 — Blue/Green Deployments (Zero Downtime)
🎯 Goal
Deploy a new version without impacting users, then switch traffic instantly.

By the end of Day 13:


Two versions run side‑by‑side

Traffic switch is controlled

Rollback is instant (no rebuilds)

1️⃣ Blue/Green Concept
```
Blue → current stable version

Green → new version

Both run at the same time

Service selector decides who gets traffic
```
This avoids:

Partial rollouts

Broken releases

Slow rollbacks

2️⃣ Blue Deployment (Stable Version)
blue-dep.yaml

yaml
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devops-python-app-blue
  namespace: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: devops-python-app
      version: blue
  template:
    metadata:
      labels:
        app: devops-python-app
        version: blue
    spec:
      containers:
        - name: app
          image: devopsacr7295.azurecr.io/devops-python-app:v3.0.3
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: db-secret   # ensures DB connection works
```
Apply:

bash
```
kubectl apply -f blue-dep.yaml
```
3️⃣ Green Deployment (New Version)
green-dep.yaml

yaml
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devops-python-app-green
  namespace: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: devops-python-app
      version: green
  template:
    metadata:
      labels:
        app: devops-python-app
        version: green
    spec:
      containers:
        - name: app
          image: devopsacr7295.azurecr.io/devops-python-app:v3.0.4
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: db-secret
```
Apply:

bash
```
kubectl apply -f green-dep.yaml
```
4️⃣ Service + LoadBalancer (Browser Access)
service.yaml

yaml
```
apiVersion: v1
kind: Service
metadata:
  name: devops-python-service
  namespace: app
spec:
  type: LoadBalancer
  selector:
    app: devops-python-app
    version: blue   # initially points to Blue
  ports:
    - port: 80
      targetPort: 8000
```
Apply:

bash
```
kubectl apply -f service.yaml
kubectl get svc -n app
```
You’ll see an EXTERNAL-IP (Azure Load Balancer).
Test in browser:

Code
```
http://<EXTERNAL-IP>/health
http://<EXTERNAL-IP>/read
```
5️⃣ Traffic Switch (Zero Downtime)
Switch traffic to Green:

bash
```
kubectl patch service devops-python-service -n app \
  -p '{"spec":{"selector":{"app":"devops-python-app","version":"green"}}}'
```
⚡ Traffic instantly shifts to Green pods, external IP stays the same.

6️⃣ Instant Rollback
Switch back to Blue:

bash
```
kubectl patch service devops-python-service -n app \
  -p '{"spec":{"selector":{"app":"devops-python-app","version":"blue"}}}'
```
Rollback is immediate — no rebuilds, no waiting.

7️⃣ Cleanup (Optional)
Once Green is stable:

bash
kubectl delete deployment devops-python-app-blue -n app
Or keep both for next release cycle.

✅ Day 13 Success Checklist
✔ Blue deployment running
✔ Green deployment running
✔ Service exposed via LoadBalancer
✔ Traffic switched without downtime
✔ Rollback tested
✔ Browser access verified

🧠 Interview Gold
“We use Blue/Green deployments on Kubernetes by running two versions in parallel and switching traffic at the Service level for zero‑downtime releases. The external IP stays constant, so users never see disruption.”






## 🚀 Day 14 — Canary Deployments (Progressive Traffic)
🎯 Goal
Send a portion of traffic to the new version (Canary) while most traffic continues to hit the stable version (Blue). This allows safe, incremental rollout and instant rollback.

1️⃣ Canary Concept
```
Blue → stable version (majority of traffic)

Canary → new version (small portion of traffic)

Service selector → includes both Blue + Canary pods

Traffic split → controlled by replica counts
```
This avoids:

Risky full rollouts

User disruption if Canary fails

Slow rollback

2️⃣ Blue Deployment (Stable Version)
blue-dep.yaml
```
yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devops-python-app-blue
  namespace: app
spec:
  replicas: 4
  selector:
    matchLabels:
      app: devops-python-app
      version: blue
  template:
    metadata:
      labels:
        app: devops-python-app
        version: blue
        release-track: canary-blue   # shared label
    spec:
      containers:
        - name: app
          image: devopsacr7295.azurecr.io/devops-python-app:v3.0.3
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: db-secret
```
3️⃣ Canary Deployment (New Version)
canary-dep.yaml
```
yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devops-python-app-canary
  namespace: app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: devops-python-app
      version: canary
  template:
    metadata:
      labels:
        app: devops-python-app
        version: canary
        release-track: canary-blue   # shared label
    spec:
      containers:
        - name: app
          image: devopsacr7295.azurecr.io/devops-python-app:v3.0.4
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: db-secret
```
4️⃣ Service (LoadBalancer)
service.yaml
```
yaml
apiVersion: v1
kind: Service
metadata:
  name: devops-python-service
  namespace: app
spec:
  type: LoadBalancer
  selector:
    release-track: canary-blue   # selects Blue + Canary pods only
  ports:
    - port: 80
      targetPort: 8000
```
Apply:

bash
```
kubectl apply -f service.yaml
kubectl get svc -n app
```
Test in browser:

Code
```
http://<EXTERNAL-IP>/health
http://<EXTERNAL-IP>/read
```
5️⃣ Traffic Split by Replicas
Traffic distribution is proportional to pod count:
```
Blue: 4 replicas

Canary: 1 replica

Result: ~80% traffic → Blue, ~20% traffic → Canary.
```
Scale deployments:

bash
```
kubectl scale deployment devops-python-app-blue --replicas=4 -n app
kubectl scale deployment devops-python-app-canary --replicas=1 -n app
```
6️⃣ Progressive Rollout Plan
Increase Canary gradually:

bash
```
# Step 1: 10% Canary
kubectl scale deployment devops-python-app-blue --replicas=9 -n app
kubectl scale deployment devops-python-app-canary --replicas=1 -n app

# Step 2: 25% Canary
kubectl scale deployment devops-python-app-blue --replicas=6 -n app
kubectl scale deployment devops-python-app-canary --replicas=2 -n app

# Step 3: 50% Canary
kubectl scale deployment devops-python-app-blue --replicas=5 -n app
kubectl scale deployment devops-python-app-canary --replicas=5 -n app

# Step 4: 100% Canary (full rollout)
kubectl scale deployment devops-python-app-blue --replicas=0 -n app
kubectl scale deployment devops-python-app-canary --replicas=10 -n app
7️⃣ Rollback Instantly
```
If Canary fails:

bash
```
kubectl scale deployment devops-python-app-canary --replicas=0 -n app
kubectl scale deployment devops-python-app-blue --replicas=10 -n app
```
All traffic returns to Blue.

✅ Day 14 Success Checklist
✔ Service selector includes Blue + Canary pods
✔ LoadBalancer IP routes traffic to both versions
✔ Replica counts control traffic percentage
✔ Verified responses from both versions in browser
✔ Canary scaled up/down safely
✔ Rollback tested

🧠 Interview Gold
“We implement Canary deployments by assigning Blue and Canary pods a shared label, then pointing the Service selector to that label. Traffic distribution is controlled by replica counts, allowing progressive rollout and instant rollback without downtime.”




# Day 15 — Monitoring & Observability (Prometheus + Grafana)

## 🎯 Goal
By the end of Day 15:
- Prometheus installed in AKS
- Grafana dashboard accessible
- Cluster & pod metrics visible (CPU, memory, status)
- Observability basics understood

---

## 🛠 Installation

### Step 1 — Add Helm Repo
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```
Step 2 — Install kube-prometheus-stack
bash
```
kubectl create namespace monitoring

helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring
```
This installs Prometheus, Grafana, Alertmanager, Node Exporter, and supporting components.

✅ Verification
Step 3 — Check Pods
bash
```
kubectl get pods -n monitoring
```
Expected: Prometheus, Grafana, Alertmanager, Node Exporter all running.

⚠️ Issues Faced & Debugging Journey
1. Grafana Access Issue
Problem: Grafana was only accessible via kubectl port-forward.

Fix: Exposed Grafana via Ingress.

Patched Grafana Deployment with:

yaml
```
GF_SERVER_ROOT_URL=http://<IP>/grafana
GF_SERVER_SERVE_FROM_SUB_PATH=true
```
Created Ingress path /grafana.

2. Prometheus Access Issue
Problem: Direct StatefulSet edits reverted (managed by Operator).

Fix: Edited Prometheus Custom Resource (CR):

yaml
```
externalUrl: http://<IP>/prometheus
routePrefix: /prometheus
```
Created Ingress path /prometheus.

3. Grafana Showing “No Data”
Problem: Dashboards empty despite Prometheus targets being UP.

Debugging Steps:

Checked Prometheus /targets → confirmed node-exporter, kube-state-metrics, kubelet all UP.

Verified Grafana datasource → pointed to internal service (monitoring-kube-prometheus-prometheus.monitoring:9090).

Root Cause: Grafana was querying Prometheus at wrong URL (cluster‑internal, not Ingress).

Fix:

Edited ConfigMap:

bash
```
kubectl edit configmap monitoring-kube-prometheus-grafana-datasource -n monitoring
```
Changed Prometheus datasource URL:

yaml
```
url: http://<Ingress-IP>/prometheus
```
Restarted Grafana:

bash
```
kubectl rollout restart deployment monitoring-grafana -n monitoring
```
Re-tested query up in Grafana Explore → metrics visible.

📊 Results
Prometheus scraping targets successfully:

Node Exporter

Kube State Metrics

Kubelet

CoreDNS

Apiserver

Grafana dashboards now show:

Cluster CPU & memory usage

Pod status & restarts

Node metrics

🧠 Lessons Learned
Ingress vs Port-Forward:  
Production monitoring tools must be exposed via Ingress, not port-forward.

Operator Reconciliation:  
Prometheus Operator manages StatefulSets. Always edit the CR, not the StatefulSet.

Datasource Alignment:  
Grafana must query Prometheus via the same external path (/prometheus).
Internal service URLs won’t work when accessed via Ingress.

Debugging Flow:

Check Prometheus /targets → confirms scraping.

Check Grafana datasource → confirms query path.

Fix ConfigMap → restart Grafana → validate with up query.

✅ Day 15 Success Checklist
[x] Prometheus installed

[x] Grafana running via Ingress

[x] Pod & node metrics visible

[x] CPU/memory charts working

[x] Debugging journey documented


# 🚀 Day 16 — Horizontal Pod Autoscaling (HPA)

## 🎯 Goal
By the end of Day 16, we enabled **Horizontal Pod Autoscaler (HPA)** in our Kubernetes cluster to:
- Automatically scale pods based on CPU usage.
- Understand how Kubernetes achieves production‑grade elasticity.
- Validate scaling behavior under simulated load.

---

## 🧠 Why HPA Matters
- Without HPA, replicas are set manually (`replicas: 2`, `replicas: 4`).
- In real systems, traffic and CPU usage fluctuate.
- HPA allows Kubernetes to **scale pods up/down automatically** based on resource usage.
- This ensures reliability, prevents outages, and optimizes resource costs.

---

## ⚡ Metrics Server

### What is Metrics Server?
- A lightweight aggregator that collects CPU and memory usage from **Kubelets**.
- Provides metrics to the Kubernetes API so HPA can make scaling decisions.

### Why We Use It
- HPA depends on metrics‑server to calculate utilization.
- Without metrics‑server, HPA shows `<unknown>` for CPU targets.

### Verification
```bash
kubectl get deployment metrics-server -n kube-system
kubectl top nodes
kubectl top pods -n app
```
If CPU/memory values are visible → metrics‑server is working.

⚡ Horizontal Pod Autoscaler (HPA)
What is HPA?
A Kubernetes resource that automatically adjusts the number of pod replicas in a deployment.

Scaling is based on observed CPU/memory usage or custom metrics.

How It Works
Metrics‑server reports CPU/memory usage.

HPA compares usage against the target threshold (e.g., 50% CPU).

If usage > target → scale up pods (up to max).

If usage < target → scale down pods (not below min).

⚡ YAML Modifications
Original Deployment (simplified)
```
yaml
containers:
  - name: app
    image: devopsacr7295.azurecr.io/devops-python-app:v1
    ports:
      - containerPort: 8000
    readinessProbe:
      httpGet:
        path: /health
        port: 8000
    livenessProbe:
      httpGet:
        path: /health
        port: 8000
```
Modified Deployment (added resources)
yaml
```
containers:
  - name: app
    image: devopsacr7295.azurecr.io/devops-python-app:v1
    ports:
      - containerPort: 8000
    readinessProbe:
      httpGet:
        path: /health
        port: 8000
    livenessProbe:
      httpGet:
        path: /health
        port: 8000
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
      limits:
        cpu: "500m"
        memory: "256Mi"
```
👉 Why?  
HPA requires CPU requests to calculate utilization. Without them, HPA fails with missing request for cpu.

⚡ Creating HPA
```
bash
kubectl autoscale deployment devops-python-app \
  --cpu=50% \
  --min=2 \
  --max=6 \
  -n app
Target CPU = 50% of requested CPU.

Minimum pods = 2.

Maximum pods = 6.
```
⚡ Verification
Check HPA:

bash
```
kubectl get hpa -n app
```
Example output:

Code
```
NAME                REFERENCE                      TARGETS        MINPODS   MAXPODS   REPLICAS   AGE
devops-python-app   Deployment/devops-python-app   cpu: 39%/50%   2         6         2          11m
```
👉 This means pods are using ~39% of requested CPU, below the 50% target, so replicas remain at 2.

⚡ Simulating Load
Run a busybox pod to generate traffic:

bash
```
kubectl run -it --rm load-generator \
  --image=busybox \
  -- /bin/sh
  ```
Inside container:

bash
```
while true; do wget -q -O- http://devops-python-service.app.svc.cluster.local; done
```
Watch scaling:

bash
```
kubectl get pods -n app -w
```
Pods will increase if CPU rises above 50%.

✅ Day 16 Success Checklist
[x] Metrics‑server installed and working.

[x] Resource requests/limits added to deployments.

[x] HPA created successfully.

[x] kubectl top shows metrics.

[x] HPA reports utilization (cpu: 39%/50%).

[x] Pods scale under load.

🧠 What You Learned
Metrics‑server provides resource usage data.

HPA uses that data to scale pods automatically.

Resource requests are mandatory for HPA to compute utilization.

This is production elasticity — the foundation of cloud‑native reliability.



# 🚀 Day 17 — Graceful Shutdown + Zero‑Downtime Behavior

## 🎯 Goal
Ensure application pods shut down gracefully during:
- Rolling updates
- Node drain
- Scaling events

This prevents:
- Half‑completed database writes
- Broken API requests
- Sudden 502 errors

---

## 🧠 Why This Matters
When Kubernetes removes a pod, it follows this sequence:

1. **SIGTERM sent** → Kubernetes politely asks the container to stop.
2. **terminationGracePeriodSeconds** → Kubernetes waits this long before force‑killing the pod.
3. **SIGKILL sent** → If the pod hasn’t stopped by then, Kubernetes kills it immediately.

👉 If the app doesn’t handle SIGTERM properly:
- Requests drop
- DB connections break
- Users see errors

---

## ⚡ Key Concepts

### SIGTERM
- A signal meaning “please terminate.”
- Gives the application a chance to finish ongoing work before shutting down.

### terminationGracePeriodSeconds
- The time Kubernetes waits after sending SIGTERM before force‑killing the pod.
- Default = 30 seconds.
- Can be configured in the pod spec.

### preStop Hook
- A lifecycle hook that runs before the container shuts down.
- Example: `sleep 10` → pod waits 10 seconds before stopping.
- Allows time for draining connections and finishing requests.

---

## ⚡ YAML Modifications

### Original Deployment (simplified)
```yaml
spec:
  containers:
    - name: app
      image: devopsacr7295.azurecr.io/devops-python-app:v1
      ports:
        - containerPort: 8000
Modified Deployment (graceful shutdown)
yaml
spec:
  terminationGracePeriodSeconds: 30
  containers:
    - name: app
      image: devopsacr7295.azurecr.io/devops-python-app:v1
      ports:
        - containerPort: 8000
      lifecycle:
        preStop:
          exec:
            command: ["/bin/sh", "-c", "sleep 10"]
```
⚡ Hands‑On Verification
Apply changes:
```
bash
kubectl apply -f deployment.yaml
```
Trigger rolling update:
```
bash
kubectl set image deployment/devops-python-app app=devopsacr7295.azurecr.io/devops-python-app:v3.0.0 -n app
```
Watch pods:
```
bash
kubectl get pods -n app -w
```
Expected behavior:

Old pod enters Terminating.

Stays alive briefly (grace period + preStop).

New pod becomes Ready.

Traffic shifts → no downtime.

✅ Day 17 Success Checklist
[x] Added terminationGracePeriodSeconds

[x] Added preStop hook

[x] Applied deployment changes

[x] Triggered rolling update

[x] Verified pods terminate gracefully while new ones come up

🧠 Interview Power
If asked:
“How do you prevent request drops during deployment?”

You can say:

“We configure terminationGracePeriodSeconds and preStop hooks so pods drain connections and finish requests before shutting down.”



# 🚀 Day 18 — Network Policies (Cluster Security)

## 🎯 Goal
Implement Kubernetes **NetworkPolicies** to:
- Restrict pod-to-pod communication.
- Allow only required traffic paths.
- Prevent lateral movement in case of a compromised pod.

---

## 🧠 Why This Matters
By default, Kubernetes networking is **open**:
- Any pod can talk to any other pod.
- This is convenient for development but unsafe in production.

### Risks:
- A compromised pod can scan the cluster.
- Sensitive services (DB, APIs) are exposed.
- Attackers can move laterally across workloads.

👉 NetworkPolicies act like **firewalls inside Kubernetes**, enforcing isolation and security.

---

## ⚡ Key Concepts

### NetworkPolicy
- A Kubernetes resource that controls **Ingress** (incoming) and **Egress** (outgoing) traffic for pods.
- Works at the **pod level**, based on labels.
- Enforced by the CNI plugin (Azure CNI in AKS supports this).

### Default-Deny
- A baseline policy that blocks all traffic.
- Ensures pods cannot communicate unless explicitly allowed.

### Allow Rules
- Policies that permit specific communication paths.
- Example: allow only `app: devops-python-app` pods to talk to each other.

---

## ⚡ YAML Configurations

### Step 1 — Default Deny Policy
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: app
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```
👉 Effect: All traffic blocked in namespace app.

Step 2 — Allow App Traffic
```
yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-app-traffic
  namespace: app
spec:
  podSelector:
    matchLabels:
      app: devops-python-app
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: devops-python-app
  policyTypes:
  - Ingress
  - Egress
```
👉 Effect: Only pods with label app: devops-python-app can talk to each other.

⚡ Hands-On Verification
1. Launch Test Pod
```
bash
kubectl run test-pod --rm -it --image=busybox -n app -- /bin/sh
```
2. Try Communication
Inside test-pod:
```
bash
wget -qO- http://devops-python-app.app.svc.cluster.local:8000/health
```
With default-deny → request fails.

With allow-app-traffic → request succeeds only if source pod has correct label.

3. Direct Pod Testing
```
bash
kubectl exec -it <pod-name> -n app -- /bin/sh
curl http://devops-python-app.app.svc.cluster.local:8000/health
```
✅ Day 18 Success Checklist

```
[x] Verified AKS supports NetworkPolicy (Azure CNI).

[x] Applied default-deny policy.

[x] Confirmed communication blocked.

[x] Applied allow-app-traffic policy.

[x] Verified only labeled pods can communicate.
```
🧠 Interview Power
If asked:
“How do you secure pod-to-pod communication?”

You can say:

“We implement Kubernetes NetworkPolicies with a default-deny baseline and then allow only required traffic paths. This prevents lateral movement and enforces least-privilege networking.”





## 🚀 Day 19 — Terraform Fundamentals

This project demonstrates the basics of using **Terraform with Azure** to provision infrastructure declaratively.

---

## 📂 Project Structure
```
terraform-azure/
├── main.tf
├── provider.tf
├── variables.tf
└── outputs.tf
```
Code

### File Purposes
- **provider.tf** → Configures the Azure provider.
- **main.tf** → Defines the resources (here, a Resource Group).
- **variables.tf** → Holds input variables (parameterization).
- **outputs.tf** → Defines outputs (useful values after apply).

---

## 🛠 Steps

### Step 1 — Install Terraform
Check if installed:
```bash
terraform -v
```
If not:
```
bash
sudo apt-get update
sudo apt-get install -y terraform
```
Step 2 — Create Project Structure
```
bash
mkdir terraform-azure && cd terraform-azure
touch main.tf provider.tf variables.tf outputs.tf
```
Step 3 — Provider Configuration
```
provider.tf:

hcl
provider "azurerm" {
  features {}
}
```
Step 4 — Define Resource Group
```
main.tf:

hcl
resource "azurerm_resource_group" "devops_rg" {
  name     = "tf-devops-rg"
  location = "East US"
}
```
Step 5 — Initialize Terraform
```
bash
terraform init
```
Step 6 — Plan
```
bash
terraform plan
```
Expected output:
```
Code
Plan: 1 to add, 0 to change, 0 to destroy
```
Step 7 — Apply
```
bash
terraform apply
Type yes when prompted.
```

Check Azure Portal → Resource Group tf-devops-rg created.

🧠 Concepts Learned
Terraform Workflow:

Write code (.tf files)

terraform init → initialize provider plugins

terraform plan → preview changes

terraform apply → apply changes

State File (terraform.tfstate):

Tracks what Terraform has created.

Maps your code to real resources in Azure.

Must be secured (contains sensitive data).

Enables Terraform to know what to add/change/destroy.

🎯 Day 19 Success Checklist
```
✔ Terraform installed
✔ Provider configured
✔ Resource group created
✔ Understood state file
```



# 🚀 Day 20 — Provision Azure Container Registry (ACR) via Terraform

This project builds on Day 19 by provisioning **real cloud resources** in Azure using Terraform.  
We introduce **variables** to avoid hardcoding values and reinforce the importance of **Terraform state**.

---

## 📂 Project Structure
```
terraform-azure/
├── main.tf
├── provider.tf
├── variables.tf
└── outputs.tf
```
Code

### File Purposes
- **provider.tf** → Configures the Azure provider.
- **main.tf** → Defines resources (Resource Group + ACR).
- **variables.tf** → Declares input variables (location, RG name, ACR name).
- **outputs.tf** → Prints useful values after apply (e.g., ACR login server).

---

## 🛠 Step 1 — Add Variables

`variables.tf`:
```hcl
variable "location" {
  default = "East US"
}

variable "resource_group_name" {
  default = "tf-devops-rg"
}

variable "acr_name" {
  default = "tfdevopsacr12345"
}
```
⚠️ Note: ACR names must be globally unique. Change the number if needed.

🛠 Step 2 — Update main.tf
`main.tf`:
```
hcl
resource "azurerm_resource_group" "devops_rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.devops_rg.name
  location            = var.location
  sku                 = "Basic"
  admin_enabled       = true
}
```
Here:

Resource Group is created using variables.

ACR depends on the Resource Group (resource_group_name = azurerm_resource_group.devops_rg.name).

🛠 Step 3 — Run Terraform
Initialize:
```
bash
terraform init
```
Plan:
```
bash
terraform plan
```
Expected:
```
Code
Plan: 1 to add, 0 to change, 0 to destroy
```
Apply:
```
bash
terraform apply
```
Type yes when prompted.

Check Azure Portal → ACR created.

🧠 Concepts Learned
1. Variables
Avoid hardcoding values.

Make configuration reusable and professional.

2. Resource Dependencies
Terraform automatically knows ACR depends on the Resource Group.

Ensures correct creation order.

3. State File (terraform.tfstate)
Tracks what Terraform has created.

Prevents duplicate creation.

Allows modification tracking.

If deleted → Terraform forgets infra exists.

🎯 Day 20 Success Checklist
```
✔ ACR created via Terraform
✔ Variables used cleanly
✔ No hardcoded values
✔ Terraform state understood
```



## 🚀 Day 21 — Provision AKS Using Terraform

## 🎯 Goal
Provision an **Azure Kubernetes Service (AKS)** cluster using Terraform, ensuring:
- Declarative infrastructure (no manual CLI).
- Reproducible cluster creation.
- Node pool defined in code.
- Terraform state tracks the cluster.

---

## 🧠 Why This Matters
- Manual cluster creation (via Azure CLI/Portal) is error‑prone and not reproducible.
- Terraform allows **Infrastructure as Code (IaC)**:
  - Clusters can be recreated consistently across environments.
  - Configurations are version‑controlled.
  - State tracks resources for drift detection.

👉 This is how platform engineers ensure **environment parity** and **automation**.

---

## ⚡ Terraform AKS Resource

### main.tf
```hcl
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "tf-devops-aks"
  location            = var.location
  resource_group_name = azurerm_resource_group.devops_rg.name
  dns_prefix          = "tfdevops"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
  }
}
```
Key Arguments
```
name → Cluster name.

default_node_pool → Defines node pool size and VM type.

identity → SystemAssigned managed identity for cluster resources.

network_profile → Azure CNI plugin for networking.
```
⚡ Provisioning Workflow
Step 1 — Initialize Terraform
```
bash
terraform init
```
Step 2 — Plan Resources
```
bash
terraform plan
```
Shows what Terraform will create.

Step 3 — Apply
```
bash
terraform apply
```
Creates AKS cluster (takes 5–10 minutes).

⚡ Step 3 — Outputs (Cluster Access)

Add to `outputs.tf`:
```
hcl
output "kube_config" {
  value     = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}
```
Why?
Normally, you’d run az aks get-credentials to fetch kubeconfig.

With Terraform, we output kubeconfig directly → fully automated.

Sensitive = true hides secrets from logs.

Usage
After apply:
```
bash
terraform output kube_config > kubeconfig
export KUBECONFIG=$(pwd)/kubeconfig
kubectl get nodes
```
👉 If nodes are listed, kubectl is connected to your Terraform‑provisioned AKS cluster.

✅ Day 21 Success Checklist

[x] AKS resource defined in Terraform.

[x] Cluster created via terraform apply.

[x] kubeconfig exported from Terraform outputs.

[x] kubectl get nodes shows cluster nodes.

[x] No manual Azure CLI used.

🧠 Interview Power
```
If asked:
“How do you create your Kubernetes cluster?”

You can say:

“We provision AKS clusters using Terraform modules. Terraform outputs the kubeconfig, which we export to connect with kubectl. This ensures reproducibility, automation, and environment parity.”
```




# 🚀 Day 22 — Remote State + Variables (Professional Terraform)

## 🎯 Goal
By the end of Day 22:
- Terraform state stored remotely in Azure Blob Storage
- State locking enabled
- Backend configured
- Variables moved to `terraform.tfvars`
- Professional project structure achieved

---

## 🧠 Why Remote State Matters
Terraform state = **source of truth** for your infrastructure.

Problems with local state:
- If laptop crashes → state lost
- Team members can’t collaborate
- Risk of infra drift
- No locking → multiple engineers can overwrite each other

👉 Remote state solves this by storing state in a shared, resilient backend.

---

## ⚡ Step 1 — Create Storage Account + Container
Use Azure CLI (one‑time setup):

```bash
az storage account create \
  --name tfdevopsstorage12345 \
  --resource-group tf-devops-rg \
  --location eastus \
  --sku Standard_LRS

az storage container create \
  --name tfstate \
  --account-name tfdevopsstorage12345

 ```
This creates a storage account and a container to hold the Terraform state file.

# ⚡ Step 2 — Backend Configuration
Create `backend.tf`:
```
hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "tf-devops-rg"
    storage_account_name = "tfdevopsstorage12345"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
```
👉 This tells Terraform to use Azure Blob Storage as the backend.

# ⚡ Step 3 — Reinitialize Terraform
Run:

bash
```
terraform init
```
Terraform detects the backend change.

It asks: “Do you want to copy existing state to the new backend?”

Type yes → local state is migrated into Azure Blob Storage.

State locking is enabled automatically.

# ⚡ Step 4 — Confirm Remote State
Delete local state files:
```
bash

rm terraform.tfstate terraform.tfstate.backup
Run:

bash
terraform plan
```
👉 If Terraform still knows about your resources, it’s reading state from Azure Blob Storage.

# ⚡ Step 5 — Move Variables to terraform.tfvars
Create `terraform.tfvars`:
```
hcl
location            = "eastus"
resource_group_name = "tf-devops-rg"
acr_name            = "tfdevopsacr12345"
```
👉 Cleaner, production style. No hard‑coding in main.tf.

✅ Day 22 Success Checklist
[x] Azure Storage created

[x] Backend configured

[x] State migrated to remote

[x] Local state deleted

[x] Variables moved to tfvars

🧠 Interview Power
```
If asked:
“How do you manage Terraform state?”

You can say:

“We use Azure Blob Storage backend with state locking to ensure safe collaboration and prevent drift. Variables are managed via tfvars for clean, production‑ready structure.”
```
🎯 Interview Power
```
If asked:
“How do you manage variables in Terraform?”  
You can say:

“We define variables in variables.tf for clarity and type safety, and supply values via terraform.tfvars. This separation ensures clean, production‑ready Terraform code and makes it easy to manage multiple environments.”
```



## Day 23 – Terraform Azure Modular Infrastructure
📌 Overview
On Day 23, we built a modular Terraform project that provisions:

Azure Resource Group

Azure Container Registry (ACR)

Azure Kubernetes Service (AKS)

PostgreSQL Flexible Server

Remote backend for state management

This project follows production‑style best practices: modular structure, variable separation, remote state, and reusable code. It also documents real‑world troubleshooting (name uniqueness, VM size restrictions, zone mismatches).

📂 Project Structure
Code
```
terraform-azure/
│
├── backend.tf
├── provider.tf
├── variables.tf
├── terraform.tfvars
├── main.tf
│
└── modules/
    ├── resource-group/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    │
    ├── acr/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    │
    ├── aks/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    │
    └── postgres/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```
⚙️ Root Files
`provider.tf`
```hcl

provider "azurerm" {
  features {}
}
```
variables.tf
```hcl
variable "location" {}
variable "resource_group_name" {}
variable "acr_name" {}
variable "aks_name" {}
variable "postgres_name" {}
variable "db_admin_user" {}
variable "db_admin_password" {
  sensitive = true
}
```
`terraform.tfvars`
```hcl

location            = "Central US"
resource_group_name = "tf-devops-rg"
acr_name            = "tfdevopsacr98765"
aks_name            = "tf-devops-aks"
postgres_name       = "tfdevopspg98765"
db_admin_user       = "appuser"
db_admin_password   = "StrongPass@123"
backend.tf
hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "tfstateaccount123"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
```
`main.tf`

```hcl

module "resource_group" {
  source   = "./modules/resource-group"
  name     = var.resource_group_name
  location = var.location
}

module "acr" {
  source              = "./modules/acr"
  acr_name            = var.acr_name
  resource_group_name = module.resource_group.name
  location            = var.location
}

module "aks" {
  source              = "./modules/aks"
  aks_name            = var.aks_name
  resource_group_name = module.resource_group.name
  location            = var.location
}

module "postgres" {
  source              = "./modules/postgres"
  postgres_name       = var.postgres_name
  resource_group_name = module.resource_group.name
  location            = var.location
  admin_user          = var.db_admin_user
  admin_password      = var.db_admin_password
}
```

`backend.tf`
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "tfstateaccount123"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
```
📦 Modules
Resource Group
`main.tf`

```hcl
resource "azurerm_resource_group" "this" {
  name     = var.name
  location = var.location
}
```
`variables.tf`

```hcl
variable "name" {}
variable "location" {}
```
`outputs.tf`

```hcl
output "name" {
  value = azurerm_resource_group.this.name
}
```
ACR
`main.tf`

```hcl
resource "azurerm_container_registry" "this" {
  name                = var.acr_name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "Basic"
  admin_enabled       = true
}
```
`variables.tf`

```hcl
variable "acr_name" {}
variable "resource_group_name" {}
variable "location" {}
```
`outputs.tf`

```hcl
output "login_server" {
  value = azurerm_container_registry.this.login_server
}
```
AKS
`main.tf`

```hcl
resource "azurerm_kubernetes_cluster" "this" {
  name                = var.aks_name
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = var.aks_name

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_D2s_v3"   # Supported in Central US
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
  }
}
```
`variables.tf`

```hcl
variable "aks_name" {}
variable "resource_group_name" {}
variable "location" {}
```
`outputs.tf`

```hcl
output "kube_config" {
  value     = azurerm_kubernetes_cluster.this.kube_config_raw
  sensitive = true
}
```
PostgreSQL
`main.tf`

```hcl
resource "azurerm_postgresql_flexible_server" "this" {
  name                   = var.postgres_name
  resource_group_name    = var.resource_group_name
  location               = var.location
  version                = "14"
  administrator_login    = var.admin_user
  administrator_password = var.admin_password
  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768

  zone = "1"

  high_availability {
    mode = "Disabled"
  }
}
```
`variables.tf`

```hcl
variable "postgres_name" {}
variable "resource_group_name" {}
variable "location" {}
variable "admin_user" {}
variable "admin_password" {
  sensitive = true
}
```
`outputs.tf`

```hcl
output "postgres_fqdn" {
  value = azurerm_postgresql_flexible_server.this.fqdn
}
```
🚀 Deployment Steps
```bash
terraform init
terraform plan
terraform apply -auto-approve
```
`Post‑Apply`
Export kubeconfig:

```bash
terraform output -raw module.aks.kube_config > kubeconfig
export KUBECONFIG=$(pwd)/kubeconfig
kubectl get nodes
```
🛠️ Troubleshooting Notes
ACR Name Conflict → Must be globally unique. Changed to tfdevopsacr98765.

AKS VM Size Restriction → Standard_B2s not allowed in Central US. Switched to Standard_D2s_v3.

PostgreSQL Zone Error → Fixed by explicitly setting zone = "1" and disabling HA.

🧹 Cleanup
Destroy resources to avoid cost:

```bash
terraform destroy -auto-approve
```
🎯 Outcome
By the end of Day 23:

You deployed a modular, production‑style Terraform project.

You overcame region restrictions, VM size quotas, and zone mismatches.

You now have a portfolio‑ready project demonstrating real‑world troubleshooting.


## 🚀 Day 24 — Full Reproducibility Test (Destroy & Recreate Drill)

## 📌 Overview
Up to now, we’ve been building infrastructure incrementally.  
Day 24 is different — it’s about **proving reproducibility**.  

> “My infrastructure is fully reproducible from code.”

This is a **maturity checkpoint** in Infrastructure as Code (IaC).  
If you can destroy and recreate everything without manual steps, you’ve reached true platform engineering level.

---

## 🎯 Goal of Day 24
By the end of today, you will:
- ✔ Destroy entire infrastructure
- ✔ Recreate from scratch
- ✔ Redeploy application
- ✔ Verify ingress works
- ✔ Confirm zero manual steps

---

## 🛠 Step 1 — Destroy Everything
From the Terraform root:
```bash
terraform destroy
```
Type:

```Code

yes
```
Wait until:

```Code
Destroy complete
```
Verify in Azure Portal → nothing left.

🛠 Step 2 — Recreate Infrastructure
Run:

```bash
terraform apply
```
Terraform will provision:

AKS cluster

PostgreSQL Flexible Server

Azure Container Registry (ACR)

🛠 Step 3 — Get kubeconfig
Export kubeconfig for AKS:

```bash
terraform output -raw module.aks.kube_config > kubeconfig
export KUBECONFIG=$(pwd)/kubeconfig
kubectl get nodes
```
🛠 Step 4 — Redeploy Application
Reapply Kubernetes manifests:

```bash
kubectl create namespace app
kubectl apply -f db-secret.yaml -n app
kubectl apply -f deployment.yaml -n app
kubectl apply -f service.yaml -n app
kubectl apply -f ingress.yaml -n app
```
Test endpoints:

```bash
curl http://<INGRESS-IP>/health
curl http://<INGRESS-IP>/read
curl http://<INGRESS-IP>/write
```
If everything works → Day 24 success!

🧠 Why This Is Massive
Most learners:

Build once

Never test reproducibility

Panic if infra is deleted

You:

Can destroy and recreate confidently

Prove infra is code-driven, not manual

This is real IaC maturity.

📈 Interview Power
If asked:

“What happens if someone deletes your cluster?”

You answer:

We recreate the entire platform using Terraform modules and redeploy through CI/CD. Everything is reproducible from code with zero manual steps.

That’s a calm, professional engineering mindset.

🎯 Day 24 Success Checklist
```
✔ Infra destroyed

✔ Infra recreated

✔ Kubeconfig exported

✔ App redeployed

✔ Ingress verified

✔ No manual steps
```



## 🚀 Day 25 — Terraform Workspaces (Multi-Environment Infrastructure)

## 📌 Overview
Until now, we managed infrastructure in a single environment.  
In real-world companies, infrastructure is split into **multiple environments**:

- **dev** — for development and testing
- **staging** — for pre-production validation
- **prod** — for production workloads

Each environment requires:
- Separate Terraform state
- Different resource sizes/configurations
- Strict isolation

Terraform **workspaces** help us achieve this while reusing the same codebase.

---

## 🎯 Goal of Day 25
By the end of this day, you will:
- ✔ Create Terraform workspaces
- ✔ Manage dev / staging / prod environments
- ✔ Understand environment isolation
- ✔ Deploy infrastructure to the **dev** workspace

---

## 🛠 Step 1 — Check Current Workspace
Run:
```bash
terraform workspace lis
```
Output:

```Code
* default
```
🛠 Step 2 — Create Workspaces
```bash
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod
```
Check again:

```bash
terraform workspace list
```
Example output:

```Code
default
dev
staging
* prod
```
🛠 Step 3 — Switch Workspace
Select the workspace you want to work in:

```bash
terraform workspace select dev
```
Now your infrastructure belongs to the dev environment.
Each workspace maintains its own state file.

🛠 Step 4 — Apply Infrastructure to DEV
Deploy resources in the dev environment:

```bash
terraform apply
```
Later, you can switch to staging:

```bash
terraform workspace select staging
terraform apply
```
This creates isolated infrastructure for staging.

🧠 What This Means
Instead of one cluster, you can have:

dev cluster

staging cluster

prod cluster

All managed from the same Terraform codebase.

This is professional environment management.

✅ Day 25 Success Checklist
```
✔ Workspaces created

✔ Switched to dev workspace

✔ Terraform apply works

✔ Infra created in dev environment
```
📈 Interview Tip
If asked:

“How do you manage multiple environments with Terraform?”

Answer:

We use Terraform workspaces to isolate environments such as dev, staging, and production while sharing the same infrastructure codebase.

That’s a strong DevOps answer.
