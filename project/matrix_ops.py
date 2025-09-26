"""
Implementation of vector operations: scalar multiplication,
length calculation, angle between vectors.

"""

while True:
    print("Enter the size of your matrices(one number >0): ", end='')
    try:
        n = int(input())
        if n > 0:
            break
        else:
            print("Size must be greater than 0")
    except ValueError:
        print("Invalid input, try again")

matrix_1 = []
matrix_2 = []

print("Fill the first matrix")
for i in range(n):
    while True:
        print(f"Enter {i + 1} row(e.g. 1,2,3) ", end='')
        try:
            row = list(map(float, input().split(",")))
            if len(row) == n:
                matrix_1.append(row)
                break
            else:
                print(f"Row size must be equal to {n}")
        except ValueError:
            print("Invalid input, try again")

print("Fill the second matrix")
for i in range(n):
    while True:
        print(f"Enter {i + 1} row(e.g. 1,2,3) ", end='')
        try:
            row = list(map(float, input().split(",")))
            if len(row) == n:
                matrix_2.append(row)
                break
            else:
                print(f"Row size must be equal to {n}")
        except ValueError:
            print("Invalid input, try again")
            
print(
    "Available operations:\n1. Addition\n2. Multiplication\n3. Transposition"
)
while True:
    print("Enter operation number: ", end="")
    try:
        operation = int(input())
        if 1 <= operation <= 3:
            if operation == 1:
                print(
                    f"Addition: {[[matrix_1[i][j] + matrix_2[i][j] for j in range(n)] for i in range(n)]}"
                )
            
            elif operation == 2:
                print(f"Product: {[[sum([matrix_1[i][k] * matrix_2[k][j] for k in range(n)]) for j in range(n)] for i in range(n)]}")
                
            else:
                 while True:
                    print(
                        "Enter the number of matrix you want to transpose: ",
                        end="",
                    )
                    try:
                        p = int(input())
                        if p == 1:
                            print(
                                f"First matrix transposed: {[[matrix_1[j][i] for j in range(n)] for i in range(n)]}"
                            )
                            break
                        elif p == 2:
                            print(
                                f"Second matrix transposed: {[[matrix_2[j][i] for j in range(n)] for i in range(n)]}"
                            )
                            break
                        else:
                            print("Enter 1 or 2")
                    except ValueError:
                        print("Invalid input, try again")
   
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

