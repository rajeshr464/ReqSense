import pandas as pd
import os
import json

def process_and_save_dataset(file_obj, user_id, base_media_path):
    ext = file_obj.name.split('.')[-1].lower()
    
    if ext == 'csv':
        df = pd.read_csv(file_obj)
    elif ext in ['xls', 'xlsx']:
        df = pd.read_excel(file_obj)
    else:
        raise ValueError("Unsupported file format. Please upload CSV or Excel.")
    
    # Drop rows where everything is missing
    df = df.dropna(how='all')
    
    # If the file had blank rows at the top, pandas names columns "Unnamed: X".
    # If most columns are "Unnamed", the actual header is probably the first row of data.
    unnamed_count = sum(1 for col in df.columns if str(col).lower().startswith('unnamed'))
    if len(df.columns) > 0 and unnamed_count > len(df.columns) / 2:
        if not df.empty:
            # Set the first meaningful row as the header
            new_header = df.iloc[0]
            df = df[1:]
            df.columns = new_header
            df.reset_index(drop=True, inplace=True)
            
    # Drop columns where everything is missing

    df = df.dropna(axis=1, how='all')
    df.columns = [str(col).strip().lower().replace(' ', '_').replace('-', '_') for col in df.columns]
    
    user_dir = os.path.join(base_media_path, 'datasets', str(user_id))
    os.makedirs(user_dir, exist_ok=True)
    
    clean_filename = file_obj.name.replace(' ', '_')
    if not clean_filename.endswith('.csv'):
        clean_filename += '.csv'
        
    save_path = os.path.join(user_dir, f"cleaned_{clean_filename}")
    df.to_csv(save_path, index=False)
    
    columns_info = [{"name": col, "type": str(dtype)} for col, dtype in df.dtypes.items()]
    
    return {
        "file_path": save_path,
        "columns_json": json.dumps(columns_info),
        "num_rows": len(df)
    }
