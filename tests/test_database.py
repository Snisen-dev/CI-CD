from Application.database import get_connection


def test_insert_user():
    conn = get_connection()
    cursor = conn.cursor()

    test_email = "pytest@example.com"

    try:
        cursor.execute(
            """
            INSERT INTO users (name, age, city, email, created_at)
            VALUES (?, ?, ?, ?, CURDATE())
            """,
            ("Pytest User", 25, "Stockholm", test_email),
        )
        conn.commit()

        cursor.execute(
            "SELECT name, age, city, email FROM users WHERE email = ?",
            (test_email,),
        )

        user = cursor.fetchone()

        assert user is not None
        assert user[0] == "Pytest User"
        assert user[1] == 25
        assert user[2] == "Stockholm"
        assert user[3] == test_email

    finally:
        cursor.execute(
            "DELETE FROM users WHERE email = ?",
            (test_email,),
        )
        conn.commit()

        cursor.close()
        conn.close()
