import sys
from plane_client import PlaneAPIClient

# ==========================================
# CONFIGURATION
# ==========================================
PLANE_BASE_URL = "https://plane.confer.today"
PLANE_WORKSPACE_SLUG = "confer-solutions-ai"
PLANE_API_KEY = "plane_api_711fe8ee2ce24a1e86ade3031******"
PLANE_PROJECT_ID = "a4babd39-1f6e-4494-b494-e858e7c*****"

PARENT_ISSUE_TITLE = "NocoDB: Employee Training & Onboarding"

SUB_ISSUES = [
    {
        "title": "Story 1: Data Completeness Verification (Self-Check)",
        "description": """**Description:** Conduct a line-by-line audit to ensure zero data loss from the source (Monday.com) to NocoDB. Every column, row, and specific data point must be present before handing off for peer validation.

**Acceptance Criteria:**
*   Record count in NocoDB matches Monday.com exactly.
*   All custom fields from Monday.com are mapped and populated.""",
        "priority": "medium"
    },
    {
        "title": "Story 2: View Configuration & Mirroring",
        "description": """**Description:** Configure specific Views in NocoDB to look exactly like the views used in Monday.com. This ensures familiarity for leadership during the transition.

**Acceptance Criteria:**
*   Views created match the naming convention of Monday.com.
*   Column ordering and visibility in these views match the legacy system.
*   Filters applied exactly as they were in the previous system.""",
        "priority": "medium"
    },
    {
        "title": "Story 3: Independent QA Validation (Role Separation)",
        "description": """**Description:** Assign a team member to validate the data and views. Note: The creator cannot perform this task.

**Acceptance Criteria:**
*   Validator confirms data accuracy and view structure.
*   Any discrepancies found are logged as sub-tasks/bugs.""",
        "priority": "medium"
    },
    {
        "title": "Story 4: Draft Leadership Communication",
        "description": """**Description:** Draft the official onboarding email to be sent to the leadership team. This email will invite them to the new system.

**Acceptance Criteria:**
*   Email draft includes login instructions and links to the specific Views created in Story 2.
*   Tone is professional and clear.
*   Draft approved by manager before sending.""",
        "priority": "medium"
    },
    {
        "title": "Story 5: Prepare Demo & Training Agenda",
        "description": """**Description:** Prepare the flow for the Friday morning demo. Outline exactly which views and features will be shown to prove the system works.

**Acceptance Criteria:**
*   Demo script/outline created.
*   Workflow is tested and ready to show.
*   Ready for Friday morning presentation.""",
        "priority": "medium"
    }
]

def main():
    print("--- Starting Sub-Issue Creation Script ---")

    client = PlaneAPIClient(
        base_url=PLANE_BASE_URL,
        api_key=PLANE_API_KEY,
        workspace_slug=PLANE_WORKSPACE_SLUG
    )

    try:
        # 1. Find the Parent Issue ID
        print(f"Searching for parent issue: '{PARENT_ISSUE_TITLE}'...")
        issues = client.get_issues(PLANE_PROJECT_ID)
        
        parent_id = None
        for issue in issues:
            if issue.get('name') == PARENT_ISSUE_TITLE:
                parent_id = issue.get('id')
                break
        
        if not parent_id:
            print(f"Error: Parent issue '{PARENT_ISSUE_TITLE}' not found in project.")
            return

        print(f"Found Parent Issue ID: {parent_id}")

        # 2. Get 'Todo' State ID (Optional)
        todo_state_id = client.get_state_id_by_name(PLANE_PROJECT_ID, "Todo")

        # 3. Create Sub-Issues
        for story in SUB_ISSUES:
            print(f"Creating sub-issue: {story['title']}...")
            new_issue = client.create_issue(
                project_id=PLANE_PROJECT_ID,
                title=story['title'],
                description=story['description'],
                priority=story['priority'],
                state_id=todo_state_id,
                parent_id=parent_id
            )
            print(f"Successfully created sub-issue: {new_issue.get('name')} (ID: {new_issue.get('id')})")

        print("\n--- Script Completed Successfully ---")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
