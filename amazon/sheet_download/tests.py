from django.test import TestCase

# Create your tests here.
from .views import _query, _create_sheet


class Query_function_test(TestCase):
    def simple_query_function_test(self):
        selected_field = "AmazonOrderId"
        conditions = "PurchaseDate>'2018-03-25 00:00:00'"
        self.assertIsInstance(_query(selected_field, conditions), list)


class Create_sheet_function_test(TestCase):
    def simple_create_sheet_function_test(self):
        data = (('111-001', ), )
        fields = 'orders.AmazonOrderId'
        self.assertIs(_create_sheet(data, fields), './temp_files/20180327_072300.xlsx')
