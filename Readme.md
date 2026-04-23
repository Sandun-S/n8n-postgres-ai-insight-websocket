### Quick Start Summary for the Engineer:

1.  **Database Connection:** Your DB is running on `localhost:5432`. Use the credentials `postgres` / `qube_password`.
2.  **Data Migration:** - Ensure you have `psycopg2` installed (`pip install psycopg2-binary`).
      - Place your 3 JSON files in the same folder as `migrate.py`.
      - Run: `python migrate.py` to populate the `telemetry` table.
3.  **n8n Access:** Open `http://localhost:5678`.
4.  **RAG Knowledge Base:** - Place your `qube_manual.txt` inside the `./knowledge_base` folder on your computer.
      - Inside n8n, use the path `/home/node/.n8n-files/qube_manual.txt`.

**Troubleshooting Note:** Your logs show that n8n attempted to start a Python task runner but failed because Python is not inside the n8n container. This is fine; we are running our migration script **outside** the container (on your host machine) which is the recommended engineering practice for this test-bench.

````python
import os

readme_content = """# Qube Industrial Test-Bench: AI Telemetry Optimizer

This repository contains the infrastructure and logic for the **Qube Industrial AI Engine**. It simulates an edge-to-cloud data pipeline where raw industrial telemetry is processed into engineering insights using RAG (Retrieval-Augmented Generation).

## 🏗 System Architecture

The test-bench consists of three primary layers:
1. **Data Layer**: TimescaleDB (PostgreSQL) container for time-series telemetry.
2. **Logic Layer**: n8n workflow engine with LangChain AI Agent integration.
3. **Knowledge Layer**: RAG system using `.txt` manuals stored in a secured Docker volume.

---

## 🚀 Getting Started

### 1. Prerequisites
- **Docker & Docker Compose** installed.
- **Python 3.x** installed on your host machine.
- **API Keys**: Google Gemini (for Embeddings) and OpenRouter (for Gemma 4).

### 2. Infrastructure Setup
Run the following command to start the database and the workflow engine:

```bash
docker-compose up -d
````

**Services:**

  - **n8n Editor**: [http://localhost:5678](https://www.google.com/search?q=http://localhost:5678)
  - **PostgreSQL/TimescaleDB**: `localhost:5432` (User: `postgres`, Pass: `qube_password`)

-----

## 📥 Data Ingestion

The system requires three telemetry JSON files (Energy, Power-Factor, and Maximum-Demand).

1.  **Prepare Environment**:

    ```bash
    pip install psycopg2-binary
    ```

2.  **Execute Migration**:
    Place your JSON files and `migrate.py` in the root directory and run:

    ```bash
    python migrate.py
    ```

    *This script pivots the raw JSON data and inserts it into the `telemetry` table in the `qube-db`.*

-----

## 🧠 AI & RAG Configuration

### Knowledge Base (RAG)

To provide the AI with technical manuals:

1.  Place your `.txt` files in the `./knowledge_base` directory on your host.
2.  In n8n, use the **Read/Write Files from Disk** node.
3.  **Path**: `/home/node/.n8n-files/your_manual.txt`.

### Multi-Tenant Strategy

To support 100+ users on a single instance:

  - **Telemetry**: Query the DB using a `device_id` or `client_id` filter.
  - **RAG**: Use **Metadata Filtering** in the PGVector node to ensure users only retrieve their own technical manuals.

-----

## 🛠 Troubleshooting

### "Access to the file is not allowed" (n8n)

If n8n cannot read your `.txt` file, ensure your `docker-compose.yml` includes:

```yaml
environment:
  - N8N_BLOCK_FS_WRITE_ACCESS=false
volumes:
  - ./knowledge_base:/home/node/.n8n-files
```

### Database Initialization

If you see "Skipping initialization" in the logs, it means the database volume already exists. To perform a fresh wipe:

```bash
docker-compose down -v
docker-compose up -d
```

-----

## 📝 Engineering Log (2026-04-20)

  - Successfully implemented SQL pivoting for `peak_kva`, `avg_kwh`, and `min_pf`.
  - Integrated Gemma 4 via OpenRouter as the primary reasoning agent.
  - Configured HTML Webhook Response for live dashboarding.
  - Validated RAG retrieval using Gemini-001 Embeddings.
    """