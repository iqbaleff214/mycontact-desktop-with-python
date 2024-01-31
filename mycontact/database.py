
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox

def _create_contacts_table():
    query = QSqlQuery()
    return query.exec(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name VARCHAR(255) NOT NULL,
            phone VARCHAR(15),
            email VARCHAR(50)
        )
        """
    )

def create_connection(db_name):
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(db_name)

    if not connection.open():
        QMessageBox.warning(
            None,
            "MyContact",
            f"Database error: {connection.lastError().text()}"
        )

        return False

    _create_contacts_table()

    return True
