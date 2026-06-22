LIST_LIB = {
    "count": lambda args: len(args[0]),
    "add": lambda args: (args[0].append(args[1]) or args[0]),
    "remove": lambda args: (args[0].remove(args[1]) or args[0]) if args[1] in args[0] else args[0],
    "sort": lambda args: (args[0].sort() or args[0]),
    "reverse": lambda args: (args[0].reverse() or args[0]),
    "first": lambda args: args[0][0] if len(args[0]) > 0 else None,
    "last": lambda args: args[0][-1] if len(args[0]) > 0 else None,
    "has": lambda args: args[1] in args[0],
    "join": lambda args: str(args[1]).join(str(x) for x in args[0]) if len(args) > 1 else "".join(str(x) for x in args[0])
}
