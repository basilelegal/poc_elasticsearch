# coding: utf-8

from __future__ import unicode_literals

import json
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

DEFAULT_INDEX = 'index'
DEFAULT_DOCTYPE = 'doctype'

class DocumentConnector(object):
	def __init__(self, index=DEFAULT_INDEX, doc_type=DEFAULT_DOCTYPE):
		self.client = Elasticsearch()
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

	def add(self, body=None):
		if not body:
			with open('data/truite.json', 'r') as json_file:
				body = json.load(json_file)
		
		res = self.client.index(
			index=self.index, doc_type=self.doc_type, body=body
		)
		return res.get('_id', None)

	def get_by_id(self, id_):
		return self.client.get(
			index=self.index, doc_type=self.doc_type, id=id_
		)

	def get_by_title(self, title):
		return self.search_obj\
			.query("match", title=title) \
			.execute() \
			.hits()

	def delete_by_id(self, id_):
		self.client.delete(
			index=self.index, doc_type=self.doc_type, id=id_
		)
		
doc = DocumentConnector()
