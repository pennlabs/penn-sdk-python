from nose.tools import ok_
from penn import Calendar


class TestCalendar():

    def setUp(self):
        self.calendar = Calendar()

    def test_pull(self):
        l = self.calendar.pull_3year()
        ok_(len(l) > 0)
        for event in l:
            ok_(len(event) == 5)
            d = Calendar.range_parse(event[1], event[4])
            change = (d[1] - d[0]).total_seconds()
            ok_(change >= 0)
        years = []
        for event in l:
            if event[4]  not in years:
                years.append(event[4])
        ok_(len(years) == 2)