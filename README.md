#  Insurance quote
## local web application to 

invoke HTTP POST request to http://localhost:5000/insurance/quote to return insurance quote

### input

+ name- String
+ gender - String 
+ birth - mm-dd-yyyy, dd-MMM-yyyy, dd-mm-yyyy
+ driver_license- String with part of Intx4Stringx3Intx4
+ income_month- number support double 

Request JSON Body example
```
{"name":"Rong", "gender":"M", "birth": "23-08-2019", "driver_license":"1234XXX3423", "income_month":3033.3 }'
```



### usage

```
curl -X POST http://127.0.0.1:5000/insurance/quote -d '{"name":"Rong", "gender":"M", "birth": "23-08-2019", "driver_license":"1234XXX3423", "income_month":3033.3 }' -H "Content-Type: application/json"
```

### Success Quote
```
{"age":2,"premium_monthly":419.13,"quote_expiry_date":"07-06-2021","quote_id":5}
```
