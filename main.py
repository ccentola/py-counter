from counter import Counter


def main():
    current = Counter()

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
                current.increment()
            case "d":
                try:
                    current.decrement()
                except ValueError as e:
                    print(f"Error: {e}")
            case "r":
                current.reset()
                print("Counter reset to 0")
            case "quit":
                break
            case _:
                print("Please choose from: 'i', 'd', 'r', or 'quit'")
    print("Goodbye")


if __name__ == "__main__":
    main()
