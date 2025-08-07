from cs50 import get_int


def validate_card(number):
    first_sum = 0
    second_sum = 0
    result_sum = 0
    number = number[::-1]

    for i in number[1::2]:
        first_sum += int(int(i) * 2 % 10) + int(int(i) * 2 / 10)

    for j in number[::2]:
        second_sum += int(j)

    result_sum = first_sum + second_sum
    return ((result_sum % 10) == 0)


def get_card_type(number):

    length = len(number)

    if length == 15 and (number.startswith("34") or number.startswith("37")):
        return "AMEX"
    elif length == 16 and number[:2] in ["51", "52", "53", "54", "55"]:
        return "MASTERCARD"
    elif length in [13, 16] and number.startswith("4"):
        return "VISA"
    else:
        return "INVALID"


number = input("Number: ")

print(validate_card(number))

if number.isdigit():
    if validate_card(number):
        print(get_card_type(number))
    else:
        print("INVALID")
else:
    print("INVALID")
