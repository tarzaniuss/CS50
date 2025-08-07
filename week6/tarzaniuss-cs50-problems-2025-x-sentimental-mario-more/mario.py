from cs50 import get_int

while (True):
    number = get_int("Height: ")
    if number < 1 or number > 8:
        continue
    else:
        for i in range(1, number+1):
            for a in range(i, number):
                print(" ", end="")

            for b in range(i):
                print("#", end="")

            print("  ", end="")

            for c in range(0, i):
                print("#", end="")

            print()
    break
