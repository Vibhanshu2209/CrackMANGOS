class Solution:
    def concatenatedBinary(self, n: int) -> int:


        binconcat = ""
        for i in range(n+1):
            binconcat += str(bin(i))[2:]

        return int(binconcat,2) % (10**9 + 7) 

        