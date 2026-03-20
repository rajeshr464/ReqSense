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
    You are an AI data analyst expert. Based on the following dataset metadata and sample data, generate a JSON blueprint defining relevant KPIs, aggregations, and chart configurations.
    
    Dataset Columns and Types:
    {dataset_info}
    
    Sample Data (first 5 rows):
    {sample_data_json}
    
    Return ONLY a valid JSON object with the following structure:
    {{
        "kpis": [
            {{"name": "Total Revenue", "operation": "sum", "column": "revenue_col"}}
        ],
        "charts": [
            {{
                "title": "Revenue by Category",
                "type": "bar",
                "groupby": "category_col",
                "metric": "revenue_col",
                "aggregation": "sum"
            }}
        ]
    }}
    
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
    
    MODE 1 (Math Operation): The user explicitly requested to calculate a number, sum, average, or group the data.
    Allowed operations: 
    - "groupby_agg": requires "groupby_column", "metric_column", "aggregation_function"
    - "filter_agg": requires "filter_column", "filter_operator", "filter_value", "metric_column", "aggregation_function"
    MODE 2 (Conversation or Data Views): The user said hello, asked a general question, or asked for a visual/report based on previous context.
    Return a single JSON with a "chat_response" key.
    - "chat_response": Your HTML reply. NEVER attempt to generate charts or plugins. 
    - VERY IMPORTANT: If the user asks for data points, tables, or validation, you MUST generate beautifully styled HTML `<table>` elements PLUS a detailed text paragraph explicitly explaining *why* you chose those specific data points to validate your methodology!
    - TONE DIRECTIVE: You MUST write your explanations and validation summaries in simple, layman, non-technical business terms. AVOID heavy statistical jargon (do not say "standard deviation", "variance", etc). Explain the data simply like you are talking to a non-technical manager. 
    - If the user just says "hi", say hello concisely! DO NOT OVEREXPLAIN.
    
    CRITICAL INSTRUCTION: You MUST generate a novel, intelligent response based on the "Current User Text".
    
    Structure Example A (Greeting or Question):
    User Text: [Any conversational question]
    {{"chat_response": "[A highly focused, concise HTML response.]"}}
    
    Structure Example B (Math Request):
    User Text: "What is the total revenue?"
    {{"operation": "metric", "metric_column": "revenue", "aggregation_function": "sum"}}
    
    Structure Example C (Visual or Table Request):
    User Text: [A request to draw a chart, validate with data, or show proof]
    {{"chat_response": "Here is the data distribution you requested: <br><br><table><thead><tr><th>User</th>...</tr></thead><tbody>...</tbody></table><br><b>Validation Summary:</b> I selected these specific rows because..."}}

    
    Return ONLY pure JSON. Do not include markdown blocks like ```json.
    """
    return query_cerebras(prompt)

def generate_executive_report(dataset_name, kpis_json, anomalies_json):
    prompt = f"""
    You are an elite enterprise Data Analyst writing a formal executive summary.
    Dataset Name: "{dataset_name}"
    
    Computed Key Performance Indicators (JSON):
    {kpis_json}
    
    Detected Statistical Anomalies (JSON):
    {anomalies_json}
    
    Write a cohesive, 2-paragraph "Executive Intelligence Report" summarizing the health, trends, and outliers of this dataset.
    DO NOT use Markdown asterisks or hashtags. JUST plain text. If you want to separate paragraphs, just use a double newline.
    Do not return JSON, just the raw text of the report.
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
