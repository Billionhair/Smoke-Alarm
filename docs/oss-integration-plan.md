# Open Source Integration Plan

| Feature | OSS Component | Reason | Integration Approach |
|--------|---------------|--------|----------------------|
| Routing engine | [OSRM](http://project-osrm.org/) | Self-hostable, high performance routing | Run OSRM via Docker with Australia PBF and query through new client module respecting `OSRM_BASE_URL`. |
| Route optimization with constraints | [OR-Tools](https://developers.google.com/optimization) | Mature VRP solver supporting time windows and capacities | Use OSRM travel-time matrix as input to custom `vrptw` module wrapping OR-Tools. |
| Geocoding | [Nominatim](https://nominatim.org/) | OpenStreetMap geocoder, self-hostable | Provide adapter with rate limiting and custom `User-Agent`, configurable base URL. |
| Spreadsheet sync | [gspread](https://github.com/burnash/gspread) | Simple Google Sheets API client | New sync module using service account credentials for import/export. |
| Notifications | [Apprise](https://github.com/caronc/apprise) | Unified notification library supporting many services | Wrapper module sending messages based on `APPRISE_URLS`. |
| Report generation | [WeasyPrint](https://weasyprint.org/) + [docxtpl](https://github.com/elapouya/python-docx-template) | PDF/Word document rendering from templates | Report service rendering HTML templates to PDF and optional DOCX output. |
| Dispatcher UI | [Streamlit](https://streamlit.io/) | Rapid web apps for Python | Minimal app allowing address input and route visualization. |
| API layer | [FastAPI](https://fastapi.tiangolo.com/) | Modern async web framework | Expose `/solve` and `/job` endpoints calling internal optimizer. |
| Notifications & CI | [pre-commit](https://pre-commit.com/), GitHub Actions | Enforce style and tests | Pre-commit config and workflow running `pre-commit` and `pytest` on pushes and PRs. |
| Google Sheets sync | gspread | Manage spreadsheets programmatically | Provide simple export/import helpers using service account credentials. |
