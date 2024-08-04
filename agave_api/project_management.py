from typing import List, Optional, Dict, Any, Callable
from functools import wraps

from .client import BaseAgaveClient


def ensure_account_token(func: Callable):
    @wraps(func)
    def wrapper(self, *args, account_token: Optional[str] = None, **kwargs):
        self._ensure_account_token(account_token)
        return func(self, *args, **kwargs)
    return wrapper


def ensure_project_id(required: bool = True):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, *args, project_id: Optional[str] = None, **kwargs):
            self._ensure_project_id(project_id, required)
            return func(self, *args, project_id=project_id, **kwargs)
        return wrapper
    return decorator


class ProjectManagement:
    def __init__(
        self,
        agave_client: BaseAgaveClient,
        account_token: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        self.agave_client = agave_client
        self.headers = self.agave_client.headers.copy()
        self.account_token = account_token
        self.project_id = project_id

        if account_token:
            self._set_account_token(account_token)
        if project_id:
            self._set_project_id(project_id)

    def _ensure_account_token(self, account_token: Optional[str] = None):
        if self.account_token is None:
            if account_token:
                self._set_account_token(account_token)
            else:
                raise ValueError("Account token is required")

    def _ensure_project_id(
        self, project_id: Optional[str] = None, required: bool = True
    ):
        if project_id:
            self._set_project_id(project_id)
        elif required and not self.project_id:
            raise ValueError("Project ID is required")

    def _set_project_id(self, project_id: str):
        self.project_id = project_id
        self.headers["Project-Id"] = project_id

    def _set_account_token(self, account_token: str):
        self.account_token = account_token
        self.headers["Account-Token"] = account_token

    def _build_url(self, endpoint: str, resource_id: Optional[str] = None) -> str:
        url = f"{self.agave_client.base_url}/{endpoint}"
        if resource_id:
            url += f"/{resource_id}"
        return url

    def _add_pagination(self, params: Dict[str, Any], page: Optional[int], per_page: Optional[int]):
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

    def _add_include_source_fields(self, params: Dict[str, Any], include_source_fields: Optional[List[str]]):
        if include_source_fields:
            params["Include-Source-Data"] = ",".join(include_source_fields)

    def _api_call(self, method: str, endpoint: str, resource_id: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        url = self._build_url(endpoint, resource_id)
        params = {}
        self._add_pagination(params, kwargs.get('page'), kwargs.get('per_page'))
        self._add_include_source_fields(params, kwargs.get('include_source_fields'))
        
        headers = self.headers.copy()
        if kwargs.get('account_token'):
            headers["Account-Token"] = kwargs['account_token']
        if kwargs.get('project_id'):
            headers["Project-Id"] = kwargs['project_id']

        return getattr(self.agave_client, method)(url, params=params, headers=headers)

    @ensure_account_token
    @ensure_project_id(required=False)
    def project(self, project_id: Optional[str] = None, **kwargs) -> Optional[Dict[str, Any]]:
        return self._api_call('get', 'projects', project_id or self.project_id, **kwargs)

    @ensure_account_token
    def projects(self, **kwargs) -> Dict[str, Any]:
        return self._api_call('get', 'projects', **kwargs)

    @ensure_account_token
    @ensure_project_id()
    def rfis(self, **kwargs) -> Dict[str, Any]:
        return self._api_call('get', 'rfis', **kwargs)

    @ensure_account_token
    @ensure_project_id()
    def rfi(self, rfi_id: str, **kwargs) -> Dict[str, Any]:
        return self._api_call('get', 'rfis', rfi_id, **kwargs)

    @ensure_account_token
    @ensure_project_id()
    def submittals(self, **kwargs) -> Dict[str, Any]:
        return self._api_call('get', 'submittals', **kwargs)

    @ensure_account_token
    @ensure_project_id()
    def submittal(self, submittal_id: str, **kwargs) -> Dict[str, Any]:
        return self._api_call('get', 'submittals', submittal_id, **kwargs)

    @ensure_account_token
    @ensure_project_id()
    def specifications(self, **kwargs) -> Dict[str, Any]:
        return self._api_call('get', 'specification-sections', **kwargs)

    @ensure_account_token
    @ensure_project_id()
    def specification(self, specification_id: str, **kwargs) -> Dict[str, Any]:
        return self._api_call('get', 'specification-sections', specification_id, **kwargs)

    @ensure_account_token
    @ensure_project_id(required=False)
    def contacts(self, **kwargs) -> Dict[str, Any]:
        return self._api_call('get', 'contacts', **kwargs)

    @ensure_account_token
    @ensure_project_id(required=False)
    def contact(self, contact_id: str, **kwargs) -> Dict[str, Any]:
        return self._api_call('get', 'contacts', contact_id, **kwargs)

    @ensure_account_token
    @ensure_project_id(required=False)
    def vendors(self, **kwargs) -> Dict[str, Any]:
        return self._api_call('get', 'vendors', **kwargs)

    @ensure_account_token
    @ensure_project_id(required=False)
    def vendor(self, vendor_id: str, **kwargs) -> Dict[str, Any]:
        return self._api_call('get', 'vendors', vendor_id, **kwargs)

    @ensure_account_token
    @ensure_project_id()
    def drawings(self, **kwargs) -> Dict[str, Any]:
        return self._api_call('get', 'drawings', **kwargs)

    @ensure_account_token
    @ensure_project_id()
    def drawing(self, drawing_id: str, **kwargs) -> Dict[str, Any]:
        return self._api_call('get', 'drawings', drawing_id, **kwargs)

    @ensure_account_token
    @ensure_project_id()
    def drawing_versions(self, drawing_id: str, **kwargs) -> Dict[str, Any]:
        return self._api_call('get', f'drawings/{drawing_id}/versions', **kwargs)