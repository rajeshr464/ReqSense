import pandas as pd
import json

def execute_blueprint(df, blueprint):
    results = {"kpis": {}, "charts": {}}
    
    # Execute KPIs
    for kpi in blueprint.get("kpis", []):
        try:
            # New schema: metric / aggregation. Old fallback: column / operation
            col = kpi.get("metric") or kpi.get("column")
            op = kpi.get("aggregation") or kpi.get("operation")
            relevance = kpi.get("business_relevance", "")
            
            # Formulate a readable name for the KPI if not provided
            name = f"{op.title()} of {col}" if op and col else "Metric"
            
            if col and col in df.columns:
                if op in ["sum", "total"]: val = df[col].sum()
                elif op in ["avg", "mean", "average"]: val = df[col].mean()
                elif op == "count": val = df[col].count()
                elif op == "max": val = df[col].max()
                elif op == "min": val = df[col].min()
                else: val = 0
                
                results["kpis"][name] = {
                    "value": float(val) if pd.notnull(val) else 0,
                    "relevance": relevance
                }
        except Exception:
            pass
            
    # Execute Charts
    for i, chart in enumerate(blueprint.get("charts", [])):
        try:
            chart_type = chart.get("type", "bar")
            # New schema: x_axis / y_axis. Old fallback: groupby / metric
            groupby_col = chart.get("x_axis") or chart.get("groupby")
            metric_col = chart.get("y_axis") or chart.get("metric")
            agg = chart.get("aggregation") or chart.get("operation") or "sum"
            reason = chart.get("reason", "")
            
            # Formulate title
            title = f"{agg.title()} of {metric_col} by {groupby_col}" if groupby_col and metric_col else f"Chart {i+1}"
            
            if groupby_col in df.columns and metric_col in df.columns:
                grouped = df.groupby(groupby_col)[metric_col]
                if agg in ["sum", "total"]: agg_df = grouped.sum()
                elif agg in ["mean", "avg", "average"]: agg_df = grouped.mean()
                elif agg == "count": agg_df = grouped.count()
                else: agg_df = grouped.sum()
                    
                agg_df = agg_df.sort_values(ascending=False).head(20)
                
                results["charts"][f"chart_{i}"] = {
                    "title": title,
                    "type": chart_type,
                    "labels": [str(idx) for idx in agg_df.index],
                    "values": [float(val) if pd.notnull(val) else 0 for val in agg_df.values],
                    "reason": reason
                }
        except Exception:
            pass
            
    return results
