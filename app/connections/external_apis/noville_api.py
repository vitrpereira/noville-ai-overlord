from connections.external_apis.external_api_client import ExternalApiClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


class NovilleApi(ExternalApiClient):
    noville_api_url = "https://noville-api.onrender.com"
    headers = {"Authorization": f"{os.environ.get('NOVILLE_API_KEY')}"}

    @classmethod
    def post_tweet(cls, user_input):
        post_tweets_route = "/x/post_tweet"
        post_tweets_data = {"user_input": user_input}

        return super().post(
            cls.noville_api_url + post_tweets_route, post_tweets_data,
            cls.headers
        )

    @classmethod
    def retrive_user_info(cls):
        retrieve_user_info_route = "/x/retrieve_user_info"

        return super().get(retrieve_user_info_route, cls.headers)
