import os
from fastapi import FastAPI, HTTPException
import requests
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Middleware configuration
origins = [
    "*",  # Allows all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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

@app.get("/find/imdb/{imdb_id}")
async def find_tmdb_from_imdb(imdb_id: str):
    """
    Finds TMDB ID using IMDB ID as input.
    """
    headers = _get_tmdb_headers()
    url = f"{TMDB_BASE_URL}/find/{imdb_id}"
    params = {"external_source": "imdb_id"}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract TMDB ID from the response
        tmdb_results = {}
        if data.get("movie_results"):
            tmdb_results["movie"] = {
                "tmdb_id": data["movie_results"][0]["id"],
                "title": data["movie_results"][0]["title"],
                "media_type": "movie"
            }
        elif data.get("tv_results"):
            tmdb_results["tv"] = {
                "tmdb_id": data["tv_results"][0]["id"],
                "title": data["tv_results"][0]["name"],
                "media_type": "tv"
            }
        elif data.get("person_results"):
            tmdb_results["person"] = {
                "tmdb_id": data["person_results"][0]["id"],
                "name": data["person_results"][0]["name"],
                "media_type": "person"
            }
        else:
            raise HTTPException(status_code=404, detail="No TMDB results found for the provided IMDB ID")
        
        return {
            "imdb_id": imdb_id,
            "results": tmdb_results,
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error fetching data from TMDB: {e}")


if __name__ == "__main__":
    # Run the app with uvicorn.
    # host="0.0.0.0" makes it accessible on your network.
    # reload=True automatically restarts the server when code changes.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

