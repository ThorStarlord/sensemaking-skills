"""Simple test module for integration testing."""


def hello(name: str) -> str:
    """Greet someone by name.

    Args:
        name: The person's name

    Returns:
        A greeting string
    """
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum
    """
    return a + b


if __name__ == "__main__":
    print(hello("World"))
    print(f"2 + 3 = {add(2, 3)}")
