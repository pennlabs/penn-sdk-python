from nose.tools import ok_
from penn import Calendar
import datetime


class TestCalendar():

    def setUp(self):
        self.calendar = Calendar()

    def test_pull(self):
        cal = self.calendar.pull_3year()
        ok_(len(cal) > 0)
        for event in cal:
            ok_(len(event) == 3)

    def test_date(self):
        cal = self.calendar.pull_3year()
        ok_(len(cal) > 0)
        for event in cal:
            ok_(isinstance(event['name'], str))
            if event['name'] == "Independence Day Observed (no classes)":
                independence = event['start']
                d = datetime.datetime.strptime(independence, '%Y-%m-%d').date()
                ok_(d.month == 7)

    def test_name(self):
        cal = self.calendar.pull_3year()
        ok_(len(cal) > 0)
        for event in cal:
            ok_(isinstance(event['name'], str))
            start = datetime.datetime.strptime(event['start'], '%Y-%m-%d').date()
            end = datetime.datetime.strptime(event['end'], '%Y-%m-%d').date()
            ok_((end - start).total_seconds() >= 0)

    def test_chrono(self):
        cal = self.calendar.pull_3year()
        ok_(len(cal) > 0)
        for i, event in enumerate(cal[:-1]):
            start = datetime.datetime.strptime(event['start'], '%Y-%m-%d').date()
            nextstart = datetime.datetime.strptime(cal[i]['start'], '%Y-%m-%d').date()
            ok_((nextstart - start).total_seconds() >= 0)
