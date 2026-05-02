<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

<!-- BEGIN:python-agent-rules -->
# Python Agent Rules

## Dependencies
- All dependencies must be listed in `requirements.txt`.
- Use `uv pip install` to install dependencies.

## API
- The API is served by `uvicorn api.index:app --reload --port 8000`.

## Project Structure
- API: `api/`
- Frontend: `src/`

## Testing
- Create API tests in `tests/api/test_download.py`.
- Use `pytest tests/api/test_download.py` to run tests.

## Environment Variables
- Use `.env` file for environment variables.

<!-- END:python-agent-rules -->
