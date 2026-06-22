TEXT_LIB = {
    "upper": lambda args: str(args[0]).upper(),
    "lower": lambda args: str(args[0]).lower(),
    "length": lambda args: len(str(args[0])),
    "reverse": lambda args: str(args[0])[::-1],
    "has": lambda args: str(args[1]) in str(args[0]),
    "trim": lambda args: str(args[0]).strip(),
    "split": lambda args: str(args[0]).split(str(args[1])) if len(args) > 1 else str(args[0]).split(),
    "replace": lambda args: str(args[0]).replace(str(args[1]), str(args[2])),
    "starts_with": lambda args: str(args[0]).startswith(str(args[1])),
    "ends_with": lambda args: str(args[0]).endswith(str(args[1]))
}
