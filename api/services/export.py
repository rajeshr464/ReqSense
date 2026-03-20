from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
import json
from .ai_service import generate_executive_report

def generate_pdf_report(dataset, data_results, insights_results):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    Story = []
    
    Story.append(Paragraph(f"ReqSense AI Report: {dataset.name}", styles['Title']))
    Story.append(Spacer(1, 0.2*inch))
    
    Story.append(Paragraph("Dataset Overview", styles['Heading2']))
    Story.append(Paragraph(f"Total Rows: {dataset.num_rows}", styles['Normal']))
    Story.append(Paragraph(f"Uploaded At: {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    Story.append(Spacer(1, 0.2*inch))
    
    try:
        kpis_dump = json.dumps(data_results.get('kpis', {}))
        anom_dump = json.dumps(insights_results.get('anomalies', {}))
        exec_summary = generate_executive_report(dataset.name, kpis_dump, anom_dump)
        
        Story.append(Paragraph("Cognitive Architect Executive Summary", styles['Heading2']))
        for paragraph in exec_summary.split('\n\n'):
            if paragraph.strip():
                Story.append(Paragraph(paragraph.strip(), styles['Normal']))
                Story.append(Spacer(1, 0.1*inch))
        Story.append(Spacer(1, 0.2*inch))
    except Exception as e:
        pass
    
    if data_results and 'kpis' in data_results and data_results['kpis']:
        Story.append(Paragraph("Key Performance Indicators", styles['Heading2']))
        kpi_data = [["Metric Name", "Value"]]
        for k, v in data_results['kpis'].items():
            numVal = v if isinstance(v, (int, float)) else 0
            kpi_data.append([str(k), f"{numVal:,.2f}"])
        
        t = Table(kpi_data, style=[
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ])
        Story.append(t)
        Story.append(Spacer(1, 0.2*inch))
        
    if insights_results and 'insights' in insights_results:
        Story.append(Paragraph("AI Auto Insights", styles['Heading2']))
        for ins in insights_results['insights']:
            Story.append(Paragraph(f"• {ins}", styles['Normal']))
            Story.append(Spacer(1, 0.1*inch))
            
    if insights_results and 'anomalies' in insights_results and insights_results['anomalies']:
        Story.append(Spacer(1, 0.1*inch))
        Story.append(Paragraph("Potential Anomalies Detected", styles['Heading2']))
        for k, v in insights_results['anomalies'].items():
            Story.append(Paragraph(f"• {k}: {v} outliers (z-score > 3)", styles['Normal']))
            
    doc.build(Story)
    buffer.seek(0)
    return buffer
