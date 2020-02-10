# Here is a variable:

count = 0

# Here is a function
def increment():
    global count
    count = count + 1
    print("Count is " + str(count))


increment()
increment()
increment()
increment()
increment()
