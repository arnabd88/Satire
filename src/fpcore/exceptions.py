

class FPCoreError(Exception):
    pass


class VariableError(FPCoreError):
    """
    Indicates that a variable was used without a definition being given first
    """
    def __init__(self, name):
        self.name = name

class UnsupportedError(FPCoreError):
    """ Indicates usage of an unsuported FPCore statement type """
    def __init__(self, statement_type):
        self.statement_type = statement_type


class NoPreError(FPCoreError):
    """ Indicates that no ':pre' property was present in an FPCore """
    pass


class BadPreError(FPCoreError):
    """ Indicates that the given ':pre' was unable to be proccesed """
    def __init__(self, pre):
        self.pre = str(pre)


class DomainError(FPCoreError):
    """ Indicates that an input to an FPCore does not have a full domain """
    def __init__(self, lower, upper, name):
        self.lower = lower
        self.upper = upper
        self.name = name
