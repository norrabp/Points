import unittest
from app import create_app, PayerTotals, Transactions
from ..utils import client,timestamp


class TestSpendPositive(unittest.TestCase):
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
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr(2022,1,5,12,0,0)
        })
        rv, json = self.client.post('/api/v1/points/', data={
            'points': 100
        })
        try:
            self.assertTrue(json['Fetch'] == -100)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 0)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])

    def test1Trans1Payer1Spend_SpendLTTrans_20PointsLeft(self):
        rv, json = self.client.post('/api/v1/transactions/', data={
            'points': 100,
            'payer': 'Fetch',
            'timestamp': timestamp.getTimestampStr(2022,1,5,12,0,0)
        })
        rv, json = self.client.post('/api/v1/points/', data={
            'points': 80
        })
        try:
            self.assertTrue(json['Fetch'] == -80)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 20)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])

    def test2Trans1Payer1Spend_SpendGTEachTrans_20PointsLeft(self):
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
        rv, json = self.client.post('/api/v1/points/', data={
            'points': 180
        })
        try:
            self.assertTrue(json['Fetch'] == -180)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 20)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])

    def test2Trans2Payer1Spend_SpendGTEachTrans_SplitBetweenPayers(self):
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
        rv, json = self.client.post('/api/v1/points/', data={
            'points': 180
        })
        try:
            self.assertTrue(json['Fetch'] == -100)
            self.assertTrue(json['Epic'] == -80)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 0)
            self.assertTrue(json['Epic'] == 20)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])

    def test3Trans2Payer1Spend_SpendGTEachTrans_SplitBetweenPayers(self):
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
        rv, json = self.client.post('/api/v1/points/', data={
            'points': 201
        })
        try:
            self.assertTrue(json['Fetch'] == -101)
            self.assertTrue(json['Epic'] == -100)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        rv, json = self.client.get('/api/v1/points/')
        try:
            self.assertTrue(json['Fetch'] == 99)
            self.assertTrue(json['Epic'] == 0)
        except KeyError as e:
            self.assertTrue(False, 'Missing payer ' + e.args[0])
        
