import unittest
import json
from app import app, db

class DocTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        # Clean up the database after each test
        db.clear()

    def test_get_documents(self):
        # Test the GET /documents endpoint
        response = self.app.get('/documents')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(data, [])

    def test_get_document_revisions(self):
        # Test the GET /documents/<string:title> endpoint
        db["test_title"] = {"revisions": [{"content": "Old content", "timestamp": "2022-04-18T00:00:00.000000"}]}
        response = self.app.get('/documents/test_title')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(data, [{"content": "Old content", "timestamp": "2022-04-18T00:00:00.000000"}])

    def test_get_document_at_timestamp(self):
        # Test the GET /documents/<string:title>/<string:timestamp> endpoint
        db["test_title"] = {"revisions": [{"content": "Old content", "timestamp": "2022-04-18T00:00:00Z"}]}
        timestamp = "2022-04-18T00:00:00Z"
        response = self.app.get(f'/documents/test_title/{timestamp}')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "Old content")

    def test_get_latest_document_revision(self):
        # Test the GET /documents/<string:title>/latest endpoint
        db["test_title"] = {"revisions": [{"content": "First Revision", "timestamp": "2022-04-17T00:00:00Z"}]}
        latest_content = {"content": "New Revision", "timestamp": "2022-04-18T00:00:00Z"}
        db["test_title"]["revisions"].append(latest_content)
        response = self.app.get('/documents/test_title/latest')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, latest_content["content"])

    def test_post_new_revision(self):
        # Test the POST /documents/<string:title> endpoint
        db["test_title"] = {"revisions": []}
        new_content = {"content": "Test content"}
        response = self.app.post('/documents/test_title', json=new_content)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(data.items())[0], list(new_content.items())[0])

    # Testing Error Handling

    def test_get_documentation(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_get_document_revisions(self):
        response = self.app.get(f"/documents/unknown")
        self.assertEqual(response.status_code, 404)

    def test_get_document_at_timestamp_400(self):
        db["test_title"] = {"revisions": [{"content": "First Revision", "timestamp": "2022-04-17T00:00:00Z"}]}
        response = self.app.get("/documents/test_title/invalid-timestamp")
        self.assertEqual(response.status_code, 400)

    def test_get_document_at_timestamp_404(self):
        response = self.app.get("/documents/unknown/timestamp")
        self.assertEqual(response.status_code, 404)


    def test_get_latest_document_revision(self):
        response = self.app.get("/documents/unknown/latest")
        self.assertEqual(response.status_code, 404)

    def test_post_new_revision_400(self):
        db["test_title"] = {"revisions": [{"content": "First Revision", "timestamp": "2022-04-17T00:00:00Z"}]}
        response = self.app.post('/documents/test_title',json={})
        self.assertEqual(response.status_code, 400)

    def test_post_new_revision_404(self):
        response = self.app.post("/documents/unknown", json={"content": "New Content"})
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
