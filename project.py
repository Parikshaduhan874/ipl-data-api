from fastapi import FastAPI,HTTPException,Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
import numpy as np
import pandas as pd
import sqlite3
import os
app=FastAPI(title="IPL Data API",description="AI project")
df_matches=pd.read_csv('matches.csv')
df_deliveries=pd.read_csv('deliveries.csv')
conn=sqlite3.connect("ipl.db",check_same_thread=False)
#----------endpoint-1:dataset summary---------
@app.get("/summary")
def get_summary():
    return{
        "total_matches":len(df_matches),
        "seasons":sorted(df_matches['season'].unique().tolist()),
        "total_team":df_matches['winner'].nunique(),
        "most_successful_team":df_matches['winner'].value_counts().index[0],
        "total_deliveries":len(df_deliveries)

    }
#----endpoint-2:stats for any column------------
@app.get("/stats")
def get_column_stats(column:str=Query(...,description="Column Name from matches Dataset")):
    if column not in df_matches.columns:
        raise HTTPException(
            status_code=404,
            detail=f"Column:'{column} not found in dataset.Available={df_matches.columns.tolist()}"

        )
    col=df_matches[column]
    if col.dtype in ['int64', 'float64']:
        return {
            "column": column,
            "mean": round(float(col.mean()), 2),
            "median": round(float(col.median()), 2),
            "min": float(col.min()),
            "max": float(col.max()),
            "top_5_values": {
                str(k): int(v) 
                for k, v in col.value_counts().head(5).items()
            }
        }
    else:
        return{
            "column":column,
            "unique_values":col.nunique(),
            "top_5_values":col.value_counts().head(5).to_dict(),
            "null_count":int(col.isnull().sum())
        }
#----endpoint-3:return chart as image--------------
@app.get("/chart/{chart_name}")
def get_charts(chart_name:str):
    valid_charts=["wins_per_team","matches_per_season","toss_decision","winning_margin","correlation_heatmap","top_batsman_season"]
    if chart_name not in valid_charts:
        raise HTTPException(
            status_code=404,
            detail=f"Chart Not found.Available charts:{valid_charts}"
        )
    path=f"chart/{chart_name}.png"
    return FileResponse(path,media_type="image/png")
#----endpoint-4:Filter Matches------
class FilterRequest(BaseModel):
    season:str|None=None
    winner:str|None=None
    city:str|None=None
    toss_decision:str|None=None
@app.post("/filter")
def filter_matches(filters:FilterRequest):
    result=df_matches.copy()
    if filters.season:
        result=result[result["season"]==filters.season]
    if filters.winner:
        result=result[result["winner"]==filters.winner]
    if filters.city:
        result=result[result["city"]==filters.city]
    if filters.toss_decision:
        result=result[result["toss_decision"]==filters.toss_decision]
    return{
        "total_result":len(result),
        "matches":result.head(20).fillna("N/A").to_dict(orient="records")
    }
#----endpoint-5:Top Players Via SQL-----------
@app.get("/top_batsman")
def get_top_batsmen(limit:int=10):
    result=pd.read_sql_query(f""" SELECT batter,SUM(batsman_runs) AS total_runs,COUNT(DISTINCT match_id) AS matches_played FROM deliveries GROUP BY batter ORDER BY total_runs DESC LIMIT {limit}""",conn)
    return result.to_dict(orient="records")
@app.get("/top_bowler")
def get_top_bowler(limit:int=10):
    result=pd.read_sql_query(f"""SELECT bowler,COUNT(*) AS total_wickets FROM deliveries WHERE dismissal_kind NOT IN ('run out','retired hunt','obstructing the field') AND dismissal_kind IS NOT NULL GROUP BY bowler ORDER BY total_wickets DESC LIMIT {limit}""",conn)
    return result.to_dict(orient="records")




