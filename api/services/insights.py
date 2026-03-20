import pandas as pd
import json
from .ai_service import query_cerebras

def generate_insights_and_anomalies(df_path):
    df = pd.read_csv(df_path)
    
    anomalies = {}
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        mean = df[col].mean()
        std = df[col].std()
        if std and std > 0:
            z_scores = (df[col].dropna() - mean) / std
            outliers = df.loc[df[col].dropna().index][abs(z_scores) > 3]
            if not outliers.empty:
                anomalies[col] = len(outliers)
                
    describe_json = df.describe().to_json()
    
    prompt = f"""
    You are an AI data analyst expert. Analyze the statistical description and detected anomalies (z-score > 3) to generate **3 key business or data-quality insights**.

    Input:
    - Statistical Description JSON: {describe_json}
    - Anomalies List: {json.dumps(anomalies)}

    Requirements:
    1. Provide **plain-language insights** suitable for business managers.
    2. Explain **why each insight matters**, e.g., impact on operations, trends, or decisions.
    3. Focus on **actionable or interpretable observations**, not just numbers.
    4. Return ONLY a valid JSON array of 3 strings:
    [
      "Insight 1 explanation in plain business terms",
      "Insight 2 explanation in plain business terms",
      "Insight 3 explanation in plain business terms"
    ]
    5. Include **contextual reference** to the column or anomaly that led to the insight.
    """
    
    try:
        insights_list = query_cerebras(prompt)
    except Exception as e:
        import logging
        logging.error(f"Cerebras Insights Error: {e}", exc_info=True)
        insights_list = ["Could not parse Cerebras AI insights."]
        
    return {
        "anomalies": anomalies,
        "insights": insights_list
    }
