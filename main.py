import mysql.connector


class Software:
    def __init__(self, name, version):
        self.name = name
        self.version = version


class SoftwareManagementSystem:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS softwares
                          (name VARCHAR(255) NOT NULL UNIQUE, version VARCHAR(255))''')
        self.conn.commit()

    def add_software(self, name, version):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO softwares (name, version) VALUES (%s, %s)", (name, version))
            self.conn.commit()
            print("Software added successfully.")
        except mysql.connector.IntegrityError:
            print("Software already exists.")

    def update_software(self, name, new_version):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE softwares SET version=%s WHERE name=%s", (new_version, name))
        if cursor.rowcount > 0:
            self.conn.commit()
            print("Software updated successfully.")
        else:
            print("Software not found.")

    def delete_software(self, name):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM softwares WHERE name=%s", (name,))
        if cursor.rowcount > 0:
            self.conn.commit()
            print("Software deleted successfully.")
        else:
            print("Software not found.")

    def display_softwares(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM softwares")
        rows = cursor.fetchall()
        if rows:
            print("Software Records:")
            for row in rows:
                print(f"Name: {row[0]}, Version: {row[1]}")
        else:
            print("No software records found.")


def authenticate_user():
    # Perform user authentication here
    username = input("Enter username: ")
    password = input("Enter password: ")
    # Validate credentials and return True if authenticated, False otherwise
    return True  # Placeholder for authentication logic


def main():
    host = "localhost"
    user = "root"
    password = "2796"
    database = "pws"

    # Authenticate user before proceeding
    if not authenticate_user():
        print("Authentication failed. Exiting...")
        return

    sms = SoftwareManagementSystem(host, user, password, database)

    while True:
        print("\nSoftware Management System")
        print("1. Add Software")
        print("2. Update Software")
        print("3. Delete Software")
        print("4. Display All Softwares")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name of the software: ")
            version = input("Enter version of the software: ")
            sms.add_software(name, version)
        elif choice == "2":
            name = input("Enter name of the software to update: ")
            new_version = input("Enter new version of the software: ")
            sms.update_software(name, new_version)
        elif choice == "3":
            name = input("Enter name of the software to delete: ")
            sms.delete_software(name)
        elif choice == "4":
            sms.display_softwares()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    sms.conn.close()


if __name__ == "__main__":
    main()
