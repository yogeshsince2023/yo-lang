import math
import random as rand

MATH_LIB = {
    "round": lambda args: round(args[0]),
    "floor": lambda args: math.floor(args[0]),
    "ceil": lambda args: math.ceil(args[0]),
    "power": lambda args: args[0] ** args[1],
    "sqrt": lambda args: math.sqrt(args[0]),
    "random": lambda args: rand.random(),
    "abs": lambda args: abs(args[0]),
    "min": lambda args: min(args[0]) if len(args) == 1 and isinstance(args[0], list) else min(args),
    "max": lambda args: max(args[0]) if len(args) == 1 and isinstance(args[0], list) else max(args)
}
