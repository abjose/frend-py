import yaml


# expects file to be named `name`.yml
# expects main data to be in a section called `name`
def load(name, typename):
    yaml_data = None
    with open(name + ".yml", 'r') as f:
        try:
            yaml_data = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    if not yaml_data:
        print("Couldn't load yaml data from ", name)
        return

    data = []
    for d in yaml_data:
        data.append(typename(d))

    return data


def save(filename, data):
    with open(f"{filename}.yml", 'w') as outfile:
        dump = yaml.dump(data)
        outfile.write(strip_python_tags(dump))


# TODO: make use of yaml type tags?
# https://stackoverflow.com/a/55828059
def strip_python_tags(s):
    tag = "!!python/"
    result = []
    lines = s.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        idx = line.find(tag)
        if idx > -1:
            # dumb check to see if we want to pull up the next line
            line = line[:idx]
            if ": " in line:
                line = line[:-1]
            else:
                # TODO: bounds checking (though shouldn't be an issue)
                line += lines[i+1].strip()
                i += 1  # skip the next line
        result.append(line)
        i += 1
    return '\n'.join(result)


# def empty_interaction(task):
#     data = {"task": task, "intimacy": None}
#     return Interaction(data)


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
