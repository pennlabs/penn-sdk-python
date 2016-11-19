from nose.tools import ok_, eq_
from penn import Laundry


class TestLaundry():

    def setUp(self):
        self.laundry = Laundry()

    def test_all(self):
        data = self.laundry.all_status()
        ok_(len(data) > 50)
        eq_('Class of 1925 House', data[0]['name'])
        # Check all halls have appropriate data points
        for i, hall in enumerate(data):
            # Not a valid check anymore because of New College House
            # eq_(hall['hall_no'], i)
            ok_(hall['dryers_available'] >= 0)
            ok_(hall['dryers_in_use'] >= 0)
            ok_(hall['washers_available'] >= 0)
            ok_(hall['washers_in_use'] >= 0)

    def test_single_hall(self):
        for i in range(1):
            data = self.laundry.hall_status(i)
            machines = data['machines']
            # Check all machines have appropriate data points
            for i, machine in enumerate(machines):
                eq_(machine['number'], str(i + 1))
                ok_('available' in machine)
                ok_('machine_type' in machine)
                ok_('time_left' in machine)

    def test_usage(self):
        for i in xrange(10):
            data = self.laundry.machine_usage(i)
            for j in data:
                ok_(j in self.laundry.days)
                for k in data[j]:
                    ok_(k in self.laundry.busy_dict.values())
