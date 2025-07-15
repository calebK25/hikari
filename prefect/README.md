# Prefect Configuration

This directory contains the Prefect workflow orchestration configuration for the Hikari project.

## Files

- `prefect.yaml` - Main deployment configuration file
- `deploy_nightly.py` - Python script for deploying flows with schedules
- `README.md` - This documentation file

## Setup

### 1. Start Prefect Server
```bash
prefect server start
```

### 2. Configure Local API
```bash
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```

### 3. Create Work Pool
```bash
prefect work-pool create hikari --type process
```

### 4. Deploy Flows
```bash
cd prefect
prefect deploy --all
```

### 5. Start Worker
```bash
prefect worker start --pool hikari
```

## Workflows

### Nightly Document Ingestion
- **Schedule**: 2 AM daily (`0 2 * * *`)
- **Purpose**: Process PDFs in `sample_data/` directory
- **Output**: Chunked text files in `processed_data/` directory

## Monitoring

- **UI**: http://127.0.0.1:4200
- **Deployment Name**: `hikari`
- **Work Pool**: `hikari`

## Manual Execution

To manually trigger a flow run:
```bash
prefect deployment run 'hikari/nightly-ingest'
``` 