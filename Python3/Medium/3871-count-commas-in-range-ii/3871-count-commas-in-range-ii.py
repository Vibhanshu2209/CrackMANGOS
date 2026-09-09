class Solution:
    def countCommas(self, n: int) -> int:
        if n < 1000: return 0

        totalcommas = 0
        jump = 1000
        while n >= jump:
            totalcommas += (n - jump + 1)
            jump *= 1000

        return totalcommas



        