import yaml
import bisect

class Friend:
    def __init__(self, data):
        self.name = data["name"]
        self.intimacy = float(data["intimacy"])

    def __str__(self):
        return f"Friend ({self.intimacy}): {self.name}"

class Interaction:
    def __init__(self, data):
        self.task = data["task"]
        self.intimacy = data["intimacy"]
        if self.intimacy is not None: self.intimacy = float(self.intimacy)

    def __lt__(self, other):
        if self.intimacy is None or other.intimacy is None:
            print(f"1: {self}")
            print(f"2: {other}")
            response = input("Is 1 more intimate than 2? (y/n): ")
            return response != "y"  # brittle
        return self.intimacy < other.intimacy
        
    def __str__(self):
        intimacy_str = ""
        # if self.intimacy is not None:
        #     intimacy_str = f" (intimacy {self.intimacy})"
        return f"{self.task}" + intimacy_str

class Event:
    def __init__(self):
        # just a date and an interaction?
        pass1

class Frend:
    def __init__(self):
        self.friends = []
        self.interactions = []  # sorted by increasing intimacy

    def add_interaction(self, interaction):
        pass

    def load():
        self.friends = load("friends", Friend)
        self.interactions = load("interactions", Interaction)
        self.interactions.sort(key=lambda e: e.intimacy)

# expects file to be named `name`.yaml
# expects main data to be in a section called `name`
def load(name, typename):
    yaml_data = None
    with open(name + ".yaml", 'r') as f:
        try:
            yaml_data = yaml.safe_load(f)[name]
        except yaml.YAMLError as exc:
            print(exc)

    if not yaml_data:
        print("Couldn't load yaml data from ", filename)
        return
            
    data = []
    for d in yaml_data:
        data.append(typename(d))
        print(data[-1])

    return data

def empty_interaction(task):
    data = {"task": task, "intimacy": None}
    return Interaction(data)

# TODO: allow seeding a guessed intimacy level
def find_intimacy_level(new_interaction, interactions):
    # return a intimacy level after asking a series of comparison questions
    blah = bisect.bisect_left(interactions, new_interaction)
    print(blah)
    # how to properly set intimacy? really depends on what is on either side of the insertion point
    # if very similar maybe just do in-between
    # if very different...

    # can also use this for resetting interaction intimacy levels?
    # like just insert each thing into the list with a cleared intimacy value


if __name__ == "__main__":
    interactions = load("interactions", Interaction)
    print("\n\nfinding intimacy level")
    find_intimacy_level(empty_interaction("goal intimacy for relationship"), interactions)
