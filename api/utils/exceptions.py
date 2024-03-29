class InvalidFileHeaderException(Exception):
    def __init__(self, message=""):
        """
        Constructor for InvalidFileHeaderException.

        Args:
        - message (str): Optional message for the exception.
        """
        self.message = message
        super().__init__(self.message)