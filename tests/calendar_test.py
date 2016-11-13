from nose.tools import ok_
from penn import Calendar
import datetime

class TestCalendar():

    def setUp(self):
        self.calendar = Calendar()

    def test_pull(self):
        l = self.calendar.pull_3year()
        ok_(len(l) > 0)
        for event in l:
            ok_(len(event) == 3)

    def test_date(self):
        l = self.calendar.pull_3year()
        ok_(len(l) > 0)
        for event in l:
            if event['name'] == "Independence Day Observed (no classes)":
                independence = event['start']
                ok_(isinstance(independence, datetime.date))
                ok_(independence.month == 7)

    def test_name(self):
        l = self.calendar.pull_3year()
        ok_(len(l) > 0)
        for event in l:
            start = event['start']
            end = event['end']
            ok_((end - start).total_seconds() >= 0)

    def test_chrono(self):
        l = self.calendar.pull_3year()
        ok_(len(l) > 0)        
        for i, event in enumerate(l[:-1]):            
            start = event['start']
            nextstart = l[i]['start']
            ok_((nextstart - start).total_seconds() >= 0)