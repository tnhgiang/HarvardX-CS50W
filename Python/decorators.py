def announce(f):
    # Announce decorator take f function of a input
    def wrapper():
        print('About to run the function...')
        f()
        print('Done with the function...')
    
    return wrapper

# annouce is a decorator

@announce
def hello():
    print('Hello, world!')

hello()