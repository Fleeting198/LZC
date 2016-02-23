a = {'a': 1, 'b': 10}
b = {'a': 20, 'c': 5}
from collections import Counter
A,B = Counter(a),Counter(b)
z = A + B
print z