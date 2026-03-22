# ReqSense: AI-Powered Cognitive Data Architect

ReqSense is an advanced, AI-driven data intelligence platform that transforms raw datasets into actionable business insights. Built on a modern Django stack with Cerebras LLM integration, it provides an elite analytics experience featuring automated dashboard generation, natural language querying, and executive-level reporting.

## 🚀 Key Features

- **AI-Managed Dashboarding**: Automatically metabolizes uploaded CSV/Excel files to generate dynamic, business-relevant KPIs and visualizations.
- **Cognitive Query Terminal**: A natural language interface that allows users to converse with their data using conversational charting.
- **Executive Intelligence Reports**: Automated generation of elite-level summary reports in PDF format.
- **Vanta.js Visual Extensions**: Premium UI with interactive network and motion animations for a state-of-the-art user experience.
- **Secure Data Isolation**: Multi-tenant architecture ensuring complete data privacy and user-level dataset segregation.

## 🛠️ Technology Stack

- **Backend**: Django 6.1 (Python 3.12+)
- **AI Engine**: Cerebras Cloud SDK (`gpt-oss-120b`)
- **Frontend**: Tailwind CSS + Soft UI Architecture
- **Animations**: Vanta.js & Three.js
- **Data Execution**: Pandas & NumPy
- **Database**: PostgreSQL (Production) / SQLite (Local)
- **Storage**: Supabase Storage / Local FileSystem

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rajeshr464/ReqSense.git
   cd ReqSense
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Unix/macOS
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   Create a `.env` file in the root directory and add the following keys:
   ```env
   CEREBRAS_API_KEY=your_key_here
   DATABASE_URL=your_postgres_url  # Optional for local SQLite
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   USE_SUPABASE_STORAGE=True
   DEBUG=True
   SECRET_KEY=your_django_secret_key
   ```

5. **Run Migrations**:
   ```bash
   python py manage.py migrate
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

## 📄 License
ReqSense is a product of **Reqsta**. All rights reserved.
