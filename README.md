# Streamline Backend

A FastAPI backend service to interact with The Movie Database (TMDB) API.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyour-username%2Fyour-repo-name&env=TMDB_API_KEY&envDescription=TMDB%20API%20Key%20needed%20for%20fetching%20data.&envLink=https%3A%2F%2Fdeveloper.themoviedb.org%2Fdocs%2Fgetting-started&project-name=streamline-backend&repository-name=streamline-be&build-command=pip%20install%20-r%20requirements.txt&root-directory=.)

**Note:** Replace `https://github.com/your-username/your-repo-name` in the button URL above with the actual URL of your GitHub repository for the deploy button to work correctly.

## Features

Provides endpoints to:
*   Fetch trending movies or TV shows.
*   Search for movies, TV shows, and people.
*   Get detailed information about a specific movie or TV show.
*   Get recommendations based on a movie or TV show.
*   Fetch details for a specific TV show season.

## Setup

### Prerequisites

*   Python 3.8+
*   pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd streamline_be
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory or set the environment variable directly:
    ```
    TMDB_API_KEY="your_tmdb_api_v3_auth_token"
    ```
    You can get an API key from [TMDB](https://www.themoviedb.org/settings/api).

5.  **Run the application:**
    ```bash
    uvicorn main:app --reload --host 127.0.0.1 --port 8000
    ```
    The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

*   `GET /trending/{media_type}?page={page_number}`: Get daily trending media (`movie` or `tv`).
    *   `media_type`: `movie` or `tv`
    *   `page` (optional): Defaults to 1.
*   `GET /search/multi?query={search_query}`: Search across movies, TV shows, and people.
    *   `query`: The search term.
*   `GET /details/{media_type}/{media_id}`: Get details for a specific item.
    *   `media_type`: `movie` or `tv`
    *   `media_id`: The TMDB ID of the item.
*   `GET /recommendations/{media_type}/{media_id}?language={language}&page={page_number}`: Get recommendations for a specific item.
    *   `media_type`: `movie` or `tv`
    *   `media_id`: The TMDB ID of the item.
    *   `language` (optional): Defaults to `en-US`.
    *   `page` (optional): Defaults to 1.
*   `GET /tv/{series_id}/season/{season_number}`: Get details for a specific TV show season.
    *   `series_id`: The TMDB ID of the TV show.
    *   `season_number`: The season number.

## Deployment

This project is configured for deployment on Vercel using the `vercel.json` file. Click the "Deploy with Vercel" button above to deploy your own instance. Remember to set the `TMDB_API_KEY` environment variable during the Vercel setup process.
