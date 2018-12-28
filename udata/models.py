# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class SearchDataModel(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    company_name = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    zip_codes = models.TextField(blank=True, null=True)
    street_address = models.TextField(blank=True, null=True)
    street_address_zip = models.TextField(blank=True, null=True)
    county = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)
    contact_title = models.TextField(blank=True, null=True)
    contact_gender = models.TextField(blank=True, null=True)
    actual_employee_size = models.IntegerField(blank=True, null=True)
    employee_size_range = models.TextField(blank=True, null=True)
    actual_sales_volume = models.IntegerField(blank=True, null=True)
    sales_volume_range = models.TextField(blank=True, null=True)
    primary_sic = models.IntegerField(blank=True, null=True)
    primary_sic_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'searchdatamodel'

    # Implement indexing for SearchDataModel model
    def indexing(self):
        from .search import SearchDataIndex
        obj = SearchDataIndex(
            id=self.id,
            company_name=self.company_name,
            city=self.city,
            state=self.state,
            zip_codes=self.zip_codes,
            street_address=self.street_address,
            street_address_zip=self.street_address_zip,
            county=self.county,
            last_name=self.last_name,
            first_name=self.first_name,
            contact_title=self.contact_title,
            contact_gender=self.contact_gender,
            actual_employee_size=self.actual_employee_size,
            actual_sales_volume=self.actual_sales_volume,
            primary_sic=self.primary_sic,
            primary_sic_description=self.primary_sic_description,
        )
        obj.save()
        return obj.to_dict(include_meta=True)
