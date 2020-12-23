def test(a):
    print(a)


def f(funk, *args):
    funk(args)


f(test, 1, 2, 3)