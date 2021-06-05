import unittest 
import app
from app import app
import numpy as np
from datetime import timedelta
import re
import dateutil.parser
from PremEngine  import PremiumEngine


class TestApp(unittest.TestCase):

	def test_post1(self):
		tester = app.test_client(self)
		response = tester.post('/insurance/quote', json={
        'attr': 'value', 'other': 'data'
    })

		self.assertEqual(response.status_code, 404)


	def test_post2(self):
		tester = app.test_client(self)
		response = tester.post('/insurance/quote', json={
        "name":"Rong", "gender":"f", "birth":"2012-01-12","driver_license":"1124AVV1234", "income_month":100
    })

		self.assertEqual(response.status_code,200)


	def test_post3(self):
		tester = app.test_client(self)
		response = tester.post('/insurance/quote', json={
         "gender":"f", "birth":"2012-01-12","driver_license":"1124AVV1234", "income_month":100
    })

		self.assertEqual(response.status_code,404)



	def test_post3(self):
		tester = app.test_client(self)
		response = tester.post('/insurance/quote', json={
         
    })

		self.assertEqual(response.status_code,400)

class TestPremCalc(unittest.TestCase):

	
	def test_parse_driver_license(self):
		prem_engine=PremiumEngine()
		first_4_digit ,last_4_digit= prem_engine.parse_driver_license('1234ABC2234')

		self.assertEqual(first_4_digit,1234)
		self.assertEqual(last_4_digit,2234)


	def test_parse_date1(self):
		prem_engine=PremiumEngine()
		parse_date= prem_engine.parse_date('2020-01-02')
		self.assertEqual(parse_date.day,2)
		self.assertEqual(parse_date.month,1)
		self.assertEqual(parse_date.year,2020)


	def test_parse_date2(self):
		prem_engine=PremiumEngine()
		parse_date= prem_engine.parse_date('2020-Jan-02')
		self.assertEqual(parse_date.day,2)
		self.assertEqual(parse_date.month,1)
		self.assertEqual(parse_date.year,2020)

	def test_parse_date3(self):
		prem_engine=PremiumEngine()
		parse_date= prem_engine.parse_date('01-02-2020')
		self.assertEqual(parse_date.day,2)
		self.assertEqual(parse_date.month,1)
		self.assertEqual(parse_date.year,2020)




if __name__ == '__main__':
    unittest.main()