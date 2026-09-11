from collections import Counter
class Solution:


    def totalNumbers(self, digits: list[int]) -> int:
        counts = Counter(digits) 
        distinct_evens = 0
    
        # Iterate through all possible 3-digit even numbers
        for num in range(100, 1000, 2):
            d1 = num // 100        # Hundreds digit
            d2 = (num // 10) % 10  # Tens digit
            d3 = num % 10          # Units digit (even)
        
            # Count frequency of digits needed for the current number
            needed = Counter([d1, d2, d3])
        
            # Check if the input digits array contains enough of each needed digit
            if all(counts[d] >= count for d, count in needed.items()):
                distinct_evens += 1
            
        return distinct_evens