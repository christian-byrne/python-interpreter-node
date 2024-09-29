print(f"The type of number1 when it was received was {type(number1)}")

if str(number1).isnumeric():
    number1.to(int(number1))
else:
    print(f"number1 was not a number. It was {number1}")

if number1 < 0:
    number1.to(0)