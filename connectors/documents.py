# coding: utf-8

from __future__ import unicode_literals

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

DEFAULT_INDEX = 'index'
DEFAULT_DOCTYPE = 'doctype'


class DocumentConnector(object):

    def __init__(
            self,
            index=DEFAULT_INDEX,
            doc_type=DEFAULT_DOCTYPE,
            **kwargs
    ):
        self.client = Elasticsearch(**kwargs)
        self._index = index
        self._doc_type = doc_type

    @property
    def index(self):
        return self._index

    @property
    def doc_type(self):
        return self._doc_type

    @property
    def search_obj(self):
        return Search(using=self.client, index=self.index)

    def add(self, body, **kwargs):
        res = self.client.index(
            index=self.index, doc_type=self.doc_type, body=body,
            **kwargs
        )
        return res.get('_id', None)

    def get_by_id(self, id_):
        return self.client.get(
            index=self.index, doc_type=self.doc_type, id=id_
        )

    def get_by_title(self, title):
        return self.search_obj \
            .query("match", title=title) \
            .execute() \
            .hits()

    def delete_by_id(self, id_):
        self.client.delete(
            index=self.index, doc_type=self.doc_type, id=id_
        )

    def find(self, query, fields, analyze_wildcard=True):
        """
        :param query:
        :param fields: [('title', 5), 'raw_text']
        :param analyze_wildcard: Boolean
        :return:
        """
        _fields = []
        for field in fields:
            if isinstance(field, (tuple, list)):
                _fields.append('{}^{}'.format(field[0], field[1]))
            else:
                _fields.append(field)

        response = self.client.search(
            index=self.index,
            body={
                'query': {
                    'query_string': {
                        'analyze_wildcard': analyze_wildcard,
                        'fields': _fields,
                        'query': query
                    }
                }
            }
        )

        return response['hits']['hits']
