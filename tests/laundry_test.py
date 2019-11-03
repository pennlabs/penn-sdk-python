import mock

from nose.tools import ok_
from penn import Laundry


class TestLaundry():
    def setUp(self):
        self.laundry = Laundry()

    def fakeLaundryGet(url, *args, **kwargs):
        if "suds.kite.upenn.edu" in url:
            with open("tests/laundry_snapshot.html", "rb") as f:
                m = mock.MagicMock(content=f.read())
            return m
        else:
            raise NotImplementedError

    @mock.patch("requests.get", fakeLaundryGet)
    def test_all(self):
        data = self.laundry.all_status()
        ok_(len(data) > 50)
        ok_('Class of 1925' in data)
        # Check all halls have appropriate data points
        for i, hall in data.items():
            for t in ['washers', 'dryers']:
                ok_("running" in hall[t])
                ok_("open" in hall[t])

    @mock.patch("requests.get", fakeLaundryGet)
    def test_single_hall(self):
        for i in range(3):
            data = self.laundry.hall_status(i)
            machines = data['machines']
            # Check for general hall information
            ok_('washers' in machines)
            ok_('dryers' in machines)
            # Check all machines have appropriate data points
            for machine in machines["details"]:
                ok_('id' in machine)
                ok_('type' in machine)
                ok_('status' in machine)

    # def test_usage(self):
    #     for i in range(10):
    #         data = self.laundry.machine_usage(i)
    #         for j in data:
    #             ok_(j in self.laundry.days)
    #             for k in data[j]:
    #                 ok_(k in self.laundry.busy_dict.values())
