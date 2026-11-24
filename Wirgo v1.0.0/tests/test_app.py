"""Run after pip install: python -m unittest discover -s tests -v"""
import os
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

import database
from app import app


class WirgoAPITests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_path = database.DB_PATH
        database.DB_PATH = Path(self.temp_dir.name) / 'test.db'
        database.initialize()
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def tearDown(self):
        database.DB_PATH = self.old_path
        self.temp_dir.cleanup()

    def test_views_and_demo_data(self):
        page = self.client.get('/')
        self.assertEqual(page.status_code, 200)
        self.assertIn('Wirgo'.encode(), page.data)
        state = self.client.get('/api/state').get_json()
        self.assertEqual(len(state['attractions']), 10)
        self.assertEqual(len(state['wristbands']), 3)
        self.assertEqual(len(state['menu']), 6)

    def test_f01_create_token_band_and_pass(self):
        response = self.client.post('/api/wristbands', json={'type':'tokens','tokens':10})
        self.assertEqual(response.status_code, 201)
        band = response.get_json()['wristband']
        self.assertEqual(band['id'], 'PAS-004')
        self.assertEqual(band['balance'], 10)
        response = self.client.post('/api/wristbands', json={'type':'pass','days':3})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.get_json()['wristband']['valid_until'])
        for number in (0, -2, 'abc'):
            self.assertEqual(self.client.post('/api/wristbands', json={'type':'tokens', 'tokens':number}).status_code, 400)
        self.assertEqual(self.client.post('/api/wristbands', json={'type':'pass','days':2}).status_code, 400)

    def test_f02_balance_topup_validation_and_persistence(self):
        self.assertEqual(self.client.get('/api/wristbands/PAS-001').get_json()['wristband']['balance'],12)
        self.assertEqual(self.client.post('/api/wristbands/PAS-001/recharge', json={'amount':5}).get_json()['wristband']['balance'],17)
        self.assertEqual(self.client.post('/api/wristbands/PAS-001/recharge', json={'amount':-1}).status_code,400)
        self.assertEqual(self.client.post('/api/wristbands/PAS-003/recharge', json={'amount':5}).status_code,400)
        self.assertEqual(self.client.get('/api/wristbands/NOT-EXIST').status_code,404)
        with database.connect() as db: # directly read stored data to verify SQLite
            self.assertEqual(db.execute('SELECT zetony FROM opaska WHERE id=?', ('PAS-001',)).fetchone()[0],17)

    def test_f03_order_and_rejection(self):
        response=self.client.post('/api/orders',json={'items':[{'id':'m1','qty':2},{'id':'m5','qty':1}]})
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.get_json()['order']['total'],44)
        self.assertEqual(len(response.get_json()['order']['items']),2)
        invalid=self.client.post('/api/orders',json={'items':[{'id':'not-product','qty':2}]})
        self.assertEqual(invalid.status_code,400)
        with database.connect() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM zamowienie').fetchone()[0],1)
            self.assertEqual(db.execute('SELECT COUNT(*) FROM pozycja_zamowienia').fetchone()[0],2)

    def test_f05_attraction_status_saved(self):
        changed=self.client.patch('/api/attractions/1/status',json={'status':'Zamknięta'})
        self.assertEqual(changed.status_code,200)
        self.assertEqual(changed.get_json()['attraction']['status'],'Zamknięta')
        self.assertEqual(self.client.patch('/api/attractions/1/status',json={'status':'XYZ'}).status_code,400)
        self.assertEqual(self.client.get('/api/state').get_json()['attractions'][0]['status'],'Zamknięta')

    def test_f06_entry_tokens_insufficient_closed_and_unknown(self):
        body={'wristband_id':'PAS-001','attraction_id':1}
        approved=self.client.post('/api/entry',json=body).get_json()
        self.assertTrue(approved['allowed'])
        self.assertEqual(approved['deducted'],3)
        self.assertEqual(approved['remaining'],9)
        insufficient=self.client.post('/api/entry',json={'wristband_id':'PAS-002','attraction_id':1}).get_json()
        self.assertFalse(insufficient['allowed'])
        self.assertEqual(insufficient['reason'],'not_enough_tokens')
        unknown=self.client.post('/api/entry',json={'wristband_id':'FAKE','attraction_id':1}).get_json()
        self.assertEqual(unknown['reason'],'unknown_wristband')
        self.client.patch('/api/attractions/1/status',json={'status':'Uszkodzona'})
        unavailable=self.client.post('/api/entry',json=body).get_json()
        self.assertEqual(unavailable['reason'],'attraction_closed')
        with database.connect() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM wejscie').fetchone()[0],1)
            self.assertEqual(db.execute('SELECT zetony FROM opaska WHERE id=?',('PAS-001',)).fetchone()[0],9)

    def test_f06_pass_expires_and_seed_does_not_reset(self):
        response=self.client.post('/api/entry',json={'wristband_id':'PAS-003','attraction_id':1})
        self.assertTrue(response.get_json()['allowed'])
        with database.transaction() as db:
            db.execute('UPDATE opaska SET wazna_do=? WHERE id=?',
                      ((datetime.now()-timedelta(days=1)).isoformat(timespec='seconds'),'PAS-003'))
        self.assertEqual(self.client.post('/api/entry',json={'wristband_id':'PAS-003','attraction_id':1}).get_json()['reason'],'expired')
        self.client.post('/api/wristbands/PAS-001/recharge',json={'amount':5})
        database.initialize() # simulates rerunning DB setup; must not wipe existing data
        self.assertEqual(self.client.get('/api/wristbands/PAS-001').get_json()['wristband']['balance'],17)

    def test_kitchen_demo_status(self):
        order=self.client.post('/api/orders',json={'items':[{'id':'m1','qty':1}]}).get_json()['order']
        reply=self.client.patch(f"/api/orders/{order['id']}/status",json={'status':'W trakcie'})
        self.assertEqual(reply.status_code,200)
        self.assertEqual(self.client.get('/api/state').get_json()['orders'][0]['status'],'W trakcie')


if __name__=='__main__':
    unittest.main()
