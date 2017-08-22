from django.test import TestCase
from sign.models import Event,Guest
# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(
            id=1,
            name='oneplus3 event',
            status=True,
            limit=200,
            address='shenzhen',
            start_time='2016-08-31 02:18:11',
        )
        Guest.objects.create(
            id=1,
            event_id=1,
            realname='alen',
            phone='13121641251',
            email='alen@mial.com',
            sign=False

        )

    def test_event_modles(self):
        result=Event.objects.get(name='oneplus3 event')
        self.assertEqual(result.address,"shenzhen")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='13121641251')
        self.assertEqual(result.realname, "alen")
        self.assertFalse(result.sign)
