<em><h1>API Documentation</h1></em>

The API provides endpoints to perform basic CRUD operations on a document management system. 

<em>The API endpoints are as follows:</em>

<pre class="code-snippet"> 
GET /:
Returns the API Documentation.

GET /documents:
Returns a list of available document titles.

GET /documents/{title}:
Returns a list of available revisions for a specific document.

GET /documents/{title}/{timestamp}:
Returns the content of the document at the given timestamp.

GET /documents/{title}/latest:
Returns the latest revision of the document.

POST /documents/{title}:
Creates a new revision of the document.
</pre>


<em>Note: <b>`title`</b> and <b>`timestamp`</b> are placeholders for the actual values that need to be passed to the endpoint.</em>

<em><h2>Response Codes:</h2></em>

    200 OK: Successful request.
    201 Created: New resource created.
    400 Bad Request: Invalid request data.
    404 Not Found: Resource not found.


<h3> 1) GET / documents: </h3>

Returns a list of available document titles.

<h4>Request:</h4>

<pre class="code-snippet">GET /documents</pre>

<h4>Response:</h4>


<pre class="code-snippet">200 OK
Content-Type: application/json

[
    "title1",
    "title2",
    "title3",
    "title4",
    "title5"
]
</pre>

<h3>2) GET /documents/{title}:</h3>

Returns a list of available revisions for a specific document.

<h4>Request:</h4>

<pre class="code-snippet">GET /documents/title1</pre>

<h4>Response:</h4>

<pre class="code-snippet">200 OK
Content-Type: application/json

[
    {
        "content": "This is the first revision of document1.",
        "timestamp": "2022-03-01T12:00:00.000000"
    },
    {
        "content": "This is the second revision of document1.",
        "timestamp": "2022-03-02T12:00:00.000000"
    },
    {
        "content": "This is the third revision of document1.",
        "timestamp": "2022-03-03T12:00:00.000000"
    }
]
</pre>

<h3> 3) GET /documents/{title}/{timestamp}: </h3>

Returns the content of the document at the given timestamp.

<h4>Request:</h4>

<pre class="code-snippet">GET /documents/title1/2022-03-02T13:00:00.000000</pre>

<h4>Response:</h4>

<pre class="code-snippet">200 OK
Content-Type: application/json

"This is the second revision of document1."
</pre>

<h3>4) GET /documents/{title}/latest:</h3>

Returns the latest revision of the document.

<h4>Request:</h4>

<pre class="code-snippet">GET /documents/title1/latest</pre>

<h4>Response:</h4>

<pre class="code-snippet">200 OK
Content-Type: application/json

"This is the latest revision of document1."
</pre>

<h3>5) POST /documents/{title}:</h3>

Creates a new revision of the document.

<h4>Request:</h4>

<pre class="code-snippet">POST /documents/title1

Content-Type: application/json

{
    "content": "This is a new revision of document1."
}
</pre>
<h4>Response:</h4>

<pre class="code-snippet">
201 Created
Content-Type: application/json

{
    "content": "This is a new revision of document1.",
    "timestamp": "2022-03-04T12:00:00.000000"
}
</pre>

<em><h2>Possible Error Responses:</h2></em>

<h3>1) If the document does not exist:</h3>

<pre class="code-snippet">
404 Not Found
Content-Type: application/json

{
    "error": "Document not found."
}
</pre>

<h3>2) If the timestamp is in an invalid format:</h3>

<pre class="code-snippet">

400 Bad Request
Content-Type: application/json

{
    "error": "Invalid Timestamp Format."
}
</pre>
<h3>3) If no content is provided:</h3>
<pre class="code-snippet">
400 Bad Request
Content-Type: application/json

{
    "error": "No Content Provided."
}
</pre>

<h3>4) If no revision is found for the given timestamp:</h3>

<pre class="code-snippet">
404 Not Found
Content-Type: application/json

{
    "error": "No Revision Found for this Timestamp
</pre>