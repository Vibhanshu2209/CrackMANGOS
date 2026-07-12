# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def getDecimalValue(self, head: Optional[ListNode]) -> int:

        numAsStr = ""
        if not head: return 0
        curr = head

        while curr:
            numAsStr += str(curr.val)
            curr = curr.next

        return int(numAsStr, 2)


        