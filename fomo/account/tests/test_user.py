from django.test import TestCase
from account import models as amod
from datetime import datetime
from django.utils import timezone

class FomoUserTestCase(TestCase):

    def test_create_a_user(self):
        ## Will create a user, then make sure the values were saved and that we have access to those values
        ## Assumptions
            # User would be signed in
            # User would have the permissions to create a user
        u1 = amod.FomoUser()
        u1.first_name = 'Mike'
        u1.last_name = 'W'
        u1.set_password("password")
        u1.birth_date = timezone.now()
        u1.email = 'mike@monster.com'
        u1.username = "user1"
        u1.gender = "female"
        u1.save()

        u2 = amod.FomoUser.objects.get(id=u1.id)
        self.assertEquals(u2.first_name, 'Mike')
        self.assertEquals(u2.last_name, 'W')
        self.assertEquals(u2.email, 'mike@monster.com')
        self.assertEquals(u2.username, 'user1')
        self.assertEquals(u2.gender, 'female')

        # to Run
        # python3 manage.py test account/tests/

    def test_edit_a_user(self):
        ## Will create a user and then change those values, then make sure the values were saved and that we have access to those values,
        ## Assumptions
            # User would be signed in
            # User would have the permissions to edit a user
        u1 = amod.FomoUser()
        u1.first_name = 'Mike'
        u1.last_name = 'W'
        u1.set_password("password")
        u1.birth_date = timezone.now()
        u1.email = 'mike@monster.com'
        u1.username = "user1"
        u1.gender = "female"
        u1.save()

        u1.first_name = 'Wilson'
        u1.last_name = 'M'
        u1.set_password("pw")
        u1.birth_date = timezone.now()
        u1.email = 'wilson@monster.com'
        u1.username = "user2"
        u1.gender = "male"
        u1.save()

        self.assertEquals(u1.first_name, 'Wilson')
        self.assertEquals(u1.last_name, 'M')
        self.assertEquals(u1.email, 'wilson@monster.com')
        self.assertEquals(u1.username, 'user2')
        self.assertEquals(u1.gender, 'male')


