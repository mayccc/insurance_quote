from flask import Flask,jsonify,request, abort, make_response
import datetime
import numpy as np
from datetime import timedelta
import re
import dateutil.parser
from PremEngine import PremiumEngine
from Quote import Quote
from Person import Person
from PremEngine import id_no

app= Flask(__name__)


@app.errorhandler(400)

def bad_request(error):
    global prem_quote
    return make_response(jsonify({'error_id ': prem_quote, 'validation_reason': "Bad Request"}), 400)


@app.errorhandler(404)
def data_not_found(error):
    global prem_quote
    return make_response(jsonify({'error_id ': prem_quote,  'validation_reason': "Data not found"}), 404)


@app.errorhandler(500)
def server_error(error):
    global prem_quote
    return make_response(jsonify({'error_id ': prem_quote,  'validation_reason': "Server Error"}), 500)


@app.route('/insurance/quote', methods=['POST'])
def main():
    global prem_quote
    
    prem_engine= PremiumEngine()
    if not request.json :
        prem_engine.increment_quote_no()
        prem_quote=prem_engine.quote_id 
        abort(400)

    if not ( ( 'name' in request.json )\
    and ('gender' in request.json  )\
    and ('birth' in request.json  )\
    and ('driver_license'  in request.json  )\
    and ('income_month' in request.json  )):
        prem_engine.increment_quote_no()
        prem_quote = prem_engine.quote_id
        abort(404  )

    
    p = Person( request.json['name'] ,request.json['gender'] , request.json['birth'] , request.json['driver_license'],request.json['income_month'])

    quote= prem_engine.get_quote( p )

    return jsonify({'quote_id': quote.quote_id , "premium_monthly": quote.premium_monthly , \
        "age": quote.age,  "gender":quote.gender, "quote_expiry_date": quote.quote_expiry_date }) , 200 



if __name__=='__main__':
    app.run()

