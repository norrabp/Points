import unittest
from app import create_app, PayerTotals, Transactions
from app.exceptions import ValidationError
from werkzeug.exceptions import NotFound, MethodNotAllowed
from ..utils import client,timestamp

class TestValidation(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = client.TestClient(self.app)

    def tearDown(self):
        PayerTotals.clear()
        Transactions.clear()
        self.ctx.pop()

    def test1Trans1Payer1Spend_NegSpend_RespondMustNotBeNeg(self):
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr(2022,1,5,12,0,0)
        })
        with self.assertRaises(ValidationError):
            rv, json = self.client.post('/api/v1/points/', data={
                'points': -1
            })
            self.assertTrue(rv.status_code == 400)
            self.assertTrue('message' in json)

    def testMethodNotSupportedError(self):
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr(2022,1,5,12,0,0)
        })
        with self.assertRaises(MethodNotAllowed):
            rv, json = self.client.put('/api/v1/transactions/', data={
                'points': 100,
                'payer': 'Fetch',
                'timestamp': timestamp.getTimestampStr(2022,1,5,12,0,0)
            })
            self.assertTrue(rv.status_code == 405, rv.status_code)
            self.assertTrue('error' in json)
            self.assertTrue('status' in json)
            self.assertTrue('message' in json)

    def testNotFound(self):
        with self.assertRaises(NotFound):
            rv, json = self.client.get('/api/v1/bad/')
            self.assertTrue(rv.status_code == 404)
            self.assertTrue('error' in json)
            self.assertTrue('status' in json)
            self.assertTrue('message' in json)

    def testRequiredJson(self):
        with self.assertRaises(ValidationError):
            rv, json = self.client.post('/api/v1/transactions/', data={
                'points': 100,
                'timestamp': timestamp.getTimestampStr(2022,1,5,12,0,0)
            })
            self.assertTrue(rv.statusCode == 400)
        with self.assertRaises(ValidationError):
            rv, json = self.client.post('/api/v1/transactions/', data={
                'payer': 'Fetch',
                'timestamp': timestamp.getTimestampStr(2022,1,5,12,0,0)
            })
            self.assertTrue(rv.statusCode == 400)
        with self.assertRaises(ValidationError):
            rv, json = self.client.post('/api/v1/points/', data={
                'payer': 'Fetch'
            })
            self.assertTrue(rv.statusCode == 400)

    def testNegTransMustNotMakePayerNeg(self):
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr(2022,1,5,12,0,0)
        })
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': -101,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr(2022,1,5,12,0,0)
        })
        self.assertTrue(rv.status_code == 200)
        self.assertTrue('message' in json)
        self.assertTrue(json['payer'] == 'Fetch')
        self.assertTrue(json['payer_points'] == 100)