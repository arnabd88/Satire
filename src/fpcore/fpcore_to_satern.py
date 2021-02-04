

from fpcore.exceptions import BadPreError, DomainError, NoPreError
from fpcore.fpcore_ast import Number, Operation, Variable
from fpcore.fpcore_parser import parse

import sys




def properties_to_argument_domains(fpcore):
    # Take an FPCore and return and argument->domain mapping
    # An incomplete mapping is an error
    arguments = fpcore.arguments
    properties = fpcore.properties

    def normalize_comparison(comp):
        # Given an n-arry comparison return a list of comparisons which all use
        # "<=" and only have two arguments

        # Only simple domains are supported
        # todo: add support for constant mathematical domains (eg (- 1 1/256))
        if any([type(a) not in {Variable, Number} for a in comp.args]):
            print("Dropping precondition: {}".format(comp), file=sys.stderr)
            return list()

        # Make exclusive comparisons inclusive
        if comp.op in {"<", ">"}:
            print("Turning exclusive bound to inclusive: {}".format(comp),
                  file=sys.stderr)
            comp.op += "="

        # Normalize => to >=
        if comp.op == "=>":
            comp.op = ">="

        # Reverse if comparison was >=
        if comp.op == ">=":
            comp.op = "<="
            comp.args = list(reversed(comp.args))

        # Break comparison into overlaping pairs
        ret_list = list()
        for i in range(len(comp.args)-1):
            ret_list.append(Operation("<=", comp.args[i], comp.args[i+1]))
        return ret_list

    def get_domains(precondition_list):
        # Search preconditions for variable domains
        string_arguments = {a.source for a in arguments}
        lower_domains = {s: None for s in string_arguments}
        upper_domains = {s: None for s in string_arguments}

        def is_input(x):
            return type(x) == Variable and x.source in string_arguments

        for pre in precondition_list:

            # We only get domains from comparisons
            if pre.op not in {"<", ">", "<=", ">=", "=>"}:
                print("Dropping precondition: {}".format(pre), file=sys.stderr)
                continue

            # Get list of pairs
            normal = normalize_comparison(pre)
            for comp in normal:

                # If the comparison is (<= <Variable> <Number>) it is an upper
                # bound
                if is_input(comp.args[0]) and type(comp.args[1]) == Number:
                    upper_domains[str(comp.args[0])] = comp.args[1]
                    continue

                # If the comparison is (<= <Number> <Variable>) it is a lower
                # bound
                if type(comp.args[0]) == Number and is_input(comp.args[1]):
                    lower_domains[str(comp.args[1])] = comp.args[0]
                    continue

                # Only simple domains are supported
                print("Dropping precondition: {}".format(comp), file=sys.stderr)

        # Bring upper and lower bounds together
        domains = dict()
        for name in lower_domains:
            domains[name] = (lower_domains[name], upper_domains[name])
        return domains

    # Search the FPCore's properties for the :pre property
    # todo: add support for multiple ':pre' properties
    pre = None
    for prop in properties:
        if prop.name == "pre":
            pre = prop
            continue

    # If we couldn't find ':pre' there is no domain
    if pre is None:
        raise NoPreError()

    # If pre is not an Operation we can't handle it
    if type(pre.value) != Operation:
        raise BadPreError(pre)

    # The pre can be a single bound description, or multiple joined with an and
    if pre.value.op == "and":
        property_list = list(pre.value.args)
    else:
        property_list = [pre.value]

    # Get domains and check that all are there
    domains = get_domains(property_list)
    for var, val in domains.items():
        if val[0] is None or val[1] is None:
            raise DomainError(val[0], val[1], var)

    return domains


def fpcore_to_satern(text):
    parsed = parse(text)
    assert len(parsed) == 1, "fpcore_to_satern supports only one FPCore being present"
    parsed = parsed[0]

    # Grab domain bounds
    domains = properties_to_argument_domains(parsed)
    inputs = dict()
    literals = dict()
    for name, domain in domains.items():
        # If the domain contains a single point we treat that as a literal
        # in the environment
        if domain[0] == domain[1]:
            literals[name] = domain[0]
            continue
        inputs[name] = domain

    environment = [inputs, literals]
    expanded = parsed.expression.expand(environment)

    satire_query_lines = list()

    satire_query_lines.append("INPUTS {")
    for name, domain in inputs.items():
        line = "  {} {} : ({}, {});".format(name, "fl64", domain[0], domain[1])
        satire_query_lines.append(line)
    satire_query_lines.append("}")
    satire_query_lines.append("")

    satire_query_lines.append("OUTPUTS {")
    satire_query_lines.append("  ret;")
    satire_query_lines.append("}")
    satire_query_lines.append("")

    satire_query_lines.append("EXPRS {")
    satire_query_lines.append("  ret {}= {};".format("rnd64", expanded.infix()))
    satire_query_lines.append("}")

    return "\n".join(satire_query_lines)




def main(argv):
    if len(argv) == 1:
        text = sys.stdin.read()
    elif len(argv) == 2:
        with open(argv[1], "r") as f:
            text = f.read()

    satern_query = fpcore_to_satern(text)
    print(satern_query)


if __name__ == "__main__":
    retcode = 0
    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("Goodbye")

    sys.exit(retcode)
