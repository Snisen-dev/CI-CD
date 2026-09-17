import argparse
from datetime import UTC, datetime

from Application.database import get_connection


def add_user(name, age, city, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT INTO users (name, age, city, email, created_at)
    VALUES (?, ?, ?, ?, ?)
    """,
        (name, age, city, email, datetime.now(UTC).date()),
    )

    conn.commit()

    print(f"User '{name}' added successfully.")

    cursor.close()
    conn.close()


def list_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, age, city, email, created_at
        FROM users
        ORDER BY id
        """
    )

    users = cursor.fetchall()

    if not users:
        print("No users found.")
    else:
        print(
            f"{'ID':<5} "
            f"{'NAME':<20} "
            f"{'AGE':<5} "
            f"{'CITY':<20} "
            f"{'EMAIL':<30} "
            f"{'CREATED':<12}"
        )

        print("-" * 100)

        for user in users:
            print(
                f"{user[0]:<5} "
                f"{user[1]:<20} "
                f"{user[2]:<5} "
                f"{user[3]:<20} "
                f"{user[4]:<30} "
                f"{user[5]!s:<12}"
            )

    cursor.close()
    conn.close()


def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,),
    )

    conn.commit()

    if cursor.rowcount == 0:
        print(f"No user with ID {user_id} exists.")
    else:
        print(f"User {user_id} deleted.")

    cursor.close()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="CLI application for managing users.")

    subparsers = parser.add_subparsers(dest="command")

    # add-user
    add_parser = subparsers.add_parser("add-user")

    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--age", required=True, type=int)
    add_parser.add_argument("--city", required=True)
    add_parser.add_argument("--email", required=True)

    # list-users
    subparsers.add_parser("list-users")

    # delete-user
    delete_parser = subparsers.add_parser("delete-user")
    delete_parser.add_argument("--id", required=True, type=int)

    args = parser.parse_args()

    if args.command == "add-user":
        add_user(
            args.name,
            args.age,
            args.city,
            args.email,
        )

    elif args.command == "list-users":
        list_users()

    elif args.command == "delete-user":
        delete_user(args.id)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
