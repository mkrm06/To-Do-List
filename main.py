import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import hashlib
from datetime import datetime
from typing import List, Dict, Optional


class Task:
    """Represents a single task in the to-do list"""
    def __init__(self, name: str, priority: str, due_date: str, category: str, status: str = "Pending"):
        self.name = name
        self.priority = priority
        self.due_date = due_date
        self.category = category
        self.status = status
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON storage"""
        return {
            "name": self.name,
            "priority": self.priority,
            "due_date": self.due_date,
            "category": self.category,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create task from dictionary"""
        return cls(
            name=data.get("name", ""),
            priority=data.get("priority", "Low"),
            due_date=data.get("due_date", ""),
            category=data.get("category", "Personal"),
            status=data.get("status", "Pending")
        )


class UserManager:
    """Manages user credentials and authentication"""
    def __init__(self):
        self.users_file = "users.json"
        self.users = self.load_users()
    
    def load_users(self) -> Dict:
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def save_users(self):
        """Save users to JSON file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
            return True
        except IOError:
            return False
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, password: str) -> bool:
        """Register a new user"""
        username = username.strip().lower()
        if not username or not password:
            return False
        
        if username in self.users:
            return False  # User already exists
        
        hashed_password = self.hash_password(password)
        self.users[username] = {"password": hashed_password}
        return self.save_users()
    
    def verify_user(self, username: str, password: str) -> bool:
        """Verify user credentials"""
        username = username.strip().lower()
        if username not in self.users:
            return False
        
        hashed_password = self.hash_password(password)
        return self.users[username]["password"] == hashed_password
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists"""
        username = username.strip().lower()
        return username in self.users


class TaskManager:
    """Manages tasks storage and retrieval"""
    def __init__(self, username: str):
        self.username = username
        self.filename = f"{username}_tasks.json"
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
            except (json.JSONDecodeError, IOError):
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            data = [task.to_dict() for task in self.tasks]
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except IOError:
            return False
    
    def add_task(self, task: Task):
        """Add a new task"""
        self.tasks.append(task)
        self.save_tasks()
    
    def update_task(self, index: int, task: Task):
        """Update an existing task"""
        if 0 <= index < len(self.tasks):
            self.tasks[index] = task
            self.save_tasks()
            return True
        return False
    
    def delete_task(self, index: int):
        """Delete a task"""
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks()
            return True
        return False
    
    def mark_completed(self, index: int):
        """Mark a task as completed"""
        if 0 <= index < len(self.tasks):
            self.tasks[index].status = "Completed"
            self.save_tasks()
            return True
        return False
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return self.tasks


class LoginWindow:
    """Login window for user authentication"""
    def __init__(self):
        self.user_manager = UserManager()
        self.root = tk.Tk()
        self.root.title("To-Do List - Login")
        self.root.geometry("450x300")
        self.root.resizable(False, False)
        self.username = None
        
        # Center the window
        self.center_window()
        
        # Create UI
        self.create_widgets()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create login UI widgets"""
        # Title
        title_label = tk.Label(
            self.root,
            text="To-Do List Management System",
            font=("Arial", 16, "bold"),
            pady=20
        )
        title_label.pack()
        
        # Login form frame
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)
        
        # Username
        username_frame = tk.Frame(form_frame)
        username_frame.pack(pady=8)
        tk.Label(username_frame, text="Username:", font=("Arial", 11), width=12, anchor=tk.W).pack(side=tk.LEFT, padx=5)
        self.username_entry = tk.Entry(username_frame, font=("Arial", 11), width=20)
        self.username_entry.pack(side=tk.LEFT, padx=5)
        self.username_entry.focus()
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        
        # Password
        password_frame = tk.Frame(form_frame)
        password_frame.pack(pady=8)
        tk.Label(password_frame, text="Password:", font=("Arial", 11), width=12, anchor=tk.W).pack(side=tk.LEFT, padx=5)
        self.password_entry = tk.Entry(password_frame, font=("Arial", 11), width=20, show="*")
        self.password_entry.pack(side=tk.LEFT, padx=5)
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Login button
        login_btn = tk.Button(
            button_frame,
            text="Login",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5,
            command=self.login
        )
        login_btn.pack(side=tk.LEFT, padx=5)
        
        # Register button
        register_btn = tk.Button(
            button_frame,
            text="Register",
            font=("Arial", 11, "bold"),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=5,
            command=self.register
        )
        register_btn.pack(side=tk.LEFT, padx=5)
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Validation
        if not username:
            messagebox.showerror("Error", "Please enter a username!")
            self.username_entry.focus()
            return
        
        if not password:
            messagebox.showerror("Error", "Please enter a password!")
            self.password_entry.focus()
            return
        
        # Verify credentials
        if self.user_manager.verify_user(username, password):
            self.username = username
            self.root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def register(self):
        """Handle user registration"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Validation
        if not username:
            messagebox.showerror("Error", "Please enter a username!")
            self.username_entry.focus()
            return
        
        if not password:
            messagebox.showerror("Error", "Please enter a password!")
            self.password_entry.focus()
            return
        
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters long!")
            self.password_entry.focus()
            return
        
        # Check if user already exists
        if self.user_manager.user_exists(username):
            messagebox.showerror("Registration Failed", "Username already exists! Please choose a different username.")
            self.username_entry.focus()
            return
        
        # Register new user
        if self.user_manager.register_user(username, password):
            messagebox.showinfo("Success", f"User '{username}' registered successfully! You can now login.")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
        else:
            messagebox.showerror("Registration Failed", "Failed to register user. Please try again.")
    
    def run(self) -> Optional[str]:
        """Run login window and return username"""
        self.root.mainloop()
        return self.username


class TodoApp:
    """Main To-Do List Application"""
    def __init__(self, username: str):
        self.username = username
        self.task_manager = TaskManager(username)
        self.selected_index = None
        
        # Create main window
        self.root = tk.Tk()
        self.root.title(f"To-Do List - {username}")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Center the window
        self.center_window()
        
        # Create UI
        self.create_widgets()
        
        # Load and display tasks
        self.refresh_task_list()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create main application UI"""
        # Header
        header_frame = tk.Frame(self.root, bg="#2196F3", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text=f"Welcome, {self.username}!",
            font=("Arial", 16, "bold"),
            bg="#2196F3",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Task input
        left_panel = tk.Frame(main_container, width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Task input form
        input_frame = tk.LabelFrame(left_panel, text="Add/Edit Task", font=("Arial", 12, "bold"), padx=10, pady=10)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        # Task Name
        tk.Label(input_frame, text="Task Name:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.task_name_entry = tk.Entry(input_frame, font=("Arial", 10), width=25)
        self.task_name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Priority
        tk.Label(input_frame, text="Priority:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.priority_var = tk.StringVar(value="Low")
        priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var, values=["High", "Low"], state="readonly", width=22)
        priority_combo.grid(row=1, column=1, pady=5, padx=5)
        
        # Due Date
        tk.Label(input_frame, text="Due Date:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.due_date_entry = tk.Entry(input_frame, font=("Arial", 10), width=25)
        self.due_date_entry.grid(row=2, column=1, pady=5, padx=5)
        tk.Label(input_frame, text="(YYYY-MM-DD)", font=("Arial", 8), fg="gray").grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # Category
        tk.Label(input_frame, text="Category:", font=("Arial", 10)).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar(value="Personal")
        category_combo = ttk.Combobox(
            input_frame,
            textvariable=self.category_var,
            values=["Work", "Personal", "Study", "Shopping", "Health", "Other"],
            state="readonly",
            width=22
        )
        category_combo.grid(row=4, column=1, pady=5, padx=5)
        
        # Buttons frame
        button_frame = tk.Frame(input_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        self.add_btn = tk.Button(
            button_frame,
            text="Add Task",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=5,
            command=self.add_task
        )
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.update_btn = tk.Button(
            button_frame,
            text="Update Task",
            font=("Arial", 10, "bold"),
            bg="#FF9800",
            fg="white",
            padx=15,
            pady=5,
            command=self.update_task,
            state=tk.DISABLED
        )
        self.update_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(
            button_frame,
            text="Clear",
            font=("Arial", 10),
            bg="#9E9E9E",
            fg="white",
            padx=15,
            pady=5,
            command=self.clear_form
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Right panel - Task list
        right_panel = tk.Frame(main_container)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Task list frame
        list_frame = tk.LabelFrame(right_panel, text="Task List", font=("Arial", 12, "bold"), padx=10, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for task list
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Task listbox with scrollbar
        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 10),
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            height=20
        )
        self.task_listbox.pack(fill=tk.BOTH, expand=True)
        self.task_listbox.bind('<<ListboxSelect>>', self.on_task_select)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Action buttons frame
        action_frame = tk.Frame(right_panel)
        action_frame.pack(fill=tk.X, pady=10)
        
        self.complete_btn = tk.Button(
            action_frame,
            text="Mark Completed",
            font=("Arial", 10, "bold"),
            bg="#2196F3",
            fg="white",
            padx=15,
            pady=5,
            command=self.mark_completed
        )
        self.complete_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = tk.Button(
            action_frame,
            text="Delete Task",
            font=("Arial", 10, "bold"),
            bg="#F44336",
            fg="white",
            padx=15,
            pady=5,
            command=self.delete_task
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_btn = tk.Button(
            action_frame,
            text="Refresh",
            font=("Arial", 10),
            bg="#607D8B",
            fg="white",
            padx=15,
            pady=5,
            command=self.refresh_task_list
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
    
    def validate_date(self, date_string: str) -> bool:
        """Validate date format (YYYY-MM-DD)"""
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def clear_form(self):
        """Clear the input form"""
        self.task_name_entry.delete(0, tk.END)
        self.priority_var.set("Low")
        self.due_date_entry.delete(0, tk.END)
        self.category_var.set("Personal")
        self.selected_index = None
        self.update_btn.config(state=tk.DISABLED)
        self.add_btn.config(state=tk.NORMAL)
        self.task_listbox.selection_clear(0, tk.END)
    
    def add_task(self):
        """Add a new task"""
        name = self.task_name_entry.get().strip()
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get().strip()
        category = self.category_var.get()
        
        # Validation
        if not name:
            messagebox.showerror("Error", "Please enter a task name!")
            return
        
        if due_date and not self.validate_date(due_date):
            messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD")
            return
        
        # Create and add task
        task = Task(name, priority, due_date, category, "Pending")
        self.task_manager.add_task(task)
        
        messagebox.showinfo("Success", "Task added successfully!")
        self.clear_form()
        self.refresh_task_list()
    
    def on_task_select(self, event):
        """Handle task selection from listbox"""
        selection = self.task_listbox.curselection()
        if selection:
            self.selected_index = selection[0]
            task = self.task_manager.tasks[self.selected_index]
            
            # Populate form with selected task
            self.task_name_entry.delete(0, tk.END)
            self.task_name_entry.insert(0, task.name)
            self.priority_var.set(task.priority)
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.insert(0, task.due_date)
            self.category_var.set(task.category)
            
            # Enable update button
            self.update_btn.config(state=tk.NORMAL)
            self.add_btn.config(state=tk.DISABLED)
    
    def update_task(self):
        """Update selected task"""
        if self.selected_index is None:
            messagebox.showerror("Error", "Please select a task to update!")
            return
        
        name = self.task_name_entry.get().strip()
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get().strip()
        category = self.category_var.get()
        
        # Validation
        if not name:
            messagebox.showerror("Error", "Please enter a task name!")
            return
        
        if due_date and not self.validate_date(due_date):
            messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD")
            return
        
        # Get original status
        original_task = self.task_manager.tasks[self.selected_index]
        status = original_task.status
        
        # Create updated task
        updated_task = Task(name, priority, due_date, category, status)
        
        if self.task_manager.update_task(self.selected_index, updated_task):
            messagebox.showinfo("Success", "Task updated successfully!")
            self.clear_form()
            self.refresh_task_list()
        else:
            messagebox.showerror("Error", "Failed to update task!")
    
    def delete_task(self):
        """Delete selected task"""
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a task to delete!")
            return
        
        index = selection[0]
        
        # Confirm deletion
        task = self.task_manager.tasks[index]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{task.name}'?"):
            if self.task_manager.delete_task(index):
                messagebox.showinfo("Success", "Task deleted successfully!")
                self.clear_form()
                self.refresh_task_list()
            else:
                messagebox.showerror("Error", "Failed to delete task!")
    
    def mark_completed(self):
        """Mark selected task as completed"""
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a task to mark as completed!")
            return
        
        index = selection[0]
        task = self.task_manager.tasks[index]
        
        if task.status == "Completed":
            messagebox.showinfo("Info", "Task is already completed!")
            return
        
        if self.task_manager.mark_completed(index):
            messagebox.showinfo("Success", "Task marked as completed!")
            self.clear_form()
            self.refresh_task_list()
        else:
            messagebox.showerror("Error", "Failed to update task status!")
    
    def refresh_task_list(self):
        """Refresh the task list display"""
        self.task_listbox.delete(0, tk.END)
        tasks = self.task_manager.get_all_tasks()
        
        for task in tasks:
            # Format task display
            status_icon = "✓" if task.status == "Completed" else "○"
            priority_icon = "🔴" if task.priority == "High" else "🟢"
            
            task_display = f"{status_icon} {priority_icon} {task.name} | {task.category} | Due: {task.due_date if task.due_date else 'No date'}"
            self.task_listbox.insert(tk.END, task_display)
            
            # Color completed tasks differently
            if task.status == "Completed":
                self.task_listbox.itemconfig(tk.END, {'fg': 'gray'})
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    # Show login window
    login = LoginWindow()
    username = login.run()
    
    if username:
        # Start main application
        app = TodoApp(username)
        app.run()
    else:
        print("Login cancelled.")


if __name__ == "__main__":
    main()

