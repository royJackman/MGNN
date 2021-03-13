def fibonacci(x):
    if x == 1 or x == 2:
        return 1
    else:
        return fibonacci(x - 1) + fibonacci(x - 2)

print(fibonacci(7))