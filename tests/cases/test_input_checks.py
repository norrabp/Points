import unittest
from app import create_app, PayerTotals, Transactions
from ..utils import test_client,timestamp

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = test_client.TestClient(self.app)

    def tearDown(self):
        PayerTotals.clear()
        Transactions.clear()
        self.ctx.pop()

    def test0Trans1Spend_ReturnMessage(self):
        rv, json = self.client.post('/api/v1/points/', data={'points': 100})
        self.assertTrue(rv.status_code == 200)
        self.assertTrue('message' in json)

    def test1Trans1Payer1Spend_SpendGTTrans_RespondNotEnough(self):
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr(2022,1,5,12,0,0)
        })
        rv, json = self.client.post('/api/v1/points/', data={
            'points': 101
        })
        self.assertTrue('message' in json)