# Plane API Integration Scripts

This project contains Python scripts to automate data entry into [Plane](https://plane.so/), specifically for creating work items (issues).

## Project Structure

```
plane-integration/
├── src/
│   ├── __init__.py
│   ├── plane_client.py   # The API Client class
│   └── main.py           # The main script to run
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Prerequisites

*   Python 3.8 or higher
*   A Plane account (Cloud or Self-Hosted)
*   A Plane API Key

## Setup & Installation

1.  **Navigate to the project directory:**
    ```bash
    cd plane-integration
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    # Create virtual environment (optional but recommended)
    python -m venv venv
    # Activate it (Windows)
    .\venv\Scripts\activate
    # If you get a "running scripts is disabled" error, run this first:
    # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

    # Activate it (Mac/Linux)
    source venv/bin/activate

    # Install requirements
    pip install -r requirements.txt
    ```

## Configuration

Open `src/main.py` and update the configuration section with your actual Plane details:

```python
# src/main.py

PLANE_BASE_URL = "https://api.plane.so"  # Or your self-hosted URL
PLANE_WORKSPACE_SLUG = "YOUR_WORKSPACE_SLUG"
PLANE_API_KEY = "YOUR_GENERATED_API_KEY"
PLANE_PROJECT_SLUG = "YOUR_PROJECT_SLUG" # e.g., "my-project"
```

### How to get these values:
*   **Workspace Slug**: Look at your browser URL when logged in: `https://app.plane.so/my-workspace/...` -> `my-workspace` is the slug.
*   **Project Slug**: Look at the project URL: `https://app.plane.so/my-workspace/projects/my-project/...` -> `my-project` is the slug.
*   **API Key**: Go to your Profile Settings -> API Tokens -> Generate New Token.

## Usage

Run the main script:

```bash
python src/main.py
```

This will:
1.  Connect to your Plane workspace.
2.  Find the project ID for your specified project slug.
3.  Create the sample work items defined in the script.

## Customization

*   **`src/plane_client.py`**: Contains the `PlaneAPIClient` class. You can extend this to add more methods like `create_cycle`, `create_module`, etc.
*   **`src/main.py`**: Modify the `issues_to_create` list to import your own data.
