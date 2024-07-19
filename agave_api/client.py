import httpx

from .link import Link
from .file_management import FileManagement
from .project_management import ProjectManagement


class AgaveClient:
    """
    Base class for Agave API
    """

    def __init__(self, client_id: str, client_secret: str, timeout: float = 30.0):
        """
        Initializes a new instance of the AgaveClient class.

        Args:
            client_id (str): The client ID.
            client_secret (str): The client secret.
            timeout (float): The timeout for HTTP requests in seconds. Defaults to 30 seconds.
        """
        self.base_url = "https://api.agaveapi.com"
        self.headers = {
            "API-Version": "2021-11-21",
            "Client-Id": client_id,
            "Client-Secret": client_secret,
        }
        self.account_token = None
        self.project_id = None
        self.timeout = timeout
        self.http_client = httpx.Client(timeout=self.timeout)

    @property
    def project_management(self):
        return ProjectManagement(self, self.account_token, self.project_id)

    @property
    def file_management(self):
        return FileManagement(self)

    @property
    def link(self):
        return Link(self)

    def get(self, url: str, **kwargs):
        """
        Sends a GET request using httpx.

        Args:
            url (str): The URL to send the request to.
            **kwargs: Additional keyword arguments to pass to httpx.get().

        Returns:
            httpx.Response: The response from the server.

        Raises:
            httpx.TimeoutException: If the request times out.
        """
        try:
            return self.http_client.get(url, **kwargs)
        except httpx.TimeoutException as e:
            raise httpx.TimeoutException(
                f"Request timed out after {self.timeout} seconds"
            ) from e

    def post(self, url: str, **kwargs):
        """
        Sends a POST request using httpx.

        Args:
            url (str): The URL to send the request to.
            **kwargs: Additional keyword arguments to pass to httpx.post().

        Returns:
            httpx.Response: The response from the server.

        Raises:
            httpx.TimeoutException: If the request times out.
        """
        try:
            return self.http_client.post(url, **kwargs)
        except httpx.TimeoutException as e:
            raise httpx.TimeoutException(
                f"Request timed out after {self.timeout} seconds"
            ) from e

    # Add other HTTP methods (put, delete, etc.) as needed

    def set_account_token(self, account_token: str):
        self.account_token = account_token

    def set_project_id(self, project_id: str):
        self.project_id = project_id

    def __del__(self):
        """
        Closes the httpx client when the AgaveClient instance is deleted.
        """
        self.http_client.close()
