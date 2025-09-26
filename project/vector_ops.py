"""
Implementation of vector operations: scalar multiplication,
length calculation, angle between vectors.

"""

from math import acos, pi


while True:
    print("Enter first vector(e.g. 1,2,3): ", end="")
    try:
        vector1 = list(map(float, input().split(",")))
        break
    except ValueError:
        print("Invalid input, try again")

while True:
    print("Enter second vector(e.g. 1,2,3): ", end="")
    try:
        vector2 = list(map(float, input().split(",")))
        if len(vector2) == len(vector1):
            break
        else:
            print("Vector sizes must be equal")
    except ValueError:
        print("Invalid input, try again")

print(
    "Available operations:\n1. Scalar multiplication\n2. Length\n3. Angle between vectors"
)
while True:
    print("Enter operation number: ", end="")
    try:
        operation = int(input())
        if 1 <= operation <= 3:
            if operation == 1:
                print(
                    f"Scalar product: {sum([vector1[i] * vector2[i] for i in range(len(vector1))])}"
                )
            elif operation == 2:
                while True:
                    print(
                        "Enter the number of vector which length you want to calculate: ",
                        end="",
                    )
                    try:
                        n = int(input())
                        if n == 1:
                            print(
                                f"Length of the first vector: {sum([i ** 2 for i in vector1]) ** 0.5}"
                            )
                            break
                        elif n == 2:
                            print(
                                f"Length of the second vector: {sum([i ** 2 for i in vector2]) ** 0.5}"
                            )
                            break
                        else:
                            print("Enter 1 or 2")
                    except ValueError:
                        print("Invalid input, try again")
            else:
                scal_prod = sum([vector1[i] * vector2[i] for i in range(len(vector1))])
                vec1_len = sum([i**2 for i in vector1]) ** 0.5
                vec2_len = sum([i**2 for i in vector2]) ** 0.5
                print(f"Angle: {180 * acos(scal_prod / (vec1_len * vec2_len)) / pi}")
            print(
                "If you want to perform another operation enter [y], else the program will finish: ",
                end="",
            )
            verification = input().strip()
            if verification == "y":
                continue
            break
        else:
            print("Enter a number between 1 and 3")
    except ValueError:
        print("Invalid input, try again")
