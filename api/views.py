from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from dashboard.models import Dataset
from .services.ai_service import generate_dashboard_blueprint, process_natural_language_query
from .services.data_execution import execute_blueprint
import pandas as pd
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_blueprint(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id, user=request.user)
    
    if dataset.blueprint_json and not request.data.get('force_regenerate'):
        return Response(json.loads(dataset.blueprint_json))
        
    try:
        df = pd.read_csv(dataset.file_path, nrows=10)
        sample_data = df.to_json(orient="records")
    except Exception as e:
        return Response({"error": str(e)}, status=400)
        
    try:
        blueprint = generate_dashboard_blueprint(dataset.columns_json, sample_data)
        dataset.blueprint_json = json.dumps(blueprint)
        dataset.save()
        return Response(blueprint)
    except Exception as e:
        import logging
        logging.error(f"Blueprint Error: {e}", exc_info=True)
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_data(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id, user=request.user)
    if not dataset.blueprint_json:
        return Response({"error": "No blueprint generated yet."}, status=400)
        
    try:
        df = pd.read_csv(dataset.file_path)
        blueprint = json.loads(dataset.blueprint_json)
        results = execute_blueprint(df, blueprint)
        return Response({"blueprint": blueprint, "data": results})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_query(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id, user=request.user)
    query = request.data.get('query')
    history = request.data.get('history', [])
    if not query:
        return Response({"error": "No query provided"}, status=400)
        
    try:
        json_query = process_natural_language_query(query, dataset.columns_json, history)
        
        # Intercept conversational responses before hitting the dataframe processor
        if "chat_response" in json_query:
            answer = json_query.get("chat_response", "")
            table = json_query.get("html_table", "")
            
            # Combine the narrative and the table if both exist
            full_content = answer
            if table:
                full_content += f"<div class='mt-6 overflow-x-auto'>{table}</div>"
                
            return Response({"answer": full_content, "query_logic": json_query})
            
        df = pd.read_csv(dataset.file_path)
        op = json_query.get("operation")
        
        result_text = ""
        if op == "groupby_agg":
            grp = json_query.get("groupby_column")
            metric = json_query.get("metric_column")
            agg = json_query.get("aggregation_function", "sum")
            
            if grp in df.columns and metric in df.columns:
                agg_df = getattr(df.groupby(grp)[metric], agg)()
                agg_df = agg_df.sort_values(ascending=False).head(10)
                res_list = [f"{idx}: {val:.2f}" for idx, val in agg_df.items()]
                result_text = f"**Top 10 {grp} by {agg} of {metric}**:\n<br>" + "<br>".join(res_list)
            else:
                result_text = "Columns specified in query could not be found."
                
        elif op == "filter_agg":
            filt_col = json_query.get("filter_column")
            filt_val = json_query.get("filter_value")
            metric = json_query.get("metric_column")
            agg = json_query.get("aggregation_function", "sum")
            
            if filt_col in df.columns and metric in df.columns:
                # Basic literal match filter
                filtered = df[df[filt_col].astype(str).str.contains(str(filt_val), case=False, na=False)]
                val = getattr(filtered[metric], agg)()
                result_text = f"The {agg} of {metric} where {filt_col} matches '{filt_val}' is {val:.2f}."
                
        elif op == "metric":
            metric = json_query.get("metric_column")
            agg = json_query.get("aggregation_function", "sum")
            
            if metric in df.columns:
                val = getattr(df[metric], agg)()
                result_text = f"The {agg} of {metric} is {val:.2f}."
                
        if not result_text:
            if not json_query or ("operation" not in json_query and "chat_response" not in json_query):
                result_text = f"Hello! I am your ReqSense Cognitive Architect. I have metabolized your dataset '{dataset.name}'. I can help you compute metrics, filter operations, and analyze underlying trends. How can I assist you with your data today?"
            else:
                result_text = f"I understood the numerical mapping but encountered a syntax exception against the live dataset.<br><br><span class='font-mono text-[10px] opacity-50'>{json.dumps(json_query)}</span>"
            
        return Response({"answer": result_text, "query_logic": json_query})
    except Exception as e:
        import logging
        logging.error(f"Chat Query Error: {e}", exc_info=True)
        return Response({"error": str(e)}, status=500)

from .services.insights import generate_insights_and_anomalies

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_insights(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id, user=request.user)
    try:
        res = generate_insights_and_anomalies(dataset.file_path)
        return Response(res)
    except Exception as e:
        import logging
        logging.error(f"Insights Error: {e}", exc_info=True)
        return Response({"error": str(e)}, status=500)

from django.http import FileResponse
from .services.export import generate_pdf_report

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_pdf(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id, user=request.user)
    
    data_results = {}
    if dataset.blueprint_json:
        try:
            df = pd.read_csv(dataset.file_path)
            blueprint = json.loads(dataset.blueprint_json)
            data_results = execute_blueprint(df, blueprint)
        except:
            pass
            
    insights_results = {}
    try:
         insights_results = generate_insights_and_anomalies(dataset.file_path)
    except:
         pass
         
    try:
        pdf_buffer = generate_pdf_report(dataset, data_results, insights_results)
        return FileResponse(pdf_buffer, as_attachment=True, filename=f"ReqSense_Report_{dataset.name}.pdf")
    except Exception as e:
        return Response({"error": f"Failed to generate PDF: {str(e)}"}, status=500)
