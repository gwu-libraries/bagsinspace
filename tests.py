import unittest

import inventory as inv
import settings


settings.INVENTORY_CREDENTIALS = settings.inventory_sandbox


#@skipIf(not all([sandbox.get(k) for k in sandbox.keys() if k != 'verify_ssl_cert']),
#    'sandbox inventory not set')
class InventoryTestCase(unittest.TestCase):

    def setUp(self):
        '''setUp is also a test of the post method'''
        # create a machine object
        mdata = {"url": "http://storage1.gwu.edu", "name": "Test Machine 1"}
        res1 = inv._post('machine', **mdata)
        self.assertEqual(res1.status_code, 201)
        self.machine_id = inv.parse_id(res1.headers['location'])
        # create a collection object
        cdata = {"name": "Test Collection 1", "created": "2013-06-01",
            "description": "testy", "manager": "Lemmy Kilmeister",
            "access_loc": "http://diglib.gwu.edu/collection/1"}
        res2 = inv._post('collection', **cdata)
        self.assertEqual(res2.status_code, 201)
        self.collection_loc = res2.headers['location']
        self.collection_id = inv.parse_id(res2.headers['location'])
        self.collection_uri = inv.parse_id(res2.headers['location'], uri=True)
        # create a project object
        pdata = {"name": "Test Project 1",
            "collection": inv.parse_id(res2.headers['location'], uri=True)}
        res3 = inv._post('project', **pdata)
        self.assertEqual(res3.status_code, 201)
        self.project_id = inv.parse_id(res3.headers['location'])
        self.project_uri = inv.parse_id(res3.headers['location'], uri=True)
        # create an item object
        idata = {"title": "Test Item 1", "local_id": "123456789",
            "collection": self.collection_uri,
            "project": self.project_uri,
            "created": "2013-06-01",
            "original_item_type": "1", "notes": "nonoteworthynotes",
            "access_loc": ""}
        res4 = inv._post('item', **idata)
        self.assertEqual(res4.status_code, 201)
        self.item_id = inv.parse_id(res4.headers['location'])
        # create an access bag object
        bdata = {"bagname": "Test Bag 1", "created": "2013-06-01",
            "item": inv.parse_id(res4.headers['location'], uri=True),
            "machine": inv.parse_id(res1.headers['location'], uri=True),
            "path": "mount1/bag1", "bag_type": "1"}
        res5 = inv._post('bag', **bdata)
        self.assertEqual(res5.status_code, 201)
        self.bag1_id = inv.parse_id(res5.headers['location'])
        # create a preservation bag object
        bdata = {"bagname": "Test Bag 2", "created": "2013-06-01",
            "item": inv.parse_id(res4.headers['location'], uri=True),
            "machine": inv.parse_id(res1.headers['location'], uri=True),
            "path": "mount1/bag2", "bag_type": "2"}
        res6 = inv._post('bag', **bdata)
        self.assertEqual(res6.status_code, 201)
        self.bag2_id = inv.parse_id(res6.headers['location'])
        # create an item object similar to item 1
        i2data = {"title": "Test Item 2", "local_id": "none",
            "collection": self.collection_uri,
            "project": self.project_uri,
            "created": "2013-06-01",
            "original_item_type": "1", "notes": "none",
            "access_loc": "http://diglib.gwu.edu/item/2"}
        res7 = inv._post('item', **i2data)
        self.assertEqual(res7.status_code, 201)
        self.item2_id = inv.parse_id(res7.headers['location'])
        # create a bag object
        bdata = {"bagname": "Test Bag 3", "created": "2013-06-01",
            "item": inv.parse_id(res7.headers['location'], uri=True),
            "machine": inv.parse_id(res1.headers['location'], uri=True),
            "path": "mount1/bag3", "bag_type": "1"}
        res8 = inv._post('bag', **bdata)
        self.assertEqual(res8.status_code, 201)
        self.bag3_id = inv.parse_id(res8.headers['location'])

    def tearDown(self):
        '''tearDown is also a test of the delete method'''
        # delete all objects created in setUp
        # go in reverse order until cascade rules have been removed from inventory
        res8 = inv._delete('bag', self.bag3_id)
        self.assertEqual(res8.status_code, 204)
        res7 = inv._delete('bag', self.bag2_id)
        self.assertEqual(res7.status_code, 204)
        res6 = inv._delete('bag', self.bag1_id)
        self.assertEqual(res6.status_code, 204)
        res5 = inv._delete('item', self.item2_id)
        self.assertEqual(res5.status_code, 204)
        res4 = inv._delete('item', self.item_id)
        self.assertEqual(res4.status_code, 204)
        res3 = inv._delete('project', self.project_id)
        self.assertEqual(res3.status_code, 204)
        res2 = inv._delete('collection', self.collection_id)
        self.assertEqual(res2.status_code, 204)
        res1 = inv._delete('machine', self.machine_id)
        self.assertEqual(res1.status_code, 204)

    def test_bags_to_import(self):
        bags = inv.bags_to_import(self.collection_id)
        print bags
        self.assertEqual(len(bags), 1)


if __name__ == '__main__':
    unittest.main()
