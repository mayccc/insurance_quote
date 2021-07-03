
import numpy as np
import re
import dateutil.parser
import datetime
from Quote import Quote

id_no = 0 
class PremiumEngine:
    def __init__(self) :
        global id_no 
        self.quote_id= id_no 

    def increment_quote_no(self):
        global id_no 
        id_no +=1 
        self.quote_id = id_no

    def get_quote(self, person):

        first_4_digit ,last_4_digit = self.parse_driver_license(person.driver_license)
        age_in_days=  self.get_age_in_days(person.birth)
        age_in_years=  self.get_age_in_years(person.birth)
        income_year=  self.get_yearly_income(person.income_month) 
        
        prem_mth = np.round( self.calc_premium( first_4_digit ,last_4_digit , age_in_days, age_in_years, income_year) /12,2) 
        
        self.increment_quote_no()
        
        return Quote( prem_mth , self.quote_id ,  age_in_years, person.gender) 

    def get_yearly_income(self, income_month):
        return income_month * 12


    def calc_premium( self, first_4_digit ,last_4_digit , age_in_days,age_in_years, income_year):

        prem = np.abs(  age_in_days* income_year/ (first_4_digit+ last_4_digit ) - age_in_years**2)

        return prem 


    def get_age_in_days(self, birth):

        birthday=self.parse_date(birth)
        now = datetime.date.today()
        delta = now - birthday.date()

        return delta.days

    def get_age_in_years(self, birth):

        birthday=self.parse_date(birth)
        now = datetime.date.today()
        delta = now.year - birthday.year

        return delta


    def parse_date(self, string):
        parsed_date=dateutil.parser.parse(string)
        return parsed_date


    def parse_driver_license(self, string):

        first_4_digit ,last_4_digit = re.findall(r"([0-9]{4})[A-Za-z]{3}([0-9]{4})", string)[0]

        return int(first_4_digit), int(last_4_digit)