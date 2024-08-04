from typing import Optional

from .client import BaseAgaveClient
from .link import Link
from .file_management import FileManagement
from .project_management import ProjectManagement


class AgaveClient(BaseAgaveClient):
    """
    Base class for Agave API
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        account_token: Optional[str] = None,
        project_id: Optional[str] = None,
        timeout: Optional[float] = 30.0,
    ):
        """
        Initializes a new instance of the AgaveClient class inheriting from BaseAgaveClient.

        Args:
            client_id (str): The client ID.
            client_secret (str): The client secret.
            account_token (str): The account token.
            project_id (str): The project ID.
            timeout (float): The timeout for HTTP requests in seconds. Defaults to 30 seconds.
        """
        super().__init__(client_id, client_secret, account_token, project_id, timeout)


    @property
    def project_management(self):
        return ProjectManagement(self, self.account_token, self.project_id)

    @property
    def file_management(self):
        return FileManagement(self)

    @property
    def link(self):
        return Link(self)

__all__ = ["AgaveClient", "Link", "FileManagement", "ProjectManagement"]
