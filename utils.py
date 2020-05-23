import yaml


# expects file to be named `name`.yaml
# expects main data to be in a section called `name`
def load(name, typename):
    yaml_data = None
    with open(name + ".yml", 'r') as f:
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
        # print(data[-1])

    return data


def save(filename, data):
    with open(f"{filename}.yml", 'w') as outfile:
        yaml.dump(data, outfile)#, default_flow_style=False)


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
    from frend_calendar import Event
    events = load("calendar", Event)
    print("saving")
    save("bleh.yaml", events)
