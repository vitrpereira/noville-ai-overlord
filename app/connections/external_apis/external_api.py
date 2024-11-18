import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ExternalApi:
    """
    Parent class for all External APIs handling.
    """
    class UnauthorizedError(Exception): pass

    @classmethod
    def perform(cls, endpoint_url, verb, payload, headers=None, retries=0):
        try:
            method = getattr(requests, verb)

            logger.info(f"Performing '{verb.upper()}' request to '{endpoint_url}'")

            start_time = cls._event_timestamp()
            response = method(endpoint_url, headers=headers, json=payload)
            end_time = cls._event_timestamp()

            request_duration = end_time - start_time

            logger.info(f"RESPONSE Time: {request_duration}")
            logger.info(f"RESPONSE Status Code: {response.status_code}")
            logger.info(f"RESPONSE Body: {response.json()}")

            # Retry on rate limit exceeded or bad gateway
            response = cls._retry_on_error(response, retries=retries) if retries else response

            if cls._unauthorized_response(response):
                raise cls.UnauthorizedError('Unable to authenticate with external API')

            response.raise_for_status()

            return response
        except Exception as e:
            logger.error(f"Error performing request: {e}")
            raise e
    
    @classmethod
    def _retry_on_error(cls, response, retries):
        retry_count = 0

        if response.status_code == 429 or response.status_code == 502:
            while retry_count < retries:
                logger.info(f"Rate limit exceeded. Retrying... ({retry_count}/{retries})")
                retry_count += 1

                return cls.perform(
                    response.request.url, 
                    response.request.method, 
                    response.request.json(), 
                    response.request.headers
                )
        return response
    @classmethod
    def _unauthorized_response(cls, response):
        if response.status_code == 401:
            logger.error(f"Unauthorized request: {response.json()}")
            return True
        return False

    @staticmethod
    def _event_timestamp():
        return datetime.now()
