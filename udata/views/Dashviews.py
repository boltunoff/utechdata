import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from udata.documents import DatasDocument


def generate_pie_chart(labels):
    states = []
    data = DatasDocument.search()
    result = data[0:data.count()]
    for s in result:
        states.append(s.state)
    states_df = pd.DataFrame({'State': states}).State.value_counts(normalize=True)
    states_values = []
    for v in states_df:
        states_values.append(v)

    states_values = np.array(states_values)
    pie = go.Pie(
        labels=labels,
        values=states_values,
        name='OperatorShare'
    )
    pie_data = [pie]
    pie_layout = go.Layout(
        title='Percentage of USA States',
    )
    fig = go.Figure(data=pie_data, layout=pie_layout)
    pie_chart = plotly.offline.plot(fig, auto_open=False, output_type='div')
    return pie_chart


def generate_bar_chart(labels):
    sales_volumes = []
    data = DatasDocument.search()
    result = data[0:data.count()]
    for s in result:
        sales_volumes.append(s.actual_sales_volume)

    sales_df = pd.DataFrame({'Sales_Volume': sales_volumes}).Sales_Volume.value_counts(normalize=True)
    print('total is : {}'.format(len(sales_volumes)))
    sales_values = []
    for sv in sales_df:
        sales_values.append(sv)
    sales_values = np.array(sales_volumes)
    print('total sales vol is : {}'.format(len(sales_values)))
    trace0 = go.Bar(
        x=labels,
        y=sales_values
    )
    bar_data = [trace0]
    bar_layout = go.Layout(
        title='Sales Volumes for USA States',
    )
    bar_fig = go.Figure(data=bar_data, layout=bar_layout)
    bar_chart = plotly.offline.plot(bar_fig, auto_open=False, output_type='div', )
    return bar_chart


class DashboardChartsView(generic.DetailView, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        states = []
        data = DatasDocument.search()
        result = data[0:data.count()]
        for s in result:
            states.append(s.state)
        labels_array = pd.DataFrame({'State': states}).State.value_counts(normalize=True).reset_index()
        labels = []
        for a in labels_array['index']:
            labels.append(str(a))
        labels = np.array(labels)
        pie = generate_pie_chart(labels)
        bar = generate_bar_chart(labels)
        data = {
            'pie': pie,
            'bar': bar
        }
        return render(request, 'Utechdata/profile.html', {'dd': data})
