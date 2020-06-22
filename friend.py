from utils import clamp
from interests import query_interests


class Friend:
    def __init__(self, name, intimacy, goal_intimacy, past_events,
                 likes, dislikes):
        self.name = name  # TODO: should enforce uniqueness
        self.intimacy = float(intimacy)
        self.goal_intimacy = float(goal_intimacy)
        self.past_events = past_events

        # For now these are just "interests" tags.
        self.likes = set(likes)
        self.dislikes = set(dislikes)

    def __str__(self):
        return f"{self.name}"

    def list_events(self):
        print(f"Events with {self.name}:")
        print("\n".join(map(str, self.events)))

    def complete_event(self, event):
        # TODO: implement "backoff" when something goes badly
        # could start with some value (say, 7 days)
        # on positive responses, move towards "min" value
        # on negative responses, move towards "max" value
        # Not sure about this wording - can imagine being in a state of mind where can't imagine
        # anyone enjoying spending time with you.
        response = input(f"Do you think {self.name} enjoyed this interaction? (y/n): ")
        self.update_intimacy(event, response == "y")

        # Ask about new interests
        print("Any new interests you learned about?")
        new_interests = query_interests(self)
        # TODO: ruamel uses "CommentedSets" which doesn't have update, figure out how to use set instead
        for new_interest in new_interests:
            self.likes.add(new_interest)

        # Move to past_events
        self.past_events.append(event)

    def update_intimacy(self, event, positive_reponse):
        # TODO: make this better
        # Trying to approximate true intimacy
        # If response was positive or negative  and we didn't expect it to be,
        # proportionally change intimacy.
        if ((positive_reponse and event.interaction.intimacy > self.intimacy) or
            (not positive_reponse and event.interaction.intimacy <= self.intimacy)):
            # Expected to go well, decrease intimacy
            delta = (event.interaction.intimacy - self.intimacy) * 0.1
            delta = clamp(delta, -0.1, 0.1)
            self.intimacy = clamp(self.intimacy + delta, 0, 1)
