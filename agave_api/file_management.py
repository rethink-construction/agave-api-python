from typing import List, Optional

from .client import BaseAgaveClient


class FileManagement:
    """
    Manages files and folders within the Agave API.

    Inherits from:
        AgaveClient: Provides basic HTTP methods and configuration.
    """

    def __init__(
        self,
        agave_client: BaseAgaveClient,
    ):
        """
        Initializes a new instance of the FileManagement class.

        Args:
            client_id (str): The client ID.
            client_secret (str): The client secret.
            account_token (str): The account token.
            project_id (Optional[str]): The project ID.
        """
        self.agave_client = agave_client
        self.agave_client = agave_client
        self.headers = self.agave_client.headers.copy()
        self.account_token = None
        self.project_id = None

    def file(self, file_id: str, include_source_fields: Optional[List[str]] = None):
        """
        Fetches a file by its ID.

        Args:
            file_id (str): The ID of the file.
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.

        Returns:
            dict: The file.
        """
        url = f"{self.base_url}/files/{file_id}"
        if include_source_fields:
            self.headers["Include-Source-Data"] = ",".join(include_source_fields)
        response = self.get(url, headers=self.headers)
        return response.json()

    def files(self, folder_id: str, include_source_fields: Optional[List[str]] = None):
        """
        Fetches all files in a folder by its ID.

        Args:
            folder_id (str): The ID of the folder.
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.

        Returns:
            list: A list of files in the specified folder.
        """
        url = f"{self.base_url}/folders/{folder_id}/files"
        if include_source_fields:
            self.headers["Include-Source-Data"] = ",".join(include_source_fields)
        response = self.get(url, headers=self.headers)
        return response.json()

    def folder(self, folder_id: str, include_source_fields: Optional[List[str]] = None):
        """
        Fetches a folder by its ID.

        Args:
            folder_id (str): The ID of the folder.
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.

        Returns:
            dict: The folder.
        """
        url = f"{self.base_url}/folders/{folder_id}"
        if include_source_fields:
            self.headers["Include-Source-Data"] = ",".join(include_source_fields)
        response = self.get(url, headers=self.headers)
        return response.json()

    def root_folder(
        self,
        project_id: Optional[str] = None,
        include_source_fields: Optional[List[str]] = None,
    ):
        """
        Fetches the root folder for a given project.

        Args:
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.

        Returns:
            list: A list of folders and files in the root folder.
        """
        url = f"{self.base_url}/root-folder"

        if project_id is None:
            if self.project_id is None:
                raise ValueError("Project ID is required")
            project_id = self.project_id
        else:
            self.headers["Project-Id"] = project_id

        if include_source_fields:
            self.headers["Include-Source-Data"] = ",".join(include_source_fields)
        response = self.get(url, headers=self.headers)
        return response.json()

    def file_tree(
        self,
        folder_id: Optional[str] = None,
        include_source_fields: Optional[List[str]] = None,
    ):
        """
        Recursively fetches all files and folders starting from the given folder ID or the root folder.

        Args:
            folder_id (Optional[str]): The ID of the folder to start from, defaults to the root folder.
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.

        Returns:
            dict: A dictionary representing the folder structure including all subfolders and files.
        """
        if folder_id is None:
            folder_data = self.root_folder(include_source_fields=include_source_fields)
        else:
            folder_data = self.folder(
                folder_id, include_source_fields=include_source_fields
            )

        # Recursively fetch subfolders and update each subfolder in place
        for subfolder in folder_data.get("folders", []):
            # Recursive call to fetch the tree for the subfolder
            nested_folder_data = self.file_tree(subfolder["id"], include_source_fields)
            # Update the subfolder dictionary with nested data
            subfolder.update(nested_folder_data)

        # No need to fetch files separately as they are already included in the folder data
        return folder_data
