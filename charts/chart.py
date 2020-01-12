from matplotlib.dates import date2num
import pylab
from datetime import datetime
from os import remove


class ChartBuilder:
    def __init__(self, queryset, owner, days: int):
        self.queryset = queryset
        self.owner = owner
        self.values = {k.time: k.value if k.payment_type == '+' else (0-k.value) for k in self.queryset}
        self.numeric_dates = date2num([i for i in self.values.keys()])
        self.targets = [i.target for i in queryset]
        self.plus_values = {k.target: k.value for k in queryset if k.payment_type == '+'}
        self.minus_values = {k.target: (0-k.value) for k in queryset if k.payment_type == '-'}
        self.data_format = '%H:%M' if days == 1 else '%d.%m %H:%M'
        self.saved_charts = []

    def __repr__(self):
        return f'ChartBuilder for {self.owner} {len(self.queryset)}'

    @property
    def first_payment_date(self):
        return [i for i in self.values.keys()][0].strftime(self.data_format)

    @property
    def last_payment_date(self):
        return [i for i in self.values.keys()][-1].strftime(self.data_format)

    @staticmethod
    def save_chart_and_clean_canvas(name: str):
        pylab.savefig(name)
        pylab.close()

    def makename_and_add2list(self):
        name = f'chart={self.owner}={datetime.now()}.png'
        self.saved_charts.append(name)
        return name

    def test_plot(self):
        pylab.bar(self.values.keys(), self.values.values(), width=0.1, )
        pylab.grid()
        pylab.xlabel(f'платежи с {self.first_payment_date} по {self.last_payment_date}')
        self.save_chart_and_clean_canvas(self.makename_and_add2list())

    def pie_chart_plus(self):
        pylab.pie(x=[i for i in self.plus_values.values()], labels=self.plus_values.keys())
        self.save_chart_and_clean_canvas(self.makename_and_add2list())

    def pie_chart_minus(self):
        pylab.pie(x=[abs(i) for i in self.minus_values.values()], labels=self.minus_values.keys())
        self.save_chart_and_clean_canvas(self.makename_and_add2list())

    def delete_all_charts(self):
        for i in self.saved_charts:
            remove(i)
        self.saved_charts.clear()

