from connections.external_apis.external_api_client import ExternalApiClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


class NovilleApi(ExternalApiClient):
    def __init__(self):
        self.noville_api_url = "https://noville-api.onrender.com"
        self.headers = {
            "Authorization": f"{os.environ.get('NOVILLE_API_KEY')}"
            }
        super().__init__(self.noville_api_url)

    def post_tweet(self, user_input):
        post_tweets_route = "/x/post_tweet"
        post_tweets_data = {"user_input": user_input}

        return super().post(post_tweets_route, post_tweets_data, self.headers)

    def retrive_user_info(self):
        retrieve_user_info_route = "/x/retrieve_user_info"

        return super().get(retrieve_user_info_route, self.headers)
