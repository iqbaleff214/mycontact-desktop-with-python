
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QTableView,
    QAbstractItemView,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QLineEdit,
    QFormLayout,
    QDialogButtonBox,
    QMessageBox,
)

from .model import ContactModel

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("MyContact Desktop")
        self.resize(550, 250)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.contact_model = ContactModel()

        self.setup_ui()

    def setup_ui(self):
        self.table = QTableView()
        self.table.setModel(self.contact_model.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()

        self.add_button = QPushButton("Add...")
        self.add_button.clicked.connect(self.new_contact_dialog)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_contact)
        
        self.clear_all_button = QPushButton("Clear All")
        self.clear_all_button.clicked.connect(self.clear_contact)

        layout = QVBoxLayout()
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addStretch()
        layout.addWidget(self.clear_all_button)

        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def new_contact_dialog(self):
        dialog = Dialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.contact_model.save(dialog.data)
            self.table.resizeColumnsToContents()

    def delete_contact(self):
        row = self.table.currentIndex().row()
        if row < 0:
            return
        
        message_box = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected contact?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if message_box == QMessageBox.Ok:
            self.contact_model.delete(row)

    def clear_contact(self):
        message_box = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove all your contact?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if message_box == QMessageBox.Ok:
            self.contact_model.clear()


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Contact")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.data = None

        self.setup_ui()

    def setup_ui(self):
        self.name_field = QLineEdit()
        self.name_field.setObjectName("name")

        self.phone_field = QLineEdit()
        self.phone_field.setObjectName("phone")

        self.email_field = QLineEdit()
        self.email_field.setObjectName("email")

        layout = QFormLayout()
        layout.addRow("Name", self.name_field)
        layout.addRow("Phone", self.phone_field)
        layout.addRow("Email", self.email_field)
        self.layout.addLayout(layout)

        self.button_box = QDialogButtonBox(self)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def accept(self):
        self.data = []
        for field in (self.name_field, self.phone_field, self.email_field):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a contact's {field.objectName()}"
                )
                self.data = None
                return
            
            self.data.append(field.text())

        return super().accept()

