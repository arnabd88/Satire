

from fpcore.fpcore_lexer import FPCoreLexer
from fpcore.exceptions import UnsupportedError, VariableError

import sys




UNARY_PREFIX = {"+", "-"}
INFIX = {"+", "-", "*", "/"}


def list_to_str(l, sep=" "):
    if l is None:
        return ""
    return sep.join([str(i) for i in l])


def list_to_repr(l):
    if l is None:
        return ""
    return ", ".join([repr(i) for i in l])


# +---------------------------------------------------------------------------+
# | ASTNode                                                                   |
# +---------------------------------------------------------------------------+
class ASTNode:
    def __init__(self):
        pass

    def __str__(self):
        class_name = type(self).__name__
        msg = "__str__ is not defined for {}".format(class_name)
        raise NotImplementedError(msg)

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({{}})".format(class_name)

    def expand(self, environment_stack):
        class_name = type(self).__name__
        msg = "expand not implemented for class {}".format(class_name)
        raise NotImplementedError(msg)

    def infix(self):
        class_name = type(self).__name__
        msg = "infix not implemented for class {}".format(class_name)
        raise NotImplementedError(msg)


# +---------------------------------------------------------------------------+
# | Expr                                                                      |
# +---------------------------------------------------------------------------+
class Expr(ASTNode):
    def __init__(self):
        super().__init__()
        self.properties = list()

    def add_properties(self, properties):
        self.properties.extend(properties)
        return self

    def __str__(self):
        if len(self.properties) == 0:
            return "{}"
        return "(! {} {{}})".format(list_to_str(self.properties))

    def __repr__(self):
        format_repr = super().__repr__()
        if len(self.properties) == 0:
            return format_repr
        props = list_to_repr(self.properties)
        prop_repr = ".add_properites([{}])".format(props)
        return format_repr + prop_repr


# +---------------------------------------------------------------------------+
# | Atoms                                                                     |
# +---------------------------------------------------------------------------+
class Atom(Expr):
    def __init__(self, source):
        super().__init__()
        self.source = source

    def __str__(self):
        format_str = super().__str__()
        return format_str.format(self.source)

    def __repr__(self):
        format_repr = super().__repr__()
        return format_repr.format(repr(self.source))

    def expand(self, environment_stack):
        return self

    def infix(self):
        return self.source


class Number(Atom):
    pass


class Constant(Atom):
    pass


class Variable(Atom):
    def expand(self, environment_stack):
        # First search the environment stack
        if environment_stack is None:
            raise VariableError(self.source)

        for environment in reversed(environment_stack):
            # If found expand and return the value
            if self.source in environment:
                val = environment[self.source]
                if type(val) == tuple:
                    return self
                return val

        # Exit if no definition is found
        raise VariableError(self.source)


# +---------------------------------------------------------------------------+
# | Operations                                                                |
# +---------------------------------------------------------------------------+
class Operation(Expr):
    def __init__(self, op, *args):
        super().__init__()
        if len(args) == 1 and op not in FPCoreLexer.UNARY_OPERATIONS:
            print("Operation '{}' is not unary, given: {}".format(op, args),
                  file=sys.stderr)
            print("Possible unary operations:\n{}".format(
                         "\n".join(sorted(FPCoreLexer.UNARY_OPERATIONS))),
                  file=sys.stderr)
            sys.exit(1)

        elif len(args) == 2 and op not in FPCoreLexer.BINARY_OPERATIONS:
            print("Operation '{}' is not binary, given: {}".fomrat(op, args),
                  file=sys.stderr)
            print("Possible binary operations:\n{}".format(
                         "\n".join(sorted(FPCoreLexer.BINARY_OPERATIONS))),
                  file=sys.stderr)
            sys.exit(1)

        elif len(args) == 3 and op not in FPCoreLexer.TERNARY_OPERATIONS:
            print("Operation '{}' is not ternary, given: {}".format(op, args),
                  file=sys.stderr)
            print("Possible ternary operations:\n{}".format(
                         "\n".join(sorted(FPCoreLexer.TERNARY_OPERATIONS))),
                  file=sys.stderr)
            sys.exit(1)

        elif len(args) >= 4 and op not in FPCoreLexer.NARY_OPERATIONS:
            print("Operation '{}' is not n-ary, given: {}".format(op, args),
                  file=sys.stderr)
            print("Possible n-ary operations:\n{}".format(
                         "\n".join(sorted(FPCoreLexer.NARY_OPERATIONS))),
                  file=sys.stderr)
            sys.exit(1)

        self.op = op
        self.args = args

    def __str__(self):
        format_str = super().__str__()
        this_str = "({} {})".format(self.op, list_to_str(self.args))
        return format_str.format(this_str)

    def __repr__(self):
        format_repr = super().__repr__()
        this_repr = "{}, {}".format(repr(self.op), list_to_repr(self.args))
        return format_repr.format(this_repr)

    def expand(self, environment_stack):
        # Expand all arguments and return a new operation
        args = [a.expand(environment_stack) for a in self.args]
        return Operation(self.op, *args)

    def infix(self):
        # Infix arguments
        args = [a.infix() for a in self.args]

        # Grab unary prefix operations
        if len(args) == 1 and self.op in UNARY_PREFIX:
            return "({} {})".format(self.op, args[0])

        # Grab infix binary operations
        if len(args) == 2 and self.op in INFIX:
            return "({} {} {})".format(args[0], self.op, args[1])

        # Everything else is a function call
        return "{}({})".format(self.op, ", ".join(args))


# +---------------------------------------------------------------------------+
# | If                                                                        |
# +---------------------------------------------------------------------------+
class If(Expr):
    def __init__(self, cond, true, false):
        UnsupportedError("If")


# +---------------------------------------------------------------------------+
# | Let                                                                       |
# +---------------------------------------------------------------------------+
class Let(Expr):
    def __init__(self, bindings, body):
        super().__init__()
        self.bindings = bindings
        self.body = body

    def __str__(self):
        format_str = super().__str__()
        this_str = "(let ({}) {})".format(list_to_str(self.bindings),
                                          self.body)
        return format_str.format(this_str)

    def __repr__(self):
        format_repr = super().__repr__()
        this_repr = "[{}], {}".format(list_to_repr(self.bindings),
                                      repr(self.body))
        return format_repr.format(this_repr)

    def expand(self, environment_stack):
        # Setup the new entry in the environment stack
        binding_list = [b.expand(environment_stack)
                        for b in self.bindings]
        new_environment = dict(binding_list)
        environment_stack.append(new_environment)

        # Transform body using the updated stack
        expanded = self.body.expand(environment_stack)

        # Remove our enironment
        environment_stack.pop()

        return expanded


class LetStar(Let):
    def __str__(self):
        format_str = super().__str__()
        this_str = "(let* ({}) {})".format(list_to_str(self.bindings),
                                           self.body)
        return format_str.format(this_str)

    def expand(self, environment_stack):
        # Bindings may reference previous bindings in the let
        # So add each to the stack one at a time
        for b in self.bindings:
            name, val = b.expand(environment_stack)
            environment_stack.append({name: val})

        # Transform body using the updated stack
        expanded = self.body.expand(environment_stack)

        # Remove our enironments
        for _ in self.bindings:
            environment_stack.pop()

        return expanded


# +---------------------------------------------------------------------------+
# | While                                                                     |
# +---------------------------------------------------------------------------+
class While(Expr):
    def __init__(self, cond, while_bindings, body):
        UnsupportedError("While")


class WhileStar(While):
    def __str__(self):
        UnsupportedError("WhileStar")


# +---------------------------------------------------------------------------+
# | Cast                                                                      |
# +---------------------------------------------------------------------------+
class Cast(Expr):
    def __init__(self, body):
        UnsupportedError("Cast")


# +---------------------------------------------------------------------------+
# | Pair                                                                      |
# +---------------------------------------------------------------------------+
class Pair(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        format_repr = super().__repr__()
        this_repr = list_to_repr((self.name, self.value))
        return format_repr.format(this_repr)


class Property(Pair):
    def __str__(self):
        value_str = str(self.value)
        if type(self.value) in {tuple, list}:
            value_str = "({})".format(list_to_str(self.value))
        return ":{} {}".format(self.name, value_str)


class Binding(Pair):
    def __str__(self):
        return "[{} {}]".format(self.name, self.value)

    def expand(self, environment_stack):
        # Expand body using the environment stack
        expanded = self.value.expand(environment_stack)

        # Note: This deviates from the normal return of a Variable. An
        # environment mapping pair is returned.
        return self.name.source, expanded


# +---------------------------------------------------------------------------+
# | WhileBinding                                                              |
# +---------------------------------------------------------------------------+
class WhileBinding(ASTNode):
    def __init__(self, name, init, step):
        UnsupportedError("WhileBinding")


# +---------------------------------------------------------------------------+
# | FPCore                                                                    |
# +---------------------------------------------------------------------------+
class FPCore(ASTNode):
    def __init__(self, arguments, properties, expression):
        self.arguments = arguments
        self.properties = properties
        self.expression = expression

    def __str__(self):
        arguments_str = list_to_str(self.arguments)
        properties_str = list_to_str(self.properties, "\n  ")
        return ("(FPCore ({})\n"
                "  {}\n"
                "  {})").format(arguments_str,
                                properties_str,
                                self.expression)

    def __repr__(self):
        arguments_repr = list_to_repr(self.arguments)
        properties_repr = list_to_repr(self.properties)
        return ("FPCore([{}],\n"
                "       [{}],\n"
                "       {})").format(arguments_repr,
                                     properties_repr,
                                     repr(self.expression))
