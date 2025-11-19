import subprocess
import sys
import pwd  # check if user exists (reads /etc/passwd)
import re   # for username validation
import getpass  # to get current username


def show_menu():
    print("\n=== Linux User & Permission Manager ===")
    print("1. List all system users")
    print("2. Check if a user exists")
    print("3. Create new user")
    print("4. Delete user")
    print("5. Exit")


def list_users(): #List all users in the system.
    print("\n--- System Users ---")
    subprocess.run(["getent", "passwd"])


def user_exists(username: str) -> bool: #Return True if the user exists in the system.
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False
    
def validate_username(username: str) -> bool: #Validate the username according to Linux username rules
    pattern = r'^[a-z_][a-z0-9_-]{0,31}$' # Linux username rules 
    return re.match(pattern, username) is not None

def get_current_username() -> str: #Return the username of the current user running this script
    return getpass.getuser()

def check_user(): #Check if a user exists in the system.
    username = input("Enter username to check: ").strip()

    if not username:
        print("Please enter a username.")
        return

    if user_exists(username):
        print(f"User '{username}' exists in the system.")
    else:
        print(f"User '{username}' does NOT exist.")

def create_user(): #Create a new user in the system.
    username = input("Enter NEW username to create: ").strip()

    if not username:
        print("Username cannot be empty!")
        return

    if not validate_username(username):
        print("Invalid username!")
        print("  - must start with a lowercase letter or underscore")
        print("  - can contain lowercase letters, digits, underscore, hyphen")
        print("  - max length = 32 characters")
        return

    if user_exists(username):
        print(f"User '{username}' already exists!")
        return

    print(f"About to create user: {username}")
    confirm = input("Proceed? (y/N): ").strip().lower()

    if confirm != "y":
        print("Cancelled.")
        return

    # Run Linux command: sudo useradd -m -s /bin/bash <username>
    try:
        result = subprocess.run(
            ["sudo", "useradd", "-m", "-s", "/bin/bash", username],
            check=True
        )
        print(f"User '{username}' created successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to create user.")
        print("   Error:", e)

def delete_user():
    """
    Delete an existing Linux user (with safety checks).
    Uses: sudo userdel -r <username>
    """
    username = input("Enter username to DELETE: ").strip()

    if not username:
        print("⚠ Username cannot be empty.")
        return

    if not user_exists(username):
        print(f"User '{username}' does NOT exist.")
        return

    # Safety: do not allow deleting root
    if username == "root":
        print("Refusing to delete 'root' user.")
        return

    # Safety: do not allow deleting the current user
    current = get_current_username()
    if username == current:
        print(f"Refusing to delete the current user '{current}'.")
        return

    print(f"About to DELETE user: {username}")
    confirm = input("Type the username again to confirm: ").strip()

    if confirm != username:
        print("Confirmation mismatch. Cancelled.")
        return

    final = input("Are you SURE? This will remove the account (y/N): ").strip().lower()
    if final != "y":
        print("Cancelled.")
        return

    try:
        subprocess.run(
            ["sudo", "userdel", "-r", username],
            check=True
        )
        print(f"User '{username}' deleted successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to delete user.")
        print("   Error:", e)

if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Select option: ").strip()

        if choice == "1":
            list_users()
        elif choice == "2":
            check_user()
        elif choice == "3":            
            create_user()
        elif choice == "4":
            delete_user()
        elif choice == "5":
            print("Goodbye")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")
