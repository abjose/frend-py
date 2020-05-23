import bisect

from utils import load, save
from friend import Friend
from frend_calendar import Event, Calendar
from interaction import Interaction

""" TODO
- add config file with stuff like:
  - start, min, max rescheduling times
  - what 01/01/11 means (see parser docs) for get_date_from_user
"""

class Frend:
    def __init__(self):
        # self.friends = []  # friend name => Friend
        # self.interactions = []  # sorted by increasing intimacy
        # self.calendar = []
        self.load()

    def run(self):
        for due_event in self.calendar.get_due_events():
            self.complete_event(due_event)

        for unscheduled_friend in self.calendar.get_unscheduled_friends(self.friends.values()):
            self.schedule_interaction(unscheduled_friend)

        # save and exit
        self.save()

    def complete_event(self, event):
        # while doing this should set a field for next time to schedule an event
        # need to record response for each friend involved!
        # how to implement "backoff"?
        # what to start with?
        # could start with some value (say, 7 days)
        # on positive responses, move towards "min" value
        # on negative responses, move towards "max" value
        # maybe leave this as a TODO?
        print("completing!", event)

    def schedule_interaction(self, friend):
        # call this
        # look up friend

        # should suggest a few possibilities
        # including a "stretch" option
        print("scheduling!", friend)

    def load(self):
        self.friends = dict([(f.intimacy, f) for f in load("friends", Friend)])
        self.calendar = Calendar(load("calendar", Event))
        self.interactions = load("interactions", Interaction)
        self.interactions.sort(key=lambda e: e.intimacy)

    def save(self):
        save("friends", list(self.friends.values()))
        save("calendar", self.calendar.events)
        save("interactions", self.interactions)  # will this ever change?


if __name__ == "__main__":
    # interactions = load("interactions", Interaction)
    # print("\n\nfinding intimacy level")
    # find_intimacy_level(empty_interaction("goal intimacy for relationship"), interactions)

    # print(get_date_from_user())

    # events = load("calendar", Event)
    # events = load("friends", Friend)

    Frend().run()
