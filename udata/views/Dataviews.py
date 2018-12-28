from django.shortcuts import render
from django.views import generic
from elasticsearch_dsl.query import Q
import plotly.offline as opy
import colorlover as cl
import operator
from functools import reduce
from udata.forms import FetchDataForm
from udata.models import SearchDataModel
from udata.documents import DatasDocument

# Create your views here.


# def search(author):
#     SearchDataIndex.init()
#
#     response = s.execute()
#     return response


class FetchDataView(generic.FormView):
    form_class = FetchDataForm

    def post(self, request, *args, **kwargs):
        dd = {}
        if request.method == 'POST':
            print('get post req')
            form = FetchDataForm(request.POST)
            data = None
            if form.is_valid():
                # data = None
                print('form is valid')
                if self.request.user.is_authenticated:
                    print('Authenticated req')
                    what = form.cleaned_data['what']
                    where = form.cleaned_data['where']
                    if ',' not in what and len(what) > 0:
                        get_len_what = len(what.split(','))
                    elif ',' in what and len(what) > 0:
                        get_len_what = len(what.split(','))
                    else:
                        get_len_what = len(what.split(',')) - 1
                    if ',' not in where and len(where) > 0:
                        get_len_where = len(where.split(','))
                    elif ',' in where and len(where) > 0:
                        get_len_where = len(where.split(','))
                    else:
                        get_len_where = len(where.split(',')) - 1
                    print('What len is {}'.format(get_len_what))
                    print('where len is {}'.format(get_len_where))
                    keyword = None
                    company = None
                    city = None
                    state = None
                    zip_code = None
                    st_address = None
                    queries = []
                    if get_len_what == 2:
                        keyword_list = what.split(',')[1:]
                        company_list = what.split(',')[:-1]
                        keyword = ''.join(keyword_list)
                        company = ''.join(company_list)
                        queries.append(Q(
                            'match_phrase',
                            company_name=company,
                        ))
                        queries.append(Q(
                            'match_phrase',
                            primary_sic_description=keyword
                        ))
                        print('keyword code is: {}'.format(keyword))
                        print('company code is: {}'.format(company))
                    elif get_len_what == 1:
                        company_list = what.split(',')[:]
                        company = ''.join(company_list)
                        queries.append(Q(
                            'match_phrase',
                            company_name=company
                        ))
                    print('Keyword is {} and comany is {}'.format(keyword, company))

                    if get_len_where == 0:
                        pass
                    elif get_len_where == 1:
                        city_list = where.split(',')[:]
                        city = ''.join(city_list)
                        queries.append(Q(
                            'match_phrase',
                            city=city
                        ))
                    elif get_len_where == 2:
                        city_list = where.split(',')[0]
                        city = ''.join(city_list)
                        state_list = where.split(',')[1]
                        state = ''.join(state_list)
                        queries.append(Q(
                            'match_phrase',
                            city=city,
                        ))
                        queries.append(Q(
                            'match_phrase',
                            state=state
                        ))
                    elif get_len_where == 3:
                        city_list = where.split(',')[0]
                        city = ''.join(city_list)
                        state_list = where.split(',')[1]
                        state = ''.join(state_list)
                        zip_list = where.split(',')[2]
                        zip_code = ''.join(zip_list)
                        queries.append(Q(
                            'match_phrase',
                            city=city,
                        ))
                        queries.append(Q(
                            'match_phrase',
                            state=state
                        ))
                        queries.append(Q(
                            'match_phrase',
                            zip_codes=zip_code
                        ))
                    elif get_len_where == 4:
                        city_list = where.split(',')[0]
                        city = ''.join(city_list)
                        print('city is: {}'.format(city))
                        state_list = where.split(',')[1]
                        state = ''.join(state_list)
                        print('state is: {}'.format(state))
                        zip_list = where.split(',')[2]
                        zip_code = ''.join(zip_list)
                        print('zip code is: {}'.format(zip_code))
                        street_addr_list = where.split(',')[3]
                        st_address = ''.join(street_addr_list)
                        print('st_address code is: {}'.format(st_address))
                        queries.append(Q(
                            'match_phrase',
                            city=city,
                        ))
                        queries.append(Q(
                            'match_phrase',
                            state=state
                        ))
                        queries.append(Q(
                            'match_phrase',
                            zip_codes=zip_code
                        ))
                        queries.append(Q(
                            'match_phrase',
                            street_address=st_address
                        ))
                    print('Queries are : {}'.format(queries))
                    if not len(queries) == 0:
                        result = DatasDocument.search().query(
                            reduce(operator.iand, queries)
                        )
                        states = []
                        sales_volumes = []
                        result = result[0:result.count()]
                        # rest = result[:20]
                        print(result.count())
                        for s in result:
                            states.append(s.state)
                            sales_volumes.append(s.actual_sales_volume)
                            # print(s.state)

                        print('States are: {}'.format(len(states)))
                        print('Sales are: {}'.format(len(sales_volumes)))
                        map_data = [dict(
                            type='choropleth',
                            colorscale='Viridis',
                            autocolorscale=False,
                            locations=states,
                            z=sales_volumes,
                            locationmode='USA-states',
                            text='Sales Volume',
                            marker=dict(
                                line=dict(
                                    color='rgb(255,255,255)',
                                    width=2
                                )),
                            colorbar=dict(
                                title="Thousands USD")
                        )]
                        layout = dict(
                            title='U-tech-Data Sales volume for companies across the USA.',
                            geo=dict(
                                scope='usa',
                                projection=dict(type='albers usa'),
                                showlakes=True,
                                # lakecolor='rgb(66, 165, 245)'),
                                lakecolor='rgb(255, 255, 255)'),
                        )
                        fig = dict(data=map_data, layout=layout)
                        div = opy.plot(fig, auto_open=False, output_type='div')

                        data = {
                            'what': what,
                            'where': where,
                            'dd': result,
                            'graph': div
                        }
                        return render(request, 'Utechdata/layout.html', {'dd': data})

                    else:
                        data = {
                            'message': 'You haven\'t passed the query!'
                        }

                    return render(request, 'Utechdata/layout.html', {'dd': data})

                elif not self.request.user.is_authenticated:
                    print('anonymous req')
                    what = form.cleaned_data['what']
                    where = form.cleaned_data['where']
                    if ',' not in what and len(what) > 0:
                        get_len_what = len(what.split(','))
                    elif ',' in what and len(what) > 0:
                        get_len_what = len(what.split(','))
                    else:
                        get_len_what = len(what.split(',')) - 1
                    if ',' not in where and len(where) > 0:
                        get_len_where = len(where.split(','))
                    elif ',' in where and len(where) > 0:
                        get_len_where = len(where.split(','))
                    else:
                        get_len_where = len(where.split(',')) - 1
                    print('What len is {}'.format(get_len_what))
                    print('where len is {}'.format(get_len_where))
                    keyword = None
                    company = None
                    city = None
                    state = None
                    zip_code = None
                    st_address = None
                    queries = []
                    if get_len_what == 2:
                        keyword_list = what.split(',')[1:]
                        company_list = what.split(',')[:-1]
                        keyword = ''.join(keyword_list)
                        company = ''.join(company_list)
                        queries.append(Q(
                            'match_phrase',
                            company_name=company,
                        ))
                        queries.append(Q(
                            'match_phrase',
                            primary_sic_description=keyword
                        ))
                        print('keyword code is: {}'.format(keyword))
                        print('company code is: {}'.format(company))
                    elif get_len_what == 1:
                        company_list = what.split(',')[:]
                        company = ''.join(company_list)
                        queries.append(Q(
                            'match_phrase',
                            company_name=company
                        ))
                    print('Keyword is {} and comany is {}'.format(keyword, company))

                    if get_len_where == 0:
                        pass
                    elif get_len_where == 1:
                        city_list = where.split(',')[:]
                        city = ''.join(city_list)
                        queries.append(Q(
                            'match_phrase',
                            city=city
                        ))
                    elif get_len_where == 2:
                        city_list = where.split(',')[0]
                        city = ''.join(city_list)
                        state_list = where.split(',')[1]
                        state = ''.join(state_list)
                        queries.append(Q(
                            'match_phrase',
                            city=city,
                        ))
                        queries.append(Q(
                            'match_phrase',
                            state=state
                        ))
                    elif get_len_where == 3:
                        city_list = where.split(',')[0]
                        city = ''.join(city_list)
                        state_list = where.split(',')[1]
                        state = ''.join(state_list)
                        zip_list = where.split(',')[2]
                        zip_code = ''.join(zip_list)
                        queries.append(Q(
                            'match_phrase',
                            city=city,
                        ))
                        queries.append(Q(
                            'match_phrase',
                            state=state
                        ))
                        queries.append(Q(
                            'match_phrase',
                            zip_codes=zip_code
                        ))
                    elif get_len_where == 4:
                        city_list = where.split(',')[0]
                        city = ''.join(city_list)
                        print('city is: {}'.format(city))
                        state_list = where.split(',')[1]
                        state = ''.join(state_list)
                        print('state is: {}'.format(state))
                        zip_list = where.split(',')[2]
                        zip_code = ''.join(zip_list)
                        print('zip code is: {}'.format(zip_code))
                        street_addr_list = where.split(',')[3]
                        st_address = ''.join(street_addr_list)
                        print('st_address code is: {}'.format(st_address))
                        queries.append(Q(
                            'match_phrase',
                            city=city,
                        ))
                        queries.append(Q(
                            'match_phrase',
                            state=state
                        ))
                        queries.append(Q(
                            'match_phrase',
                            zip_codes=zip_code
                        ))
                        queries.append(Q(
                            'match_phrase',
                            street_address=st_address
                        ))
                    print('Queries are : {}'.format(queries))
                    if not len(queries) == 0:
                        result = DatasDocument.search().query(
                            reduce(operator.iand, queries)
                        )
                        states = []
                        sales_volumes = []
                        result = result[0:result.count()]
                        rest = result[:20]
                        print(rest.count())
                        for s in rest:
                            states.append(s.state)
                            sales_volumes.append(s.actual_sales_volume)
                            # print(s.state)

                        print('States are: {}'.format(len(states)))
                        print('Sales are: {}'.format(sales_volumes))
                        map_data = [dict(
                            type='choropleth',
                            colorscale='Viridis',
                            autocolorscale=False,
                            locations=states,
                            z=sales_volumes,
                            locationmode='USA-states',
                            text='Sales Volume',
                            marker=dict(
                                line=dict(
                                    color='rgb(255,255,255)',
                                    width=2
                                )),
                            colorbar=dict(
                                title="Thousands USD")
                        )]
                        layout = dict(
                            title='U-tech-Data Sales volume for companies across the USA.',
                            geo=dict(
                                scope='usa',
                                projection=dict(type='albers usa'),
                                showlakes=True,
                                # lakecolor='rgb(66, 165, 245)'),
                                lakecolor='rgb(255, 255, 255)'),
                        )
                        fig = dict(data=map_data, layout=layout)
                        div = opy.plot(fig, auto_open=False, output_type='div')

                        data = {
                            'what': what,
                            'where': where,
                            'dd': result,
                            'graph': div
                        }
                        return render(request, 'Utechdata/layout.html', {'dd': data})

                    else:
                        data = {
                            'message': 'You haven\'t passed the query!'
                        }

                return render(request, 'Utechdata/layout.html', {'dd': data})
            else:
                return render(request, 'Utechdata/layout.html', {})


