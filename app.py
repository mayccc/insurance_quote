from flask import Flask,jsonify,request, abort, make_response
import datetime
import numpy as np
from datetime import timedelta
import re
import dateutil.parser


app= Flask(__name__)


@app.errorhandler(400)

def not_found(error):
    global id_no
    id_no+=1
    return make_response(jsonify({'error_id ': id_no, 'validation_reason': "Bad Request"}), 400)


@app.errorhandler(404)
def server_error(error):
    global id_no
    id_no+=1
    return make_response(jsonify({'error_id ': id_no,  'validation_reason': "Data not found"}), 404)


@app.errorhandler(500)
def server_error(error):
    global id_no
    id_no+=1
    return make_response(jsonify({'error_id ': id_no,  'validation_reason': "Server Error"}), 500)

class Person:
    def __init__(self, name , gender, birth, driver_license, income_month):
        self.name=name
        self.gender= gender
        self.birth= birth
        self.driver_license= driver_license
        self.income_month= income_month

#id_no =0
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

id_no=0 

class PremiumEngine:
    def __init__(self) :
        global id_no 
        self.quote_id=  id_no

    def increment_quote_no(self):
        global id_no
        id_no+=1 
        self.quote_id=id_no

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


@app.route('/insurance/quote', methods=['POST'])
def main():

    prem_engine= PremiumEngine()

    if not request.json :
        prem_engine.increment_quote_no()
        abort(400)

    if not ( ( 'name' in request.json )\
    and ('gender' in request.json  )\
    and ('birth' in request.json  )\
    and ('driver_license'  in request.json  )\
    and ('income_month' in request.json  )):
        prem_engine.increment_quote_no()
        abort(404)

    
    p = Person( request.json['name'] ,request.json['gender'] , request.json['birth'] , request.json['driver_license'],request.json['income_month'])

    quote= prem_engine.get_quote( p )

    return jsonify({'quote_id': quote.quote_id , "premium_monthly": quote.premium_monthly , \
        "age": quote.age,  "gender":quote.gender, "quote_expiry_date": quote.quote_expiry_date }) , 200 



if __name__=='__main__':
    app.run()

