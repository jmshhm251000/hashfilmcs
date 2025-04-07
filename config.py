import os
from dotenv import load_dotenv
load_dotenv()
DOCUMENT_ID = os.getenv('DOCUMENT_ID')
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']