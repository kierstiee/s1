from django.test import TestCase, Client
from django.contrib.auth.models import Group, Permission, ContentType
from django.contrib.auth import authenticate, login, logout
from account import models as amod


class UserClassTestCase(TestCase):

    def setUp(self):
        """Sets up user for every test"""
        self.u1 = amod.User()
        self.u1.first_name = 'Lisa'
        self.u1.last_name = 'Simpson'
        self.u1.email = 'lisa@simpsons.com'
        self.u1.set_password('password')
        self.u1.address = '123 S Street'
        self.u1.city = 'Springfield'
        self.u1.state = 'State'
        self.u1.zipcode = '12345'
        self.u1.save()

    def test_load_save(self):
        """Test creating, saving, and reloading a user"""
        u2 = amod.User.objects.get(email = 'lisa@simpsons.com') # or could say 'email = u1.email'
        self.assertEqual(self.u1.first_name, u2.first_name)
        self.assertEqual(self.u1.last_name, u2.last_name)
        self.assertEqual(self.u1.email, u2.email)
        self.assertTrue(u2.check_password('password'))
        self.assertEqual(self.u1.address, u2.address)
        self.assertEqual(self.u1.city, u2.city)
        self.assertEqual(self.u1.state, u2.state)
        self.assertEqual(self.u1.zipcode, u2.zipcode)

    def test_adding_group_perm(self):
        """Test adding a group w/ permissions"""
        new_group = Group(name = 'test_group')
        new_group.save()

        account = ContentType.objects.get_for_model(amod.User)
        permission = Permission(codename='change_product_price',
                                name = 'Change Price of a Product',
                                content_type = account)
        permission.save()
        new_group.permissions.add(permission)
        new_group.save()

        self.u1.groups.add(new_group)
        self.u1.save()

        test = self.u1.has_perm('account.change_product_price')
        self.assertTrue(test)

    def test_adding_user_perm(self):
        """Test adding a user w/ permissions"""
        account = ContentType.objects.get_for_model(amod.User)
        permission = Permission.objects.create(codename='add_product', name = 'Can Add Product',
                                               content_type = account)
        permission.save()

        self.u1.user_permissions.add(permission)
        self.u1.save()

        test = self.u1.has_perm('account.add_product')
        self.assertTrue(test)


    def test_log_in(self):
        """Test logging in"""
        user = authenticate(self, username = self.u1.email, password = self.u1.password)
        if user is not None:
            login(user)

        self.assertFalse(self.u1.is_anonymous)

    def test_logout(self):
        """Test logout"""
        logout(self.u1)
        self.assertTrue(self.u1.is_anonymous)

    def test_password(self):
        """Testing the password"""
        self.u1.set_password("doublecheck")
        self.u1.check_password("doublecheck")

    def test_changes(self):
        """Test random changes"""
        self.u1.first_name='Martha'
        self.assertEqual('Martha', self.u1.first_name)

        self.u1.last_name='Stewart'
        self.assertEqual('Stewart', self.u1.last_name)

        self.u1.address='456 Circle Lane'
        self.assertEqual('456 Circle Lane', self.u1.address)
