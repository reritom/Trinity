'''
    Call all the scripts in tests.py
    create a log,
    etc
    split tests into seperate files by type

'''

def run_all():
    import tests
    for i in dir(tests):
        item = getattr(tests,i)
        if callable(item):
            print(item.__doc__)
            item()
            print("\n")

if __name__ == '__main__':
    run_all()
