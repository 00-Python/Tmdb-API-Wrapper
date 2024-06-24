import json
import requests
from requests.models import Response


class TMDB:

    def __init__(self):

        self.api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzN2MyMmQ5YWMzZTJiZmViYjA1NmE5ZjJiN2RlZmRhYiIsInN1YiI6IjY0MWM0YzJlZjlhYTQ3MDA3ZmM1M2ViZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zCHylbZQP2w9rnxh9AaiQYZx55rceZCw-nUtf8gniEo"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.backdrop_image_base_url = "https://image.tmdb.org/t/p/original"

    def authentication(self):
        auth_url = "https://api.themoviedb.org/3/authentication"

        return requests.get(auth_url, headers=self.headers)

    def movie_search(self, query,  adult: str = "false", lang: str = "en-GB", page: str = "1", year: str = "", air_year: str = ""):
        movie_url = f"https://api.themoviedb.org/3/search/movie?query={query}&first_air_date_year={air_year}&include_adult={adult}&language={lang}&page={page}&year={year}"
        result = requests.get(movie_url, headers=self.headers)
        json_data = json.loads(result.text)
        movies = json_data['results']
        return movies

    def tv_search(self, query, **params) -> Response:
        params['query'] = query
        tv_url = f"https://api.themoviedb.org/3/search/tv"
        return requests.get(tv_url, headers=self.headers, params=params)

    def tv_details(self, show_id) -> Response:
        movie_url = f"https://api.themoviedb.org/3/tv/{show_id}?append_to_response=seasons&language=en-US"
        return requests.get(movie_url, headers=self.headers)

    def episode_details(self, show_id, season_number, episode_number) -> Response:
        episode_url = f"https://api.themoviedb.org/3/tv/{show_id}/season/{season_number}/episode/{episode_number}"
        return requests.get(episode_url, headers=self.headers)

    def movie_details(self, query, show_id):
        movie_url = f"https://api.themoviedb.org/3/tv/{show_id}"
        result = requests.get(movie_url, headers=self.headers)
        json_data = json.loads(result.text)
        tv = json_data['results']
        return tv

    def multi_search(self, query, adult: str = "false", lang: str = "en-GB", page: str = "1"):
        multi_url = f"https://api.themoviedb.org/3/search/multi?query={query}&include_adult={adult}&language={lang}&page={page}"
        result = requests.get(multi_url, headers=self.headers)
        json_data = json.loads(result.text)

        tv_results = []
        movie_results = []

        for result in json_data['results']:
            if result['media_type'] == 'tv':
                tv_results.append(result)
            elif result['media_type'] == 'movie':
                movie_results.append(result)

        return tv_results, movie_results

    def get_movie_details_by_id(self, movie_id):
        # Construct the URL for fetching movie details by ID
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
        
        # Send a GET request to fetch movie details
        response = requests.get(movie_url, headers=self.headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error fetching movie details: {response.status_code}")
            return {"error": f"Failed to fetch details for movie with ID {movie_id}"}
        
        # Parse the JSON response
        movie_details = response.json()
        
        return movie_details

    def get_movie_cast_and_crew(self, movie_id):
        # Construct the URL for fetching movie credits
        credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"
        
        # Send a GET request to fetch movie credits
        response = requests.get(credits_url, headers=self.headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error fetching movie credits: {response.status_code}")
            return {"error": f"Failed to fetch credits for movie with ID {movie_id}"}
        
        # Parse the JSON response
        credits_data = response.json()
        
        # Extract cast and crew information
        cast = credits_data.get('cast', [])
        crew = credits_data.get('crew', [])
        
        return cast, crew

    def get_external_ids(self, movie_id):
        """Fetch external IDs for a specific movie by its ID."""
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/external_ids"
        response = requests.get(url, headers=self.headers)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error fetching external IDs: {response.status_code}")
            return {"error": f"Failed to fetch external IDs for movie with ID {movie_id}"}
        
        # Parse and return the JSON response
        return response.json()


    def trending_movies(self):
        trending_movies_url = f"https://api.themoviedb.org/3/trending/movie/day?language=en-US"
        result = requests.get(trending_movies_url, headers=self.headers)
        json_data = json.loads(result.text)
        trending_movies = json_data['results']
        return trending_movies

    def trending_tv(self):
        trending_tv_url = f"https://api.themoviedb.org/3/trending/tv/day?language=en-US"
        result = requests.get(trending_tv_url, headers=self.headers)
        json_data = json.loads(result.text)
        trending_tv = json_data['results']
        return trending_tv

    def get_seasons_and_episodes_by_search_query(self, query):
        # Perform TV show search
        tv_results, _ = self.multi_search(query)

        if not tv_results:
            return {"error": "No TV show found with the given query."}

        # Get the ID of the first TV show
        show_id = tv_results[0]['id']

        # Fetch TV show details including seasons
        tv_details = self.tv_details(show_id)

        if 'seasons' not in tv_details:
            return {"error": "No seasons found for the TV show."}

        # Prepare data
        seasons_and_episodes = []
        for season in tv_details['seasons']:
            season_info = {
                "season_number": season['season_number'],
                "season_name": season['name'],
                "episodes": []
            }
            for episode_number in range(1, season['episode_count']+1):
                episode_details = self.episode_details(
                    show_id, season['season_number'], episode_number)
                season_info["episodes"].append({
                    "episode_number": episode_details['episode_number'],
                    "episode_details": episode_details
                })
            seasons_and_episodes.append(season_info)

        return seasons_and_episodes

    def get_seasons_and_episodes_by_id(self, series_id):
        # Fetch TV show details including seasons
        tv_details_url = f"https://api.themoviedb.org/3/tv/{series_id}?language=en-US"
        response = requests.get(tv_details_url, headers=self.headers)
        if response.status_code != 200:
            print(f"Error fetching TV details: {response.status_code}")
            return {"error": f"Failed to fetch details for TV show with ID {series_id}"}

        tv_details = response.json()

        # Prepare data
        seasons_and_episodes = []
        for season in tv_details.get('seasons', []):
            season_number = season['season_number']
            # Fetching details for each season including episodes
            season_details_url = f"https://api.themoviedb.org/3/tv/{series_id}/season/{season_number}?language=en-US"
            season_response = requests.get(season_details_url, headers=self.headers)
            if season_response.status_code == 200:
                season_info = season_response.json()
                season_info_filtered = {
                    "season_number": season_number,
                    "season_name": season.get('name', 'N/A'),
                    "episodes": season_info.get('episodes', [])
                }
                seasons_and_episodes.append(season_info_filtered)

        return seasons_and_episodes
url = "https://api.themoviedb.org/3/tv/333/episode_groups"


if __name__ == "__main__":
    ent = TMDB()

    # auth = ent.authentication()
    # tv, movie = ent.multi_search("Alan Partridge")
    # print(movie)
    # ent.get_pages_and_results(q)

    # for result in tv:
    #     # Some entries have 'name', some have 'title'
    #     print("Title:", result.get('name') or result.get('title'))
    #     # Some entries have 'original_name', some have 'original_title'
    #     print("Original Title:", result.get('original_name')
    #           or result.get('original_title'))
    #     # print("Type:", result['media_type']) # movie search does not have this
    #     print("Overview:", result['overview'])
    #     # Some entries have 'release_date', some have 'first_air_date'
    #     print("Release Date:", result.get('release_date')
    #           or result.get('first_air_date'))
    #     print("Vote Average:", result['vote_average'])
    #     print("Vote Count:", result['vote_count'])
    #     print("Popularity:", result['popularity'])
    #     print("Genre IDs:", result['genre_ids'])
    #     print("Backdrop Path:", result['backdrop_path'])
    #     print("Poster Path:", result['poster_path'])
    #     print("Adult:", result['adult'])
    #     print("Original Language:", result['original_language'])
    #     # print("Origin Country:", result['origin_country'])
    #     print(result['id'])
    #     print("-" * 50)

    # tv_details = ent.tv_details(tv[0]['id'])
    # # data = json.loads(tv_details)  # This is no longer necessary

    # # Retrieve the number of seasons directly from the 'tv_details' dictionary
    # data = tv_details
    # # num_episodes = tv_details['number_of_episdoes']

    # # print("Number of seasons:", num_seasons)

    # for season in data['seasons']:
    #     print(f"Season {season['season_number']}: {season['name']}")
    #     for episode in range(1, season['episode_count']+1):
    #         print(f"Episode {episode}")
    #         print(ent.episode_details(tv[0]['id'], season['season_number'], episode))
    #     print()
    # for season in tv_details['seasons']:
    #     episodes = season['episode_count']
    #     print(f"Season {season['season_number']}. {season['name']} has {episodes} episodes")

    #  Episode indformation Test
    # ent = TMDB()

    # tv, movie = ent.multi_search("Alan Partridge")

    # tv_details = ent.tv_details(tv[0]['id'])

    # for season in tv_details['seasons']:
    #     print(f"Season {season['season_number']}: {season['name']}")
    #     for episode_number in range(1, season['episode_count'] + 1):
    #         episode_details = ent.episode_details(
    #             tv[0]['id'], season['season_number'], episode_number)
    #         print(f"Episode {episode_details['episode_number']}")
    #         # Print episode details as JSON
    #         print(json.dumps(episode_details, indent=2))
    #     print()

    # ent = TMDB()
    # data = ent.get_seasons_and_episodes_by_id(87058)
    # print(data)

    ent = TMDB()
    movie_id = 929590  # Replace this with the ID of the movie you want to retrieve details for
    movie_details = ent.get_movie_cast_and_crew(movie_id)
    print(movie_details)
