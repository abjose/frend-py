import bisect

from utils import load, save, present_options, query_friendship_level
from friend import Friend
from frend_calendar import Event, Calendar, get_date_from_user
from interaction import Interaction

""" TODO
- add config file with stuff like:
  - start, min, max rescheduling times
  - what 01/01/11 means (see parser docs) for get_date_from_user
  - "fudge" factors in schedule_interactions (for left and right intimacy bound)
- add comments to things so hideshow works better
"""

class Frend:
    def __init__(self):
        # self.friends = []  # friend name => Friend
        # self.interactions = []  # sorted by increasing intimacy
        # self.calendar = []
        self.load()

    def run(self):
        options = []

        due_events = self.calendar.get_due_events()
        if len(due_events) > 0:
            options.append(f"Process due events ({len(due_events)} pending)")

        unscheduled_friends = self.calendar.get_unscheduled_friends(self.friends.values())
        if len(unscheduled_friends) > 0:
            options.append(f"Schedule unscheduled friends ({len(unscheduled_friends)} pending)")

        options += [
            "Add a friend",
            "Edit a friend",
            "Add an event",
            "Edit an event",
            "Start a new recurring event",
        ]

        # TODO: don't switch on string values
        _, selection = present_options(options)
        if "Process due events" in selection:
            self.process_due_events(due_events)
        elif "Schedule unscheduled friends" in selection:
            self.schedule_unscheduled_friends(unscheduled_friends)
        elif "Add a friend" == selection:
            self.add_friend()
        elif "Edit a friend" == selection:
            self.edit_friend()
        else:
            print("Unhandled selection:", selection)

        # save and loop
        self.save()
        self.run()

    def process_due_events(self, due_events):
        for due_event in due_events:
            self.complete_event(due_event)

    def complete_event(self, event):
        print("Collecting data for the following event:")
        print(event)
        for friend_name in event.friends:
            self.friends[friend_name].complete_event(event)
        self.calendar.remove_event(event)

    def schedule_unscheduled_friends(self, unscheduled_friends):
        for unscheduled_friend in unscheduled_friends:
            self.schedule_interaction(unscheduled_friend)

    def add_friend(self):
        # TODO: replace explicit friend level choice with binary interaction search?
        name = input("What's their name?: ")
        data = {
            "name": name,
            "intimacy": query_friendship_level("About how well do you  know {name}?"),
            "goal_intimacy": query_friendship_level("How well would you like to know {name}?"),
            "past_events": [],
        }
        self.friends[name] = Friend(data)
        print(f"Successfully added {name}")

    def edit_friend(self):
        print("Which friend would you like to edit?")
        _, friend_name = present_options(list(self.friends.values()))
        # TODO, though maybe just have them edit the text file
        pass

    # TODO: move this into friend.py?
    def schedule_interaction(self, friend_name):
        print("Scheduling a new event with", friend_name)
        # make "fudge" factors configurable
        friend = self.friends[friend_name]
        # TODO: take goal intimacy into account
        left_bound = bisect.bisect_left(self.interactions, friend.intimacy - .1)
        right_bound = bisect.bisect_right(self.interactions, friend.intimacy + .1)
        # TODO: allow skipping
        _, interaction = present_options(self.interactions[left_bound:right_bound+1])
        print("choice:", interaction)
        # TODO: come up with a suggested date (see notes in complete_event)
        date = get_date_from_user()
        # TODO: allow multi-friend events? maybe not in here though
        #       could just ask if they want to add more friends
        self.calendar.schedule_event([friend], date, interaction)

    def load(self):
        self.friends = dict([(f.name, f) for f in load("friends.yml")])
        self.calendar = Calendar(load("calendar.yml"))
        self.interactions = load("interactions.yml")
        self.interactions.sort(key=lambda e: e.intimacy)

    def save(self):
        save("friends", list(self.friends.values()))
        save("calendar", self.calendar.events)
        save("interactions", self.interactions)  # will this ever change?


if __name__ == "__main__":
    Frend().run()
