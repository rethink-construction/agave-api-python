from .client import BaseAgaveClient


class Link:
    """
    Handles authentication-related functionalities for the Agave API.
    """

    def __init__(self, agave_client: BaseAgaveClient):
        self.agave_client = agave_client

    def create(self, reference_id: str):
        """
        Creates a link token with an reference ID.

        Args:
            reference_id (str): A reference ID associated with the token.

        Returns:
            dict: The response containing the link token.
        """
        url = f"{self.agave_client.base_url}/link/token/create"
        data = {"reference_id": reference_id}
        response = self.agave_client.post(
            url, headers=self.agave_client.headers, data=data
        )
        return response.json()

    def exchange(self, public_token):
        """
        Exchanges a public token for an access token.

        Args:
            public_token (str): The public token to exchange.

        Returns:
            dict: The response containing the access token.
        """
        url = f"{self.agave_client.base_url}/link/token/exchange"
        data = {"public_token": public_token}
        response = self.agave_client.post(
            url, headers=self.agave_client.headers, data=data
        )
        return response.json()
