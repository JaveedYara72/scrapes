b = 1
c = 1
def func(b):
    b = b + 1
    print(b)
    c = b
    print(c)

    print('outside')

func(b)

print(b)
print(c)
