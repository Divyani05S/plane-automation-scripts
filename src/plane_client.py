import requests
import logging
from typing import Optional, Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PlaneAPIClient:
    """
    A client to interact with the Plane API.
    """

    def __init__(self, base_url: str, api_key: str, workspace_slug: str):
        """
        Initialize the Plane API client.

        Args:
            base_url (str): The base URL of the Plane instance (e.g., "https://api.plane.so").
            api_key (str): The API key for authentication.
            workspace_slug (str): The slug of the workspace.
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.workspace_slug = workspace_slug
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def _handle_response(self, response: requests.Response) -> Any:
        """
        Helper method to handle API responses and errors.
        """
        try:
            response.raise_for_status()
            data = response.json()
            
            # Handle pagination: if 'results' key exists, return that list
            if isinstance(data, dict) and "results" in data:
                return data["results"]
            
            return data
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            logger.error(f"Response Content: {response.text}")
            raise
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise

    def get_projects(self) -> List[Dict[str, Any]]:
        """
        Retrieve all projects in the workspace.
        """
        endpoint = f"{self.base_url}/api/v1/workspaces/{self.workspace_slug}/projects/"
        logger.info(f"Fetching projects from: {endpoint}")
        response = requests.get(endpoint, headers=self.headers)
        return self._handle_response(response)

    def get_project_id_by_slug(self, project_slug: str) -> Optional[str]:
        """
        Helper to find a project ID given its slug.
        """
        projects = self.get_projects()
        # Depending on API response structure, this might need adjustment.
        # Assuming list of dicts with 'identifier' or 'slug' or 'name'.
        # Plane usually uses 'identifier' as the slug in the response or 'slug'.
        # Let's check for 'slug' or 'identifier'.
        
        for project in projects:
            # Check both 'slug' and 'identifier' just in case
            if project.get('identifier') == project_slug or project.get('slug') == project_slug:
                return project.get('id')
            # Also check if the user passed the name instead of slug
            if project.get('name') == project_slug:
                 return project.get('id')
        
        logger.warning(f"Project with slug '{project_slug}' not found.")
        return None

    def get_issues(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all issues in a project.
        """
        endpoint = f"{self.base_url}/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/"
        logger.info(f"Fetching issues from: {endpoint}")
        response = requests.get(endpoint, headers=self.headers)
        return self._handle_response(response)

    def create_issue(self, project_id: str, title: str, description: str = "", priority: str = "None", state_id: Optional[str] = None, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new issue (work item) in the specified project.

        Args:
            project_id (str): The UUID of the project.
            title (str): The title of the issue.
            description (str): The description of the issue (Markdown supported).
            priority (str): Priority of the issue (e.g., "urgent", "high", "medium", "low", "none").
            state_id (str, optional): The UUID of the state (e.g., "Todo", "In Progress"). 
                                      If None, uses the default state.
            parent_id (str, optional): The UUID of the parent issue (for creating sub-issues).

        Returns:
            Dict[str, Any]: The created issue data.
        """
        endpoint = f"{self.base_url}/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/"
        
        payload = {
            "name": title,
            "description_html": description, 
            "priority": priority,
        }
        
        if state_id:
            payload["state"] = state_id
            
        if parent_id:
            payload["parent"] = parent_id

        logger.info(f"Creating issue '{title}' in project {project_id}")
        response = requests.post(endpoint, headers=self.headers, json=payload)
        return self._handle_response(response)

    def get_states(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get available states for a project (to find state IDs like 'Todo', 'Done').
        """
        endpoint = f"{self.base_url}/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/states/"
        response = requests.get(endpoint, headers=self.headers)
        return self._handle_response(response)

    def get_state_id_by_name(self, project_id: str, state_name: str) -> Optional[str]:
        """
        Helper to find a state ID by its name (e.g., "Todo").
        """
        states = self.get_states(project_id)
        for state in states:
            if state.get('name').lower() == state_name.lower():
                return state.get('id')
        return None

