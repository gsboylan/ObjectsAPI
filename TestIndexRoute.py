import sys
import unittest
from flask import json

import TestSuite

INDEX_ROUTE = '/api/objects/'

class TestIndexRoute(unittest.TestCase):

    def testGetEmptyStorage(self):
        TestSuite.setServerObjects({})
        expected = { "objects" : [] }

        response = TestSuite.client.get(INDEX_ROUTE)

        self.assertEquals(json.loads(response.data), expected)

    def testGetSingleObject(self):
        TestSuite.setServerObjects({"uid00112233": {"FieldOne" : "One", "Field2" : 2, "uid" : "uid00112233"}})
        expected = { "objects" : [{"url" : "http://localhost/api/objects/uid00112233"}] }

        response = TestSuite.client.get(INDEX_ROUTE)

        self.assertEquals(json.loads(response.data), expected)

    def testGetMultipleObjects(self):
        TestSuite.setServerObjects({
            "uid00112233": {"FieldOne" : "One", "Field2" : 2, "uid" : "uid00112233"},
            "uid44556677": {"FieldOne" : "One", "Field2" : 2, "uid" : "uid44556677"}})
        expected = { "objects" : [{"url" : "http://localhost/api/objects/uid00112233"},
                                  {"url" : "http://localhost/api/objects/uid44556677"}] }

        response = TestSuite.client.get(INDEX_ROUTE)

        self.assertEquals(json.loads(response.data), expected)

    def testPostEmptyRequest(self):
        TestSuite.setServerObjects({});

        expected = {
              "message": "400: Bad Request",
              "url": "http://localhost/api/objects/",
              "verb": "POST"
            }

        response = TestSuite.client.post(INDEX_ROUTE, content_type = 'application/json')

        self.assertEquals(json.loads(response.data), expected)

    def testPostBrokenJSON(self):
        TestSuite.setServerObjects({})

        expected = {
              "message": "400: Bad Request",
              "url": "http://localhost/api/objects/",
              "verb": "POST"
            }

        response = TestSuite.client.post(INDEX_ROUTE,
            data = '{ "field1" : "brokendata }',
            content_type = 'application/json')

        self.assertEquals(json.loads(response.data), expected)

    def testPostSingleObject(self):
        TestSuite.setServerObjects({})

        postObject = { "field1" : "data1", "field two" : 2 }

        response = TestSuite.client.post(INDEX_ROUTE,
            data = json.dumps(postObject),
            content_type = 'application/json')

        responseObject = json.loads(response.data)

        # Check that response contains a UID
        self.assertTrue("uid" in responseObject)
        self.assertTrue(responseObject["uid"])

        # Check that response contains the same keys and values as request
        for key in postObject:
            self.assertTrue(key in responseObject)
            self.assertEquals(postObject[key], responseObject[key])

        # Check that response is present in the server's stored objects
        self.assertEquals(TestSuite.getServerObjects()[responseObject["uid"]], responseObject)

    def testPostMultipleObjects(self):
        TestSuite.setServerObjects({})

        postObject = [
            { "field1" : "data1", "field two" : 2 },
            { "field3" : "data3", "field four" : 4 }
            ]

        response = TestSuite.client.post(INDEX_ROUTE,
            data = json.dumps(postObject),
            content_type = 'application/json')

        responseObject = json.loads(response.data)

        # Check that a list of objects is returned with the correct number of entries
        self.assertTrue(isinstance(responseObject["objects"], list))
        self.assertEquals(len(responseObject["objects"]), len(postObject))

        # Check that each has a uid and that the uid is present in the server's stored objects
        for item in responseObject["objects"]:
            self.assertTrue("uid" in item)
            self.assertTrue(item["uid"] in TestSuite.getServerObjects())

    def testPostRepeat(self):
        TestSuite.setServerObjects({})

        postObject = { "field1" : "data1", "field two" : 2 }

        firstResponse = TestSuite.client.post(INDEX_ROUTE,
            data = json.dumps(postObject),
            content_type = 'application/json')

        secondResponse = TestSuite.client.post(INDEX_ROUTE,
            data = json.dumps(postObject),
            content_type = 'application/json')

        firstResponseObject = json.loads(firstResponse.data)
        secondResponseObject = json.loads(secondResponse.data)

        # Check that the only differentiating factor between the two objects is the uid
        self.assertNotEqual(firstResponseObject, secondResponseObject)
        del firstResponseObject["uid"]
        del secondResponseObject["uid"]
        self.assertEquals(firstResponseObject, secondResponseObject)

    def testPut(self):
        TestSuite.setServerObjects({});

        expected = {
              "message": "405: Method Not Allowed",
              "url": "http://localhost/api/objects/",
              "verb": "PUT"
            }

        response = TestSuite.client.put(INDEX_ROUTE, content_type = 'application/json')

        self.assertEquals(json.loads(response.data), expected)

    def testDelete(self):
        TestSuite.setServerObjects({});

        expected = {
              "message": "405: Method Not Allowed",
              "url": "http://localhost/api/objects/",
              "verb": "DELETE"
            }

        response = TestSuite.client.delete(INDEX_ROUTE, content_type = 'application/json')

        self.assertEquals(json.loads(response.data), expected)
