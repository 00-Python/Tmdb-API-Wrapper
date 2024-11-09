# TMDB API Integration Module

This module provides a Python wrapper around the [TMDb API](https://www.themoviedb.org/documentation/api) for accessing and retrieving movie and TV show information. With a few lines of code, developers can use this module to interact with TMDb data, conduct multi-media searches, and obtain detailed information on media titles.

## Features

- **Authentication**: Initializes and authenticates with TMDb.
- **Search Movies**: Search for movies by title and filter results by year, language, or adult content.
- **Search TV Shows**: Search for TV shows by title and get detailed metadata, including seasons and episodes.
- **Trending Media**: Retrieve the trending movies and TV shows of the day.
- **Cast & Crew**: Fetch cast and crew details for a specific movie.
- **Detailed Media Information**: Retrieve detailed information on movies and TV shows, including external IDs for cross-referencing.

## Installation

Install the necessary library using pip:

```bash
pip install requests
```

## Usage

First, import the `TMDB` class and create an instance:

```python
from your_module_name import TMDB

tmdb = TMDB()
```

### Example Calls

- **Search for a Movie**:

  ```python
  results = tmdb.movie_search(query="Inception")
  print(results)
  ```

- **Fetch Trending Movies**:

  ```python
  trending_movies = tmdb.trending_movies()
  print(trending_movies)
  ```

- **Get Detailed TV Show Info**:

  ```python
  show_details = tmdb.tv_details(show_id=87058)
  print(show_details)
  ```

- **Retrieve Cast & Crew for a Movie**:

  ```python
  movie_cast_crew = tmdb.get_movie_cast_and_crew(movie_id=929590)
  print(movie_cast_crew)
  ```

## API Reference

### `movie_search(query, adult, lang, page, year, air_year)`
Search for movies based on a query string with additional filters such as adult content, language, and year.

### `tv_search(query, **params)`
Search for TV shows by title, with optional parameters.

### `trending_movies()`
Fetches a list of trending movies.

### `get_movie_cast_and_crew(movie_id)`
Retrieves cast and crew for a specific movie.

### `get_seasons_and_episodes_by_id(series_id)`
Fetches detailed season and episode information for a TV show by its ID.

## License

This module is provided "as-is" under an open-source license, and TMDb API terms of use apply. Visit [TMDb's API documentation](https://www.themoviedb.org/documentation/api) for details.
