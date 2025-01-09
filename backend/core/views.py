import pandas as pd
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Document
from .serializers import DocumentSerializer

# Hugging Face API URL
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/google/tapas-large-finetuned-wtq"
API_TOKEN = "token"

# Helper function to call Hugging Face API
def query_huggingface_api(question, table):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    payload = {
        "inputs": {
             "question": "What is the age of Alice?",
    "table": 
      {"Name": "Alice", "Age": 25, "Score": 85},
      
    
        }
    }
    print("Payload:", payload)
    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
    print("Response:", response)  # Debug response
    return response.json()

# Document Upload View
class DocumentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = DocumentSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            file = request.FILES['file']
            data = pd.read_excel(file)
            data.columns = data.columns.astype(str)  # Ensure column names are strings
            data = data.fillna("") 
            print(data.head())

            # Convert the DataFrame to a list of dictionaries
            global dp
            dp = data.to_dict(orient='records')
            print(dp[:5])
            request.session.modified = True
            return Response({"message": "File uploaded successfully!"})
        else:
            return Response(file_serializer.errors)
# Query View
class QueryView(APIView):
    def post(self, request):
        question = request.data.get("query")
        table = dp  # Pass the parsed data directly

        # Call Hugging Face API
        result = query_huggingface_api(question=question, table=table)
        print(result)

        # Return the answer
        answer = result.get("answer", "No answer")
        return Response({"answer": answer})
