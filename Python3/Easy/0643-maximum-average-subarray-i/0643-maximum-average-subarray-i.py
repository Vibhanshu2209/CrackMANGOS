class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:

        currsum = sum(nums[:k])
        max_avg = currsum/k
        left = 0
        right = k

        while right < len(nums):
            currsum += nums[right] - nums[left]
            max_avg = max(max_avg, currsum/k)
            right += 1
            left += 1

        return max_avg