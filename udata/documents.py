from django_elasticsearch_dsl import DocType, Index
from udata.models import SearchDataModel

datas = Index('datas')

@datas.doc_type
class DatasDocument(DocType):
    class Meta:
        model = SearchDataModel

        fields = [
            'id',
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
            'employee_size_range',
            'actual_sales_volume',
            'sales_volume_range',
            'primary_sic',
            'primary_sic_description',
        ]
