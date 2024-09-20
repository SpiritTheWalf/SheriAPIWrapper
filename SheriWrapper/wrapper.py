import importlib.resources
import os
import json
import aiohttp

from dotenv import load_dotenv
load_dotenv()

with importlib.resources.open_text("SheriWrapper", "endpoints.json") as file:
    data = json.load(file)

sfw_endpoints = data['SFW_ENDPOINTS']
nsfw_endpoints = data['NSFW_ENDPOINTS']


class InvalidEndpointError(Exception):
    """
    Error that is called if an invalid endpoint is passed
    """
    print("That is not a valid endpoint!")


class UnauthorizedError(Exception):
    """
    Error that is called if you do not have a valid API key
    """
    def __init__(self, message="Unauthorized, please make sure your API key is correct"):
        self.message = message
        super().__init__(self.message)


class SheriWrapper:
    """
    The class for the Wrapper itself
    """
    api_key = os.getenv("API_KEY")
    user_agent = os.getenv("USER_AGENT")
    api_url = "https://sheri.bot/api"
    headers = {
        "Authorization": f"Token {api_key}",
        "User-Agent": user_agent
    }

    def __init__(self):
        pass

    @staticmethod
    async def lookup(endpoint):
        """
         Method that takes one parameter, endpoint, and returns a parsed dict of responses
        """
        if endpoint not in sfw_endpoints and endpoint not in nsfw_endpoints:
            raise InvalidEndpointError("That endpoint is not in the list")

        url = f"{SheriWrapper.api_url}/{endpoint}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=SheriWrapper.headers) as response:
                if response.status == 401:
                    raise UnauthorizedError()

                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    raise Exception(response.status)
