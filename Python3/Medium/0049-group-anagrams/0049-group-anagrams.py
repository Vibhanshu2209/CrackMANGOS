class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:

        groups = {}

        for i in strs:
            sag = "".join(sorted(i))
            if sag not in groups: groups[sag] = []
            groups[sag].append(i)

        return list(groups.values())

        