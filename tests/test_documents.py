# coding: utf-8

from __future__ import unicode_literals

import unittest

try:
    import unittest.mock as mock
except ImportError:
    from mock import mock

from elasticsearch.exceptions import NotFoundError
from elasticmock import elasticmock, FakeElasticsearch

from connectors.documents import DocumentConnector

from elasticsearch.exceptions import NotFoundError
from elasticmock import elasticmock
from connectors.documents import DocumentConnector

BASE_JSON = {
    "title": "Template Base",
    "raw_text": "Ceci est le template de base, il contient les mots clés: test, truite et biensur python PYTHON Python",
    "version_date_utc": "2017-09-21T10:38:05+00:00"
}


TRUITE_JSON = {
    "title": "Guide de pêche à la truite",
    "raw_text": "Utiliser de la viande de cheval keywords: findus, professionel, wth",
    "version_date_utc": "2017-10-21T11:38:05+00:00"
}   

class TestDocumentConnector(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls._patcher = mock.patch("connectors.documents.Elasticsearch", FakeElasticsearch)
        cls._patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls._patcher.stop()

    @elasticmock
    def setUp(self):
        self.connector = DocumentConnector()
        self.truite_id = '1337'
        doc_id = 50000
        id_ = self.connector.add(body=BASE_JSON, doc_id=doc_id)
        self.assertEqual(id_, str(doc_id))

    @elasticmock
    def test_get_by_id__failure(self):
        unknowed_id = 1000000
        with self.assertRaises(NotFoundError):
            self.connector.get_by_id(unknowed_id)

    @elasticmock
    def test_get_by_id__success(self):
        res = self.connector.get_by_id(self.truite_id)
        self.assertIsInstance(res, dict)
        self.assertTrue(res['found'])

    @elasticmock
    def test_get_by_id__success(self):
        res = self.connector.get_by_id(self.truite_id)
        self.assertIsInstance(res, dict)
        self.assertTrue(res['found'])

    @elasticmock
    def test_find_simple(self):
        pass

    @elasticmock
    def test_delete_by_id(self):
        res = self.connector.delete_by_id(id_=self.truite_id)
        self.assertIsNone(res)
        with self.assertRaises(NotFoundError):
            self.connector.get_by_id(id_=self.truite_id)

if __name__ == "__main__":
    unittest.main()
