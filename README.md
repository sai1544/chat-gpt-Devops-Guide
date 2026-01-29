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
