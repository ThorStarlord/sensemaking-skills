"""Medium repo test module."""

class TestClass:
    def __init__(self):
        self.value = 42

    def method(self):
        return self.value

def test_function():
    obj = TestClass()
    return obj.method()
