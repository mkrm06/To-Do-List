# Software Requirements Specification (SRS)
## To-Do List Management System

**Version:** 1.0  
**Date:** 23/12/2025  
**Prepared by:** Mohamed Mukarram  
**Status:** Final

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Features](#3-system-features)
4. [External Interface Requirements](#4-external-interface-requirements)
5. [System Requirements](#5-system-requirements)
6. [System Architecture](#6-system-architecture)
7. [System Design](#7-system-design)
8. [Implementation Details](#8-implementation-details)
9. [Testing Requirements](#9-testing-requirements)
10. [Appendices](#10-appendices)

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) document provides a comprehensive description of the To-Do List Management System. It describes the system's purpose, features, interfaces, and constraints. This document is intended for developers, testers, project managers, and stakeholders involved in the development and maintenance of the system.

### 1.2 Scope

The To-Do List Management System is a standalone desktop application that allows users to:

- **User Authentication**: Register and login with username and password
- **Task Management**: Create, view, edit, delete, and complete tasks
- **Task Organization**: Categorize tasks and set priorities
- **Data Persistence**: Automatically save and load tasks from local storage
- **User Interface**: Intuitive graphical user interface built with Tkinter

The system is designed for single-user operation on a local machine. It does not support:
- Multi-user collaboration
- Cloud synchronization
- Network-based access
- Mobile platforms

### 1.3 Definitions, Acronyms, and Abbreviations

| Term | Definition |
|------|------------|
| **Task** | A to-do item created by the user containing name, priority, due date, category, and status |
| **Status** | Indicates whether a task is "Pending" or "Completed" |
| **Priority** | Task importance level: "High" or "Low" |
| **Category** | Task classification: Work, Personal, Study, Shopping, Health, or Other |
| **CLI** | Command Line Interface |
| **GUI** | Graphical User Interface |
| **JSON** | JavaScript Object Notation - data storage format |
| **SHA-256** | Secure Hash Algorithm 256-bit - password hashing algorithm |
| **SRS** | Software Requirements Specification |
| **CRUD** | Create, Read, Update, Delete operations |

### 1.4 References

- Python 3.6+ Documentation: https://docs.python.org/3/
- Tkinter Documentation: https://docs.python.org/3/library/tkinter.html
- JSON Specification: https://www.json.org/

### 1.5 Overview

This document is organized into sections covering:
- System overview and perspective
- Functional and non-functional requirements
- User interface specifications
- System architecture and design
- Implementation details
- Testing requirements

---

## 2. Overall Description

### 2.1 Product Perspective

The To-Do List Management System is a standalone Python application that operates independently without requiring external services or network connectivity. The system consists of:

- **Application Layer**: Python application with Tkinter GUI
- **Storage Layer**: JSON-based file storage for user credentials and tasks
- **Authentication Layer**: User registration and login system with password hashing

```
┌─────────────────────────────────────┐
│     To-Do List Application          │
│  ┌──────────────┐  ┌──────────────┐ │
│  │   GUI Layer  │  │  Logic Layer │ │
│  └──────────────┘  └──────────────┘ │
│         │                 │          │
│  ┌──────────────┐  ┌──────────────┐ │
│  │ Auth Manager │  │Task Manager  │ │
│  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────┘
         │                 │
    ┌────────┐      ┌──────────────┐
    │users.json│    │username_tasks.json│
    └────────┘      └──────────────┘
```

### 2.2 Product Features

#### 2.2.1 Core Features

1. **User Authentication System**
   - User registration with username and password
   - Secure login with password verification
   - Password hashing using SHA-256
   - User credential storage

2. **Task Management**
   - Add new tasks with complete details
   - View all tasks in organized list
   - Edit existing tasks
   - Delete tasks with confirmation
   - Mark tasks as completed

3. **Task Attributes**
   - Task name (required)
   - Priority: High or Low
   - Due date (optional, YYYY-MM-DD format)
   - Category: Work, Personal, Study, Shopping, Health, Other
   - Status: Pending or Completed

4. **Data Management**
   - Automatic task saving
   - Automatic data loading on startup
   - Per-user task storage
   - Persistent storage using JSON files

5. **User Interface**
   - Modern, intuitive GUI
   - Color-coded visual indicators
   - Input validation and error handling
   - Responsive layout

### 2.3 User Classes and Characteristics

**Primary User**: Individual users managing personal tasks
- **Technical Skill**: Basic computer literacy
- **Usage Pattern**: Daily task management
- **Requirements**: Simple, intuitive interface

### 2.4 Operating Environment

- **Operating System**: Windows, macOS, Linux (any OS supporting Python)
- **Python Version**: 3.6 or higher
- **Dependencies**: Tkinter (included with Python standard library)
- **Storage**: Local file system
- **Hardware**: Standard PC/laptop with minimal requirements

### 2.5 Design and Implementation Constraints

1. **Technology Constraints**
   - Must use Python 3.6+
   - Must use Tkinter for GUI (standard library)
   - Must use JSON for data storage
   - No external dependencies required

2. **Platform Constraints**
   - Desktop application only
   - Single-user operation
   - Local storage only
   - No network connectivity required

3. **Security Constraints**
   - Passwords must be hashed (SHA-256)
   - No plaintext password storage
   - Local-only data storage

### 2.6 Assumptions and Dependencies

**Assumptions:**
- Users have Python 3.6+ installed
- Users have basic computer literacy
- Users will use the system regularly
- Users will not enter malicious inputs
- File system is accessible and writable

**Dependencies:**
- Python standard library (Tkinter, json, hashlib, os, datetime)
- Operating system file system access
- Sufficient disk space for data storage

---

## 3. System Features

### 3.1 User Authentication System

#### 3.1.1 User Registration

**Description**: New users can create an account by providing a username and password.

**Functional Requirements:**
- **FR-1.1**: System shall accept username and password input
- **FR-1.2**: System shall validate username is not empty
- **FR-1.3**: System shall validate password is at least 4 characters
- **FR-1.4**: System shall check if username already exists
- **FR-1.5**: System shall hash password using SHA-256 before storage
- **FR-1.6**: System shall store user credentials in `users.json`
- **FR-1.7**: System shall display success message upon registration
- **FR-1.8**: System shall display error message if username exists

**Input**: Username (string), Password (string)  
**Output**: Success/Error message, User account created

#### 3.1.2 User Login

**Description**: Existing users can access the system by providing valid credentials.

**Functional Requirements:**
- **FR-2.1**: System shall accept username and password input
- **FR-2.2**: System shall validate both fields are not empty
- **FR-2.3**: System shall hash input password using SHA-256
- **FR-2.4**: System shall compare hashed password with stored hash
- **FR-2.5**: System shall grant access if credentials match
- **FR-2.6**: System shall deny access and show error if credentials don't match
- **FR-2.7**: System shall load user's tasks upon successful login

**Input**: Username (string), Password (string)  
**Output**: Access granted/denied, Main application window

### 3.2 Task Management System

#### 3.2.1 Add Task

**Description**: Users can create new tasks with specified attributes.

**Functional Requirements:**
- **FR-3.1**: System shall accept task name (required)
- **FR-3.2**: System shall accept priority selection (High/Low)
- **FR-3.3**: System shall accept due date (optional, YYYY-MM-DD format)
- **FR-3.4**: System shall accept category selection
- **FR-3.5**: System shall validate task name is not empty
- **FR-3.6**: System shall validate date format if provided
- **FR-3.7**: System shall set default status as "Pending"
- **FR-3.8**: System shall save task to user's task file
- **FR-3.9**: System shall refresh task list display
- **FR-3.10**: System shall clear input form after successful addition

**Input**: Task name, Priority, Due date, Category  
**Output**: Task added, Task list updated

#### 3.2.2 View Tasks

**Description**: Users can view all their tasks with complete details.

**Functional Requirements:**
- **FR-4.1**: System shall load all tasks from user's task file
- **FR-4.2**: System shall display tasks in scrollable list
- **FR-4.3**: System shall show task name, priority, category, due date, and status
- **FR-4.4**: System shall use visual indicators for priority (🔴 High, 🟢 Low)
- **FR-4.5**: System shall use visual indicators for status (✓ Completed, ○ Pending)
- **FR-4.6**: System shall display completed tasks in gray color
- **FR-4.7**: System shall update display when tasks are modified

**Input**: None  
**Output**: Task list display with all task details

#### 3.2.3 Edit Task

**Description**: Users can modify existing task attributes.

**Functional Requirements:**
- **FR-5.1**: System shall allow task selection from list
- **FR-5.2**: System shall populate form with selected task data
- **FR-5.3**: System shall allow modification of task name, priority, due date, category
- **FR-5.4**: System shall preserve task status during edit
- **FR-5.5**: System shall validate modified data
- **FR-5.6**: System shall update task in storage
- **FR-5.7**: System shall refresh task list display
- **FR-5.8**: System shall clear form after update

**Input**: Selected task, Modified task data  
**Output**: Task updated, Task list refreshed

#### 3.2.4 Delete Task

**Description**: Users can remove tasks from their list.

**Functional Requirements:**
- **FR-6.1**: System shall allow task selection
- **FR-6.2**: System shall display confirmation dialog
- **FR-6.3**: System shall delete task if confirmed
- **FR-6.4**: System shall update storage file
- **FR-6.5**: System shall refresh task list display
- **FR-6.6**: System shall cancel deletion if not confirmed

**Input**: Selected task, Confirmation  
**Output**: Task deleted, Task list updated

#### 3.2.5 Mark Task as Completed

**Description**: Users can mark tasks as completed.

**Functional Requirements:**
- **FR-7.1**: System shall allow task selection
- **FR-7.2**: System shall change task status to "Completed"
- **FR-7.3**: System shall update task in storage
- **FR-7.4**: System shall refresh task list display
- **FR-7.5**: System shall show visual indicator for completed status
- **FR-7.6**: System shall prevent marking already completed tasks

**Input**: Selected task  
**Output**: Task status updated, Visual indicator changed

### 3.3 Data Persistence

#### 3.3.1 Save Tasks

**Description**: System automatically saves tasks to persistent storage.

**Functional Requirements:**
- **FR-8.1**: System shall save tasks after each modification
- **FR-8.2**: System shall store tasks in JSON format
- **FR-8.3**: System shall use filename format: `[username]_tasks.json`
- **FR-8.4**: System shall handle file write errors gracefully
- **FR-8.5**: System shall maintain data integrity

**Input**: Task data  
**Output**: JSON file updated

#### 3.3.2 Load Tasks

**Description**: System automatically loads tasks on startup.

**Functional Requirements:**
- **FR-9.1**: System shall load tasks from user's task file on login
- **FR-9.2**: System shall handle missing file gracefully (empty task list)
- **FR-9.3**: System shall handle corrupted JSON files
- **FR-9.4**: System shall display loaded tasks in task list

**Input**: Username  
**Output**: Tasks loaded and displayed

---

## 4. External Interface Requirements

### 4.1 User Interface

#### 4.1.1 Login Window

**Layout:**
- Window title: "To-Do List - Login"
- Window size: 450x300 pixels
- Centered on screen

**Components:**
- Title label: "To-Do List Management System"
- Username entry field with label
- Password entry field with label (masked with *)
- Login button (green)
- Register button (blue)

**Interactions:**
- Enter key navigates: Username → Password → Login
- Click Login: Validates and authenticates user
- Click Register: Creates new user account

#### 4.1.2 Main Application Window

**Layout:**
- Window title: "To-Do List - [username]"
- Window size: 900x700 pixels (resizable)
- Header bar (blue background)
- Two-panel layout: Input form (left) and Task list (right)

**Left Panel - Task Input Form:**
- Task Name entry field
- Priority dropdown (High/Low)
- Due Date entry field with format hint
- Category dropdown (Work, Personal, Study, Shopping, Health, Other)
- Buttons: Add Task (green), Update Task (orange), Clear (gray)

**Right Panel - Task List:**
- Scrollable listbox displaying all tasks
- Visual indicators for priority and status
- Action buttons: Mark Completed (blue), Delete Task (red), Refresh (gray)

**Color Scheme:**
- Primary actions: Green (#4CAF50)
- Update actions: Orange (#FF9800)
- Delete actions: Red (#F44336)
- Info actions: Blue (#2196F3)
- Secondary: Gray (#9E9E9E, #607D8B)

### 4.2 Hardware Interface

**Requirements:**
- Standard PC/laptop
- Keyboard for input
- Mouse for navigation
- Display screen (minimum 1024x768 resolution)
- Local storage (minimal space required)

### 4.3 Software Interface

**Operating System:**
- Windows 10/11
- macOS 10.14+
- Linux (any distribution with Python support)

**Python Environment:**
- Python 3.6 or higher
- Tkinter library (included with Python)
- Standard library modules: json, hashlib, os, datetime

**File System:**
- Read/write access to application directory
- JSON file format for data storage
- UTF-8 encoding

### 4.4 Communication Interface

**Not Applicable** - This is a standalone application with no network communication requirements.

---

## 5. System Requirements

### 5.1 Functional Requirements Summary

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1.1 to FR-1.8 | User Registration | High |
| FR-2.1 to FR-2.7 | User Login | High |
| FR-3.1 to FR-3.10 | Add Task | High |
| FR-4.1 to FR-4.7 | View Tasks | High |
| FR-5.1 to FR-5.8 | Edit Task | High |
| FR-6.1 to FR-6.6 | Delete Task | High |
| FR-7.1 to FR-7.6 | Mark Completed | High |
| FR-8.1 to FR-8.5 | Save Tasks | High |
| FR-9.1 to FR-9.4 | Load Tasks | High |

### 5.2 Non-Functional Requirements

#### 5.2.1 Performance Requirements

- **NFR-1**: Application shall respond to user actions within 1 second
- **NFR-2**: Task list shall load within 2 seconds for up to 1000 tasks
- **NFR-3**: File operations (save/load) shall complete within 500ms
- **NFR-4**: GUI shall remain responsive during all operations

#### 5.2.2 Usability Requirements

- **NFR-5**: Interface shall be intuitive for users with basic computer literacy
- **NFR-6**: All actions shall provide visual feedback
- **NFR-7**: Error messages shall be clear and actionable
- **NFR-8**: Keyboard navigation shall be supported (Enter key, Tab key)

#### 5.2.3 Reliability Requirements

- **NFR-9**: System shall not lose data under normal operation
- **NFR-10**: System shall handle file I/O errors gracefully
- **NFR-11**: System shall validate all user inputs
- **NFR-12**: System shall prevent data corruption

#### 5.2.4 Security Requirements

- **NFR-13**: Passwords shall be hashed using SHA-256
- **NFR-14**: No plaintext passwords shall be stored
- **NFR-15**: User data shall be isolated per user
- **NFR-16**: System shall prevent unauthorized access

#### 5.2.5 Portability Requirements

- **NFR-17**: Application shall run on Windows, macOS, and Linux
- **NFR-18**: No platform-specific code dependencies
- **NFR-19**: Standard Python libraries only

#### 5.2.6 Maintainability Requirements

- **NFR-20**: Code shall be well-documented
- **NFR-21**: Code shall follow Python PEP 8 style guidelines
- **NFR-22**: Modular design for easy updates

---

## 6. System Architecture

### 6.1 Architecture Overview

The system follows a layered architecture:

```
┌─────────────────────────────────────────┐
│         Presentation Layer             │
│  (LoginWindow, TodoApp - Tkinter GUI)  │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│          Business Logic Layer           │
│  (UserManager, TaskManager, Task)       │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│          Data Access Layer               │
│  (JSON File I/O Operations)             │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│          Storage Layer                   │
│  (users.json, username_tasks.json)      │
└─────────────────────────────────────────┘
```

### 6.2 Component Description

#### 6.2.1 Presentation Layer

**LoginWindow Class:**
- Handles user authentication UI
- Manages login and registration forms
- Interacts with UserManager

**TodoApp Class:**
- Main application window
- Task management UI
- Interacts with TaskManager

#### 6.2.2 Business Logic Layer

**UserManager Class:**
- User registration
- Password hashing and verification
- User credential management

**TaskManager Class:**
- Task CRUD operations
- Task storage management
- Task file I/O operations

**Task Class:**
- Task data model
- Task serialization/deserialization

#### 6.2.3 Data Access Layer

- JSON file reading/writing
- Error handling for file operations
- Data validation

### 6.3 Data Flow

**Registration Flow:**
```
User Input → LoginWindow → UserManager → Hash Password → Save to users.json
```

**Login Flow:**
```
User Input → LoginWindow → UserManager → Verify Password → Load Tasks → TodoApp
```

**Task Operations Flow:**
```
User Action → TodoApp → TaskManager → Update JSON File → Refresh Display
```

---

## 7. System Design

### 7.1 Data Structure

#### 7.1.1 User Credentials Structure

**File**: `users.json`

```json
{
  "username1": {
    "password": "hashed_password_sha256"
  },
  "username2": {
    "password": "hashed_password_sha256"
  }
}
```

#### 7.1.2 Task Data Structure

**File**: `[username]_tasks.json`

```json
[
  {
    "name": "Task Name",
    "priority": "High",
    "due_date": "2024-12-20",
    "category": "Work",
    "status": "Pending"
  },
  {
    "name": "Another Task",
    "priority": "Low",
    "due_date": "",
    "category": "Personal",
    "status": "Completed"
  }
]
```

#### 7.1.3 Task Object Model

**Task Class Attributes:**
- `name` (string): Task name
- `priority` (string): "High" or "Low"
- `due_date` (string): Date in YYYY-MM-DD format or empty
- `category` (string): Work, Personal, Study, Shopping, Health, Other
- `status` (string): "Pending" or "Completed"

### 7.2 Database Design

**Not Applicable** - System uses JSON file storage instead of a database.

### 7.3 Algorithm Design

#### 7.3.1 Password Hashing Algorithm

```
Input: password (string)
Process:
  1. Encode password to bytes
  2. Apply SHA-256 hash function
  3. Convert to hexadecimal string
Output: hashed_password (string)
```

#### 7.3.2 Authentication Algorithm

```
Input: username, password
Process:
  1. Hash input password
  2. Load users.json
  3. Check if username exists
  4. Compare hashed passwords
Output: authenticated (boolean)
```

#### 7.3.3 Task Validation Algorithm

```
Input: task_data
Process:
  1. Validate task name is not empty
  2. Validate priority is "High" or "Low"
  3. Validate date format if provided (YYYY-MM-DD)
  4. Validate category is in allowed list
Output: valid (boolean), error_message (string)
```

---

## 8. Implementation Details

### 8.1 Technology Stack

- **Programming Language**: Python 3.6+
- **GUI Framework**: Tkinter
- **Data Storage**: JSON files
- **Password Hashing**: SHA-256 (hashlib)

### 8.2 File Structure

```
To-Do-Application/
├── main.py                 # Main application file
├── README.md              # User documentation
├── SRS_Report.md          # This document
├── users.json             # User credentials (auto-generated)
└── [username]_tasks.json  # User tasks (auto-generated)
```

### 8.3 Key Classes and Methods

#### 8.3.1 UserManager Class

**Methods:**
- `load_users()`: Load user data from JSON
- `save_users()`: Save user data to JSON
- `hash_password(password)`: Hash password using SHA-256
- `register_user(username, password)`: Register new user
- `verify_user(username, password)`: Verify login credentials
- `user_exists(username)`: Check if user exists

#### 8.3.2 TaskManager Class

**Methods:**
- `load_tasks()`: Load tasks from JSON file
- `save_tasks()`: Save tasks to JSON file
- `add_task(task)`: Add new task
- `update_task(index, task)`: Update existing task
- `delete_task(index)`: Delete task
- `mark_completed(index)`: Mark task as completed
- `get_all_tasks()`: Retrieve all tasks

#### 8.3.3 Task Class

**Methods:**
- `to_dict()`: Convert task to dictionary
- `from_dict(data)`: Create task from dictionary

### 8.4 Error Handling

**File I/O Errors:**
- Handle missing files gracefully
- Handle corrupted JSON files
- Handle permission errors

**Input Validation:**
- Validate required fields
- Validate date format
- Validate data types

**User Feedback:**
- Display clear error messages
- Provide success confirmations
- Show validation errors

---

## 9. Testing Requirements

### 9.1 Unit Testing

**Test Cases:**
1. User registration with valid data
2. User registration with duplicate username
3. User registration with short password
4. User login with valid credentials
5. User login with invalid credentials
6. Task creation with all fields
7. Task creation with required fields only
8. Task validation (empty name, invalid date)
9. Task update functionality
10. Task deletion with confirmation
11. Mark task as completed
12. Password hashing consistency
13. File I/O operations
14. Data persistence after restart

### 9.2 Integration Testing

**Test Scenarios:**
1. Complete user registration and login flow
2. Add task, edit task, delete task workflow
3. Data persistence across sessions
4. Multiple user isolation
5. Error recovery scenarios

### 9.3 User Acceptance Testing

**Test Scenarios:**
1. New user can register and login
2. User can add multiple tasks
3. User can edit and delete tasks
4. User can mark tasks as completed
5. Tasks persist after application restart
6. Interface is intuitive and responsive

### 9.4 Performance Testing

**Test Cases:**
1. Application startup time (< 2 seconds)
2. Task list load time for 100 tasks (< 1 second)
3. Task save operation time (< 500ms)
4. GUI responsiveness during operations

---

## 10. Appendices

### 10.1 Glossary

- **CRUD**: Create, Read, Update, Delete operations
- **GUI**: Graphical User Interface
- **JSON**: JavaScript Object Notation
- **SHA-256**: Secure Hash Algorithm 256-bit
- **SRS**: Software Requirements Specification

### 10.2 Sample Data

**Sample User Credentials:**
```json
{
  "john_doe": {
    "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
  }
}
```

**Sample Task Data:**
```json
[
  {
    "name": "Complete project report",
    "priority": "High",
    "due_date": "2024-12-20",
    "category": "Work",
    "status": "Pending"
  },
  {
    "name": "Buy groceries",
    "priority": "Low",
    "due_date": "2024-12-18",
    "category": "Shopping",
    "status": "Completed"
  }
]
```

### 10.3 Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Dec 2024 | Development Team | Initial SRS document |

### 10.4 Approval

**Prepared by:** Development Team  
**Reviewed by:** _________________  
**Approved by:** _________________  
**Date:** _________________

---

## Document Control

**Document Status**: Final  
**Last Updated**: December 2024  
**Next Review**: As needed  
**Distribution**: Development Team, Stakeholders

---

**End of Document**


