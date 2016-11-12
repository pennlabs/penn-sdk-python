from nose.tools import ok_
from penn import Calendar
import datetime

class TestCalendar():

    def setUp(self):
        self.calendar = Calendar()

    def test_pull(self):
        l = self.calendar.pull_3year()
        ok_(len(l) > 0)
        for i, event in enumerate(l[:-1]):
            ok_(len(event) == 3)
            start = event['start']
            end = event['end']
            ok_((end - start).total_seconds() >= 0)
            nextstart = l[i]['start']
            ok_((nextstart - start).total_seconds() >= 0)