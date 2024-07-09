from typing import List, Optional, Dict, Any


class ProjectManagement:
    """
    Manages projects and related resources within the Agave API.

    This class provides methods to interact with various project-related endpoints
    of the Agave API, including projects, RFIs, submittals, specifications,
    contacts, vendors, and drawings.
    """

    def __init__(
        self,
        agave_client,
    ):
        """
        Initializes a new instance of the ProjectManagement class.

        Args:
            agave_client (AgaveClient): The Agave client instance for making API requests.
        """
        self.agave_client = agave_client
        self.headers = self.agave_client.headers.copy()
        self.account_token = None
        self.project_id = None

    def _ensure_account_token(self, account_token: Optional[str] = None):
        """
        Ensures that an account token is set.

        Raises:
            ValueError: If no account token is set.
        """
        if self.account_token is None:
            if account_token:
                self._set_account_token(account_token)
            else:
                raise ValueError("Account token is required")

    def _ensure_project_id(
        self, project_id: Optional[str] = None, required: bool = True
    ):
        """
        Ensures that a project_id is set.

        Raises:
            ValueError: If no project_id is set.
        """
        if project_id:
            self._set_project_id(project_id)
        else:
            if required and not self.project_id:
                raise ValueError("Project ID is required")

    def _add_include_source_fields(self, include_source_fields: Optional[List[str]]):
        """
        Adds the Include-Source-Data header if include_source_fields is provided.

        Args:
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.
        """
        if include_source_fields:
            self.headers["Include-Source-Data"] = ",".join(include_source_fields)

    def _set_project_id(self, project_id: str):
        """
        Sets the project ID for the current instance and updates the headers.

        Args:
            project_id (str): The project ID to set.
        """
        self.project_id = project_id
        self.headers["Project-Id"] = project_id

    def _set_account_token(self, account_token: str):
        """
        Sets the account token for the current instance and updates the headers.

        Args:
            account_token (str): The account token to set.
        """
        self.account_token = account_token
        self.headers["Account-Token"] = account_token

    def project(
        self,
        project_id: Optional[str] = None,
        include_source_fields: Optional[List[str]] = None,
        account_token: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Fetches a project by its ID.

        Args:
            project_id (Optional[str]): The project ID. If not provided, uses the instance's project_id.
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.
            account_token (Optional[str]): The account token. If not provided, uses the instance's account_token.

        Returns:
            Optional[Dict[str, Any]]: The project data as a dictionary, or None if an error occurs.

        Raises:
            ValueError: If neither project_id nor account_token is set.
        """
        try:
            self._ensure_account_token(account_token)
            
            self._ensure_project_id(project_id, required=False)

            url = f"{self.agave_client.base_url}/projects/{project_id}"
            self._add_include_source_fields(include_source_fields)
            response = self.agave_client.get(url, headers=self.headers)
            return response.json()
        except Exception as e:
            print(f"Error fetching project: {e}")
            return None

    def projects(
        self,
        include_source_fields: Optional[List[str]] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 100,
        account_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fetches all projects.

        Args:
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.
            page (Optional[int]): The page number to fetch. Defaults to 1.
            per_page (Optional[int]): The number of results per page. Defaults to 100.
            account_token (Optional[str]): The account token. If not provided, uses the instance's account_token.

        Returns:
            Dict[str, Any]: A dictionary containing a list of projects and pagination metadata.

        Raises:
            ValueError: If account_token is not set.
        """
        self._ensure_account_token(account_token)

        url = f"{self.agave_client.base_url}/projects"
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        if params:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            url += f"?{query_string}"

        self._add_include_source_fields(include_source_fields)
        response = self.agave_client.get(url, headers=self.headers)
        return response.json()

    def rfis(
        self,
        include_source_fields: Optional[List[str]] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 100,
        account_token: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fetches all RFIs (Requests for Information).

        Args:
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.
            page (Optional[int]): The page number to fetch. Defaults to 1.
            per_page (Optional[int]): The number of results per page. Defaults to 100.
            account_token (Optional[str]): The account token. If not provided, uses the instance's account_token.
            project_id (Optional[str]): The project ID. If not provided, uses the instance's project_id.

        Returns:
            Dict[str, Any]: A dictionary containing a list of RFIs and pagination metadata.

        Raises:
            ValueError: If neither account_token nor project_id is set.
        """
        self._ensure_account_token(account_token)
        
        self._ensure_project_id(project_id)

        url = f"{self.agave_client.base_url}/rfis"

        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        self._add_include_source_fields(include_source_fields)
        response = self.agave_client.get(url, headers=self.headers)
        return response.json()

    def rfi(
        self,
        rfi_id: str,
        include_source_fields: Optional[List[str]] = None,
        account_token: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fetches an RFI by its ID.

        Args:
            rfi_id (str): The ID of the RFI.
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.
            account_token (Optional[str]): The account token. If not provided, uses the instance's account_token.
            project_id (Optional[str]): The project ID. If not provided, uses the instance's project_id.

        Returns:
            Dict[str, Any]: The RFI data as a dictionary.

        Raises:
            ValueError: If neither account_token nor project_id is set.
        """
        self._ensure_account_token(account_token)
        
        self._ensure_project_id(project_id)

        url = f"{self.agave_client.base_url}/rfis/{rfi_id}"
        self._add_include_source_fields(include_source_fields)
        response = self.agave_client.get(url, headers=self.headers)
        return response.json()

    def submittals(
        self,
        include_source_fields: Optional[List[str]] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 100,
        account_token: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fetches all submittals.

        Args:
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.
            page (Optional[int]): The page number to fetch. Defaults to 1.
            per_page (Optional[int]): The number of results per page. Defaults to 100.
            account_token (Optional[str]): The account token. If not provided, uses the instance's account_token.
            project_id (Optional[str]): The project ID. If not provided, uses the instance's project_id.

        Returns:
            Dict[str, Any]: A dictionary containing a list of submittals and pagination metadata.

        Raises:
            ValueError: If neither account_token nor project_id is set.
        """
        self._ensure_account_token(account_token)
        
        self._ensure_project_id(project_id)

        url = f"{self.agave_client.base_url}/submittals"
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        if params:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            url += f"?{query_string}"

        self._add_include_source_fields(include_source_fields)
        response = self.agave_client.get(url, headers=self.headers)
        return response.json()

    def submittal(
        self,
        submittal_id: str,
        include_source_fields: Optional[List[str]] = None,
        account_token: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fetches a submittal by its ID.

        Args:
            submittal_id (str): The ID of the submittal.
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.
            account_token (Optional[str]): The account token. If not provided, uses the instance's account_token.
            project_id (Optional[str]): The project ID. If not provided, uses the instance's project_id.

        Returns:
            Dict[str, Any]: The submittal data as a dictionary.

        Raises:
            ValueError: If neither account_token nor project_id is set.
        """
        self._ensure_account_token(account_token)
        
        self._ensure_project_id(project_id)

        url = f"{self.agave_client.base_url}/submittals/{submittal_id}"
        self._add_include_source_fields(include_source_fields)
        response = self.agave_client.get(url, headers=self.headers)
        return response.json()

    def specifications(
        self,
        include_source_fields: Optional[List[str]] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        account_token: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fetches all specifications.

        Args:
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.
            page (Optional[int]): The page number to fetch.
            per_page (Optional[int]): The number of results per page.
            account_token (Optional[str]): The account token. If not provided, uses the instance's account_token.
            project_id (Optional[str]): The project ID. If not provided, uses the instance's project_id.

        Returns:
            Dict[str, Any]: A dictionary containing a list of specifications and pagination metadata.

        Raises:
            ValueError: If neither account_token nor project_id is set.
        """
        self._ensure_account_token(account_token)

        self._ensure_project_id(project_id)

        url = f"{self.agave_client.base_url}/specification-sections"

        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        if params:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            url += f"?{query_string}"

        self._add_include_source_fields(include_source_fields)
        response = self.agave_client.get(url, headers=self.headers)
        return response.json()

    def specification(
        self,
        specification_id: str,
        include_source_fields: Optional[List[str]] = None,
        account_token: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fetches a specification by its ID.

        Args:
            specification_id (str): The ID of the specification.
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.
            account_token (Optional[str]): The account token. If not provided, uses the instance's account_token.
            project_id (Optional[str]): The project ID. If not provided, uses the instance's project_id.

        Returns:
            Dict[str, Any]: The specification data as a dictionary.

        Raises:
            ValueError: If neither account_token nor project_id is set.
        """
        self._ensure_account_token(account_token)

        self._ensure_project_id(project_id)

        url = f"{self.agave_client.base_url}/specification-sections/{specification_id}"
        self._add_include_source_fields(include_source_fields)
        response = self.agave_client.get(url, headers=self.headers)
        return response.json()

    def contacts(
        self,
        include_source_fields: Optional[List[str]] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 100,
        account_token: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fetches all contacts.

        Args:
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.
            page (Optional[int]): The page number to fetch.
            per_page (Optional[int]): The number of results per page.

        Returns:
            dict: A dictionary containing a list of contacts and pagination metadata.
        """
        self._ensure_account_token(account_token)

        self._ensure_project_id(project_id, required=False)

        url = f"{self.agave_client.base_url}/contacts"
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        if params:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            url += f"?{query_string}"

        self._add_include_source_fields(include_source_fields)
        response = self.agave_client.get(url, headers=self.headers)
        return response.json()

    def contact(
        self,
        contact_id: str,
        include_source_fields: Optional[List[str]] = None,
        account_token: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        """
        Fetches a contact by its ID.

        Args:
            contact_id (str): The ID of the contact.
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.

        Returns:
            dict: The contact.
        """
        self._ensure_account_token(account_token)

        self._ensure_project_id(project_id, required=False)

        url = f"{self.agave_client.base_url}/contacts/{contact_id}"
        self._add_include_source_fields(include_source_fields)
        response = self.agave_client.get(url, headers=self.headers)
        return response.json()

    def vendors(
        self,
        include_source_fields: Optional[List[str]] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 100,
        account_token: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        """
        Fetches all vendors.

        Args:
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.
            page (Optional[int]): The page number to fetch.
            per_page (Optional[int]): The number of results per page.

        Returns:
            dict: A dictionary containing a list of vendors.
        """
        self._ensure_account_token(account_token)

        self._ensure_project_id(project_id, required=False)

        url = f"{self.agave_client.base_url}/vendors"
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        if params:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            url += f"?{query_string}"

        self._add_include_source_fields(include_source_fields)
        response = self.agave_client.get(url, headers=self.headers)
        return response.json()

    def vendor(
        self,
        vendor_id: str,
        include_source_fields: Optional[List[str]] = None,
        account_token: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        """
        Fetches a vendor by its ID.

        Args:
            vendor_id (str): The ID of the vendor.
            include_source_fields (Optional[List[str]]): A list of fields to include in the response.

        Returns:
            dict: The vendor.
        """
        self._ensure_account_token(account_token)

        self._ensure_project_id(project_id, required=False)

        url = f"{self.agave_client.base_url}/vendors/{vendor_id}"
        self._add_include_source_fields(include_source_fields)
        response = self.agave_client.get(url, headers=self.headers)
        return response.json()

    def drawings(
        self,
        include_source_fields: Optional[List[str]] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 100,
        account_token: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        """
        Fetches all drawings.
        """

        self._ensure_account_token(account_token)

        self._ensure_project_id(project_id)

        url = f"{self.agave_client.base_url}/drawings"
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        if params:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            url += f"?{query_string}"

        self._add_include_source_fields(include_source_fields)
        response = self.agave_client.get(url, headers=self.headers)
        return response.json()

    def drawing(
        self,
        drawing_id: str,
        include_source_fields: Optional[List[str]] = None,
        account_token: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        """
        Fetches a drawing by its ID.
        """

        self._ensure_account_token(account_token)

        self._ensure_project_id(project_id)

        url = f"{self.agave_client.base_url}/drawings/{drawing_id}"
        self._add_include_source_fields(include_source_fields)
        response = self.agave_client.get(url, headers=self.headers)
        return response.json()
