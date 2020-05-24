import bisect

from utils import load, save, present_options
from friend import Friend
from frend_calendar import Event, Calendar, get_date_from_user
from interaction import Interaction

""" TODO
- add config file with stuff like:
  - start, min, max rescheduling times
  - what 01/01/11 means (see parser docs) for get_date_from_user
  - "fudge" factors in schedule_interactions (for left and right intimacy bound)
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
        # should you ask if want to increase or not? but that's the point of setting a goal level
        for friend_name in event.friends:
            self.friends[friend_name].past_events.append(event)
        self.calendar.remove_event(event)

    def schedule_interaction(self, friend_name):
        print("Scheduling a new event with", friend_name)
        # make "fudge" factors configurable
        friend = self.friends[friend_name]
        left_bound = bisect.bisect_left(self.interactions, friend.intimacy - .1)
        right_bound = bisect.bisect_right(self.interactions, friend.intimacy + .1)
        # TODO: allow skipping
        interaction = present_options(self.interactions[left_bound:right_bound+1])
        print("choice:", interaction)
        # TODO: come up with a suggested date (see notes in complete_event)
        date = get_date_from_user()
        # TODO: allow multi-friend events? maybe not in here though
        #       could just ask if they want to add more friends
        self.calendar.schedule_event([friend], date, interaction)

    def load(self):
        self.friends = dict([(f.name, f) for f in load("friends", Friend)])
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
