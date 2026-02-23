def main():
    current = 0

    # menu
    print("===== Welcome to py-counter =====")
    print("- 'i' increments the counter")
    print("- 'd' decrements the counter")
    print("- 'r' resets the counter")
    print("- 'quit' exits the application")
    print("\n")

    while True:
        user_input = input(
            f"Current: {current} | Enter a command or type 'quit' to exit: "
        )
        # if command from terminal is "i" -> increment
        if user_input == "i":
            current += 1
            print(current)
        # if command from terminal is "d" -> decrement
        elif user_input == "d":
            current -= 1
            print(current)
        # if command is "r" -> reset the counter
        elif user_input == "r":
            current = 0
            print("Counter reset to 0")
        # "quit" exits the program
        if user_input == "quit":
            break
    print("Goodbye")


if __name__ == "__main__":
    main()
