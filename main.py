import sys
import logging
import sqlite3

DB_FILE = 'expenses.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

with get_db_connection() as conn:
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        note TEXT
    )""")
    conn.commit()

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt='%d/%m/%y %H:%M'
)
file_handler = logging.FileHandler("expense_tracker.log", encoding='utf-8')
file_handler.setFormatter(formatter)

main_logger = logging.getLogger("ExpenseTracker")
main_logger.setLevel(logging.DEBUG)
main_logger.addHandler(file_handler)

loggers = {
    name: logging.getLogger(name)
    for name in [
        "AddExpense", "ViewExpense", "Total",
        "CategorySummary", "LastExpense",
        "ExpenseByID", "DeleteExpense", "Menu"
    ]
}
for logger in loggers.values():
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

class ExpenseTracker:
    def __init__(self):
        main_logger.info("Expense Tracker started")

    def main_menu(self):
        print("\nPersonal Expense Tracker")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Spent")
        print("4. View Category Summary")
        print("5. View Last Expense")
        print("6. View Expense by ID")
        print("7. Delete Expense by ID")
        print("0. Exit")

    def add_expense(self):
        try:
            amount = float(input("How much is the expense?\n-> "))
            category = input("What category is it?\n-> ").strip()
            note = input("Note (optional):\n-> ").strip()
            with get_db_connection() as conn:
                c = conn.cursor()
                c.execute(
                    "INSERT INTO expenses (amount, category, note) VALUES (?, ?, ?)",
                    (amount, category, note)
                )
                conn.commit()
                new_id = c.lastrowid
            print(f"Expense added with ID: {new_id}")
            loggers["AddExpense"].info(
                f"Added expense ID {new_id} - ₹{amount} - {category} - '{note}'"
            )
        except ValueError:
            loggers["AddExpense"].warning("Failed to add expense — invalid amount")
            print("Invalid amount. Please enter a number.")

    def view_expenses(self):
        with get_db_connection() as conn:
            items = conn.execute(
                "SELECT * FROM expenses ORDER BY id"
            ).fetchall()
        if not items:
            print("No expenses yet.")
            loggers["ViewExpense"].info("Tried to view expenses — none found")
            return

        print(f"ID\tAmount\tCategory\tNote")
        for row in items:
            print(f"{row['id']}\t₹{row['amount']}\t{row['category']}\t{row['note']}")
        loggers["ViewExpense"].info("Viewed all expenses")

    def view_total(self):
        with get_db_connection() as conn:
            total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0
        print(f"Total amount spent: ₹{total}")
        loggers["Total"].info(f"Viewed total spent: ₹{total}")

    def view_category_summary(self):
        with get_db_connection() as conn:
            rows = conn.execute(
                "SELECT category, SUM(amount) AS total FROM expenses GROUP BY category"
            ).fetchall()
        if not rows:
            print("No expenses to summarize.")
            loggers["CategorySummary"].info("Tried to view category summary — none found")
            return

        print("Category-wise Summary:")
        for row in rows:
            print(f"{row['category']}: ₹{row['total']}")
        loggers["CategorySummary"].info("Viewed category summary")

    def view_last_expense(self):
        with get_db_connection() as conn:
            row = conn.execute(
                "SELECT * FROM expenses ORDER BY id DESC LIMIT 1"
            ).fetchone()
        if not row:
            print("No expenses found.")
            loggers["LastExpense"].info("Tried to view last expense — none found")
        else:
            print("Last Expense ->")
            print(f"ID: {row['id']}")
            print(f"Amount: ₹{row['amount']}")
            print(f"Category: {row['category']}")
            print(f"Note: {row['note']}")
            loggers["LastExpense"].info(f"Viewed last expense: ID {row['id']}")

    def view_expense_by_id(self):
        try:
            expense_id = int(input("Enter expense ID to view:\n-> "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            loggers["ExpenseByID"].warning("Invalid input when trying to view by ID")
            return

        with get_db_connection() as conn:
            row = conn.execute(
                "SELECT * FROM expenses WHERE id = ?", (expense_id,)
            ).fetchone()
        if row:
            print("\nExpense Found:")
            print(f"ID: {row['id']}")
            print(f"Amount: ₹{row['amount']}")
            print(f"Category: {row['category']}")
            print(f"Note: {row['note']}")
            loggers["ExpenseByID"].info(f"Viewed expense ID {expense_id}")
        else:
            print("Expense with that ID not found.")
            loggers["ExpenseByID"].warning(f"Expense ID {expense_id} not found")

    def delete_expense(self):
        try:
            expense_id = int(input("Enter expense ID to delete:\n-> "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            loggers["DeleteExpense"].warning("Invalid input when trying to delete by ID")
            return

        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            if c.rowcount:
                conn.commit()
                print(f"Deleted expense with ID: {expense_id}")
                loggers["DeleteExpense"].info(f"Deleted expense ID {expense_id}")
            else:
                print("Expense ID not found.")
                loggers["DeleteExpense"].warning(f"Expense ID {expense_id} not found")

    def run(self):
        while True:
            self.main_menu()
            try:
                choice = int(input("Choose an option:\n-> "))
            except ValueError:
                print("Please enter a valid number.")
                loggers["Menu"].warning("Invalid menu input — not a number")
                continue

            if choice == 0:
                print("Goodbye!")
                main_logger.info("App exited by user")
                sys.exit()
            elif choice == 1:
                self.add_expense()
            elif choice == 2:
                self.view_expenses()
            elif choice == 3:
                self.view_total()
            elif choice == 4:
                self.view_category_summary()
            elif choice == 5:
                self.view_last_expense()
            elif choice == 6:
                self.view_expense_by_id()
            elif choice == 7:
                self.delete_expense()
            else:
                print("Invalid input. Try again.")
                loggers["Menu"].warning("Invalid menu option selected")

if __name__ == "__main__":
    app = ExpenseTracker()
    app.run()