MAX = 1000
class MyHashMap:

    arr: list[int]

    def __init__(self, capacity: int = MAX):
        self.capacity = capacity
        self.arr = [[] for _ in range(capacity)]


    def hashFunction(self, value:str):
        return value % len(self.arr)
    
    def __str__(self):
        return str(self.arr)
    
    def findIndexForKey(self, bucket:list, key: int):
        for i, (k, v) in enumerate(bucket):
            if key == k:return i
        return -1
    
    def getBucket(self, key):
        return self.arr[key % self.capacity]
    
    def put(self, key: str, value):
        bucket = self.getBucket(key)
        index = self.findIndexForKey(bucket, key)
        if index != -1: bucket[index][1] = value
        else: bucket.append([key, value])


    def get(self, key):
        bucket = self.getBucket(key)
        index = self.findIndexForKey(bucket, key)
        if index == -1: return -1
        return bucket[index][1]
    
    def remove(self, key):
        bucket = self.getBucket(key)
        index = self.findIndexForKey(bucket, key)
        if index == -1: return
        del bucket[index]
