from flask import Flask,jsonify,request, abort, make_response
from compute_premium import get_quote


app= Flask(__name__)


@app.errorhandler(400)
def not_found(error):
    global id_no
    id_no += 1
    return make_response(jsonify({'error_id ': id_no, 'validation_reason': "Bad Request"}), 400)


@app.errorhandler(404)
def server_error(error):
    global id_no
    id_no += 1
    return make_response(jsonify({'error_id ': id_no, 'validation_reason': "Data not found"}), 404)


@app.errorhandler(500)
def not_found(error):
    global id_no
    id_no += 1
    return make_response(jsonify({'error_id ': id_no, 'validation_reason': "Server Error"}), 500)


id_no =1
@app.route('/insurance/quote', methods=['POST'])
def main():

    global id_no

    if not request.json :
        abort(400)

    if not ( ( 'name' in request.json )\
    and ('gender' in request.json  )\
    and ('birth' in request.json  )\
    and ('driver_license'  in request.json  )\
    and ('income_month' in request.json  )):
        abort(404)

    id_no += 1

    name= request.json['name']
    gender= request.json['gender']
    birth= request.json['birth']
    license= request.json['driver_license']
    income_month=  request.json['income_month']
	
    prem_monthly , quote_expiry,age  = get_quote(birth, license, income_month)

    return jsonify({'quote_id':id_no , "premium_monthly": prem_monthly ,"age": age,  "quote_expiry_date": quote_expiry }) , 200 



if __name__=='__main__':
	app.run(port=2225)
