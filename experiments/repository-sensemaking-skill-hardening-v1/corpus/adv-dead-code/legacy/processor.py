# Legacy processor - looks important
import time

class Processor:
    """The core processor (docs say)."""
    def process(self, data):
        time.sleep(1)
        return data.upper()

    def validate(self, data):
        return True

    def transform(self, data):
        return data

    def export(self, data):
        return data

    def notify(self, data):
        return data
