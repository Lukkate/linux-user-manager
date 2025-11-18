import subprocess
import sys
import pwd  # check if user exists (reads /etc/passwd)


def show_menu():
    print("\n=== Linux User & Permission Manager ===")
    print("1. List all system users")
    print("2. Check if a user exists")
    print("3. Exit")


def list_users():
    """
    List all users in the system.
    Uses: getent passwd
    """
    print("\n--- System Users ---")
    subprocess.run(["getent", "passwd"])


def user_exists(username: str) -> bool:
    """
    Return True if the user exists in the system.
    Uses Python's pwd module (reads /etc/passwd).
    """
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


def check_user():
    """
    Ask for username and check if exists.
    """
    username = input("Enter username to check: ").strip()

    if not username:
        print("Please enter a username.")
        return

    if user_exists(username):
        print(f"User '{username}' exists in the system.")
    else:
        print(f"User '{username}' does NOT exist.")


if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Select option: ").strip()

        if choice == "1":
            list_users()
        elif choice == "2":
            check_user()
        elif choice == "3":
            print("Goodbye")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")
