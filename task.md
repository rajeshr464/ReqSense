# ReqSense Development Task List

## 1. Project Setup
- [x] Initialize Python environment and [requirements.txt](file:///f:/ReqSense/requirements.txt) (Django, Pandas, python-dotenv, google-generativeai, reportlab).
- [x] Create Django project `reqsense` and apps (`accounts`, [dashboard](file:///f:/ReqSense/api/views.py#35-49), `api`).
- [x] Configure [settings.py](file:///f:/ReqSense/reqsense/settings.py) (Templates, Static files, Installed Apps).

## 2. User Authentication & Isolation
- [x] Implement Custom User Model in `accounts`.
- [x] Implement Registration, Login, and Logout views.
- [x] Secure routes with Django's login_required decorators.
- [x] Ensure datasets are isolated per user.
- [x] Remove redundant sidebar branding and add user personalization.

## 3. Storage and File Upload
- [x] Create UI for uploading CSV/Excel files (Bootstrap).
- [x] Implement endpoint in [dashboard](file:///f:/ReqSense/api/views.py#35-49) to receive, validate, and store uploaded files.
- [x] Process incoming files using Pandas (clean data, drop/fill nulls, normalize column names).
- [x] Store processed dataframe metadata (columns, dtypes, path to file) in Django DB via `Dataset` model.

## 4. AI Blueprint Generation
- [x] Extract 5-10 random rows and column definitions from the uploaded file.
- [x] Construct LLM prompt requesting a JSON blueprint for KPIs, aggregations, and charts.
- [x] Integrate with Google Generative AI to fetch the blueprint.
- [x] Validate and parse the returned JSON blueprint.

## 5. Blueprint Execution & Dashboard Rendering
- [x] Parse JSON blueprint to apply Pandas groupby, filters, and aggregations on the full dataset.
- [x] Return structured chart-ready data and top-level KPI metrics via `api` endpoints.
- [x] Build a frontend dashboard using Chart.js to render the metrics and charts automatically.

## 6. Natural Language Query (Chat Interface)
- [x] Build a chat UI wrapper.
- [x] Route user query + schema to AI API to generate JSON query logic.
- [x] Safely execute the generated query on the dataset utilizing Pandas.
- [x] Return textual response or mini-chart to the frontend.

## 7. Additional Modules (Insights & Anomalies)
- [x] Implement basic statistical anomaly detection (e.g., z-score) on numeric columns.
- [x] Generate automated text insights utilizing the AI API given basic dataset stats.
- [x] Display Insights & Anomalies on the dashboard.

## 8. Export Module
- [x] Implement endpoint to generate a PDF report of the dashboard KPIs & Insights.
- [x] Allow downloading the PDF on the frontend.
- [x] **Phase 10: Version Control & Handoff**
    - [x] Initialize Git repository and [.gitignore](file:///f:/ReqSense/.gitignore).
    - [x] Push production codebase to GitHub at `https://github.com/rajeshr464/ReqSense.git`.
    - [x] Resolve CSRF 403 Forbidden errors for ngrok tunneling.
- [x] **Phase 5: Aesthetic Overhaul & Dynamic UI**
    - [x] Integrate Soft UI Dashboard Tailwind architecture over old Bootstrap.
    - [x] Redesign Dataset Overview JSON parser to feature User-Friendly Labels.
    - [x] Implement AI Chat enhancements and format generation natively into HTML.
    - [x] Engineer a magnificent public SaaS Landing Page replicating `Landing.tsx`.

- [ ] **Phase 6: Cognitive Architect Multi-Page Overhaul**
    - [x] Remodel Authentication (Login/Register) using localized Templates.
    - [x] Construct centralized [base_dashboard.html](file:///f:/ReqSense/templates/dashboard/base_dashboard.html) with persistent NavBar/SideBar.
    - [x] Refactor Data Management Endpoint (Dataset Index + Dropzone).
    - [x] Refactor Intelligence Overview Endpoint (KPIs + Insights).
    - [x] Pioneer dedicated AI Query Terminal Route (`/chat/`).
    - [x] Pioneer dedicated Intelligence Reports Route (`/reports/`).

- [x] **Phase 8: Cerebras LLM Migration & Chat Visualizations**
    - [x] Install `cerebras_cloud_sdk` and rebuild [ai_service.py](file:///f:/ReqSense/api/services/ai_service.py) around `gpt-oss-120b`.
    - [x] Revise prompt engineering payload to allow conversational charting via JSON hidden blocks.
    - [x] Upgrade JavaScript terminal parser in [chat.html](file:///f:/ReqSense/templates/dashboard/chat.html) to instantiate Chart.js canvases locally inside text bubbles.
    - [x] Solidify Report and Table markdown generation capabilities.

- [x] **Phase 9: Global Aesthetic Synchronization**
    - [x] Refactor [base_dashboard.html](file:///f:/ReqSense/templates/dashboard/base_dashboard.html) to use a Light theme with Open Sans and Purple/Pink gradients.
    - [x] Update Dashboard Hub ([index.html](file:///f:/ReqSense/templates/dashboard/index.html)) styling for light mode consistency.
    - [x] Synchronize AI Query Terminal ([chat.html](file:///f:/ReqSense/templates/dashboard/chat.html)) bubbles and layout colors.
    - [x] Standardize Report visuals ([reports.html](file:///f:/ReqSense/templates/dashboard/reports.html)) to match the new branding.
    - [x] Update landing page footer to mention ReqSense as a product of Reqsta.

- [x] **Phase 11: Prompt Engineering & Business Context**
    - [x] Refactor 'Dashboard Blueprint Generation' prompt (Business Relevance & Reason).
    - [x] Refactor 'Natural Language Query' prompt.
    - [x] Refactor 'Executive Intelligence Report' prompt.
    - [x] Refactor 'Insights & Anomalies' prompt.

- [x] **Phase 12: Visual Enhancements (Vanta.js)**
    - [x] Integrate Vanta.js Network animation into [login.html](file:///f:/ReqSense/templates/accounts/login.html).
    - [x] Integrate Vanta.js Network animation into [register.html](file:///f:/ReqSense/templates/accounts/register.html).
    - [x] Integrate Vanta.js Network animation into [forgot_password.html](file:///f:/ReqSense/templates/accounts/forgot_password.html).
    - [x] Integrate Vanta.js Birds animation into [landing.html](file:///f:/ReqSense/templates/dashboard/landing.html).

