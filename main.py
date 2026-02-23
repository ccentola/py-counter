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
        match user_input:
            case "i":
                current += 1
                print(current)
            case "d":
                if current == 0:
                    print("Counter cannot be less than 0")
                else:
                    current -= 1
                    print(current)
            case "r":
                current = 0
                print(current)
            case "quit":
                break
            case _:
                print("Please choose from: 'i', 'd', 'r', or 'quit'")
    print("Goodbye")


if __name__ == "__main__":
    main()
