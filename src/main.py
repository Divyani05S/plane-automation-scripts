import sys
from plane_client import PlaneAPIClient

# ==========================================
# CONFIGURATION - REPLACE WITH YOUR VALUES
# ==========================================

# 1. Your Plane Workspace URL
PLANE_BASE_URL = "https://plane.confer.today"

# 2. Your Plane Workspace Slug
#    Found in your URL: https://plane.confer.today/confer-solutions-ai/...
PLANE_WORKSPACE_SLUG = "confer-solutions-ai"

# 3. Your Plane API Key
PLANE_API_KEY = "plane_api_711fe8ee2ce24a1e86ade30******"

# 4. The Project ID (Extracted from your URL)
#    URL: .../projects/a4babd39-1f6e-4494-b494-e858e7c97582/issues/
PLANE_PROJECT_ID = "a4babd39-1f6e-4494-b494-e858e7c97582"

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
        # Step 1: Use the provided Project ID directly
        project_id = PLANE_PROJECT_ID
        print(f"Using Project ID: {project_id}")

        # Step 2: (Optional) Get State ID for 'Todo'
        print("Fetching project states...")
        # Note: If 'Todo' state doesn't exist, it will default to the project's default state (usually Backlog or Todo)
        todo_state_id = client.get_state_id_by_name(project_id, "Todo")
        if todo_state_id:
            print(f"Found 'Todo' state ID: {todo_state_id}")
        else:
            print("Could not find 'Todo' state, using default.")

        # Step 3: Create Work Items (Issues)
        # Note: Priority values usually need to be lowercase (urgent, high, medium, low, none)
        issues_to_create = [
            {"title": "Moxie: Task Organization Verification", "description": "Audit and confirm all project tasks are correctly assigned and structured by owner/user role.", "priority": "medium"},
            {"title": "NocoDB: Employee Data Ingestion", "description": "Populate the NocoDB database with current employee records and user details.", "priority": "medium"},
            {"title": "NocoDB: Employee Training & Onboarding", "description": "Develop and deliver training sessions on using NocoDB for Moxie employees.", "priority": "medium"},
            {"title": "Moxie: n8n Automation Flow Setup", "description": "Configure and deploy core automation workflows using n8n for critical business processes.", "priority": "high"},
            {"title": "VAPI: Phone Call Integration Deployment", "description": "Integrate vAPI to handle and log phone call interactions within the system.", "priority": "high"},
            {"title": "VAPI: Website Voice Widget Setup", "description": "Implement vAPI for the interactive voice widget feature on the company website.", "priority": "medium"},
            {"title": "Internal Chatbot: UI & Deployment", "description": "Develop the internal AI chatbot application and deploy its web-based user interface.", "priority": "high"},
            {"title": "Langfuse: Reporting & Analytics Delivery", "description": "Monitor Langfuse logs, generate new reports, analyze insights, and deliver findings to stakeholders.", "priority": "medium"},
            {"title": "Website Chatbot: Maintenance & Updates", "description": "Ongoing maintenance, feature updates, and knowledge base refreshment for the website chatbot.", "priority": "low"},
            {"title": "Anywhere Chatbot: Maintenance & Updates", "description": "Ongoing maintenance and knowledge base updates for the Anywhere platform chatbot.", "priority": "low"},
            {"title": "Internal Chatbot: Maintenance & Updates", "description": "Ongoing maintenance and knowledge base updates for the internal web-based chatbot.", "priority": "low"},
            {"title": "BPMN: Camunda Process Modeling", "description": "Document core business processes using BPMN standards and the Camunda modeling tool.", "priority": "medium"},
            {"title": "Documentation: Cleanup and Structure", "description": "Standardize, consolidate, and organize existing project documentation for clarity and accessibility.", "priority": "low"},
            {"title": "Documentation: Role & Department SOPs", "description": "Create standardized operating procedures (SOPs) and process guides tailored for specific roles and departments.", "priority": "medium"},
            {"title": "IT: Comprehensive Backup Strategy", "description": "Design and document a robust, tested strategy for all critical IT systems and data backups.", "priority": "high"},
            {"title": "Decision Engine / LOS Replacement (Target Feb 2026)", "description": "Planning and execution of the replacement project for the current Lending Origination System (LOS) / Decision Engine.", "priority": "high"},
            {"title": "Vendor Review: Licensing & Cost Audit", "description": "Review all current vendor contracts, licensing, pricing, and evaluate potential replacement options.", "priority": "medium"},
            {"title": "Jungo: Sales Reporting Refinement", "description": "Clean up and optimize sales data and reporting within the Jungo platform.", "priority": "medium"},
            {"title": "Payment Strategy (ACH, Wells, etc.)", "description": "Define the full technical and operational payment strategy.", "priority": "high"}
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
