from django.test import TestCase
from catalog import models as cmod
from decimal import Decimal
import json as json

class FomoUserTestCase(TestCase):

    def test_create_a_unique_product(self):
        ## Will create a category and a unique product, then make sure the values saved and that we have access to those values
        ## Assumptions
            # User would be logged in
            # User would have the permissions to create a product

        # Create a category
        cat5 = cmod.Category()
        cat5.codename = 'st'
        cat5.name = 'Strings'
        cat5.save()

        # Create a Unique Product
        p1 = cmod.UniqueProduct()
        p1.product = p1
        p1.serial_number = '1234asdf'
        p1.name = 'Violin'
        p1.category = cat5
        p1.price = Decimal('250.99')
        dList = ['Violin hand made in 1456', 'Played be Bach and Beethoved', 'Korys favorite instrument']
        p1.descriptionList = json.dumps(dList)
        iList = ['/static/homepage/media/img/violin.jpg', '/static/homepage/media/img/violin2.png', '/static/homepage/media/img/violin3.jpg', '/static/homepage/media/img/thumbnail_violin.jpg']
        p1.imgList = json.dumps(iList)
        p1.save()

        p2 = cmod.Product.objects.get(id=p1.id)
        self.assertEquals(p2.serial_number, '1234asdf')
        self.assertEquals(p2.name, 'Violin')
        self.assertEquals(p2.category, cat5)
        self.assertEquals(p2.price, Decimal('250.99'))
        self.assertEquals(p2.descriptionList, json.dumps(dList))
        self.assertEquals(p2.imgList, json.dumps(iList))

    def test_create_a_Bulk_Product(self):
        ## Will create a category and a Bulk product, then make sure the values saved and that we have access to those values
        ## Assumptions
            # User would be logged in
            # User would have the permissions to create a product

        # Create a category
        cat4 = cmod.Category()
        cat4.codename = 'ac'
        cat4.name = 'Accessories'
        cat4.save()

        # Create a Bulk Product
        p3 = cmod.BulkProduct()
        p3.name = 'Sheet Music 1'
        p3.category = cat4
        p3.price = Decimal('9.50')
        p3.quantity = 20
        p3.reorder_trigger = 5
        p3.reorder_quantity = 30
        dList = ['Holy sheet music', 'From Beethoven to T-swizzle']
        p3.descriptionList = json.dumps(dList)
        iList = ['/static/homepage/media/img/sh1.jpg', '/static/homepage/media/img/sh2.jpg', '/static/homepage/media/img/sh3.png']
        p3.imgList = json.dumps(iList)
        p3.save()

        p4 = cmod.Product.objects.get(id=p3.id)
        self.assertEquals(p4.name, 'Sheet Music 1')
        self.assertEquals(p4.category, cat4)
        self.assertEquals(p4.price, Decimal('9.50'))
        self.assertEquals(p4.descriptionList, json.dumps(dList))
        self.assertEquals(p4.imgList, json.dumps(iList))
        self.assertEquals(p4.quantity, 20)
        self.assertEquals(p4.reorder_quantity, 30)
        self.assertEquals(p4.reorder_trigger, 5)

        # to Run
        # python3 manage.py test catalog/tests/ test_product


