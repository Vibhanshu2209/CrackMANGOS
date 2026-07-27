class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        
        maxprod = 0

        for i in range(len(nums)-1):
            for j in range(i+1, len(nums)):
                currprod = (nums[i]-1) * (nums[j]-1)
                if currprod > maxprod: maxprod = currprod

        return maxprod