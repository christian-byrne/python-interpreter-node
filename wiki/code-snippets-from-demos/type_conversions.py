
print(f"The type of number1 when it was received was {type(number1)}")

if str(number1).isnumeric():
    number1.to(int(number1))
else:
    print(f"number1 was not a number. It was {number1}")

# Maybe change to 0 if it's negative (e.g., you are padding image1 to match image2 size but image1 is larger than in one dimension)
if number1 < 0:
    number1.to(0)