# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
print("Hello world:input the operation")
var1 = 10
var2 = 5
print("what's your option")
option = input()    
print("got option")
print(option)
match option:
    case "plus":
        result = var1 + var2
    case "minus":
        result = var1 - var2
    case "multi":
        result = var1 * var2
    case "divi":
        result = var1 / var2
    case _:
        print("wrong input:plus/minus/multi/divi")
print("result is " + str(result))


