# Imports elasticsearch and elasticsearch_dsl
from django_elasticsearch_dsl import DocType, Index
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import connections

# import our own models
from udata.models import *

# Create a global connection
connections.create_connection(hosts=['localhost'], timeout=20)

search_data_model = Index('search_index_datas')
# # See Elasticsearch Indices API reference for available settings
search_data_model.settings(
    number_of_shards=1,
    number_of_replicas=0
)


# Our indexing class
@search_data_model.doc_type
class SearchDataIndex(DocType):
    class Meta:
        model = SearchDataModel
        fields = [
            'company_name',
            'city',
            'state',
            'zip_codes',
            'street_address',
            'street_address_zip',
            'county',
            'last_name',
            'first_name',
            'contact_title',
            'contact_gender',
            'actual_employee_size',
            'actual_sales_volume',
            'primary_sic',
            'primary_sic_description',
        ]


# A method for bulk indexing
def bulk_indexing():
    SearchDataIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in
                             SearchDataModel.objects.all().iterator()))
