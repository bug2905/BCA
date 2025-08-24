import calculator
import history

while True:
    print("\n--- Calculator ---")
    print("1. Add\n2. Subtract\n3. Multiply\n4. Divide\n5. Show History\n6. Exit")
    choice = int(input("Enter choice: "))

    if choice in [1,2,3,4]:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))

        if choice == 1:
            result = calculator.add(a, b)
            expr = f"{a} + {b}"
        elif choice == 2:
            result = calculator.subtract(a, b)
            expr = f"{a} - {b}"
        elif choice == 3:
            result = calculator.multiply(a, b)
            expr = f"{a} * {b}"
        elif choice == 4:
            result = calculator.divide(a, b)
            expr = f"{a} / {b}"

        print("Result:", result)
        history.save_history(expr, result)

    elif choice == 5:
        print("\n--- History ---")
        print(history.show_history())
    elif choice == 6:
        break
    else:
        print("Invalid choice")
