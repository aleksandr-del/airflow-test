# Airflow Testing Project

A comprehensive Apache Airflow testing project demonstrating various DAG patterns, custom operators, and workflow orchestration concepts.

## Features

- **Custom Operators**: DuckDB integration with templated SQL queries
- **HTTP Operations**: API integration with external services
- **XCom Communication**: Inter-task data passing and communication
- **Conditional Branching**: Dynamic workflow execution based on conditions
- **Template Engine**: Jinja2 templating for dynamic SQL queries
- **Error Handling**: Retry mechanisms and failure management

## Project Structure

```
airflow-test/
├── dags/
│   ├── duckdb_dag.py          # DuckDB custom operator example
│   ├── http_dag.py            # HTTP API integration
│   ├── dag_xcom.py            # XCom push/pull operations
│   ├── dag_branch.py          # Conditional branching
│   ├── dynamic_dag.py         # Dynamic task generation
│   ├── http_sensor_dag.py     # HTTP sensor polling
│   ├── python_sensor_dag.py   # Python sensor file checking
│   ├── telegram_alerts_dag.py # Telegram failure notifications
│   ├── function.py            # Utility functions
│   └── query.sql              # Templated SQL query
├── plugins/
│   └── airflow_duckdb_plugins/
│       └── operators/
│           └── customoperator.py  # Custom DuckDB operator
```

## Setup Instructions

### 1. Create Project Directory

```bash
mkdir -p path/to/airflow-test
cd path/to/airflow-test
```

### 2. Install Apache Airflow

```bash
pip install "apache-airflow==2.10.0" --constraint "https://raw.githubusercontent.com/apache/airflow/refs/tags/constraints-2.10.0/constraints-source-providers-3.11.txt"
```

### 3. Setup Virtual Environment

```bash
python3.11 -m venv --prompt airflow .venv
echo "export AIRFLOW_HOME='/path/to/airflow-test'" >> .venv/bin/activate
echo "export AIRFLOW__CORE__LOAD_EXAMPLES=False" >> .venv/bin/activate
source .venv/bin/activate
```

### 4. Initialize Airflow Database

```bash
airflow db init
```

or

```bash
airflow dbt migrate
```

### 5. Create Admin User

```bash
airflow users create \
    --username admin \
    --firstname FIRST_NAME \
    --lastname LAST_NAME \
    --role Admin \
    --email admin@example.org \
    --password admin
```

### 6. Start Airflow Services

```bash
# Terminal 1: Start webserver
airflow webserver --port 8081

# Terminal 2: Start scheduler
airflow scheduler
```

## DAG Examples

### DuckDB Integration

- **File**: `duckdb_dag.py`
- **Features**: Custom operator, SQL templating, parameter passing
- **Schedule**: `@once`

### HTTP API Calls

- **File**: `http_dag.py`
- **Features**: External API integration, response filtering
- **Schedule**: `@once`

### XCom Communication

- **File**: `dag_xcom.py`
- **Features**: Task-to-task data passing, context usage
- **Schedule**: `@once`

### Conditional Branching

- **File**: `dag_branch.py`
- **Features**: Dynamic workflow paths based on date logic
- **Schedule**: Daily (`0 0 * * *`)

### Dynamic Task Generation

- **File**: `dynamic_dag.py`
- **Features**: Programmatically create tasks based on date ranges
- **Schedule**: `@once`

### HTTP Sensor

- **File**: `http_sensor_dag.py`
- **Features**: Poll API endpoint until condition met, response validation
- **Schedule**: `@once`

### Python Sensor

- **File**: `python_sensor_dag.py`
- **Features**: File existence checking, custom Python callable sensor
- **Schedule**: `@once`

### Telegram Alerts

- **File**: `telegram_alerts_dag.py`
- **Features**: Failure callback notifications, Telegram integration, intentional failures on even days
- **Schedule**: Daily (`15 3 * * *`)
- **Catchup**: Enabled

## Key Learning Concepts

1. **DAG Definition**: Proper DAG structure with default arguments
2. **Task Dependencies**: Linear and parallel task execution
3. **Templating**: Jinja2 templates for dynamic content
4. **Custom Operators**: Building reusable task components
5. **Context Variables**: Accessing execution metadata
6. **Connection Management**: External service integration
7. **Error Handling**: Retry logic and failure scenarios
8. **Sensors**: Polling mechanisms for external conditions (HTTP, file system)
9. **Dynamic Tasks**: Programmatic task generation based on runtime data

## Access

- **Web UI**: http://localhost:8081
- **Username**: admin
- **Password**: admin

## Requirements

- Python 3.11
- Apache Airflow 2.10.0
- DuckDB (for database operations)
- HTTP provider (for API calls)

## Tags

Each DAG includes relevant tags for easy filtering:

- `sql`, `duckdb` - Database operations
- `get`, `http` - API operations
- `push`, `pull`, `xcom` - Data communication
- `branches` - Conditional workflows
- `dynamic`, `tasks` - Dynamic task generation
- `sensor`, `api`, `file`, `python` - Sensor operations
