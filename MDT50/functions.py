def add(x, y):
  addition = x + y
  return addition

def sub(x, y):
  subtraction = x - y
  return subtraction

def mul(x, y):
  multiplication = x * y
  return multiplication


default_number1 = 10
default_number2 = 5


#input1 = input("Enter the first number (press Enter to use default): ")
#input2 = input("Enter the second number (press Enter to use default): ")

user_input = input("Enter two numbers separated by space (press Enter to use defaults): ")

#number1 = float(input("enter the first number:") if input1 else default_number1)
#number2 = float(input("enter the second number:") if input2 else default_number1)

if user_input:  # If user provides input
    try:
        number1, number2 = map(float, user_input.split())  # Convert input to floats
    except ValueError:
        print("Invalid input! Using default values.")
        number1, number2 = default_number1, default_number2
else:  # If user presses Enter
    number1, number2 = default_number1, default_number220

result1 = add(number1, number2)
result2 = sub(number1, number2)
result3 = mul(number1, number2)
print(f"the result of adding two numbers is {result1}")
print(f" the result of subtracting two numbers is {result2}")
print(f" the result of multiplication two numbers is {result3}")