# coding: utf-8

from __future__ import unicode_literals

import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from elasticsearch.exceptions import NotFoundError
from elasticmock import elasticmock, FakeElasticsearch

from connectors.documents import DocumentConnector
from connectors.documents import DEFAULT_INDEX

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

TRUITE_2_JSON = {
    "title": "Guide de pêche au cheval",
    "raw_text": "Utiliser de la truite keywords: findus, professionel, wth",
    "version_date_utc": "2017-10-21T11:38:05+00:00"
}


class TestDocumentConnector(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls._patcher = mock.patch("connectors.documents.Elasticsearch", auto_spec=True)
        cls.MockClass = cls._patcher.start()


    @classmethod
    def tearDownClass(cls):
        cls._patcher.stop()

    def setUp(self):
        self.connector = DocumentConnector()
        self.truite_id = '1337'
        id_ = self.connector.add(body=TRUITE_JSON, doc_id=self.truite_id)
        self.connector.add(body=TRUITE_2_JSON)

    # def test_get_by_id__failure(self):
    #     unknown_id = 1000000
    #     with self.assertRaises(NotFoundError):
    #         self.connector.get_by_id(unknown_id)

    # def test_get_by_id__success(self):
    #     res = self.connector.get_by_id(self.truite_id)
    #     self.assertIsInstance(res, dict)
    #     self.assertTrue(res['found'])

    # def test_delete_by_id(self):
    #     res = self.connector.delete_by_id(id_=self.truite_id)
        

    def test_find_simple(self):
        self.connector.client = self.MockClass.return_value
        fields = ['title']
        query = 'query'
        res = self.connector.find(query=query, fields=fields)
        self.assertTrue(self.connector.client.search.called)
        body={
            'query': {
                'query_string': {
                    'analyze_wildcard': True,
                    'fields': fields,
                    'query': query
                }
            }
        }
        self.connector.client.search.assert_called_once_with(index=DEFAULT_INDEX, body=mock.ANY)


if __name__ == "__main__":
    unittest.main()
