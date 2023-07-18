import inspect

def sir():
    print(inspect.stack()[0][3])
    print(inspect.stack()[1][3])

def sirsir():
    sir()

sirsir()
