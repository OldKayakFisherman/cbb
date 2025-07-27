# Census Business Builder (CBB)

## Overview

Census Business Builder (CBB) is an application that aggregates data from Census Bureau API endpoints, stores it in a containerized PostgreSQL database, and provides data visualization through a web interface. The project consists of a data pipeline, a FastAPI backend, a Vue.js frontend, and a Metabase instance for immediate data visualization.

## Project Structure

~~~ascii
cbb/
├── documentation/        # Project documentation
├── pipeline/             # Containerized Python console app for API data ingestion
│   └── .env              # Pipeline settings
├── api/                  # FastAPI backend serving data to the frontend
├── frontend/             # Vue.js application for data visualization
├── docker-compose.yml    # Orchestrates pipeline, API, frontend, and Metabase containers, PostgreSQL init folder: pginit, local storage: pgdata
└── .env                  # Docker Compose settings
~~~

## Architecture
- **Pipeline**: A containerized Python application that consumes Census Bureau API endpoints and stores responses in a PostgreSQL database.
- **API**: A FastAPI backend that serves processed data to the frontend.
- **Frontend**: A Vue.js application that consumes the API and provides data visualization capabilities.
- **Metabase**: A containerized Metabase instance for immediate data exploration and visualization.
- **Database**: A containerized PostgreSQL database for storing API data.

## Development Standards
- **Python**: Adheres to Python coding standards.
- **Vue.js**: Follows Vue.js development standards.
- **Git**: Uses Git standards for version control, with merge/pull requests for managing commits.
- **AWS**: Complies with AWS best practices for deployment and infrastructure.
- **Dependency Management**: Uses UV for managing Python dependencies and project metadata.

## Setup and Installation
1. **Clone the Repository**:
   ~~~bash
   git clone <repository-url>
   cd cbb
   ~~~ 

## Configure Environment:

- Copy the example.env (if provided) to .env in the root and pipeline/ directories.
- Update .env files with necessary configurations (e.g., PostgreSQL settings, API keys).

## Run the Application:
~~~bash
docker-compose up --build
~~~

This command starts the pipeline, API, frontend, PostgreSQL, and Metabase containers.

## Access the Application:

- Frontend: http://localhost:\<frontend-port>
- API: http://localhost:\<api-port>
- Metabase: http://localhost:\<metabase-port>

## Development Workflow

- Version Control: Hosted on Git with merge/pull requests for code integration.
- Contributions: Limited to a small internal team; public contributions are not allowed.
- Dependencies: Managed using UV. Install dependencies with:

~~~bash
uv sync
~~~

## Documentation
- Detailed project documentation is available in the documentation/ directory.
- Refer to specific standards (Python, Vue, Git, AWS) for development guidelines.

## Requirements
- Docker and Docker Compose
- Python 3.8+ (for pipeline and API development)
- Node.js (for frontend development)
- UV (for Python dependency management)
- Git

## License
This project is proprietary and intended for internal use only.


