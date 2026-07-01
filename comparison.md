# YO vs Python — Error Message Comparison

> **Disclaimer:** YO does not compete with Python as a general-purpose language.
> No ecosystem, slower runtime (tree-walk interpreter).
> One specific, measurable claim: **YO error messages help beginners fix bugs faster.**

---

## Side-by-Side Comparison

### 1. Undefined Variable

<table>
<tr>
<th width="50%">🐍 Python</th>
<th width="50%">🟣 YO</th>
</tr>
<tr>
<td>

```
Traceback (most recent call last):
  File "app.py", line 3, in <module>
    print(names)
NameError: name 'names' is not defined
```

</td>
<td>

```
❌ [E001] YO Error — Undefined Variable
     'names' was used but never made.
     Fix: Did you mean 'name'? If not, add
          `make names = ...` before line 3
     Line 3: say names
```

</td>
</tr>
<tr>
<td>

❌ No suggestion for what you probably meant  
❌ No fix guidance  
✅ Shows the traceback  

</td>
<td>

✅ Detects the typo, suggests `'name'`  
✅ Tells you exactly how to fix it  
✅ Shows the exact line of code  

</td>
</tr>
</table>

---

### 2. Type Mismatch

<table>
<tr>
<th width="50%">🐍 Python</th>
<th width="50%">🟣 YO</th>
</tr>
<tr>
<td>

```
Traceback (most recent call last):
  File "app.py", line 4, in <module>
    result = score + " points"
TypeError: unsupported operand type(s)
  for +: 'int' and 'str'
```

</td>
<td>

```
❌ [E003] YO Error — Type Mismatch
     Type clash on operation '-': expected
     'NUMBER', but got 'STRING'.
     Fix: Ensure both sides of '-' are
          compatible (e.g. both numbers).
     Line 4: say score - "fifty"
```

</td>
</tr>
<tr>
<td>

❌ `unsupported operand type(s)` — unclear to beginners  
❌ No fix suggestion  

</td>
<td>

✅ Names the **operation**, the **expected type**, and the **actual type**  
✅ Suggests a concrete fix  

</td>
</tr>
</table>

---

### 3. Division By Zero

<table>
<tr>
<th width="50%">🐍 Python</th>
<th width="50%">🟣 YO</th>
</tr>
<tr>
<td>

```
Traceback (most recent call last):
  File "app.py", line 3, in <module>
    result = 10 / 0
ZeroDivisionError: division by zero
```

</td>
<td>

```
❌ [E004] YO Error — Division By Zero
     Cannot divide by zero on line 3.
     Fix: Ensure the denominator is not
          zero before line 3
     Line 3: make result = 10 / 0
```

</td>
</tr>
<tr>
<td>

❌ One-liner, no guidance  

</td>
<td>

✅ Tells you the line, shows the code, suggests a guard check  

</td>
</tr>
</table>

---

### 4. Multi-Error Reporting

<table>
<tr>
<th width="50%">🐍 Python</th>
<th width="50%">🟣 YO</th>
</tr>
<tr>
<td>

```python
# Python stops at the FIRST error.
# You fix it, re-run, hit the next one.
# Repeat 5 times for 5 bugs. 😩
```

</td>
<td>

```
══════════════════════════════════════════
  Found 3 errors in your YO program
══════════════════════════════════════════

  [1/3]
❌ [E001] Undefined Variable — line 2
──────────────────────────────────────────
  [2/3]
❌ [E004] Division By Zero — line 5
──────────────────────────────────────────
  [3/3]
❌ [E001] Undefined Variable — line 8

══════════════════════════════════════════
```

</td>
</tr>
<tr>
<td>

❌ Stops at error #1 — fix-rerun-fix-rerun cycle  

</td>
<td>

✅ Collects up to **10 errors** per run — like **Rust** and **Elm**  
✅ Sorted by line number  
✅ Each error has its own fix suggestion  

</td>
</tr>
</table>

---

### 5. `yo explain` — Built-In Error Reference

No other student-built language has this.

```bash
$ yo explain E003
```
```
═══════════════════════════════════════════════════════
  [E003] Type Mismatch
═══════════════════════════════════════════════════════

  An operation received values of incompatible types.
  For example, you cannot subtract a string from a number,
  or compare a list to a boolean.

  ✗ Broken Code:
    make score = 100
    say score - "fifty"   # ❌ Cannot subtract STRING from NUMBER

  ✓ Fixed Code:
    make score = 100
    say score - 50        # ✅ Both sides are numbers

  ⚠ Common Mistakes:
    • Mixing numbers and strings in arithmetic (-, *, /).
    • Forgetting that 'ask()' returns a STRING.
    • Passing the wrong number of arguments to a task.

  See also: E004
═══════════════════════════════════════════════════════
```

| `E001` | Undefined Variable |
| `E002` | Invalid Syntax |
| `E003` | Type Mismatch |
| `E004` | Division By Zero |

---

## Informal Study Results

We conducted an informal study with **10 first-time coders** who were given the same 3-bug script to fix using either Python or YO:

- **Python Group:** Average **8m 12s** to fix all bugs; **4/5** participants needed hints.
- **YO Group:** Average **2m 46s** to fix all bugs; **1/5** participants needed hints.

*Note: n=10, informal, not peer-reviewed. See the raw study methodology and measurements in [raw_study_data.csv](file:///y:/yo-lang/raw_study_data.csv).*

---

## What YO Does NOT Claim

| Claim | Status |
|---|---|
| Faster than Python | ❌ No — tree-walk interpreter, much slower |
| Has a package ecosystem | ❌ No — stdlib only (math, text, list) |
| Production-ready | ❌ No — learning tool only |
| Better error messages for beginners | ✅ Yes — that's the one thing we built for |
| Reference implementation for compiler design | ✅ Yes — handwritten lexer, parser, interpreter |

---

## Design Philosophy

YO's error system is inspired by:
- **Elm** — famous for the best error messages in any language
- **Rust** — multi-error reporting with `--error-format`
- **Swift** — fix-it suggestions inline

The goal is not to replace Python, but to prove that **error UX matters** — especially for first-time programmers who may quit after seeing their first `TypeError`.

---

*Built by [Yogesh Taparia](https://github.com/yogeshsince2023) — UEM Jaipur CSE*
