import datetime as dt

class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
         
    def add_record(self, new_record):
        self.records.append(new_record)

    def get_today_stats(self):
        date_today = dt.datetime.now().date()
        return sum([i.amount for i in self.records if i.date == date_today])
        
    def get_week_stats(self):
        today = dt.datetime.now().date()
        delta = dt.timedelta(days=7)
        date_week_ago = today - delta
        return sum([
            rec.amount for rec in self.records
            if (today >= rec.date >= date_week_ago)])


class Record:
    def __init__(self, amount, comment, date=None):
        date_format = '%d.%m.%Y'
        self.amount = amount
        self.date = date
        self.comment = comment
        if self.date is None:
            self.date = dt.datetime.today().date()
        else:
            self.date = dt.datetime.strptime(self.date, date_format).date()    
    

class CashCalculator(Calculator):
    USD_RATE = 73.11
    EURO_RATE = 88.34

    def get_today_cash_remained(self, currency):
        RATES = {
             'usd': (self.USD_RATE, 'USD'),
             'eur': (self.EURO_RATE, 'Euro'),
             'rub': (1.00, 'руб')
            } 
        if currency in RATES:
            rate = RATES[currency][0]
            name = RATES[currency][1]
        else:
            return f'Не знаю такую валюту'
        if self.limit > self.get_today_stats():
            cash_remained = round(self.limit/rate 
            - self.get_today_stats()/rate, 2)
            return f'На сегодня осталось {cash_remained} {name}'
        elif self.limit/rate == self.get_today_stats()/rate:
            return 'Денег нет, держись'
        else:
            cash_remained = round(self.get_today_stats()/rate
                                  - self.limit/rate, 2)
            return f'Денег нет, держись: твой долг - {cash_remained} {name}'                          


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_limit = self.get_today_stats()
        if calories_limit > 0 and calories_limit < self.limit:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                   f'калорийностью не более ' 
                   f'{self.limit - calories_limit} кКал')
        else:
            return f'Хватит есть!'          