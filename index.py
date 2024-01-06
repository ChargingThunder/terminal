import csv
import os
import sys
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QComboBox, QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QDialog
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
script_dir = os.path.dirname(os.path.realpath(__file__))
employee_csv_path = os.path.join(script_dir, 'employees.csv')
guests_csv_path = os.path.join(script_dir, 'guests.csv')

class SecurityTerminal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Терминал охранника")
        self.tab_widget = QTabWidget()

        entry_exit_tab = QWidget()
        entry_exit_layout = QVBoxLayout()
        self.user_type_selector = QComboBox()
        self.user_type_selector.addItem("Гость")
        self.user_type_selector.addItem("Сотрудник")
        entry_exit_layout.addWidget(QLabel("Кого впускаем:"))
        entry_exit_layout.addWidget(self.user_type_selector)


        self.pass_number_input = QLineEdit()
        self.pass_number_input.setValidator(QIntValidator())
        entry_exit_layout.addWidget(QLabel("Номер пропуска:"))
        entry_exit_layout.addWidget(self.pass_number_input)
        start_button = QPushButton("Запустить")
        start_button.clicked.connect(self.start_entry)
        entry_exit_layout.addWidget(start_button)
        exit_button = QPushButton("Выпустить")
        exit_button.clicked.connect(self.start_exit)
        entry_exit_layout.addWidget(exit_button)
        entry_exit_tab.setLayout(entry_exit_layout)
        self.tab_widget.addTab(entry_exit_tab, "ВПУСТИТЬ/ВЫПУСТИТЬ")

        add_employee_tab = QWidget()
        add_employee_layout = QVBoxLayout()

        self.last_name_input = QLineEdit()
        self.first_name_input = QLineEdit()
        self.middle_name_input = QLineEdit()
        self.birth_date_input = QLineEdit()
        self.phone_number_input = QLineEdit()
        self.email_input = QLineEdit()
        self.position_input = QLineEdit()

        date_validator = QRegularExpressionValidator(QRegularExpression("\\d{2}\\.\\d{2}\\.\\d{4}"))
        self.birth_date_input.setValidator(date_validator)

        phone_validator = QRegularExpressionValidator(QRegularExpression("^\\+7\\d{10}$"))
        self.phone_number_input.setValidator(phone_validator)

        email_validator = QRegularExpressionValidator(QRegularExpression("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"))
        self.email_input.setValidator(email_validator)

        add_employee_layout.addWidget(QLabel("Фамилия*"))
        add_employee_layout.addWidget(self.last_name_input)
        add_employee_layout.addWidget(QLabel("Имя*"))
        add_employee_layout.addWidget(self.first_name_input)
        add_employee_layout.addWidget(QLabel("Отчество"))
        add_employee_layout.addWidget(self.middle_name_input)
        add_employee_layout.addWidget(QLabel("Дата рождения* (дд.мм.гггг)"))
        add_employee_layout.addWidget(self.birth_date_input)
        add_employee_layout.addWidget(QLabel("Номер телефона* (+79113920959)"))
        add_employee_layout.addWidget(self.phone_number_input)
        add_employee_layout.addWidget(QLabel("Электронная почта*"))
        add_employee_layout.addWidget(self.email_input)
        add_employee_layout.addWidget(QLabel("Должность*"))
        add_employee_layout.addWidget(self.position_input)

        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.add_employee)
        add_employee_layout.addWidget(add_button)

        clear_button = QPushButton("Очистить")
        clear_button.clicked.connect(self.clear_fields)
        add_employee_layout.addWidget(clear_button)

        add_employee_tab.setLayout(add_employee_layout)
        self.tab_widget.addTab(add_employee_tab, "ДОБАВИТЬ СОТРУДНИКА")

        add_guest_tab = QWidget()
        add_guest_layout = QVBoxLayout()
        add_guest_tab.setLayout(add_guest_layout)

        self.last_name_guest_input = QLineEdit()
        self.first_name_guest_input = QLineEdit()
        self.middle_name_guest_input = QLineEdit()
        self.birth_date_guest_input = QLineEdit()
        self.phone_number_guest_input = QLineEdit()
        self.email_guest_input = QLineEdit()
        self.validity_period_input = QLineEdit()

        date_validator_guest = QRegularExpressionValidator(QRegularExpression("\\d{2}\\.\\d{2}\\.\\d{4}"))
        self.birth_date_guest_input.setValidator(date_validator_guest)

        phone_validator_guest = QRegularExpressionValidator(QRegularExpression("^\\+7\\d{10}$"))
        self.phone_number_guest_input.setValidator(phone_validator_guest)

        email_validator_guest = QRegularExpressionValidator(QRegularExpression("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"))
        self.email_guest_input.setValidator(email_validator_guest)

        validity_period_validator = QIntValidator(1, 9999)
        self.validity_period_input.setValidator(validity_period_validator)

        add_guest_layout.addWidget(QLabel("Фамилия*"))
        add_guest_layout.addWidget(self.last_name_guest_input)
        add_guest_layout.addWidget(QLabel("Имя*"))
        add_guest_layout.addWidget(self.first_name_guest_input)
        add_guest_layout.addWidget(QLabel("Отчество"))
        add_guest_layout.addWidget(self.middle_name_guest_input)
        add_guest_layout.addWidget(QLabel("Дата рождения* (дд.мм.гггг)"))
        add_guest_layout.addWidget(self.birth_date_guest_input)
        add_guest_layout.addWidget(QLabel("Номер телефона* (+79113920959)"))
        add_guest_layout.addWidget(self.phone_number_guest_input)
        add_guest_layout.addWidget(QLabel("Электронная почта*"))
        add_guest_layout.addWidget(self.email_guest_input)
        add_guest_layout.addWidget(QLabel("Действителен (в мин)*"))
        add_guest_layout.addWidget(self.validity_period_input)

        add_guest_button = QPushButton("Добавить")
        add_guest_button.clicked.connect(self.add_guest)
        add_guest_layout.addWidget(add_guest_button)

        clear_guest_button = QPushButton("Очистить")
        clear_guest_button.clicked.connect(self.clear_guest_fields)
        add_guest_layout.addWidget(clear_guest_button)

        add_guest_tab.setLayout(add_guest_layout)
        self.tab_widget.addTab(add_guest_tab, "ДОБАВИТЬ ГОСТЯ")

        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.tab_widget)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        self.show()

    def start_entry(self):
        pass_number = self.pass_number_input.text()
        user_type = self.user_type_selector.currentText()

        if pass_number and user_type:
            base_file_path = employee_csv_path
            if(user_type == "Гость"): 
                base_file_path = guests_csv_path

            user_info = self.find_user_in_database(pass_number, base_file_path)
            if user_info:
                self.show_message(f"{user_type} {user_info} зашел.")
            else:
                self.show_message(f"{user_type} с номером пропуска {pass_number} не найден в базе данных.")
        else:
            self.show_message("Заполните обязательные поля")

    def start_exit(self):
        pass_number = self.pass_number_input.text()
        user_type = self.user_type_selector.currentText()

        if pass_number:
            base_file_path = employee_csv_path
            if(user_type == "Гость"): 
                base_file_path = guests_csv_path

            user_info = self.find_user_in_database(pass_number, base_file_path)
            if user_info:
                self.show_message(f"{user_type} {user_info} вышел.")
            else:
                self.show_message(f"{user_type} с номером пропуска {pass_number} не найден в базе данных.")
        else:
            self.show_message("Заполните обязательные поля")

    def find_user_in_database(self, pass_number, csv_path):
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                if("guest" in csv_path):
                    if row['Id'] == pass_number:
                        return f"{row['фамилия']} {row['имя']}"
                if("employees" in csv_path):
                    if row['\ufeffId'] == pass_number:
                        return f"{row['фамилия']} {row['имя']}"
        return None

    def add_employee(self):
        last_name = self.last_name_input.text()
        first_name = self.first_name_input.text()
        middle_name = self.middle_name_input.text()
        birth_date = self.birth_date_input.text()
        phone_number = self.phone_number_input.text()
        email = self.email_input.text()
        position = self.position_input.text()

        if not (last_name and first_name and birth_date and phone_number and email and position):
            self.show_message("Заполните обязательные поля: Фамилия, Имя, Дата рождения, Номер телефона, Электронная почта, Должность.")
            return

        if not self.validate_employee_fields():
            self.show_message("Пожалуйста, введите корректные данные.")
            return

        current_ids = set()
        try:
            with open(employee_csv_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                for row in reader:
                    current_ids.add(int(row['\ufeffId']))
        except FileNotFoundError:
            pass

        new_id = max(current_ids, default=0) + 1

        with open(employee_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Id', 'фамилия', 'имя', 'отчество', 'дата рождения', 'должность', 'телефон', 'почта']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            reader = csv.reader(csvfile)

            if csvfile.tell() == 0:
                writer.writeheader()

            last_line = get_last_character_from_csv(employee_csv_path)
            if(last_line != "\n"): 
                csvfile.write("\n")

            writer.writerow({'Id': str(new_id), 'фамилия': last_name, 'имя': first_name, 'отчество': middle_name, 'дата рождения': birth_date, 'должность': position, 'телефон': phone_number, 'почта': email})

        info_dialog = QDialog(self)
        info_dialog.setWindowTitle("Информация о сотруднике")

        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel(f"Фамилия: {last_name}"))
        info_layout.addWidget(QLabel(f"Имя: {first_name}"))
        info_layout.addWidget(QLabel(f"Отчество: {middle_name}"))
        info_layout.addWidget(QLabel(f"Дата рождения: {birth_date}"))
        info_layout.addWidget(QLabel(f"Номер телефона: {phone_number}"))
        info_layout.addWidget(QLabel(f"Электронная почта: {email}"))
        info_layout.addWidget(QLabel(f"Должность: {position}"))

        info_dialog.setLayout(info_layout)
        info_dialog.exec()



    def clear_fields(self):
        self.last_name_input.clear()
        self.first_name_input.clear()
        self.middle_name_input.clear()
        self.birth_date_input.clear()
        self.phone_number_input.clear()
        self.email_input.clear()
        self.position_input.clear()

    def add_guest(self):
        last_name_guest = self.last_name_guest_input.text()
        first_name_guest = self.first_name_guest_input.text()
        middle_name_guest = self.middle_name_guest_input.text()
        birth_date_guest = self.birth_date_guest_input.text()
        phone_number_guest = self.phone_number_guest_input.text()
        email_guest = self.email_guest_input.text()
        validity_period = self.validity_period_input.text()

        if not (last_name_guest and first_name_guest and birth_date_guest and phone_number_guest and email_guest and validity_period):
            self.show_message("Заполните обязательные поля: Фамилия, Имя, Дата рождения, Номер телефона, Электронная почта, Действителен (в мин).")
            return

        if not self.validate_guest_fields():
            self.show_message("Пожалуйста, введите корректные данные.")
            return
        
        current_ids = set()
        try:
            with open(guests_csv_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                for row in reader:
                    print(row)
                    current_ids.add(int(row['Id']))
        except FileNotFoundError:
            pass 

        new_id = max(current_ids, default=0) + 1

        with open(guests_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Id', 'фамилия', 'имя', 'отчество', 'дата рождения', 'срок действия', 'телефон', 'почта']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            reader = csv.reader(csvfile)

            if csvfile.tell() == 0:
                writer.writeheader()

            last_line = get_last_character_from_csv(guests_csv_path)
            if(last_line != "\n"): 
                csvfile.write("\n")

            expire_date = datetime.now() + timedelta(minutes=int(validity_period))
            writer.writerow({'Id': str(new_id), 'фамилия': last_name_guest, 'имя': first_name_guest, 'отчество': middle_name_guest, 'дата рождения': birth_date_guest, 'срок действия': expire_date, 'телефон': phone_number_guest, 'почта': email_guest})

        info_dialog = QDialog(self)
        info_dialog.setWindowTitle("Информация о госте")

        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel(f"Фамилия: {last_name_guest}"))
        info_layout.addWidget(QLabel(f"Имя: {first_name_guest}"))
        info_layout.addWidget(QLabel(f"Отчество: {middle_name_guest}"))
        info_layout.addWidget(QLabel(f"Дата рождения: {birth_date_guest}"))
        info_layout.addWidget(QLabel(f"Номер телефона: {phone_number_guest}"))
        info_layout.addWidget(QLabel(f"Электронная почта: {email_guest}"))
        info_layout.addWidget(QLabel(f"Действителен (в мин): {validity_period}"))

        info_dialog.setLayout(info_layout)
        info_dialog.exec()

    def clear_guest_fields(self):
        self.last_name_guest_input.clear()
        self.first_name_guest_input.clear()
        self.middle_name_guest_input.clear()
        self.birth_date_guest_input.clear()
        self.phone_number_guest_input.clear()
        self.email_guest_input.clear()
        self.validity_period_input.clear()

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec()

    def validate_employee_fields(self):
        if not self.birth_date_input.hasAcceptableInput() or not self.phone_number_input.hasAcceptableInput() or not self.email_input.hasAcceptableInput() or not self.position_input:
            return False

        return True

    def validate_guest_fields(self):
        if not self.birth_date_guest_input.hasAcceptableInput() or not self.phone_number_guest_input.hasAcceptableInput() or not self.email_guest_input.hasAcceptableInput() or not self.validity_period_input.hasAcceptableInput():
            return False

        return True

def get_last_character_from_csv(csv_path):
    with open(csv_path, 'rb') as csvfile:
        csvfile.seek(-1, 2)
        last_character = csvfile.read(1).decode('utf-8')

    return last_character

if __name__ == "__main__":
    app = QApplication(sys.argv)
    terminal = SecurityTerminal()
    sys.exit(app.exec())