#!/usr/bin/python

from timeofday import TimeOfDay
import unittest
from freezegun import freeze_time


class TestTimeOfDay(unittest.TestCase):

    users = {
        'behemot': 'US/Pacific',
        'oleg': 'US/Pacific',
        'marsek': 'Europe/Moscow',
        'fedor': 'Europe/Moscow',
        'pelicano': 'Asia/Taipei'
    }

    test_time = "2016-04-20 12:00:00"

    def setUp(self):
        with freeze_time(self.test_time):
            self.tod = TimeOfDay(self.users)

    def test_get_tod(self):
        self.assertEquals(self.tod.get_tod(0), 'night')
        self.assertEquals(self.tod.get_tod(7), 'morning')
        self.assertEquals(self.tod.get_tod(13), 'day')
        self.assertEquals(self.tod.get_tod(19), 'evening')

    def test_get_hour_for_tz(self):
        with freeze_time(self.test_time):
            self.assertEqual(5, self.tod.get_hour_for_tz('US/Pacific'))
            self.assertEqual(15, self.tod.get_hour_for_tz('Europe/Moscow'))
            self.assertEqual(20, self.tod.get_hour_for_tz('Asia/Taipei'))

    def test_get_tz_for_user(self):
        self.assertEquals(self.tod.get_tz_for_user('behemot'), 'US/Pacific')
        self.assertEquals(self.tod.get_tz_for_user('oleg'), 'US/Pacific')
        self.assertEquals(self.tod.get_tz_for_user('marsek'), 'Europe/Moscow')
        self.assertEquals(self.tod.get_tz_for_user('fedor'), 'Europe/Moscow')
        self.assertEquals(self.tod.get_tz_for_user('pelicano'), 'Asia/Taipei')
        self.assertEquals(self.tod.get_tz_for_user('foobar'),
                          'Unknown user foobar.')

    def test_user_list(self):
        self.assertListEqual(self.tod.get_user_list(),
                             ['oleg', 'fedor', 'pelicano',
                              'behemot', 'marsek'])

    def test_get_hour_for_user(self):
        with freeze_time(self.test_time):
            self.assertEquals(self.tod.get_hour_for_user('behemot'), 5)
            self.assertEquals(self.tod.get_hour_for_user('oleg'), 5)
            self.assertEquals(self.tod.get_hour_for_user('marsek'), 15)
            self.assertEquals(self.tod.get_hour_for_user('fedor'), 15)
            self.assertEquals(self.tod.get_hour_for_user('pelicano'), 20)

    def test_get_tod_for_tz(self):
        with freeze_time(self.test_time):
            self.assertEquals(self.tod.get_tod_for_tz('US/Pacific'), 'morning')
            self.assertEquals(self.tod.get_tod_for_tz('Europe/Moscow'), 'day')
            self.assertEquals(self.tod.get_tod_for_tz('Asia/Taipei'),
                              'evening')

    def test_fill_all(self):
        with freeze_time(self.test_time):
            self.assertEquals(self.tod.u2tod['behemot'], 'morning')
            self.assertEquals(self.tod.u2tod['oleg'], 'morning')
            self.assertEquals(self.tod.u2tod['marsek'], 'day')
            self.assertEquals(self.tod.u2tod['fedor'], 'day')
            self.assertEquals(self.tod.u2tod['pelicano'], 'evening')

            self.assertEquals(self.tod.tod_cost['morning'], 2)
            self.assertEquals(self.tod.tod_cost['day'], 4)
            self.assertEquals(self.tod.tod_cost['evening'], 3)
            self.assertEquals(self.tod.tod_cost['night'], 0)

    # TODO: Write test for debug mode.
    def test_get_time_of_day(self):
        with freeze_time(self.test_time):
            self.assertEquals(self.tod.get_time_of_day(), 'day')


if __name__ == '__main__':
    unittest.main()
