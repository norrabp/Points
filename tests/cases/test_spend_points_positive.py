import unittest
from app import create_app, PayerTotals, Transactions
from ..utils import client,timestamp


class TestSpendPositive(unittest.TestCase):
    """
    Test cases involving spending points when all transactions are positive
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
    
    
    def test1Trans1Payer1Spend_SpendEQTrans_0PointsLeft(self):
        """
        Verify that spending the total for a transaction works and sets the
        payer total to 0
        """
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr(2022,1,5,12,0,0)
        })
        rv, json = self.client.put('/api/v1/points/', data={
            'points': 100
        })
        try:
            self.assertTrue(json[0]['payer'] == 'Fetch')
            self.assertTrue(json[0]['points'] == -100)
        except KeyError as e:
            self.assertTrue(False, 'Missing ' + e.args[0])
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 0)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])

    def test1Trans1Payer1Spend_SpendLTTrans_20PointsLeft(self):
        """
        Verify that spending less than the transaction amount leaves
        some amount left to spend
        """
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr(2022,1,5,12,0,0)
        })
        rv, json = self.client.put('/api/v1/points/', data={
            'points': 80
        })
        try:
            self.assertTrue(json[0]['payer'] == 'Fetch')
            self.assertTrue(json[0]['points'] == -80)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 20)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        rv, json = self.client.put('/api/v1/points/', data={
            'points': 10
        })
        try:
            self.assertTrue(json[0]['payer'] == 'Fetch')
            self.assertTrue(json[0]['points'] == -10)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 10)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])

    def test2Trans1Payer1Spend_SpendGTEachTrans_20PointsLeft(self):
        """
        Verify that spending points over two transactions works
        """
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.put('/api/v1/points/', data={
            'points': 180
        })
        try:
            self.assertTrue(json[0]['payer'] == 'Fetch')
            self.assertTrue(json[0]['points'] == -180)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 20)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])

    def test2Trans2Payer1Spend_SpendGTEachTrans_SplitBetweenPayers(self):
        """
        Verify that spending over two transactions from different payers 
        updates each payer total
        """
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Epic',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.put('/api/v1/points/', data={
            'points': 180
        })
        try:
            self.assertTrue(json[0]['payer'] == 'Fetch')
            self.assertTrue(json[0]['points'] == -100)
            self.assertTrue(json[1]['payer'] == 'Epic')
            self.assertTrue(json[1]['points'] == -80)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 0)
            self.assertTrue(json['Epic'] == 20)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])

    def test3Trans2Payer1Spend_SpendGTEachTrans_SplitBetweenPayers(self):
        """
        Test that spending over three transactions and two payers with the
        middle transaction being a different payer will spend all of the second
        payer's points before spending on the third transaction
        """
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Epic',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr()
        })
        rv, json = self.client.put('/api/v1/points/', data={
            'points': 201
        })
        try:
            self.assertTrue(json[0]['payer'] == 'Fetch')
            self.assertTrue(json[0]['points'] == -101)
            self.assertTrue(json[1]['payer'] == 'Epic')
            self.assertTrue(json[1]['points'] == -100)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 99)
            self.assertTrue(json['Epic'] == 0)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        
