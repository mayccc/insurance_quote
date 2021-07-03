#id_no =0
import datetime
from datetime import timedelta
class Quote:
    def __init__(self, prem_monthly, quote_id, age, gender):
        self.premium_monthly= prem_monthly
        self.quote_expiry_date= self.get_quote_expiry_date( today= datetime.date.today())
        self.quote_id= quote_id
        self.age= age
        self.gender= gender

    
    def get_quote_expiry_date(self,today ):
        dt = today  + timedelta(days=10)
        return dt.strftime("%d-%m-%Y")