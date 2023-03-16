## link

- https://connascence.io/name.html

# Static Connascences

## Connascence of Name

Connascence of name is when multiple components must agree on the name of an entity. Method names are an example of this form of connascence: if the name of a method changes, callers of that method must be changed to use the new name.

Almost any code example involves connascence of name. Consider the following class declaration taken from the Python standard library (method implementation has been omitted for clarity):

```python
class Request:

    def __init__(self, url, data=None, headers={},
                 origin_req_host=None, unverifiable=False,
                 method=None):
        pass

    def set_proxy(self, host, type):
        pass
```

Changing the name of any part of this code will cause code that uses this class to break, including:

- Changing the class name from Request.
- Changing any of the method names (such as set_proxy).
- Changing the name of any of the parameters to either **init** or set_proxy.

Connascence of name is unavoidable, since we refer to entities using labels. If we change the name of an entity when we declare it, we must also change all code that refers to that entity. For this reason, connascence of name is the weakest connascence. However, it also illustrates how important it is to name entities in code well.

## Connascence of Type

Connascence of type is when multiple components must agree on the type of an entity. In a statically typed language, these issues are often (but not always) caught by the compiler. Consider the following trivial C++ code:

```
std::string cost;

cost = 10.95; // OOPS!
```

Dynamically typed languages typically suffer from less obvious instances of connascence of type. Consider a function that calculates your age, given your day, month, and year of birth:

```python
def calculate_age(birth_day, birth_month, birth_year): # do the calculation here:
```

How is this function supposed to be called? Here are a few different options:

```python
calculate_age(1, 9, 1984)
calculate_age(1, 9, 84)
calculate_age('1', '9', '1984')
calculate_age('1', 'September', '1984')
```

## Connascence of Meaning
Connascence of meaning is when multiple components must agree on the meaning of particular values. Consider some code that processes credit card payments. The following function might be used to determine if a given credit card number is valid or not:

```
def is_credit_card_number_valid(card_number):
    # Check for 'test' credit card numbers:
    if card_number == "9999-9999-9999-9999":
        return True
    # Do normal validation:
    # ...
```

The problem here is that all parts of this system must agree that 9999-9999-9999-9999 is the test credit card number. If that value changes in one place, it must also change in another.

Here's another example where user roles are encoded as integers:

```python
def get_user_role(username):
    user = database.get_user_object_for_username(username)
    if user.is_admin:
        return 2
    elif user.is_manager:
        return 1
    else:
        return 0
```
Elsewhere, code might need to check that a given username is an administrator, like so:

```
if get_user_role(username) != 2:
    raise PermissionDenied("You must be an administrator")
```

Connascence of meaning can be improved to connascence of name by moving the "magic values" to named constants, and referring to the constants instead of the values. However in doing so, we have increased the amount of connascence of name (since we now need a third location to store the constant).

Another common example of connascence of meaning is when None is used as a return value. This frequently occurs in functions that are tasked with finding an object. If that object isn't found, the function might return None.

```python
def find_user_in_database(username):
    return database.find_user(username=username) or None
```

However, the function might also return None in an error condition:

```
def find_user_in_database(username):
    try:
        return database.find_user(username=username) or None
    except DatabaseError:
        return None
```

The problem in both these cases is that a semantic meaning is being assigned to the None value. If multiple different meanings are assigned to the same None value in the same codebase, the programmer must remember which meaning applies to which case. This can be improved to connascence of name by returning an explicit object that represents the case in question:

```
def find_user_in_database(username):
    try:
        return database.find_user(username=username) or ObjectNotFound
    except DatabaseError:
        return None
```

We still have connascence of meaning in the error case, but at least the None value is no longer ambigous. The error case could also be improved to connascence of name in a similar way.

Another common example of connascence of meaning is when we use primitive numeric types to represent more complex values. Consider this line of code in a codebase that processes payments:

```
unit_cost = 49.95
```

What currency is that cost expressed in? US dollars? British pounds? How do you ensure that two costs with different currencies are not added together? Similar to the examples above, the problem is that a semantic meaning is being added to the primitive type. It can be improved to connascence of type by creating a 'Cost' type that disallows operations between different currencies:

```
unit_cost = Cost(49.95, 'USD')
```

This particular problem is often called "Primitive Obsession", and can be generically described as using primitive data types to represent more complex domains.

## Connascence of Position
Connascence of position is when multiple entities must agree on the order of values.

In Data Structures
For example, consider a function that retrieves a user's details:

```python
def get_user_details():
    # Returns a user's details as a list:
    # first_name, last_name, year_of_birth, is_admin
    return ["Thomas", "Richards", 1984, True]
```

This is a somewhat contrived example, but it's not uncommon to see data returned in lists or tuples. Elsewhere in the code we might need to perform some check on whether the user is an administrator or not:

```python
def launch_nukes(user):
    if user[3]:
        # actually launch the nukes
    else:
        raise PermissionDeniedError("User is not an administrator!")
```

These two functions are linked by connascence of position. If the order of the values in the user list ever changes, both locations must be updated (this example is particularly scary if someone were to update the user list to be [first_name, initials, last_name, year_of_birth, is_admin] without updating the check inside launch_nukes).

This connascence can be improved to connascence of name by turning the list into a dictionary or class. The following example shows how the above functions might look as a dictionary:

```python
def get_user_details():
    return {
        "first_name": "Thomas",
        "last_name": "Richards",
        "year_of_birth": 1984,
        "is_admin": True,
    }


def launch_nukes(user):
    if user['is_admin']:
        # actually launch the nukes
    else:
        raise PermissionDeniedError("User is not an administrator!")
```

Note that these two functions are still coupled, but we've turned connascence of position into the weaker connascence of name. This has also increased the readability of the get_user_details function - the explicit comment is no longer needed to document the order of the keys.

A similar solution is to use a class instead of a dictionary, and this can be beneficial if the structure being returned has constraints or operations associated with it.

In Function Arguments
Connascence of position also frequently occurs in function argument lists. Consider the following function declaration from a mythical email-sending utility library:

```python
def send_email(firstname, lastname, email, subject, body, attachments=None):
```

Code calling this send_email function must remember the order of arguments. Should that order ever change, all calling locations must also be updated. This example could also be improved to connascence of name by passing a structured object (a class or dictionary) instead of a number of parameters.

## Connascence of Algorithm
Connascence of algorithm is when multiple components must agree on a particular algorithm.

In Data Transmission
Connascence of algorithm frequently occurs when two entities must manipulate data in the same way. For example, if data is being transmitted from one service to another, some sort of checksum algorithm is commonly used. The sender and receiver must agree on which algorithm is to be used. If the sender changes the algorithm used, the receiver must change as well.

In Data Validation and Encoding
Consider a hypothetical piece of software that required users to provide a valid email address when creating an account. The software must validate that the email address is valid, but this might happen in several places, including:

In a database model object.
In a webapp 'controller' class method.
In a form field in the front-end UI.
These pieces of code might well be in different languages, and will almost certainly be far apart from each other. The consequence of these algorithms being different might include users not being able to register, but recieving no feedback as to why.

Another common example of connascence of algorithm is when unicode strings are written to disk. Imagine a hypothetical piece of software that writes a data string to a cache file on disk:

```python
def write_data_to_cache(data_string):
    with open('/path/to/cache', 'wb') as cache_file:
        cache_file.write(data_string.encode('utf8'))
```

A matching function is used to retrieve the data from the cache file:

```python
def read_data_from_cache():
    with open('/path/to/cache', 'rb') as cache_file:
        return cache_file.read().decode('utf8')
```

The connascence of algorithm here is that both functions must agree on the encoding being used. If the write_data_to_cache function changes to encrypt the data on disk (the data being stored is potentially sensitive), the read_data_from_cache must also be updated.

In Test Code
Test code often contains connascence of algorithm. Consider this hypothetical test:

```python
def test_user_fingerprint(self):
    user = User.new(name="Thomi Richards")
    actual = user.fingerprint()
    expected = hashlib.md5(user.name).hexdigest()
    self.assertEqual(expected, actual)
```

This test is supposed to be testing that the 'fingerprint' method of the User class works as expected. However, it contains connascence of algorithm, which limits it's effectiveness. If the User class ever changes the way fingerprints are calculated, this test will fail.
