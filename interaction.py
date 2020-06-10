""" TODO
data to track:
- level of intimacy
- interest tags
- "setting" tag? like if happens at work, etc. - to try to get to know people in more contexts
- some hierarchy info? like if it's an instance of another one (like "go to this specific club" vs. "goto a club"
- whether it's sustained / can recur

intimacy scale, from 0 to 1
- 0:    a stranger
- 0.25: a kind acquaintance
- 0.5:  a casual friend
- 0.75: a very close friend
- 1:    someone you love and trust
"""

class Interaction:
    def __init__(self, task, intimacy, tags):
        self.task = task
        self.intimacy = intimacy
        self.tags = set(tags)

    def __lt__(self, other):
        other_intimacy = other if type(other) is float else other.intimacy
        if self.intimacy is None or other_intimacy is None:
            # Ask the user
            print(f"1: {self}")
            print(f"2: {other}")
            response = input("Is 1 more intimate than 2? (y/n): ")
            return response != "y"  # brittle
        return self.intimacy < other_intimacy

    def __eq__(self, other):
        if type(other) is float:
            return self.intimacy == other

        return self.task == other.task and self.intimacy == other.intimacy

    def __gt__(self, other):
        return not self == other and not self < other

    def __str__(self):
        intimacy_str = ""
        if self.intimacy is not None:
            intimacy_str = f" ({self.intimacy})"
        return f"{self.task}" + intimacy_str


if __name__ == "__main__":
    # quick tool to populate interest tags, should integrate into Frend
    from interests import Interests
    from friend import Friend
    from utils import load, save

    print("Enter nothing to progress to next interaction")

    interests = Interests()

    # interactions = load("interactions")
    # for interaction in interactions:
    #     while True:
    #         print("Adding tags to:", str(interaction))
    #         response = interests.query_for_interest()
    #         if response == "":
    #             break
    #         interaction.tags.add(response)
    #         save("interactions", interactions)

    friends = dict([(f.name, f) for f in load("friends")])
    for friend_name in friends:
        while True:
            print("Adding tags to:", friend_name)
            response = interests.query_for_interest()
            if response == "":
                break
            friends[friend_name].likes.add(response)
            save("friends", list(friends.values()))
