def fact(a):
    if a > 1:
        return fact(a - 1) + fact(a - 2) + 3
    else:
        return a
    
print(fact(1))
print(fact(2))
print(fact(3))
print(fact(4))
print(fact(5))
print(fact(6))
print(fact(7))
print(fact(8))
print(fact(9))
