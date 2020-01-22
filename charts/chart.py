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
        self.menu_chart = {}
        self.make_menu()

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
        pylab.bar(self.values.keys(), self.values.values(), width=0.001)
        pylab.grid()
        pylab.xlabel(f'платежи с {self.first_payment_date} по {self.last_payment_date}')
        self.save_chart_and_clean_canvas(self.makename_and_add2list())

    def pie_chart_plus(self):
        pylab.pie(x=[i for i in self.plus_values.values()], labels=self.plus_values.keys())
        pylab.xlabel('Доходы')
        self.save_chart_and_clean_canvas(self.makename_and_add2list())

    def pie_chart_minus(self):
        pylab.pie(x=[abs(i) for i in self.minus_values.values()], labels=self.minus_values.keys())
        pylab.xlabel('Расходы')
        self.save_chart_and_clean_canvas(self.makename_and_add2list())

    def delete_all_charts(self):
        for i in self.saved_charts:
            remove(i)
        self.saved_charts.clear()

    def make_all_charts(self):
        self.test_plot()
        if len(self.minus_values) > 1:
            self.pie_chart_minus()
        if len(self.plus_values) > 1:
            self.pie_chart_plus()

    def make_menu(self):
        self.menu_chart['общий'] = 'all'
        if len(self.plus_values) > 1:
            self.menu_chart['график доходов'] = 'plus'
        if len(self.minus_values) > 1:
            self.menu_chart['график трат'] = 'minus'
        return self.menu_chart

    def build_chart_for_callback(self, type_chart):
        chart = {'all': self.test_plot, 'plus': self.pie_chart_plus, 'minus': self.pie_chart_minus}
        chart[type_chart]()
        return self.saved_charts[-1]
