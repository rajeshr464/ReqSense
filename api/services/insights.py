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
    You are an AI data analyst expert. Analyze the statistical description and generate 3 key business or data quality insights.
    
    Statistical Description:
    {describe_json}
    
    Anomalies found (columns with rows where z-score > 3):
    {json.dumps(anomalies)}
    
    Return ONLY a valid JSON array of 3 strings.
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
