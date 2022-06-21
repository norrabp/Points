import unittest
from app import create_app, PayerTotals, Transactions
from app.exceptions import ValidationError
from ..utils import client,timestamp

class TestInputs(unittest.TestCase):
    """
    Test cases involving verifying that input does not make point totals negative
    """
    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = client.TestClient(self.app)

    def tearDown(self):
        PayerTotals.clear()
        Transactions.clear()
        self.ctx.pop()

    def test0Trans1Spend_ReturnMessage(self):
        """
        Verify that if there are no transactions a code 200 returns along with
        a message stating why the spend was not possible
        """
        rv, json = self.client.post('/api/v1/points/', data={'points': 100})
        self.assertTrue(rv.status_code == 200)
        self.assertTrue('message' in json)

    def test1Trans1Payer1Spend_SpendGTTrans_RespondNotEnough(self):
        """
        Verify that if there are not enough points to spend then code 200
        returns with a message stating why the spend was not possible
        """
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr(2022,1,5,12,0,0)
        })
        rv, json = self.client.post('/api/v1/points/', data={
            'points': 101
        })
        self.assertTrue('message' in json)
        self.assertTrue(rv.status_code == 200)

    def testNegTransMustNotMakePayerNeg(self):
        """
        Verify that a negative transaction cannot set a payer's total to 0
        """
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

    