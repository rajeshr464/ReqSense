from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client, Client
import os
import io

class SupabaseStorage(Storage):
    def __init__(self, **kwargs):
        self.url = os.environ.get("SUPABASE_URL")
        self.key = os.environ.get("SUPABASE_KEY")
        self.bucket = os.environ.get("SUPABASE_STORAGE_BUCKET", "datasets")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables.")
            
        self.client: Client = create_client(self.url, self.key)

    def _open(self, name, mode='rb'):
        # Supabase returns the raw public URL or downloadable content.
        # For simplicity, we'll fetch the content and return a File-like object.
        res = self.client.storage.from_(self.bucket).download(name)
        return io.BytesIO(res)

    def _save(self, name, content):
        # Convert content to bytes if needed
        file_data = content.read()
        
        # Ensure name doesn't lead with slash
        clean_name = name.lstrip('/')
        
        # Upload
        # Upsert=True allows replacing if name matches
        self.client.storage.from_(self.bucket).upload(
            path=clean_name,
            file=file_data,
            file_options={"upsert": "true"}
        )
        return name

    def exists(self, name):
        # Supabase doesn't have a simple exists(), we check if we can get info
        try:
            res = self.client.storage.from_(self.bucket).list(os.path.dirname(name))
            basename = os.path.basename(name)
            return any(item['name'] == basename for item in res)
        except:
            return False

    def url(self, name):
        # Return the public URL
        # Note: bucket must be public or have policy
        res = self.client.storage.from_(self.bucket).get_public_url(name)
        return res

    def size(self, name):
        # Check details
        res = self.client.storage.from_(self.bucket).get_metadata(name)
        return res.get('size', 0)

    def delete(self, name):
        self.client.storage.from_(self.bucket).remove([name])
