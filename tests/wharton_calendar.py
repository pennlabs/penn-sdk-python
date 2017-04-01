from nose.tools import ok_
from penn import whartonCalendar
import datetime

class TestCalendar():

    def setUp(self):
        self.calendar = Calendar()

    def test_pull(self):
        l = self.whartonCalendar.pull_wharton_events_on_date('2015-09-16')
        ok_(len(l) == 9)
        for event in l:
            ok_(len(event) == 5)

    def test_time(self):
        l = self.whartonCalendar.pull_wharton_events_on_date('2015-09-16')
        ok_(len(l) == 9)
        for event in l:
            ok_(isinstance(event['title'], str))
            if event['name'] == 'Research to Go':
                ok_(event['startTime'] == '12:30 PM')

    def test_time(self):
        l = self.whartonCalendar.pull_wharton_events_on_date('2015-09-16')
        ok_(len(l) > 0)
        for event in l:
            ok_(isinstance(event['name'], str))
            start = datetime.datetime.strptime(event['startTime'], '%I:%M %p').date()
            end = datetime.datetime.strptime(event['endTime'], '%I:%M %p').date()
            ok_((end - start).total_seconds() >= 0)

    def test_chrono(self):
        l = self.whartonCalendar.pull_wharton_events_on_date('2015-09-16')
        ok_(len(l) > 0)        
        for i, event in enumerate(l[:-1]):            
            start = datetime.datetime.strptime(event['startTime'], '%Y-%m-%d').date()
            nextstart = datetime.datetime.strptime(l[i]['startTime'], '%Y-%m-%d').date()
            ok_((nextstart - start).total_seconds() >= 0)
