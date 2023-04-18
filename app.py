import re
from datetime import datetime
from utils import db,timestamp_matching,readme_text
import markdown
from flask import Flask, jsonify,request,abort,render_template

app = Flask(__name__)

@app.route('/')
def home():
    readme_html = markdown.markdown(
        readme_text
    )
    # Render the documentation template with the README HTML
    return render_template('documentation.html', readme_html=readme_html)

@app.route('/documents')
def get_documents():
    # Return a list of available document titles
    titles = list(db.keys())
    return jsonify(titles)

# Define the endpoint for returning a list of available revisions for a specific document
@app.route('/documents/<string:title>')
def get_document_revisions(title:str):
    # Return a list of available revisions for a specific document
    if title in db:
        revisions = db[title]["revisions"]
        return jsonify(revisions)
    else:
        abort(404,"Document not Found")

@app.route('/documents/<string:title>/<string:timestamp>')
def get_document_at_timestamp(title:str, timestamp:str):
    if title in db:
        # check that the timestamp is in the correct format
        if not timestamp_matching(timestamp):
            return abort(400 ,'Invalid Timestamp Format')

        revisions = db[title]['revisions']
        closest_revision = None
        for revision in sorted(revisions, key=lambda x: x["timestamp"], reverse=True):
            if revision['timestamp'] <= timestamp:
                closest_revision = revision
                break
        if closest_revision:
            #return jsonify({'content': closest_revision['content'], 'timestamp': closest_revision['timestamp']})
            return jsonify(closest_revision['content'])
        else:
            return abort(404, "No Revision found for this Timestamp")
    else:
        return abort(404, "Document not Found")

# Define the endpoint for returning the latest version of the document
@app.route('/documents/<string:title>/latest')
def get_latest_document_revision(title:str):
    # Return the latest version of the document with the given title
     if title in db:
         revisions = db[title]["revisions"]
         # Sorting based on timestamp
         latest_revision = sorted(revisions, key=lambda x: x["timestamp"])[-1]['content']
         return jsonify(latest_revision)
     else:
         abort(404, "Document not Found")


@app.route('/documents/<string:title>', methods=['POST'])
def post_new_revision(title:str):
    # Check if the document exists and retrieve its revisions
    if title not in db:
        return abort(404, "Document not Found")

    # Retrieve the new content from the request JSON
    new_content = request.json.get('content')
    if not new_content:
        return abort(400, "No Content Provided")

    # Create a new revision object with the current timestamp
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'

    new_revision = {'content': new_content, 'timestamp': timestamp}

    # Append the new revision to the document's revisions
    db[title]['revisions'].append(new_revision)

    # Return the new revision object
    return jsonify(new_revision)

