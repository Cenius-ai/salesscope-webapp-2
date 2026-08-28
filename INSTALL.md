# Installation

## 1. Prerequisites

- Python **3.11 or later**

## 2. Get the Code

Clone the repository or download the project files to your local machine.

## 3. Create a Virtual Environment

```bash
python -m venv .venv && . .venv/bin/activate
```

On Windows use `.venv\Scripts\activate` instead.

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Generate Sample Data

The dashboard requires a `sales_data.csv` file. Generate it with:

```bash
python generate_data.py
```

This creates `data/sales_data.csv` containing 1000 realistic sales records.

## 6. Run the Development Server

Start the Streamlit app:

```bash
streamlit run app.py
```

By default the server listens on `localhost:8501`. To serve head‑less on all interfaces:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

## 7. Production Deployment

For production, run the Streamlit server behind a reverse proxy (e.g., nginx) with the same command:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

## 8. Troubleshooting

- **`FileNotFoundError: sales_data.csv`** – Run `python generate_data.py` first.
- **Virtual environment activation fails** – On Windows use `.venv\Scripts\activate`; on Unix ensure you are in the correct shell.
- **Port 8501 already in use** – Use `--server.port <different_port>`.
- **Missing dependencies** – Ensure you ran `pip install -r requirements.txt` inside the activated environment.