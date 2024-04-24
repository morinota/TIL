## refs

https://medium.com/@m.nusret.ozates/good-design-practices-with-python-design-by-contract-a2a2d07b37d0

# Good Design Practices with Python — Design by Contract

## Introduction

As software engineers, we write code most of the time. We have some tight deadlines and because of these deadlines, we tend to write code fast without thinking about the design. This choice comes with consequences. It actually makes you slower because you write the code so urgently that you forgot that client’s requests will change faster than you thought and when that time comes to you, it will be very hard to change your code. You will look at the code and say “oh I need to change this part and it is done” and then you will realize that the change broke a completely different part of the code, you will change that too and realize this change broke another part of your code and so on…

We don’t want that, think before coding, and give yourself some time to design architecture. Think about how you could test that chunk of code and only after that start coding. To make your life easier, there are some design “principals” out there and I will explain them with examples using Python. This is part 1 and I will explain “Design by Contract” in this part.

## Design by Contract

We write code to be used by some clients using APIs or libraries. When creating a function, we decide what is needed for making that function run and what we will return if conditions are met. For a basic example:

```python
def sum(first: int, second: int) -> int:

	return first + second
```

In this function, we basically say “I want you to give me to integer and as a result, I will give you another integer, which is the sum of these two integers”. If we don’t check the type of the variables, our program will crash or not work as expected. This was a basic example and you shouldn’t think that “Oh okay it is just type checking!”. Because just doing this would be just trying to make python a statically typed language.

To make a function work properly, we need to design a contract. A contract has these elements:

Preconditions: They are checks we need to do before running the function. If these values are not as expected, running the function would be pointless. We could check for the type of the parameter, the value range of the parameter, or maybe if it is a string and we are expecting that string must contain an e-mail, we should check if it contains an e-mail using a regex. If there is a problem with the condition check, we need to raise an exception with a meaningful message. We can even raise a custom exception if needed.

Postconditions: This is what we promise to give. We need to check if the returned value of our function satisfies the conditions of what we will promise to give. If these conditions return False, which means there is a problem with our code.

Let’s do an example:

```python
from typing import Union

def check_id(user_id: str) -> bool:
    """
    Check if user_id is valid
    Args:
        user_id: user id
    Returns:
        True if user_id is valid, raise Error otherwise
    """
    if not isinstance(user_id, str):
        raise TypeError("user_id must be a string")
    if not user_id.isdigit():
        raise ValueError("user_id must be a number")
    if not len(user_id) == 8:
        raise ValueError("user_id must be 8 digits")
    return True


def get_user(user_id: str) -> Union[User, None]:
    """ Get user info from database

    Args:
        user_id: user id
    Returns:
         User object
    """
    return User.from_id(user_id)


def check_user(user: User):
    """
    Check if user is valid
    Args:
        user: user object
    Returns:
        Nothing if user is valid, raise Error otherwise
    """
    if user is None:
        raise ValueError("user not found")


def user_info(user_id: str) -> User:
    """ Get user info from database
    user_id must be valid:
        - user_id must be a string
        - user_id must be a number
        - user_id must be 8 digits

    Args:
        user_id: user id
    Returns:
        User object if user_id is valid and user can be found, raise Error otherwise
    """
    check_id(user_id)
    user = get_user(user_id)
    check_user(user)
    return user
```

This is still not an advanced example but I think it gives a good idea. First, we check if the given input is a string with a length of 8 and contains only digits. Then we search for the user and check if we can give the result as promised. If we can’t we return an error.

> Don’t forget that you need to document those conditions in the docstrings!

Now a little bit fun part! I have access to Github Copilot and just wrote: “ # Design by contract example” and add a “def” to help it. Here is the beautiful result for checking preconditions using annotations:

```python
# Design by contract example

def contract(func):
    def wrapper(*args, **kwargs):
        if len(args) + len(kwargs) != func.__code__.co_argcount:
            raise TypeError("Wrong number of arguments")
        return func(*args, **kwargs)

    return wrapper


@contract
def add(x, y):
    return x + y
```

By using the design by contract, you can be sure where was the problem if the function doesn’t work. As result, you will have more robust code. Using this approach will cause doing extra work but it will be better for you in the long run. At least, you should use this approach in the critical parts of your program.

And that’s all! Thank you for reading!
