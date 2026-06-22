# 🚀 YO Language

> **YO — A Programming Language That Talks Like You**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Beginner Friendly](https://img.shields.io/badge/Style-Beginner%20Friendly-green.svg)](#)

---

## 📝 What is YO?

YO is a beginner-friendly, dynamic programming language designed to make coding intuitive and fun. Built from scratch in Python, it prioritizes readability with conversational syntax and color-coded, actionable error diagnostics. It offers nested environments for functions, an interactive REPL mode, and built-in standard libraries for math, text, and lists.

---

## ⚙️ Quick Install

YO runs on Python 3.10+. To install the required dependencies (primarily for colorized formatting), run:

```bash
pip install colorama
```

---

## 👋 Hello World

Create a file named `hello.yo` and add the following code:

```yolang
make greeting = "Hello World!"
say greeting
```

---

## 📋 Syntax Cheatsheet

### 1. Variables (`make`)
Declares a new variable. Reassign variables without the `make` keyword.
```yolang
make name = "Yogesh"
name = "Yogesh Kumar"
```

### 2. Print Output (`say`)
Prints text or numbers to the console.
```yolang
say "My name is " + name
```

### 3. Conditionals (`when`)
Executes code blocks based on conditions.
```yolang
make age = 21
when age >= 18 {
    say "You are an adult"
} else {
    say "You are a minor"
}
```

### 4. Counted Loops (`repeat`)
Loops a block of code a specific number of times.
```yolang
repeat 3 times {
    say "YO!"
}
```

### 5. List Loops (`for each`)
Iterates over elements in a list.
```yolang
for each num in [1, 2, 3] {
    say num
}
```

### 6. Functions (`task`)
Declares reusable tasks with arguments and return statements.
```yolang
task add(a, b) {
    return a + b
}

make sum = add(5, 10)
say sum
```

---

## 🚀 Running YO

### Run a Script
To run a `.yo` file, use the `yo.py` runner:
```bash
python yo.py myfile.yo
# OR
python yo.py run myfile.yo
```

### Interactive REPL Mode
Running `yo.py` with no arguments boots up interactive mode:
```bash
python yo.py
```
```
YO v1.0 — Interactive Mode
Type 'exit' to quit, 'clear' to reset variables
yo> make x = 5
yo> say x
5
yo> exit
```

---

## 📚 Standard Libraries

Load built-in standard libraries using the `use` keyword.

### 🧮 Math Library
Exposes: `round`, `floor`, `ceil`, `power`, `sqrt`, `random`, `abs`, `min`, `max`.
```yolang
use math
say math.sqrt(25) # Outputs 5.0
```

### 🔤 Text Library
Exposes: `upper`, `lower`, `length`, `reverse`, `has`, `trim`, `split`, `replace`, `starts_with`, `ends_with`.
```yolang
use text
say text.upper("hello") # Outputs HELLO
```

### 📋 List Library
Exposes: `count`, `add`, `remove`, `sort`, `reverse`, `first`, `last`, `has`, `join`.
```yolang
use list
make my_list = [3, 1, 2]
say list.sort(my_list) # Outputs [1, 2, 3]
```

---

## 📁 Project Structure

```
yo-lang/
├── stdlib/            # Standard Library Python modules
│   ├── list_lib.py    # List primitives
│   ├── math_lib.py    # Mathematical primitives
│   └── text_lib.py    # String primitives
├── tests/             # Sample YO scripts
│   ├── test1.yo       # Basics test
│   ├── test2.yo       # Functions and lists test
│   └── test3.yo       # Standard libraries test
├── environment.py     # Environment variable scope tracking
├── errors.py          # Color-coded error styling & formatting
├── interpreter.py     # AST execution engine
├── lexer.py           # Handwritten scanner & tokenizer
├── parser.py          # Handwritten recursive descent parser
├── README.md          # Project documentation
└── yo.py              # CLI & REPL entrypoint
```

---

## 🎓 Built By
*   **Yogesh Taparia** - UEM Jaipur CSE

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
