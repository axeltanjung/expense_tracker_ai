## Expense Tracker AI

Personal Finance Intelligence Engine (not a CRUD app)

Expense Tracker AI is a predictive, behavioral-aware personal finance engine built on time-series database, analytics views, and ML forecasting — designed to change financial trajectory, not just record spending.

Architecture Philosophy
Database = Feature Store
Backend  = Semantic API
ML       = Intelligence Layer
UI       = Visualization Only

Tech Stack
Layer	Tech
DB	PostgreSQL + TimescaleDB
Backend	FastAPI
ML	Prophet, IsolationForest
Feature Store	SQL Semantic Views
Scheduler	Airflow
UI	Next.js
Infra	Docker
Repo Structure
expense_tracker_ai/
│
├── docker-compose.yml
├── migrations/
│   ├── 001_init_schema.sql
│   ├── 002_views.sql
│   └── 003_feature_views.sql
│
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── db.py
│   ├── insights.py
│   └── schemas.py
│
└── ui/   (optional)

Quick Start
1. Clone
git clone <repo_url>
cd expense_tracker_ai

2. Start Infra
docker-compose up --build


This will automatically:

Boot TimescaleDB

Create all tables & analytic views

Start FastAPI intelligence engine

API Documentation

Open:

http://localhost:8000/docs


Available intelligence endpoints:

Endpoint	Purpose
/insights/spend?user_id=	Multi-horizon spend
/insights/runway?user_id=	Cash runway
/insights/subscriptions	Subscription leakage
/insights/risk (soon)	Payday survival
Database as Feature Store

All analytics live as SQL semantic views:

View	Purpose
spend_7d	Short-term burn
spend_30d	Monthly burn
spend_90d	Structural lifestyle
cash_velocity	Burn rate
subscriptions_detect	Money leakage
Roadmap
Phase	Capability
Phase 1	Semantic finance engine
Phase 2	Forecasting & anomaly detection
Phase 3	Behavioral nudging
Phase 4	FIRE simulator
Core Principle

If your system only records money — it dies.
If it predicts & changes behavior — it compounds.

Author

Built for engineers who want to build AI-first financial systems, not CRUD trackers.