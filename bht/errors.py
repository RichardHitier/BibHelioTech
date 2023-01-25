__all__ = ["BhtError",
           "BhtPathError"
           ]


class BhtError(Exception):
    """BHT pipeline base exception"""

    def __init__(self, message="BHT Error"):
        self.message = message
        super().__init__(self.message)


class BhtPathError(BhtError):
    """File or Dir path error"""
    pass
