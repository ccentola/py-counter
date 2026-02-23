class Counter:
    """
    A simple accumulator that manages a non-negative integer state.

    This class provides core logic for incrementing, decrementing, and
    resetting a counter value, ensuring the value never drops below zero.

    Attributes:
        value (int): The current count held by the instance.
    """

    def __init__(self, initial_value=0) -> None:
        """
        Initializes the Counter with an optional starting value.

        Args:
            initial_value (int): The number to start the counter at. Defaults to 0.
        """
        self.value = initial_value

    def increment(self) -> None:
        """Adds 1 to the current value"""
        self.value += 1

    def decrement(self) -> None:
        """
        Subtracts 1 from the current value.

        Raises:
            ValueError: If the current value is 0, to prevent negative counts.
        """
        if self.value <= 0:
            raise ValueError("Counter cannot be negative")
        self.value -= 1

    def reset(self) -> None:
        """Resets the current counter to 0"""
        self.value = 0

    def __str__(self) -> str:
        return str(self.value)
