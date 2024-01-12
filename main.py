
from typing import Dict, List
from utils import query
from modal import Image, Stub, web_endpoint
from urllib.parse import quote

image = Image.debian_slim().pip_install("pandas").pip_install().copy_local_file("preprocessed.csv")
stub = Stub("cal-admissions-api", image=image)

# For development: python3 -m modal serve main.py
# For production: python3 -m modal deploy main.py

@stub.function()
@web_endpoint(method="POST")
def query_endpoint(data: Dict):
    return quote(query(cols=data['columns'], filters=data['filters']).to_csv())

# gcloud functions deploy api --runtime python38 --trigger-http --allow-unauthenticated
# def api(request):
#     """HTTP Cloud Function.
#     Args:
#         request (flask.Request): The request object.
#         <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
#     Returns:
#         The response text, or any set of values that can be turned into a
#         Response object using `make_response`
#         <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
#     """
#     request_json = request.get_json(silent=True)

#     if request_json and 'columns' in request_json and 'filters' in request_json:
#         columns, filters = request_json['columns'], request_json['filters']
#         try:
#             return escape(query(columns, filters).to_csv())
#         except Exception as e:
#             return 'error:' + str(e)
#     else:
#         return escape('error: missing parameters')
