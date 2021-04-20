"""
d = {"1": 11, "2": 22}

for p in d:
    print(type(p))
"""

"""
class NodeTest:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value


d = {
    "1": NodeTest(11),
    "2": NodeTest(22),
    "3": NodeTest(33)
}


print(max(d, key=lambda k: d[k].get_value()))
"""

l = [1, 2, 3]

print(l[::-1])