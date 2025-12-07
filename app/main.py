from fastapi import FastAPI, HTTPException, Query
import mysql.connector
import requests
from bs4 import BeautifulSoup

app = FastAPI()

def run_select_query(sql: str):
    # Only allow SELECT queries
    if not sql.strip().lower().startswith("select"):
        raise HTTPException(status_code=400, detail="Only SELECT queries are allowed.")

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="call_transcripts",
            port=3306
        )
        cursor = conn.cursor()

        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/query")
def execute_query(q: str = Query(..., description="SELECT query to run")):
    return run_select_query(q)

@app.get("/search")
def internet_search(q: str = Query(...)):
    try:
        url = "https://lite.duckduckgo.com/lite/"
        params = {"q": q}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(url, params=params, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        # Lite search results have <a class="result-link">
        for link in soup.select("a.result-link"):
            title = link.get_text(strip=True)
            url = link.get("href")
            snippet_tag = link.find_next("td", class_="result-snippet")

            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""

            results.append({
                "title": title,
                "url": url,
                "snippet": snippet
            })

        return {"query": q, "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))