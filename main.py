from flask import escape, jsonify
from utils import query

# gcloud functions deploy api --runtime python38 --trigger-http --allow-unauthenticated
def api(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)

    if request_json and 'columns' in request_json and 'filters' in request_json:
        columns, filters = request_json['columns'], request_json['filters']
        return escape(query(columns, filters).to_csv())
    else:
        return escape('error')