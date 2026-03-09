# House Prices Data Pipeline - Apache Airflow with Docker

## 📋 Project Overview

This project demonstrates how to set up **Apache Airflow** using **Docker Compose** to orchestrate a data pipeline that reads JSON data and converts it to CSV format.

**Key Features:**
- ✅ Fully containerized Airflow setup with PostgreSQL, Redis, and Workers
- ✅ Custom DAG that executes a Python data conversion script
- ✅ Distributed task execution using Celery workers
- ✅ Easy local development and testing environment

**Dataset:** Housing prices data from [Agents for Data](https://www.agentsfordata.com/json/sample)

---

## 🔧 Prerequisites

- **Docker Desktop** installed and running (Windows/Mac/Linux)
- **Python 3.8+** installed (for local development and Fernet key generation)
- **Git** (optional, for version control)
- Basic understanding of Docker, Python, and Airflow concepts

---

## 📁 Project Structure

```
house_prices/
├── data/
│   ├── house_prices.json       # Source data
│   └── house_prices.csv        # Generated output (created after DAG runs)
├── dags/
│   └── house_prices_dag.py     # Airflow DAG definition
├── logs/                        # Airflow task execution logs
├── plugins/                     # Custom Airflow plugins
├── venv/                        # Virtual environment (created locally)
├── convert_json_to_csv.py      # Python script to convert data
├── generate_fernet_key.py      # Script to generate Fernet key dynamically
├── docker-compose.yml          # Docker Compose configuration
├── requirements.txt            # Python dependencies (pandas, cryptography)
├── .env                        # Environment variables (generated)
├── .gitignore                  # Git ignore file
└── Docs/
    └── readme.md               # This file
```

![VS Code Project View](vs%20code%20screenshot.png)
*Figure 1: VS Code editor showing the project structure and files.*

---

## � Fernet Key Setup

**Important Security Note:** This project uses dynamic Fernet key generation for Airflow encryption. The Fernet key is used to encrypt sensitive data like connection passwords and API tokens.

### Why Dynamic Key Generation?

- **Security Best Practice**: Each deployment gets its own unique encryption key
- **No Hardcoded Keys**: Keys are never committed to version control
- **Fresh Keys**: New keys are generated each time the setup script runs

### Setup Requirements

Every user who clones this repository must generate their own Fernet key:

1. **Run the key generation script** (required before starting services)
2. **The `.env` file is gitignored** to prevent key exposure
3. **Each environment gets a unique key** for proper security isolation

---
## 🐍 Local Development Setup (Optional)

For local development and testing the Python scripts before running Docker:

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate Fernet Key

```bash
python generate_fernet_key.py
```

**Note:** The `convert_json_to_csv.py` script automatically detects whether it's running locally or in a Docker container and uses the appropriate paths:
- **Local**: Uses `data/house_prices.json`
- **Container**: Uses `/opt/airflow/data/house_prices.json`

### 7. Test Scripts Locally (Optional)

You can test the data conversion script locally:

```bash
python convert_json_to_csv.py
```

### 7. Deactivate Virtual Environment (When Done)

```bash
deactivate
```

---
## 🚀 Quick Start (Docker Deployment)

**Note:** The Docker deployment runs everything in containers, so the virtual environment setup above is not required for production deployment. The local setup is only needed if you want to test or develop the Python scripts locally.

### 1. Generate Fernet Key

If you haven't already done so in the local setup:

```bash
python generate_fernet_key.py
```

This will create a `.env` file with a randomly generated Fernet key.

### 2. Start All Services

```bash
docker-compose up -d
```

Docker will:
- Download required images (Airflow, PostgreSQL, Redis)
- Create and start all containers
- Initialize the Airflow database
- Create the admin user

![Docker Desktop Running Containers](Docker%20desktop%20Screenshot.png)
*Figure 2: Docker Desktop showing all Airflow services running successfully.*

### 3. Access Airflow UI

Open your browser and navigate to:
```
http://localhost:8080
```

**Login Credentials:**
- Username: `admin`
- Password: `admin`

### 3. Trigger the DAG

1. In the Airflow UI, find the `house_prices_conversion` DAG
2. Click the **Play** button to trigger a run
3. Monitor the task execution in real-time

![Airflow UI DAG Completion](Airflow%20completion%20Screenshot.png)
*Figure 3: Airflow web interface showing successful DAG run with completed tasks.*

### 4. View Results

After the DAG completes successfully:
- Check the `data/` folder for `house_prices.csv`
- View task logs in the Airflow UI under the DAG run details

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  Airflow Web UI                          │
│              (http://localhost:8080)                     │
└────────────────────┬─────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    ┌────▼──┐   ┌───▼───┐   ┌──▼─────┐
    │Webser │   │Schedul│   │Triggere│
    │ver    │   │er     │   │r       │
    └───────┘   └───┬───┘   └────────┘
                    │
            ┌───────▼────────┐
            │  Redis Queue   │
            │  (Message Bus) │
            └───────┬────────┘
                    │
           ┌────────▼────────┐
           │ Celery Worker(s)│
           │ Execute Tasks   │
           └────────┬────────┘
                    │
    ┌───────────────┴────────────────┐
    │                                │
┌──▼──────────┐           ┌────────▼──┐
│ PostgreSQL  │           │   Data    │
│ (Metadata)  │           │ (Volumes) │
└─────────────┘           └───────────┘
```

**Components:**

| Component | Purpose | Port |
|-----------|---------|------|
| **PostgreSQL** | Airflow metadata database (DAG runs, task status, logs) | 5432 |
| **Redis** | Celery message broker (task queue) | 6379 |
| **Webserver** | Airflow UI and REST API | 8080 |
| **Scheduler** | Parses DAGs and schedules tasks | - |
| **Worker** | Executes scheduled tasks (Celery) | - |
| **Triggerer** | Handles async task triggers | - |

---

## 📝 Configuration Details

### Docker Compose Environment Variables

```yaml
AIRFLOW__CORE__EXECUTOR: CeleryExecutor        # Distributed task execution
AIRFLOW__CORE__FERNET_KEY: <encrypted_key>    # Encryption for sensitive data
AIRFLOW__CORE__LOAD_EXAMPLES: 'false'         # Disable example DAGs
AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'  # Pause DAGs on creation
```

### Database Credentials

```
PostgreSQL:
  User: airflow
  Password: airflow
  Database: airflow

Redis: Default port 6379
```

---

## 🔄 DAG Details

**DAG Name:** `house_prices_conversion`

**Task:** `convert_json_to_csv`
- Executes: `/opt/airflow/convert_json_to_csv.py`
- Operator: BashOperator
- Input: `data/house_prices.json`
- Output: `data/house_prices.csv`

**How the Task Works:**
1. Script automatically detects environment (local vs container)
2. Uses appropriate data paths:
   - **Local**: `data/house_prices.json` → `data/house_prices.csv`
   - **Container**: `/opt/airflow/data/house_prices.json` → `/opt/airflow/data/house_prices.csv`
3. Uses pandas to convert JSON to DataFrame
4. Writes the converted CSV file

---

## 📚 Useful Commands

### Check Docker Compose Configuration
```bash
docker-compose config
```
Validates YAML syntax and resolves variables.

### View Service Logs
```bash
# All services
docker-compose logs

# Specific service (last 50 lines)
docker-compose logs --tail 50 airflow-webserver
docker-compose logs --tail 50 airflow-scheduler

# Follow logs in real-time
docker-compose logs -f airflow-webserver
```

### Check Service Status
```bash
docker-compose ps
```

### Stop All Services
```bash
docker-compose down
```

### Restart All Services
```bash
docker-compose down
docker-compose up -d
```

### Execute Commands Inside Container
```bash
# List all DAGs
docker-compose exec airflow-webserver airflow dags list

# List tasks in a DAG
docker-compose exec airflow-webserver airflow tasks list house_prices_conversion

# Test a task
docker-compose exec airflow-webserver airflow tasks test house_prices_conversion convert_json_to_csv
```

---

## 🐛 Troubleshooting

### "Invalid login. Please try again."
- **Solution:** Ensure all containers are healthy: `docker-compose ps`
- Wait 60+ seconds for full initialization
- Check logs: `docker-compose logs airflow-webserver --tail 50`

### "Failed to build 'pandas' when getting requirements to build wheel"
- **Reason:** Pandas wheels may not be available for your Python version, causing pip to attempt building from source
- **Solutions:**
  - Upgrade pip: `python -m pip install --upgrade pip`
  - Use compatible pandas version: `pip install "pandas>=2.2.0"`
  - Install pre-compiled wheels: `pip install --only-binary=all pandas`
  - For Python 3.13+, ensure you're using pandas 2.2.x or later

### "No matching distribution found for pandas"
- **Solution:** Check your Python version compatibility. Use `python --version` and ensure requirements match your Python version.

### Containers Keep Restarting
- Check logs: `docker-compose logs`
- Ensure PostgreSQL and Redis are `Healthy`
- Verify sufficient disk space available
- Try: `docker-compose down && docker-compose up -d`

### Port 8080 Already in Use
- Find and stop the process using port 8080, or
- Change the port in `docker-compose.yml`: `"8081:8080"`

### DAG Not Appearing in UI
- Ensure DAG file is in `dags/` folder
- Check DAG syntax: `docker-compose exec airflow-webserver airflow dags validate`
- Restart scheduler: `docker-compose restart airflow-scheduler`

---

## 📦 Dependencies

Managed via `requirements.txt`:
```
pandas>=2.2.0
cryptography>=42.0.0
```

Automatically installed during Docker container initialization.

---

## 🔐 Security Notes

This is a **sample/development project**. For production:
- ✅ Use actual secrets management (Vault, AWS Secrets Manager)
- ✅ Change default credentials
- ✅ Enable authentication and RBAC
- ✅ Use SSL/TLS for connections
- ✅ Store sensitive data in `.env` files (excluded from Git via `.gitignore`)

---

## 📖 Learn More

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [Celery Executor](https://airflow.apache.org/docs/apache-airflow/stable/executors/celery.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 📄 License

This is a sample project for educational and development purposes.
