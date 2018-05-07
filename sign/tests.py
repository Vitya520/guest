from django.test import TestCase
from sign.models import Event, Guest

# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name="test event", status=True, limit=2000, address='shenzhen', start_time='2018-08-01')
        Guest.objects.create(id=1, event_id=1,realname='tester', phone='1111', email='tester@mail.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='test event')
        self.assertEqual(result.address, "shenzhen")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='1111')
        self.assertEqual(result.realname, 'tester')
        self.assertFalse(result.sign)