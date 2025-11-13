# JSON Generator

This script takes a **JSON template** and a **CSV file** as input, then produces an **output JSON** file where each line in the CSV generates one JSON object based on the template.
Every column in the CSV (e.g., `exclusionValue`, `description`) will overwrite the matching key in the template.

---

## 🧩 Example

### **Template (template.json)**

```json
[
    {
        "exclusionType": "URLToFilter",
        "exclusionFamily": "urlFilteringExclusions",
        "description": "",
        "exclusionValue": "",
        "state": "NEW"
    }
]
```

### **Input CSV (input.csv)**

```csv
exclusionValue;description
google.com;test
amazon.com;1
microsoft.com;2
```

### **Resulting Output (output.json)**

```json
[
    {
        "exclusionType": "URLToFilter",
        "exclusionFamily": "urlFilteringExclusions",
        "description": "test",
        "exclusionValue": "google.com",
        "state": "NEW"
    },
    {
        "exclusionType": "URLToFilter",
        "exclusionFamily": "urlFilteringExclusions",
        "description": "1",
        "exclusionValue": "amazon.com",
        "state": "NEW"
    },
    {
        "exclusionType": "URLToFilter",
        "exclusionFamily": "urlFilteringExclusions",
        "description": "2",
        "exclusionValue": "microsoft.com",
        "state": "NEW"
    }
]
```

---

## ⚙️ Installation

### 1. Clone or copy the repository

```bash
mkdir ~/json_generator
cd ~/json_generator
```

### 2. Install Python 3 (if not already installed)

```bash
sudo apt update
sudo apt install python3
```

### 3. Verify Python is installed

```bash
python3 --version
```

### 4. Place the following files in the same directory:

```
json_generator.py
template.json
input.csv
```

---

## ▶️ Usage

Run the script with:

```bash
python3 json_generator.py template.json input.csv output.json
```

### Optional flags:

| Flag     | Description                                              | Example  |
| -------- | -------------------------------------------------------- | -------- |
| `-d ";"` | Set a custom CSV delimiter (default: auto-detect or `,`) | `-d ";"` |

Example with semicolon-separated CSV:

```bash
python3 json_generator.py template.json input.csv output.json -d ";"
```

---

## 💡 Features

✅ Supports **CSV files with one or multiple columns**
✅ Automatically **detects the delimiter** (`,` `;` `|` `Tab`)
✅ Works even if the **output file already exists** — new entries will be appended
✅ Handles **broken or empty JSON files** gracefully
✅ Keeps the output **pretty-printed** for readability

---

## 🛠 Troubleshooting

| Issue                            | Cause                                         | Solution                                                    |
| -------------------------------- | --------------------------------------------- | ----------------------------------------------------------- |
| `Could not determine delimiter`  | The CSV only has one column                   | Use `-d ';'` or `-d ','` manually                           |
| `ValueError: Column ... missing` | CSV header doesn’t match your JSON fields     | Make sure your CSV headers (first row) match your JSON keys |
| Empty output                     | CSV contains empty rows or mismatched headers | Clean up CSV and ensure consistent column names             |

---

## 📘 License

MIT License — you can freely use and modify this script.
