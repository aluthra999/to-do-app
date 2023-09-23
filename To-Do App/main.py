import tkinter as tk
from tkinter import ttk, messagebox
import csv
import calendar


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do App")
        self.tasks = []

        # Create and configure a calendar
        self.cal = calendar.Calendar()

        # Create labels and entry fields
        self.date_label = ttk.Label(root, text="Select Date:")
        self.date_label.pack()

        self.date_entry = ttk.Combobox(root, values=self.get_dates())
        self.date_entry.pack()

        self.task_label = ttk.Label(root, text="Task:")
        self.task_label.pack()

        self.task_entry = ttk.Entry(root)
        self.task_entry.pack()

        # Create task list
        self.task_listbox = tk.Listbox(root, height=10, selectmode=tk.SINGLE)
        self.task_listbox.pack()

        # Create buttons
        self.add_button = ttk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.remove_button = ttk.Button(root, text="Remove Task", command=self.remove_task)
        self.remove_button.pack()

        self.mark_important_button = ttk.Button(root, text="Mark Important", command=self.mark_important)
        self.mark_important_button.pack()

        self.mark_done_button = ttk.Button(root, text="Mark Done/Undone", command=self.mark_done)
        self.mark_done_button.pack()

        # Load tasks from CSV file
        self.load_tasks()

    def get_dates(self):
        return [str(date) for date in self.cal.itermonthdates(2023, 9)]

    def add_task(self):
        date = self.date_entry.get()
        task_text = self.task_entry.get()

        if date and task_text:
            self.tasks.append({"date": date, "task": task_text, "important": False, "done": False})
            self.update_task_listbox()
            self.save_tasks()
            self.clear_inputs()
        else:
            messagebox.showwarning("Warning", "Please enter a date and task text.")

    def remove_task(self):
        selected_index = self.task_listbox.curselection()

        if selected_index:
            index = selected_index[0]
            del self.tasks[index]
            self.update_task_listbox()
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    def mark_important(self):
        selected_index = self.task_listbox.curselection()

        if selected_index:
            index = selected_index[0]
            self.tasks[index]["important"] = not self.tasks[index]["important"]
            self.update_task_listbox()
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as important.")

    def mark_done(self):
        selected_index = self.task_listbox.curselection()

        if selected_index:
            index = selected_index[0]
            self.tasks[index]["done"] = not self.tasks[index]["done"]
            self.update_task_listbox()
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as done/undone.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_text = task["task"]
            if task["important"]:
                task_text = "❗ " + task_text
            if task["done"]:
                task_text = "✔ " + task_text
            self.task_listbox.insert(tk.END, task_text)

    def clear_inputs(self):
        self.date_entry.set("")
        self.task_entry.delete(0, tk.END)

    def save_tasks(self):
        with open("tasks.csv", mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["date", "task", "important", "done"])
            writer.writeheader()
            writer.writerows(self.tasks)

    def load_tasks(self):
        try:
            with open("tasks.csv", mode="r") as file:
                reader = csv.DictReader(file)
                self.tasks = [row for row in reader]
                self.update_task_listbox()
        except FileNotFoundError:
            self.tasks = []


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.geometry("250x350")
    root.mainloop()
