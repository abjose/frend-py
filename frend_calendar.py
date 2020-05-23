import datetime

from utils import load
from dateutil import parser as date_parser
from interaction import Interaction


class Event:
    def __init__(self, data):
        self.friends = data["friends"]  # TODO: validate friends exists :(
        self.datetime = data["datetime"]
        self.interaction = Interaction(data["interaction"])

    def __str__(self):
        return f"- On {self.datetime} with {', '.join(map(str, self.friends))}:\n  {self.interaction}"


class Calendar:
    def __init__(self, events):
        # TODO: should be able to print due events and schedule new ones
        self.events = events

    def get_due_events(self):
        # sorted by oldest
        now = datetime.datetime.now()
        return sorted([e for e in self.events if e.datetime <= now], key=lambda e: e.datetime)

    def get_unscheduled_friends(self, friends):
        scheduled_friends = set()
        for event in self.events:
            scheduled_friends.update(event.friends)
        # actually should you just return the Friend objects here?
        return [f.name for f in friends if f.name not in scheduled_friends]


def get_date_from_user():
    # TODO: allow aborting
    # TODO: have relative dates like "1 week"
    while True:
        try:
            return date_parser.parse(input("Enter date: "))
        except:
            print("Couldn't parse the date, try again")


if __name__ == "__main__":
    print("woof")
    events = load("calendar", Event)
