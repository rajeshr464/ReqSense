from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .forms import UploadFileForm
from .models import Dataset
from api.services.data_processor import process_and_save_dataset

def landing(request):
    """Public landing page"""
    return render(request, 'dashboard/landing.html')

@login_required
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            dataset_name = form.cleaned_data['dataset_name']
            uploaded_file = request.FILES['file']
            
            try:
                result = process_and_save_dataset(uploaded_file, request.user.id, settings.MEDIA_ROOT)
                
                dataset = Dataset.objects.create(
                    user=request.user,
                    name=dataset_name,
                    file_path=result['file_path'],
                    columns_json=result['columns_json'],
                    num_rows=result['num_rows']
                )
                messages.success(request, f'Dataset "{dataset.name}" uploaded successfully.')
                return redirect('dashboard:view', pk=dataset.pk)
            except Exception as e:
                import logging
                logging.error(f"Dataset Processing Error: {e}", exc_info=True)
                messages.error(request, f'Error processing file: {str(e)}')
    else:
        form = UploadFileForm()
        
    datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'dashboard/index.html', {'form': form, 'datasets': datasets})

import json

@login_required
def view_dataset(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk, user=request.user)
    try:
        raw_columns = json.loads(dataset.columns_json)
        columns_list = []
        for col in raw_columns:
            # Human readable names: 'project_name' -> 'Project Name'
            r_name = col['name'].replace('_', ' ').title()
            ctype = col['type'].lower()
            if 'object' in ctype or 'str' in ctype:
                htype = 'Text'
            elif 'datetime' in ctype:
                htype = 'Date/Time'
            elif 'int' in ctype or 'float' in ctype:
                htype = 'Number'
            else:
                htype = col['type']
            columns_list.append({"name": r_name, "type": htype, "raw_name": col['name']})
    except:
        columns_list = []
    return render(request, 'dashboard/view.html', {'dataset': dataset, 'columns_list': columns_list})

@login_required
def chat_terminal(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk, user=request.user)
    return render(request, 'dashboard/chat.html', {'dataset': dataset})

@login_required
def reports_view(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk, user=request.user)
    return render(request, 'dashboard/reports.html', {'dataset': dataset})

@login_required
def delete_dataset(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk, user=request.user)
    if request.method == 'POST':
        dataset.delete()
        messages.success(request, f'Dataset "{dataset.name}" deleted successfully.')
    return redirect('dashboard:index')
