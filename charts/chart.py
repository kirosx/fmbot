from matplotlib.dates import date2num


class ChartBuilder:
    def __init__(self, queryset, owner):
        self.queryset = queryset
        self.owner = owner
        self.values = {k.time: k.value if k.payment_type == '+' else (0-k.value) for k in self.queryset}
        self.numeric_dates = date2num([i for i in self.values.keys()])
        self.targets = [i.target for i in queryset]
        self.pluses, self.minuses = [], []
        for i in self.values.values():
            self.pluses.append(i) if i > 0 else self.minuses.append(i)

    def __repr__(self):
        return f'ChartBuilder for {self.owner} {len(self.queryset)}'
