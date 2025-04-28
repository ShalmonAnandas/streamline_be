import os
from fastapi import FastAPI, HTTPException
import requests
import uvicorn

app = FastAPI()

TMDB_BASE_URL = "https://api.themoviedb.org/3"

def _get_tmdb_headers():
    """
    Returns TMDB API headers or raises an HTTPException if the key is missing.
    """
    tmdb_api_key = os.getenv("TMDB_API_KEY")
    if not tmdb_api_key or tmdb_api_key == "YOUR_DEFAULT_TOKEN_IF_NOT_SET": # Check if key is missing or default
        raise HTTPException(status_code=500, detail="TMDB_API_KEY environment variable is not set.")

    return {
        "accept": "application/json",
        "Authorization": tmdb_api_key,
        "User-Agent": "StreamlineBE/1.0 Python/FastAPI" # Updated User-Agent
    }

@app.get("/")
async def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Streamline Backend API is running"}

@app.get("/trending/{media_type}")
async def get_trending(media_type: str, page: int = 1):
    """
    Fetches trending media from TMDB.
    """
    headers = _get_tmdb_headers()
    url = f"{TMDB_BASE_URL}/trending/{media_type}/day?language=en-US&page={page}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error fetching data from TMDB: {e}")

@app.get("/search/multi")
async def search_multi(query: str):
    """
    Searches TMDB across multiple media types.
    """
    headers = _get_tmdb_headers()
    url = f"{TMDB_BASE_URL}/search/multi"
    params = {"query": query, "language": "en-US"} # Added language param for consistency
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error fetching data from TMDB: {e}")

@app.get("/details/{media_type}/{media_id}")
async def get_media_details(media_type: str, media_id: int):
    """
    Fetches details for a specific media item from TMDB.
    """
    headers = _get_tmdb_headers()
    url = f"{TMDB_BASE_URL}/{media_type}/{media_id}?append_to_response=external_ids&language=en-US"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error fetching data from TMDB: {e}")

@app.get("/recommendations/{media_type}/{media_id}")
async def get_recommendations(media_type: str, media_id: int, language: str = "en-US", page: int = 1):
    """
    Fetches recommendations for a specific media item from TMDB.
    """
    headers = _get_tmdb_headers()
    url = f"{TMDB_BASE_URL}/{media_type}/{media_id}/recommendations"
    params = {"language": language, "page": page}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error fetching data from TMDB: {e}")

@app.get("/tv/{series_id}/season/{season_number}")
async def get_season_details(series_id: int, season_number: int):
    """
    Fetches details for a specific TV show season from TMDB.
    """
    headers = _get_tmdb_headers()
    url = f"{TMDB_BASE_URL}/tv/{series_id}/season/{season_number}?language=en-US"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error fetching data from TMDB: {e}")


if __name__ == "__main__":
    # Run the app with uvicorn.
    # host="0.0.0.0" makes it accessible on your network.
    # reload=True automatically restarts the server when code changes.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

