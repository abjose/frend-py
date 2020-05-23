class Friend:
    def __init__(self, data):
        self.name = data["name"]  # should enforce uniqueness
        self.intimacy = float(data["intimacy"])
        self.events = []

    def __str__(self):
        # return f"Friend ({self.intimacy}): {self.name}"
        return f"{self.name}"

    def list_events(self):
        print(f"Events with {self.name}:")
        print("\n".join(map(str, self.events)))
