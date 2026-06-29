# YO Language — VS Code Extension

Syntax highlighting, snippets, and a Run command for the **YO** programming language.

![VS Code](https://img.shields.io/badge/VS%20Code-1.75+-blue?logo=visual-studio-code)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

### 🎨 Syntax Highlighting

Full TextMate grammar for `.yo` files:

| Element | Color | Example |
|---|---|---|
| Keywords | **purple** | `make`, `task`, `when`, `else`, `repeat`, `for each`, `say`, `return` |
| Strings | **green** | `"Hello, World!"` |
| Numbers | **blue** | `42`, `3.14` |
| Comments | **gray** | `# this is a comment` |
| Booleans | **orange** | `true`, `false`, `null` |
| Operators | **cyan** | `==`, `!=`, `+`, `-`, `*`, `/` |
| Stdlib calls | **blue** | `math.round()`, `text.upper()`, `list.sort()` |

### 📝 Snippets

Type a prefix and press `Tab` to expand:

| Prefix | Expands to |
|---|---|
| `task` | Full function template with params and return |
| `make` | Variable declaration |
| `when` | Condition block |
| `whenelse` | Condition with else branch |
| `repeat` | Repeat N times loop |
| `foreach` | For each loop over a list |
| `say` | Print statement |
| `use` | Library import (math/text/list) |
| `ask` | User input |
| `list` | List declaration |

### ▶️ Run YO File

- **Command**: `YO: Run YO File`
- **Keybinding**: `Ctrl+Shift+R` (Windows/Linux) / `Cmd+Shift+R` (Mac)
- **Play button**: Appears in the editor title bar for `.yo` files

The command saves the current file, opens an integrated terminal, and runs:
```
yo run filename.yo
```

---

## 📦 Installation

### From Source (Development)

1. Clone or copy the `yo-lang-vscode/` directory
2. Open it in VS Code
3. Press `F5` to launch the Extension Development Host
4. Open any `.yo` file to see syntax highlighting

### Package as VSIX

```bash
npm install -g @vscode/vsce
cd yo-lang-vscode
vsce package
```

Then install the generated `.vsix` file via:  
**Extensions** → **⋯** → **Install from VSIX...**

---

## 🔧 Requirements

- **VS Code** 1.75 or later
- **YO interpreter** installed and available on PATH (`pip install yo-lang`)

---

## 📁 Extension Structure

```
yo-lang-vscode/
├── package.json                  # Extension manifest
├── extension.js                  # Run command logic
├── language-configuration.json   # Brackets, comments, indentation
├── syntaxes/
│   └── yo.tmLanguage.json        # TextMate grammar
├── snippets/
│   └── yo.snippets.json          # Code snippets
└── README.md                     # This file
```

---

## 📄 License

MIT — see the [yo-lang repository](https://github.com/yogeshsince2023/yo-lang) for details.
