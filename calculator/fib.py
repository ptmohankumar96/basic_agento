import sys

def fibonacci(n):
    a, b = 0, 1
    count = 0
    while count < n:
        print(a, end=" ")
        a, b = b, a + b
        count += 1
    print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fib.py <number_of_fib_numbers>")
        sys.exit(1)
    try:
        num = int(sys.argv[1])
        if num <= 0:
            print("Please enter a positive integer.")
        else:
            fibonacci(num)
    except ValueError:
        print("Invalid input. Please enter an integer.")
