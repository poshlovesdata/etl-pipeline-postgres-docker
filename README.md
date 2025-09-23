ETL Pipeline with Docker and PostgreSQL

## Pipeline Architecture
![Pipeline Architecture](/postgres-docker-etl-architecture.png)

## Overview:
This project demonstrates a simple ETL (Extract -> Transform -> Load) pipeline using Docker.

ETL Container - runs a Python script (etl.py) that:

Extracts crypto price data from CoinGecko API

Transforms the data using pandas

Loads the cleaned data into PostgreSQL using SQLAlchemy

Postgres Container - runs PostgreSQL as the database target.

The containers communicate over a Docker network.

---

## Project Structure
```
etl-pipeline-postgres-docker/
│── etl.py               # Python ETL script
│── requirements.txt     # Python dependencies
│── .env                 # Environment variables
│── run_etl.sh           # Bash script to run the ETL container
│── README.md            # Project documentation
```

## Prerequisites
- Docker
- Python 3.10+ (for local testing)
- Bash shell (Linux/macOS, or Git Bash on Windows)

---

## Running the Project
1. Make `run_etl.sh` script executable
```bash
chmod +x run_etl.sh 
```
2. Execute bash script `run_etl.sh`
```bash
./run_etl.sh
```
3. Set up environment variables
On first run, you’ll be prompted to populate `.env`:
```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
```

4. Verify database 
After the ETL completes, it connects to the database
Test database with SQL queries
```sql
SELECT * FROM coin_price;
```

---
## Concepts covered:
1. API data extraction
2. Static typing in Python
3. Git/Github for version control
4. Environment variable for secure credentials
5. Python Functions
6. Data transformation with pandas
7. Bash Scripting for automation
8. Docker basics: Dockerfile, containers, networks