import os
import json
from cerebras.cloud.sdk import Cerebras

def query_cerebras(prompt):
    api_key = os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        raise ValueError("CEREBRAS_API_KEY not found in environment variables. Please add it to your .env file.")
        
    client = Cerebras(api_key=api_key)
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are ReqSense Cognitive Architect, an elite data analysis AI."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3.1-8b",
        stream=False,
        max_completion_tokens=4096,
        temperature=0.2,
        top_p=1,
    )
    
    import re
    content = response.choices[0].message.content.strip()
    
    # Locate code blocks
    match = re.search(r'```(?:json)?\s*([\s\S]*?)```', content)
    if match:
        content = match.group(1).strip()
    else:
        # Fallback to pure bracket isolation
        first_curly = content.find('{')
        last_curly = content.rfind('}')
        first_square = content.find('[')
        last_square = content.rfind(']')
        
        # Determine whether it's an object or an array
        if first_curly != -1 and last_curly != -1 and (first_square == -1 or first_curly < first_square):
            content = content[first_curly:last_curly+1]
        elif first_square != -1 and last_square != -1:
            content = content[first_square:last_square+1]
        
    return json.loads(content.strip())

def generate_dashboard_blueprint(dataset_info, sample_data_json):
    prompt = f"""
    You are an AI data analyst expert. Analyze the following dataset metadata and sample data. Generate a **JSON blueprint** defining **relevant KPIs, aggregations, and chart configurations** for an initial dashboard. 

    Requirements:
    1. Select KPIs that provide **immediate insight into business performance**.
    2. For each KPI, specify:
       - metric: the column name
       - aggregation: type (sum, average, count, etc.)
       - business_relevance: why this KPI matters in layman terms
    3. For each chart, specify:
       - type: (bar, line, pie, etc.)
       - x_axis: the groupby column
       - y_axis: the metric column
       - reason: why this chart effectively visualizes the data in layman terms
    
    Dataset Columns and Types:
    {dataset_info}
    
    Sample Data (first 5 rows):
    {sample_data_json}

    Only return **a valid JSON object** with this structure:
    {{
      "kpis": [
        {{"metric": "...", "aggregation": "...", "business_relevance": "..."}},
        ...
      ],
      "charts": [
        {{"type": "...", "x_axis": "...", "y_axis": "...", "reason": "..."}},
        ...
      ]
    }}

    **Tone:** Layman, non-technical business terms. Explain choices clearly so a non-technical manager can understand why each KPI and chart is included.
    Do not include markdown blocks, just the raw JSON.
    """
    return query_cerebras(prompt)

def process_natural_language_query(query, dataset_info, history=[]):
    history_str = ""
    for msg in history[-4:]:
        role = "User" if msg.get("role") == "user" else "ReqSense Architect"
        history_str += f"{role}: {msg.get('content')}\n"
        
    prompt = f"""
    You are an AI data query generator interacting with a user.
    Dataset Columns and Types:
    {dataset_info}
    
    Previous Conversation Context:
    {history_str}
    
    Current User Text: "{query}"
    
    You must output a single JSON object. Choose ONE of two modes:
    
    MODE 1 (Math Operation):
    - The user explicitly requests a calculation (e.g., sum, average, count). 
    - Perform the calculation **only on numeric columns**.
    - If the column is non-numeric, return a JSON with a "chat_response" explaining clearly that the operation cannot be performed.
    - Fields: "operation", "metric_column", "aggregation_function", "groupby_column" (optional), "filter_column" (optional), etc.

    MODE 2 (Conversation):
    - Return a JSON object with the following keys:
    {{
      "chat_response": "...",     // plain-language, executive-friendly answer
      "html_table": "..."         // fully styled HTML table (optional, only if relevant)
    }}

    When generating HTML tables:
    1. Include **column headers** in plain-language terms.
    2. For numeric columns:
       - Include rows for: **Lowest, Highest, Average (Typical), Median, % of Total / Max**.
       - Add a **Contextual Insight** column that explains in plain language what the numbers indicate.
    3. For categorical columns:
       - Include **top 5 most frequent values**, with counts and percentages.
       - Include a **plain-language insight** explaining why these values are significant.

    Additional Rules:
    - Always **explain why you chose the data points** in a detailed text paragraph within "chat_response".
    - Avoid technical jargon: write in **simple, layman, non-technical business terms**.
    - Never assume any specific industry or dataset structure.
    - Handle missing or non-numeric values gracefully.
    - Keep HTML valid and clean for rendering in the app. Use standard <table>, <thead>, <tbody>, <tr>, <th>, <td> tags.

    CRITICAL INSTRUCTION: You MUST generate a novel, intelligent response based on the "Current User Text".
    
    Return ONLY pure JSON. Do not include markdown blocks like ```json.
    """
    return query_cerebras(prompt)

def generate_executive_report(dataset_name, kpis_json, anomalies_json):
    prompt = f"""
    You are an elite enterprise Data Analyst. Write a **two-paragraph Executive Intelligence Report** based on the dataset "{dataset_name}", summarizing:

    1. Dataset Health
    - Missing values, inconsistencies, duplicates
    - Any notable data quality issues

    2. Trends & Outliers
    - Key patterns or clusters in numeric and categorical columns
    - Extreme or anomalous values
    - Highlight percentages, averages, or ranges in layman terms

    Computed Key Performance Indicators (JSON):
    {kpis_json}
    
    Detected Statistical Anomalies (JSON):
    {anomalies_json}

    Requirements:
    - Use **plain business language**, avoiding jargon
    - Include **contextual interpretation** of numbers (e.g., what high/low values indicate)
    - Do **not use Markdown formatting**, hashtags, or asterisks
    - Keep it concise, readable, and executive-friendly
    - Do not return JSON, just the raw text of the report.
    """
    try:
        api_key = os.environ.get("CEREBRAS_API_KEY")
        client = Cerebras(api_key=api_key)
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional business intelligence writer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3.1-8b",
            stream=False,
            max_completion_tokens=1000,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Warning: Cognitive Architect failed to generate the executive report sequence. (Exception: {str(e)})"
