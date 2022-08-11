#in dict
dict = [100,3,22]

def max():
    if dict[0] > dict[1] and dict[2]:
        print(dict[0], " is high number in dict")
    elif dict[1] > dict[2]:
        print(dict[1], " is high number in dict")
    else:
        print(dict[2], " is high number in dict")

max()

#using argument passing
def maxx(a,b,c):
    if a > b and a > c:
        print(a)
    elif b > c:
        print(b)
    else:
        print(c)

maxx(200,1000,88)
