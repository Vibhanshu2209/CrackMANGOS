class MyHashSet:
    hs: set

    def __init__(self):
        self.hs = set()

    def add(self, key: int) -> None:
        if self.hs is None: self.hs = set()
        self.hs.add(key)

    def remove(self, key: int) -> None:
        if key in self.hs: self.hs.remove(key)
        

    def contains(self, key: int) -> bool:
        return key in self.hs
    