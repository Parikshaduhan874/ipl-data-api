# IPL Data API

A FastAPI application that exposes IPL cricket data 
(2008–2020) through REST endpoints with data analysis, 
SQL queries, and chart generation.

## Live Demo
https://your-render-url.onrender.com/docs

## Endpoints

| Endpoint | Method | Description |
|---|---|---|
| /summary | GET | Dataset overview and key stats |
| /stats?column=season | GET | Statistics for any column |
| /chart/wins_per_team | GET | Returns chart as image |
| /filter | POST | Filter matches by season/team/city |
| /top-batsmen | GET | Top run scorers all time |
| /top-bowlers | GET | Top wicket takers all time |

## Tech Stack
- FastAPI — REST API framework
- Pandas — data cleaning and analysis
- NumPy — numerical operations
- SQLite + SQL — database queries
- Matplotlib + Seaborn — data visualisation
- Render — cloud deployment

## Run locally
pip install -r requirements.txt
uvicorn main:app --reload