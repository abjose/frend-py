import datetime, parsedatetime
from utils import load
from interaction import Interaction


class Event:
    def __init__(self, friends, date, interaction, interval):
        self.friends = friends  # TODO: validate friends exist :(
        self.date = date
        self.save_timedelta(interval)
        self.interaction = interaction

    def __eq__(self, other):
        return (self.friends == other.friends and self.date == other.date and
                self.interaction == other.interaction)

    def __str__(self):
        string = f"- with {', '.join(map(str, self.friends))} on {self.date}"
        if self.recurring:
            string += f", recurring every {self.recurring}"
        string += f":\n  {self.interaction}"
        return string

    # Saving timedeltas as datetimes related to datetime(1,1,1).
    # TODO: get yaml to properly save timedeltas and remove this hack.
    def save_timedelta(self, timedelta):
        self.recurring = datetime.datetime(1,1,1) + timedelta
    def get_timedelta(self):
        return self.recurring - datetime.datetime(1,1,1)

    def recur(self):
        # Add on recurring date to current date.
        if not self.recurring: return None
        self.date += self.get_timedelta()


class Calendar:
    def __init__(self, events):
        self.events = events

    def get_due_events(self):
        # sorted by oldest
        now = datetime.datetime.now()
        return sorted([e for e in self.events if e.date <= now], key=lambda e: e.date)

    def get_unscheduled_friends(self, friends):
        scheduled_friends = set(["me"])
        for event in self.events:
            scheduled_friends.update(event.friends)
        # actually should you just return the Friend objects here?
        return [f.name for f in friends if f.name not in scheduled_friends]

    def schedule_event(self, friends, date, interaction, interval=None):
        self.events.append(Event([f.name for f in friends], date, interaction, interval))

    def remove_event(self, event):
        self.events.remove(event)

def get_date_from_user(interval=False):
    # TODO: allow aborting
    # TODO: only allow future dates?
    cal = parsedatetime.Calendar()
    while True:
        try:
            time_struct, parse_status = cal.parse(input("Enter date or interval: "))
            parsed = datetime.datetime(*time_struct[:6])
            if interval:
                return parsed - datetime.datetime.now()
            return parsed
        except KeyboardInterrupt:
            return None  # ehh
        except:
            print("Couldn't parse the date, try again")


if __name__ == "__main__":
    print(get_date_from_user(interval=True))
