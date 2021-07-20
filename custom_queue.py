class CustomQueue:
    def __init__(self):
        self.loops = {}
        self.data = {}

    def set_loop(self, id, value):
        self.loops[id] = value

    def get_loop(self, id):
        if not id in self.loops:
            return False
        return self.loops[id]

    def add(self, id, audio_name):
        if id in self.data:
            self.data[id].append(audio_name)
        else:
            self.data[id] = [audio_name]

    def clear(self, id):
        self.data[id] = []
        self.loops[id] = False

    def pop(self, id):
        if not id in self.data or self.data[id] == []:
            return None
        return self.data[id].pop(0)

    def front(self, id):
        if not id in self.data or self.data[id] == []:
            return None
        return self.data[id][0]

    def get_len(self, id):
        if not id in self.data:
            return 0
        return len(self.data[id])
