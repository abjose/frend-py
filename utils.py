import ruamel.yaml


def registered_yaml():
    # for registering with yaml
    # alternately could apss class along and register it right before loading / dumping
    from friend import Friend
    from event import Event
    from interaction import Interaction

    yaml = ruamel.yaml.YAML()
    yaml.register_class(Friend)
    yaml.register_class(Event)
    yaml.register_class(Interaction)
    return yaml


def load(filename):
    with open(f"{filename}.yml", 'r') as f:
        try:
            return registered_yaml().load(f)
        except ruamel.yaml.YAMLError as exc:
            print(exc)


def save(filename, data):
    with open(f"{filename}.yml", 'w') as outfile:
        dump = registered_yaml().dump(data, stream=outfile)


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


def query_friendship_level(question=None):
    if question: print(question)
    levels = {
        "a stranger": 0,
        "a kind acquaintance": 0.25,
        "a casual friend": 0.5,
        "a very close friend": 0.75,
        "someone you love and trust": 1,
    }
    _, choice = present_options(list(levels.keys()))
    return levels[choice]


# TODO: version that allows selecting multiple options
# TODO: handle ctrl+c better (in general)
def present_options(options):
    print("Options:")
    for i in range(len(options)):
        print(f"{i+1}: {options[i]}")
    while True:
        selection = int(input(f"Enter a selection (1-{len(options)}): ")) - 1
        if 0 <= selection < len(options):
            return selection, options[selection]
        print("Invalid selection.")


def clamp(x, low, high):
    return max(low, min(x, high))


if __name__ == "__main__":
    from frend_calendar import Event
    events = load("calendar", Event)
    print("saving")
    save("bleh.yaml", events)
