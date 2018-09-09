import os
import datetime
import pandas as pd
from copy import copy
from pytz import timezone
from my_modules import mysqlconn

from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader
from django.urls import reverse

from . import models
from .config import templates as templates_cnf


#################################################
# global variable part

# get fields from models
def _get_fields():
    fields = []
    for i in models.Orders._meta.fields:
        fields.append('orders.' + str(i).split('.')[-1])
    fields.remove('orders.id')
    for i in models.OrderItems._meta.fields:
        fields.append('orderitems.' + str(i).split('.')[-1])
    fields.remove('orderitems.id')
    for i in models.Inventory._meta.fields:
        fields.append('inventory.' + str(i).split('.')[-1])
    fields.remove('inventory.id')
    return fields


fields = _get_fields()
context = {'fields': fields,
           'selected_field': '',
           'conditions': '',
}


#################################################
# custom exception part
class QueryException(Exception):
    """It raise an exception when it comes an error using the selected_field and conditions to query"""
    pass


class CreateSheetError(Exception):
    """It raise an exception when it comes an error using the data and fields to create a sheet"""

    def __init__(self, expression=None, message=None):
        self.expression = expression
        self.message = message

    def __str__(self):
        if self.expression:
            return self.expression, self.message
        else:
            return self.message


#################################################
# view part
def index(request):
    template = loader.get_template('sheet_download/index.html')
    return HttpResponse(template.render({}, request))


def templates(request):
    template = loader.get_template('sheet_download/templates.html')
    return HttpResponse(template.render(context, request))


def orders(request):
    template = loader.get_template('sheet_download/orders.html')
    return HttpResponse(template.render(context, request))


def download(request):
    conditions = {}
    from_tz = request.POST['from_tz']
    to_tz = request.POST['to_tz']
    conditions['purchase_start'] = _form_date_str(request.POST.getlist('purchase_start'))
    conditions['purchase_end'] = _form_date_str(request.POST.getlist('purchase_end'))
    conditions['paid_start'] = _form_date_str(request.POST.getlist('paid_start'))
    conditions['paid_end'] = _form_date_str(request.POST.getlist('paid_end'))
    fields = request.POST.getlist('fields')
    _context = copy(context)

    selected_field = ", ".join(fields)
    _conditions = []
    if conditions['purchase_start'] != "0000-00-00 00:00:00":
        conditions['purchase_start'] = tz_transfer(conditions['purchase_start'], from_tz, to_tz)
        _conditions.append("orders.PurchaseDate>='%s'" % conditions['purchase_start'])
    if conditions['purchase_end'] != "0000-00-00 00:00:00":
        conditions['purchase_end'] = tz_transfer(conditions['purchase_end'], from_tz, to_tz)
        _conditions.append("orders.PurchaseDate<'%s'" % conditions['purchase_end'])
    if conditions['paid_start'] != "0000-00-00 00:00:00":
        conditions['paid_start'] = tz_transfer(conditions['paid_start'], from_tz, to_tz)
        _conditions.append("orders.PaidDate>='%s'" % conditions['paid_start'])
    if conditions['paid_end'] != "0000-00-00 00:00:00":
        conditions['paid_end'] = tz_transfer(conditions['paid_end'], from_tz, to_tz)
        _conditions.append("orders.PaidDate<'%s'" % conditions['paid_end'])
    _conditions = " and ".join(_conditions)

    try:
        assert selected_field
        data = _query(selected_field, _conditions)
        file_path = _create_sheet(data, selected_field, 'UTC', from_tz)
    except AssertionError:
        _context['error_message'] = "Must Select Some Fields"
    except QueryException:
        _context['error_message'] = "QueryError: The Date is wrong"
    except CreateSheetError:
        _context['error_message'] = "CreateSheetError: Please try again after a moment"

    if _context.get('error_message'):
        return render(request,
            'sheet_download/orders.html',
            context=_context
        )
    else:
        response = StreamingHttpResponse(_file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_path[-20:])
        return response


def custom_download(request):
    conditions = request.POST['conditions'].strip()
    selected_field = request.POST['selected_field'].strip()
    _context = copy(context)
    _context['selected_field'] = selected_field
    _context['conditions'] = conditions

    try:
        assert selected_field
        data = _query(selected_field, conditions)
        file_path = _create_sheet(data, selected_field, 'UTC', from_tz)
    except AssertionError:
        _context['error_message_custom'] = "Select Fields can't be None"
    except QueryException:
        _context['error_message_custom'] = "QueryError: Select Fields or Conditions is wrong"
    except CreateSheetError:
        _context['error_message_custom'] = "CreateSheetError: Please try again after a moment"

    if _context.get('error_message'):
        return render(request,
            'sheet_download/orders.html',
            context=_context
        )
    else:
        response = StreamingHttpResponse(_file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_path[-20:])
        return response


def templates_download(request):
    conditions = {}
    from_tz = request.POST['from_tz']
    to_tz = request.POST['to_tz']
    template_id = request.POST['template_id']
    conditions['purchase_start'] = _form_date_str(request.POST.getlist('purchase_start'))
    conditions['purchase_end'] = _form_date_str(request.POST.getlist('purchase_end'))
    conditions['paid_start'] = _form_date_str(request.POST.getlist('paid_start'))
    conditions['paid_end'] = _form_date_str(request.POST.getlist('paid_end'))
    _context = copy(context)

    selected_field = [i[0] for i in templates_cnf[template_id]['selected_field']]
    column_name = [i[1] for i in templates_cnf[template_id]['selected_field']]
    selected_field = ','.join(selected_field)
    _conditions = []
    if conditions['purchase_start'] != "0000-00-00 00:00:00":
        conditions['purchase_start'] = tz_transfer(conditions['purchase_start'], from_tz, to_tz)
        _conditions.append("orders.PurchaseDate>='%s'" % conditions['purchase_start'])
    if conditions['purchase_end'] != "0000-00-00 00:00:00":
        conditions['purchase_end'] = tz_transfer(conditions['purchase_end'], from_tz, to_tz)
        _conditions.append("orders.PurchaseDate<'%s'" % conditions['purchase_end'])
    if conditions['paid_start'] != "0000-00-00 00:00:00":
        conditions['paid_start'] = tz_transfer(conditions['paid_start'], from_tz, to_tz)
        _conditions.append("orders.PaidDate>='%s'" % conditions['paid_start'])
    if conditions['paid_end'] != "0000-00-00 00:00:00":
        conditions['paid_end'] = tz_transfer(conditions['paid_end'], from_tz, to_tz)
        _conditions.append("orders.PaidDate<'%s'" % conditions['paid_end'])
    _conditions = " and ".join(_conditions)

    try:
        assert selected_field
        data = _query(selected_field, _conditions)
        file_path = _create_sheet(data, selected_field, 'UTC', from_tz, col_repl=column_name)
    except AssertionError:
        _context['error_message'] = "Must Select Some Fields"
    except QueryException:
        _context['error_message'] = "QueryError"
    except CreateSheetError:
        _context['error_message'] = "CreateSheetError: Please try again after a moment"

    if _context.get('error_message'):
        return render(request,
            'sheet_download/templates.html',
            context=_context
        )
    else:
        response = StreamingHttpResponse(_file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_path[-20:])
        return response


def inventory_download(request):
    conditions = {}
    from_tz = request.POST['from_tz']
    to_tz = request.POST['to_tz']
    template_id = request.POST['template_id']
    marketplace_id = request.POST['marketplace']
    _context = copy(context)

    selected_field = [i[0] for i in templates_cnf[template_id]['selected_field']]
    column_name = [i[1] for i in templates_cnf[template_id]['selected_field']]
    selected_field = ','.join(selected_field)
    sql = "select %s from inventory left join price on inventory.SellerSKU=price.SellerSKU and inventory.Seller=price.Seller and inventory.MarketplaceId=price.MarketplaceId where inventory.MarketplaceId='%s';" % (selected_field, marketplace_id)

    try:
        data = _query(selected_field, conditions, sql=sql)
        file_path = _create_sheet(data, selected_field, 'UTC', from_tz, col_repl=column_name)
    except Exception:
        _context['error_message_2'] = "CreateSheetError: Please try again after a moment"

    if _context.get('error_message_2'):
        return render(request,
            'sheet_download/templates.html',
            context=_context
        )
    else:
        response = StreamingHttpResponse(_file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_path[-20:])
        return response


#################################################
# auxiliary function part

# form datetime string for PurchaseDate and PaidDate
# the PurchaseDate or PaidDate got from web request is a list like ['', '00:00:00'] or ['2018-01-01', '00:00:00']
def _form_date_str(datetime_list):
    if datetime_list[0]:
        return ' '.join(datetime_list)
    else:
        return ' '.join(['0000-00-00', datetime_list[1]])

# query in orders, orderitems and inventory tables according to the selected_field and conditions
def _query(selected_field, conditions, sql=None):
    if not sql:
        sql = "select " + selected_field + " from orders " \
              "left join orderitems on orders.AmazonOrderId=orderitems.AmazonOrderId " \
              "left join inventory on orderitems.SellerSKU=inventory.SellerSKU " \
              "and orders.Seller=inventory.Seller"
        if conditions:
              sql = sql + " where " + conditions
        # order the data by orders.LastUpdateDate to ease the later handling
        sql = sql + " order by orders.AmazonOrderId, orders.LastUpdateDate;"

    try:
        conn = mysqlconn.mysqlconn(db='DB_NAME')
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
    except:
        raise QueryException
    else:
        result = []
        # delete the duplicate data
        for i in data:
            if i not in result:
                result.append(i)
        return result
    finally:
        conn.close()


# create a sheet according to data and fields
def _create_sheet(data, fields, from_tz, to_tz, col_repl=[]):
    if isinstance(fields, str):
        fields = fields.replace(' ', '').split(',')
    elif isinstance(fields, list) or isinstance(fields, tuple):
        pass
    else:
        raise CreateSheetError(expression=fields, message="Fields Error")
    try:
        df = pd.DataFrame(data, columns=fields)

        # delete the duplicate data according to orders.AmazonOrderId and remain the latest record
        if 'orders.AmazonOrderId' in fields:
            df = df.drop_duplicates(['orders.AmazonOrderId', 'orderitems.SellerSKU'], keep='last').reset_index(drop=True)
        # tranfer timezone
        df = df_tz_transfer(df, from_tz, to_tz)
        # replace the column name with col_repl
        if col_repl:
            df.columns = col_repl

        created_time = datetime.datetime.strftime(datetime.datetime.now(),"%Y%m%d_%H%M%S")
        file_path = os.path.join(os.path.dirname(__file__), 'temp_files/', created_time+'.xlsx')
        writer = pd.ExcelWriter(file_path)
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        return file_path
    except:
        raise CreateSheetError(message="Creating Error")
    finally:
        writer.close()


# tranfer timezone of DataFrame columns of Timestamp type to a certain timezone
def df_tz_transfer(df, from_tz, to_tz):
    if df.shape[0]:
        # Check type of each column. If the time is pandas._libs.tslib.Timestamp, then change its timezone.
        for column in df.columns:
            # get the index of item in that column that is not None 
            for i in df.index:
                if df[column][i] == df[column][i]:
                    break
            if type(df[column][i]) is pd._libs.tslib.Timestamp:
                tmp = list(df[column])
                df[column] = [tz_transfer(str(i), from_tz, to_tz) for i in tmp]
        return df
    else:
        return df


# open a file in stream (using the generator method)
def _file_iterator(file_name, chunk_size=512):
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


# tranfer a time string in 'from_tz' timezone to a time string in 'to_tz' timezone
def tz_transfer(time_string, from_tz, to_tz):
    # return '' if the time_string is None
    if time_string in ('', 'NaT'):
        return ''

    from_tz = timezone(from_tz)
    to_tz = timezone(to_tz)
    fmt = '%Y-%m-%d %H:%M:%S'

    from_time = from_tz.localize(datetime.datetime.strptime(time_string, fmt))
    to_time = from_time.astimezone(to_tz)
    return to_time.strftime(fmt)
