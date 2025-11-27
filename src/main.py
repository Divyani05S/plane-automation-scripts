import sys
from plane_client import PlaneAPIClient

# ==========================================
# CONFIGURATION - REPLACE WITH YOUR VALUES
# ==========================================

# 1. Your Plane Workspace URL (e.g., https://app.plane.so or your self-hosted URL)
#    If using the cloud version, the base API URL is usually https://api.plane.so
PLANE_BASE_URL = "https://api.plane.so" 

# 2. Your Plane Workspace Slug
#    Found in your URL: https://app.plane.so/YOUR_WORKSPACE_SLUG/...
PLANE_WORKSPACE_SLUG = "YOUR_WORKSPACE_SLUG"

# 3. Your Plane API Key
#    Generate this in your Plane Profile Settings > API Tokens
PLANE_API_KEY = "TEST_API_KEY"

# 4. The Project Slug (Identifier) where you want to create issues
#    Found in the project URL or settings (e.g., "DMOXI" or "test-project")
PLANE_PROJECT_SLUG = "test-project-slug"

# ==========================================

def main():
    print("--- Starting Plane Integration Script ---")

    # Initialize the client
    client = PlaneAPIClient(
        base_url=PLANE_BASE_URL,
        api_key=PLANE_API_KEY,
        workspace_slug=PLANE_WORKSPACE_SLUG
    )

    try:
        # Step 1: Get the Project ID
        print(f"Looking for project: {PLANE_PROJECT_SLUG}...")
        project_id = client.get_project_id_by_slug(PLANE_PROJECT_SLUG)

        if not project_id:
            print(f"Error: Project with slug '{PLANE_PROJECT_SLUG}' not found.")
            print("Please check your PLANE_PROJECT_SLUG and ensure the API Key has access.")
            return

        print(f"Found Project ID: {project_id}")

        # Step 2: (Optional) Get State ID for 'Todo'
        # This ensures the issue lands in the right column.
        print("Fetching project states...")
        todo_state_id = client.get_state_id_by_name(project_id, "Todo")
        if todo_state_id:
            print(f"Found 'Todo' state ID: {todo_state_id}")
        else:
            print("Could not find 'Todo' state, using default.")

        # Step 3: Create Work Items (Issues)
        # Based on your requirements/images
        issues_to_create = [
            {
                "title": "n8n Core Automation",
                "description": "Implement the core automation logic for n8n.",
                "priority": "High"
            },
            {
                "title": "DMOXI-9.5 Error Handling & Notification Workflow",
                "description": "Implement robust error handling path within the main n8n workflow.",
                "priority": "Urgent"
            },
            {
                "title": "Flowise API Node Setup",
                "description": "Setup the API nodes for Flowise integration.",
                "priority": "Medium"
            }
        ]

        for issue_data in issues_to_create:
            print(f"Creating issue: {issue_data['title']}...")
            new_issue = client.create_issue(
                project_id=project_id,
                title=issue_data['title'],
                description=issue_data['description'],
                priority=issue_data['priority'],
                state_id=todo_state_id
            )
            print(f"Successfully created issue: {new_issue.get('name')} (ID: {new_issue.get('id')})")

        print("\n--- Script Completed Successfully ---")

    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")
        # In a real scenario, you might want to log the full traceback
        # import traceback
        # traceback.print_exc()

if __name__ == "__main__":
    main()
