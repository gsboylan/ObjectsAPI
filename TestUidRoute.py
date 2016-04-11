import sys
import unittest
from flask import json

import TestSuite

INDEX_ROUTE = '/api/objects/'

class TestUidRoute(unittest.TestCase):

    def testGetRealUid(self):
        expected = {"FieldOne" : "One", "Field2" : 2, "uid" : "uid00112233"}
        TestSuite.setServerObjects({"uid00112233" : expected})

        response = TestSuite.client.get(INDEX_ROUTE + "uid00112233")

        self.assertEquals(json.loads(response.data), expected)

    def testGetWrongUid(self):
        TestSuite.setServerObjects({})
        expected = {
              "message": "404: Not Found",
              "url": "http://localhost/api/objects/uid00112233",
              "verb": "GET"
            }

        response = TestSuite.client.get(INDEX_ROUTE + "uid00112233")

        self.assertEquals(json.loads(response.data), expected)

    def testPutRealUid(self):
        uid = "uid00112233"
        initial = {"FieldOne" : "One", "Field2" : 2, "uid" : uid}
        TestSuite.setServerObjects({uid : initial})

        putObject = {"FieldThree" : "Three", "Field4" : 4, "uid" : uid}

        response = TestSuite.client.put(INDEX_ROUTE + uid,
            data = json.dumps(putObject),
            content_type = 'application/json')

        self.assertTrue(uid in TestSuite.getServerObjects())

        self.assertEquals(TestSuite.getServerObjects()[uid], putObject)
        self.assertEquals(len(TestSuite.getServerObjects()), 1)
        self.assertEquals(json.loads(response.data), putObject)

    def testPutIdempotent(self):
        uid = "uid00112233"
        initial = {"FieldOne" : "One", "Field2" : 2, "uid" : uid}
        TestSuite.setServerObjects({uid : initial})

        putObject = {"FieldThree" : "Three", "Field4" : 4}

        firstResponse = TestSuite.client.put(INDEX_ROUTE + uid,
            data = json.dumps(putObject),
            content_type = 'application/json')

        secondResponse = TestSuite.client.put(INDEX_ROUTE + uid,
            data = json.dumps(putObject),
            content_type = 'application/json')

        self.assertEquals(json.loads(firstResponse.data), json.loads(secondResponse.data))
        self.assertEquals(len(TestSuite.getServerObjects()), 1)

    def testPutBrokenJSON(self):
        uid = "uid00112233"
        initial = {"FieldOne" : "One", "Field2" : 2, "uid" : uid}
        TestSuite.setServerObjects({uid : initial})

        expected = {
              "message": "400: Bad Request",
              "url": "http://localhost/api/objects/uid00112233",
              "verb": "PUT"
            }

        response = TestSuite.client.put(INDEX_ROUTE + uid,
            data = '{ "field1" : "brokendata }',
            content_type = 'application/json')

        self.assertEquals(json.loads(response.data), expected)
        self.assertEquals(len(TestSuite.getServerObjects()), 1)
        self.assertEquals(TestSuite.getServerObjects()[uid], initial)

    def testPutWrongUid(self):
        uid = "uid00112233"
        initial = {"FieldOne" : "One", "Field2" : 2, "uid" : uid}
        TestSuite.setServerObjects({uid : initial})

        expected = {
              "message": "404: Not Found",
              "url": "http://localhost/api/objects/uid9999",
              "verb": "PUT"
            }

        putObject = {"FieldThree" : "Three", "Field4" : 4}

        response = TestSuite.client.put(INDEX_ROUTE + "uid9999",
            data = json.dumps(initial),
            content_type = 'application/json')

        self.assertEquals(json.loads(response.data), expected)
        self.assertEquals(len(TestSuite.getServerObjects()), 1)
        self.assertEquals(TestSuite.getServerObjects()[uid], initial)

    def testDeleteRealUid(self):
        uid = "uid00112233"
        initial = {"FieldOne" : "One", "Field2" : 2, "uid" : uid}
        TestSuite.setServerObjects({uid : initial})

        response = TestSuite.client.delete(INDEX_ROUTE + uid)

        self.assertFalse(response.data)
        self.assertEquals(len(TestSuite.getServerObjects()), 0)

    def testDeleteIdempotent(self):
        uid = "uid00112233"
        initial = {"FieldOne" : "One", "Field2" : 2, "uid" : uid}
        TestSuite.setServerObjects({uid : initial})

        firstResponse = TestSuite.client.delete(INDEX_ROUTE + uid)
        secondResponse = TestSuite.client.delete(INDEX_ROUTE + uid)

        self.assertFalse(firstResponse.data)
        self.assertFalse(secondResponse.data)
        self.assertEquals(len(TestSuite.getServerObjects()), 0)

    def testDeleteWrongUid(self):
        uid = "uid00112233"
        initial = {"FieldOne" : "One", "Field2" : 2, "uid" : uid}
        TestSuite.setServerObjects({uid : initial})

        response = TestSuite.client.delete(INDEX_ROUTE + "uid9999")

        self.assertFalse(response.data)
        self.assertEquals(len(TestSuite.getServerObjects()), 1)
        self.assertEquals(TestSuite.getServerObjects()[uid], initial)

    def testPost(self):
        uid = "uid00112233"
        initial = {"FieldOne" : "One", "Field2" : 2, "uid" : uid}
        TestSuite.setServerObjects({uid : initial})

        postObject = {"FieldThree" : "Three", "Field4" : 4}

        expected = {
              "message": "405: Method Not Allowed",
              "url": "http://localhost/api/objects/uid00112233",
              "verb": "POST"
            }

        response = TestSuite.client.post(INDEX_ROUTE + uid,
            data=json.dumps(postObject),
            content_type = 'application/json')

        self.assertEquals(json.loads(response.data), expected)
