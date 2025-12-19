try:
    a=int(input("enter value for a "))
    b=int(input("enter the value for b "))
    print("res=",a/b)

except IndexError:
    print("value error has occured")