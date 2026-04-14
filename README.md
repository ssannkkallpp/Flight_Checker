# Flight Search Frontend for CS-GY-6083 Spring 2026

## Prerequisites

- Python 3.8+
- PostgreSQL

## Setup

### 1. Create and populate the database with flights.sql

### 2. Configure environment variables

Create a `.env` file:

```
DB_HOST=<db_host>
DB_PORT=<db_port>
DB_NAME=<database_name>
DB_USER=<your_postgres_user>
```

### 3. Install dependencies

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the app

```
uvicorn main:app --reload
```
