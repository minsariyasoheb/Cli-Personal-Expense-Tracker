import sys
import logging

logger = logging.getLogger("Expense Tracker")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("expense_tracker.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt='%d/%m/%y %H:%M')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.next_id = 1
        logger.info("Expense Tracker started")

    def main_menu(self):
        print("\nPersonal Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Total Spent")
        print("4. View Category Summary")
        print("5. View Last Expense")
        print("6. View Expense by ID")
        print("7. Delete Expense by ID")
        print("0. Exit")

    def add_expense(self):
        try:
            amount = float(input("How much is the expense?\n-> "))
            category = input("What category is it?\n-> ")
            note = input("Note (optional):\n-> ")
            expense = {
                "id": self.next_id,
                "amount": amount,
                "category": category,
                "note": note,
            }
            self.expenses.append(expense)
            logger.info(f"Added expense ID {self.next_id} - INR {amount} - {category}")
            print(f"Expense added with ID: {self.next_id}")
            self.next_id += 1
        except ValueError:
            logger.warning("Failed to add expense — invalid amount")
            print("Invalid amount. Please enter a number.")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses yet.")
            logger.info("Tried to view expenses — list is empty")
            return

        print(f"ID\tAmount\tCategory\tNote")
        for exp in self.expenses:
            print(f"{exp['id']}\t₹{exp['amount']}\t{exp['category']}\t\t{exp['note']}")
        logger.info("Viewed all expenses")

    def view_total(self):
        total = sum(exp['amount'] for exp in self.expenses)
        print(f"Total amount spent: ₹{total}")
        logger.info(f"Viewed total spent: INR{total}")

    def view_category_summary(self):
        if not self.expenses:
            print("No expenses to summarize.")
            logger.info("Tried to view category summary — no expenses")
            return
        summary = {}
        for exp in self.expenses:
            cat = exp['category']
            summary[cat] = summary.get(cat, 0) + exp['amount']
        print("Category-wise Summary:")
        for cat, total in summary.items():
            print(f"{cat}: ₹{total}")
        logger.info("Viewed category summary")

    def view_last_expense(self):
        if not self.expenses:
            print("No expenses found.")
            logger.info("Tried to view last expense — list is empty")
        else:
            exp = self.expenses[-1]
            print(f"Last Expense ->\nID: {exp['id']}\nAmount: ₹{exp['amount']}\nCategory: {exp['category']}\nNote: {exp['note']}")
            logger.info(f"Viewed last expense: ID {exp['id']}")

    def view_expense_by_id(self):
        try:
            expense_id = int(input("Enter expense ID to view:\n-> "))
            for exp in self.expenses:
                if exp['id'] == expense_id:
                    print(f"\nExpense Found:")
                    print(f"ID: {exp['id']}")
                    print(f"Amount: ₹{exp['amount']}")
                    print(f"Category: {exp['category']}")
                    print(f"Note: {exp['note']}")
                    logger.info(f"Viewed expense ID {expense_id}")
                    return
            print("Expense with that ID not found.")
            logger.warning(f"Expense ID {expense_id} not found when trying to view")
        except ValueError:
            print("Invalid input. Please enter a number.")
            logger.warning("Invalid input when trying to view by ID")

    def delete_expense(self):
        try:
            id_to_delete = int(input("Enter expense ID to delete:\n-> "))
            for exp in self.expenses:
                if exp['id'] == id_to_delete:
                    self.expenses.remove(exp)
                    print(f"Deleted expense with ID: {id_to_delete}")
                    logger.info(f"Deleted expense ID {id_to_delete}")
                    return
            print("Expense ID not found.")
            logger.warning(f"Expense ID {id_to_delete} not found when trying to delete")
        except ValueError:
            print("Invalid input. Please enter a number.")
            logger.warning("Invalid input when trying to delete by ID")

    def run(self):
        while True:
            self.main_menu()
            try:
                choice = int(input("Choose an option:\n-> "))
            except ValueError:
                print("Please enter a valid number.")
                logger.warning("Invalid menu input — not a number")
                continue

            if choice == 0:
                print("Goodbye!")
                logger.info("App exited by user")
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
                logger.warning("Invalid menu option selected")


if __name__ == "__main__":
    app = ExpenseTracker()
    app.run()