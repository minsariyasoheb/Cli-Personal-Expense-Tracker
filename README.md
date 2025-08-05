# CLI-Personal-Expense-Tracker

A simple, SQLite-backed personal expense tracker in the command line.

---

## 🚀 Features

- **Add** new expenses with amount, category, and optional note  
- **View** all expenses, or filter by ID  
- **Show** total amount spent  
- **Category**-wise spending summary  
- **View** the most recent expense  
- **Delete** expenses by ID  
- **Persistent storage** via SQLite  
- **Structured logging** to `expense_tracker.log`  

---

## 🛠️ Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/minsariyasoheb/Cli-Personal-Expense-Tracker.git
   cd CLI-Personal-Expense-Tracker
   ```

2. **Create & activate** a virtual environment (optional, but recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install requirements**

   ```bash
   pip install -r requirements.txt
   ```

   > *(If you have no extra dependencies, you can skip this step.)*

---

## ⚙️ Usage

Run the tracker:

```bash
python expense_tracker.py
```

You’ll see a menu:

```
1. Add Expense
2. View All Expenses
3. View Total Spent
4. View Category Summary
5. View Last Expense
6. View Expense by ID
7. Delete Expense by ID
0. Exit
```

Just enter the number for the action you want, then follow the prompts.

---

## 🔧 Configuration

* **Database file**: `expenses.db` (auto-created on first run)
* **Log file**: `expense_tracker.log`

You can change these names or paths at the top of the script.

---

## 📈 Extending & Customizing

* **Export/Import** CSV or JSON
* **Budget alerts** (e.g. warn when monthly spend > limit)
* **Report generation** (monthly/weekly)
* **GUI/Web front-end** via Tkinter, Flask, or Streamlit
* **Packaging** with `setup.py` for `pip install`

Want to contribute? Feel free to open an issue or submit a PR!

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

```

Feel free to tweak any section—especially the “Extending & Customizing” ideas—to highlight whatever extras you implement next!
```