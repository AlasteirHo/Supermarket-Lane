def my_function():
    return 1, 2, 3

# Using tuple unpacking
result1, result2, result3 = my_function()

# Using indexing
result_tuple = my_function()
result1 = result_tuple[0]
result2 = result_tuple[1]
result3 = result_tuple[2]

print(result3)
