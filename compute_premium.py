import math
import numpy
import datetime
import numpy as np
from datetime import timedelta
import re
import dateutil


def get_quote(birth, license, income_month):

	first_4_digit ,last_4_digit = parse_driver_license(license)
	age_in_days= get_age_in_days(birth)
	age_in_years= get_age_in_years(birth)
	income_year= income_month * 12
	
	prem_year= calc_premium( first_4_digit ,last_4_digit , age_in_days, age_in_years, income_year)

	return np.round( prem_year/12,2) , get_quote_expiry_date(), age_in_years



def get_quote_expiry_date():
    now = datetime.date.today()
    dt = now + timedelta(days=10)
    return dt.strftime("%d-%m-%Y")



def calc_premium( first_4_digit ,last_4_digit , age_in_days,age_in_years, income_year):

	prem = np.abs(  age_in_days* income_year/ (first_4_digit+ last_4_digit ) - age_in_years**2)
	
	return prem 


def get_age_in_days(birth):
	
	birthday=dateutil.parser.parse(birth)
	now = datetime.date.today()
	delta = now - birthday.date()
	
	return delta.days

def get_age_in_years(birth):
	
	birthday=dateutil.parser.parse(birth)
	now = datetime.date.today()
	delta = now.year - birthday.year
	
	return delta


def parse_driver_license(string):
	
	first_4_digit ,last_4_digit = re.findall(r"([0-9]{4})[A-Za-z]{3}([0-9]{4})", string)[0]
	
	return int(first_4_digit), int(last_4_digit)