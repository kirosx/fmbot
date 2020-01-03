from matplotlib.dates import date2num
import pylab
from datetime import datetime


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

    def __repr__(self):
        return f'ChartBuilder for {self.owner} {len(self.queryset)}'

    @property
    def first_payment_date(self):
        return [i for i in self.values.keys()][0].strftime(self.data_format)

    @property
    def last_payment_date(self):
        return [i for i in self.values.keys()][-1].strftime(self.data_format)

    def test_plot(self):
        pylab.bar(self.values.keys(), self.values.values(), width=0.1, data=self.targets)
        pylab.grid()
        pylab.xlabel(f'платежи с {self.first_payment_date} по {self.last_payment_date}')
        filename = f'test={self.owner}={datetime.now()}.png'
        pylab.savefig(filename)
        return filename

    def pie_chart_plus(self):
        pylab.pie(x=[i for i in self.plus_values.values()], labels=self.plus_values.keys())
        pylab.show()

    def pie_chart_minus(self):
        pylab.pie(x=[abs(i) for i in self.minus_values.values()], labels=self.minus_values.keys())
        pylab.show()
