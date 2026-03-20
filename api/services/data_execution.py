import pandas as pd
import json

def execute_blueprint(df, blueprint):
    results = {"kpis": {}, "charts": {}}
    
    # Execute KPIs
    for kpi in blueprint.get("kpis", []):
        try:
            col = kpi.get("column")
            op = kpi.get("operation")
            name = kpi.get("name", "Metric")
            if col and col in df.columns:
                if op == "sum": val = df[col].sum()
                elif op in ["avg", "mean"]: val = df[col].mean()
                elif op == "count": val = df[col].count()
                elif op == "max": val = df[col].max()
                elif op == "min": val = df[col].min()
                else: val = 0
                results["kpis"][name] = float(val) if pd.notnull(val) else 0
        except Exception:
            pass
            
    # Execute Charts
    for i, chart in enumerate(blueprint.get("charts", [])):
        try:
            chart_type = chart.get("type", "bar")
            groupby_col = chart.get("groupby")
            metric_col = chart.get("metric")
            agg = chart.get("aggregation", "sum")
            title = chart.get("title", f"Chart {i+1}")
            
            if groupby_col in df.columns and metric_col in df.columns:
                grouped = df.groupby(groupby_col)[metric_col]
                if agg == "sum": agg_df = grouped.sum()
                elif agg in ["mean", "avg"]: agg_df = grouped.mean()
                elif agg == "count": agg_df = grouped.count()
                else: agg_df = grouped.sum()
                    
                agg_df = agg_df.sort_values(ascending=False).head(20)
                
                results["charts"][f"chart_{i}"] = {
                    "title": title,
                    "type": chart_type,
                    "labels": [str(idx) for idx in agg_df.index],
                    "values": [float(val) if pd.notnull(val) else 0 for val in agg_df.values]
                }
        except Exception:
            pass
            
    return results
