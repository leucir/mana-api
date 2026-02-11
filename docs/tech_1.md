Generate a technical implementation plan that utilizes modern API standards.

1. Technology Stack
- Core: Python running as a Cloud Function in Python, to be deployed in Firebase.
- State Management: Use a lightweight, custom "Pub/Sub" or "Observer" pattern to handle the Inspection state.
- Storage: Firestore.
- Files for evidences are stored in the Firebase Cloud Storage.

2. Architecture & File Structure
- Separate concerns into:
  - /api: APIs for client and admin access.
  - /tests: testcases and any additional artifact to support the tests.
  - /model: entities/aggreagates classes with logical implementation.
  - /ai: artifacts to support AI agents logic and integration.

3. Implementation Strategies
  - Build the code with ability to ingest environment variables per environment (dev, test, prod)
  - AI functions will use Langgraph to orchestrate the Inspection workflow
  - Any external resource is configured using configuration files and factory/builder patterns
  - Use streaming to talk with LLMs if possible
  - Tests use real LLM endpoint to be configured
  - Use Makefile to centralize the commands for test, build, and deploy

4. Data Model
- Define models as JSON structure.
- Optimize for Firestore.
