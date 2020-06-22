import datetime

from utils import load
import parsedatetime
from interaction import Interaction


class Event:
    def __init__(self, friends, datetime, interaction):
        self.friends = friends  # TODO: validate friends exist :(
        self.datetime = datetime
        self.interaction = interaction

    def __eq__(self, other):
        return (self.friends == other.friends and self.datetime == other.datetime and
                self.interaction == other.interaction)

    def __str__(self):
        return f"- On {self.datetime} with {', '.join(map(str, self.friends))}:\n  {self.interaction}"


class Calendar:
    def __init__(self, events):
        self.events = events

    def get_due_events(self):
        # sorted by oldest
        now = datetime.datetime.now()
        return sorted([e for e in self.events if e.datetime <= now], key=lambda e: e.datetime)

    def get_unscheduled_friends(self, friends):
        scheduled_friends = set(["me"])
        for event in self.events:
            scheduled_friends.update(event.friends)
        # actually should you just return the Friend objects here?
        return [f.name for f in friends if f.name not in scheduled_friends]

    def schedule_event(self, friends, date, interaction):
        self.events.append(Event([f.name for f in friends], date, interaction))

    def remove_event(self, event):
        self.events.remove(event)

def get_date_from_user():
    # TODO: allow aborting
    # TODO: only allow future dates?
    cal = parsedatetime.Calendar()
    while True:
        try:
            time_struct, parse_status = cal.parse(input("Enter date or interval: "))
            return datetime.datetime(*time_struct[:6])
        except KeyboardInterrupt:
            return datetime.datetime.now()  # ehh
        except:
            print("Couldn't parse the date, try again")


if __name__ == "__main__":
    print(get_date_from_user())
