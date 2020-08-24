# Python

**Python**: Python is a very powerful language that makes it very easy to build applications quickly, because there are a lot of features that built into the language.

**Python Decorators**: Decorators are the way in Python of taking a function, modifying that function and adding some additional behavior to that function.
- Idea: Decorator is going to be a function that takes a function of input and returns a modified version of that function as output
- Pros: Decorators are very powerful tool that can be able to quickly take a function and add capability to it. 
    ```python
    def logged_in(f):
        # Define the decorator that is to check if
        # an available user whether logged in or didn't
        if user_logged_in:
            # If a user logged in, do f function
            f()
        else:
            # Do nothing
            pass
    
    # Add logged_in decorator to make sure that a user has logged in
    @logged_in
    def transfer_money()
        # Money is transfered
    ```

**Functional programming paradigm**: Python considers a function as a value that can be passed like input to another function or get it as the output of another function.

**Lambda expression**: Lambda expression is to represent a very short, one-line function in a easier way

**Exception**: Exception is to handle the possible exceptional cases where things might go wrong