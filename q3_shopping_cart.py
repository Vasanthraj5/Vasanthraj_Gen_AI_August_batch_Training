# ============================================
# Q3 - Shopping Cart with Default & Mutable Pitfall
# ============================================


# ------------------------------------------------
# Part A - Spot the Bug
# ------------------------------------------------

def add_item_bug(item, cart=[]):
    cart.append(item)
    return cart


print("Part A - Mutable Default Argument Bug")
print(add_item_bug("apple"))
print(add_item_bug("banana"))
print(add_item_bug("milk", cart=["bread"]))
print(add_item_bug("eggs"))


# ------------------------------------------------
# Part B - Correct Version
# ------------------------------------------------

def add_item(item, cart=None):
    # None is immutable and is used as a safe default.
    # A new list is created every time cart is None.
    if cart is None:
        cart = []

    cart.append(item)
    return cart


print("\nPart B - Correct Version")
print(add_item("apple"))
print(add_item("banana"))
print(add_item("milk", cart=["bread"]))
print(add_item("eggs"))


# ------------------------------------------------
# Part C - Build the Shopping Cart
# ------------------------------------------------

def create_cart(owner, discount=0):
    return {
        "owner": owner,
        "items": [],
        "discount": discount
    }


def add_to_cart(cart, name, price, qty=1):
    cart["items"].append({
        "name": name,
        "price": price,
        "qty": qty
    })


def update_price(price_tuple, new_price):
    # Tuples are immutable, so their elements cannot be changed.
    # Trying to modify a tuple element raises TypeError.
    try:
        price_tuple[0] = new_price
    except TypeError as e:
        print("TypeError:", e)


def calculate_total(cart):
    total = 0

    for item in cart["items"]:
        total += item["price"] * item["qty"]

    discount_amount = total * cart["discount"] / 100
    final_total = total - discount_amount

    return final_total


# ------------------------------------------------
# Demonstration - Two Independent Carts
# ------------------------------------------------

cart1 = create_cart("Aarav", discount=10)
cart2 = create_cart("Rahul", discount=5)

add_to_cart(cart1, "Laptop", 50000, 1)
add_to_cart(cart1, "Mouse", 1000, 2)

add_to_cart(cart2, "Keyboard", 2000, 1)
add_to_cart(cart2, "Monitor", 15000, 1)

print("\nPart C - Shopping Carts")

print("\nCart 1:")
print(cart1)
print("Final Total:", calculate_total(cart1))

print("\nCart 2:")
print(cart2)
print("Final Total:", calculate_total(cart2))


# ------------------------------------------------
# Proving that carts are independent
# ------------------------------------------------

add_to_cart(cart1, "Headphones", 3000, 1)

print("\nAfter modifying Cart 1:")

print("Cart 1 items:", cart1["items"])
print("Cart 2 items:", cart2["items"])


# ------------------------------------------------
# Demonstrating tuple immutability
# ------------------------------------------------

price_tuple = ("Laptop", 50000)

print("\nTuple before modification:", price_tuple)
update_price(price_tuple, 45000)
print("Tuple after attempted modification:", price_tuple)


# ============================================================
# Discussion Points
# ============================================================

# 1. Why is discount=0 safe but cart=[] dangerous?
#
# discount=0 is safe because integers are immutable.
# The value 0 cannot be modified in-place.
#
# cart=[] is dangerous because a list is mutable.
# Python creates the default list only once when the function
# is defined. Every call that does not provide a cart uses
# the SAME list.
#
# Therefore, items added in one call remain in later calls.
#
# The safe solution is:
# def add_item(item, cart=None):
#     if cart is None:
#         cart = []


# 2. What is the difference between rebinding and mutating?
#
# Mutating means changing the existing object.
#
# Example:
# cart.append("Apple")
#
# The same list object is modified.
#
# Rebinding means making a variable refer to a different object.
#
# Example:
# cart = []
#
# Here, the variable cart is made to refer to a new list.


# 3. Which of these are mutable?
#
# list   -> Mutable
# tuple  -> Immutable
# dict   -> Mutable
# set    -> Mutable
# str    -> Immutable
# int    -> Immutable


# 4. When you pass a list into a function and modify it,
#    do changes reflect outside? Why?
#
# Yes.
#
# Python passes object references. The function receives a
# reference to the same list object.
#
# Therefore, if the function mutates the list:
#
# def add_item(cart):
#     cart.append("Apple")
#
# the original list outside the function is also changed.
#
# However, if the function rebinds the parameter:
#
# def change_cart(cart):
#     cart = []
#
# the original list outside the function is NOT replaced.