MAX = 1000
class MyHashMap:

    arr: list[int]

    def __init__(self, capacity: int = MAX):
        self.capacity = capacity
        self.arr = [None for _ in range(capacity)]


    def hashFunction(self, value:str):
        return value % len(self.arr)
    
    def __str__(self):
        return str(self.arr)
    
    def findKey(self, key: int):
        for i, x in enumerate(self.arr):
            if x and key == x[0]: return i
        return -1
    
    
    def put(self, key: str, value):
        index = self.findKey(key)
        if index != -1: self.arr[index][1] = value
        else: self.arr.append([key, value])


    def get(self, key):
        index = self.findKey(key)
        if index == -1: return -1
        return self.arr[index][1]
    
    def remove(self, key):
        index = self.findKey(key)
        if index == -1: return
        del self.arr[index]
