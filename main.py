import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5.uic import loadUi
import sqlite3

class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)
        self.setWindowTitle("Информация о кофе")
        self.load_data()
        self.addButton.clicked.connect(self.open_add_edit_form)
        self.editButton.clicked.connect(self.open_add_edit_form)

    def load_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM coffee")
        data = cursor.fetchall()
        connection.close()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i, j, item)

    def open_add_edit_form(self):
        row = self.tableWidget.currentRow()
        form = AddEditCoffeeForm()

        if row == -1 and self.sender() == self.editButton:
            return

        if self.sender() == self.editButton:
            form.setWindowTitle("Редактирование записи о кофе")
            form.fill_data(self.tableWidget.item(row, 0).text(),
                           self.tableWidget.item(row, 1).text(),
                           self.tableWidget.item(row, 2).text(),
                           self.tableWidget.item(row, 3).text(),
                           self.tableWidget.item(row, 4).text(),
                           self.tableWidget.item(row, 5).text(),
                           self.tableWidget.item(row, 6).text()) 
        else:
            form.setWindowTitle("Добавление записи о кофе")
            form.fill_data("", "", "", "", "", "", "")  # Передаем пустые строки для новой записи

        if form.exec_() == QDialog.Accepted:
            self.load_data()

class AddEditCoffeeForm(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("addEditCoffeeForm.ui", self)
        self.acceptButton.clicked.connect(self.save_data)

    def fill_data(self, id, nazvanie_sorta, stepen_obzharki, molotiy_v_zernah, opisanie_vkusa, cena, obem_upakovki):
        self.idLineEdit.setText(id)
        self.nazvanieSortaLineEdit.setText(nazvanie_sorta)
        self.stepenObzharkiLineEdit.setText(stepen_obzharki)
        self.molotiyVZernahLineEdit.setText(molotiy_v_zernah)
        self.opisanieVkusaLineEdit.setText(opisanie_vkusa)
        self.cenaLineEdit.setText(cena)
        self.obemUpakovkiLineEdit.setText(obem_upakovki)

    def save_data(self):
        id = self.idLineEdit.text()
        nazvanie_sorta = self.nazvanieSortaLineEdit.text()
        stepen_obzharki = self.stepenObzharkiLineEdit.text()
        molotiy_v_zernah = self.molotiyVZernahLineEdit.text()
        opisanie_vkusa = self.opisanieVkusaLineEdit.text()
        cena = self.cenaLineEdit.text()
        obem_upakovki = self.obemUpakovkiLineEdit.text()

        try:
            connection = sqlite3.connect("coffee.sqlite")
            cursor = connection.cursor()

            # Получаем все ID из базы данных
            cursor.execute("SELECT ID FROM coffee")
            existing_ids = [row[0] for row in cursor.fetchall()]

            if id and int(id) in existing_ids:
                cursor.execute("UPDATE coffee SET Название_сорта=?, Степень_обжарки=?, Молотый_в_зернах=?, Описание_вкуса=?, Цена=?, Объем_упаковки=? WHERE ID=?",
                               (nazvanie_sorta, stepen_obzharki, molotiy_v_zernah, opisanie_vkusa, cena, obem_upakovki, id))
            else:
                cursor.execute("INSERT INTO coffee (Название_сорта, Степень_обжарки, Молотый_в_зернах, Описание_вкуса, Цена, Объем_упаковки) VALUES (?, ?, ?, ?, ?, ?)",
                               (nazvanie_sorta, stepen_obzharki, molotiy_v_zernah, opisanie_vkusa, cena, obem_upakovki))

            connection.commit()
            connection.close()
            self.accept()  # Закрытие диалога после сохранения данных
        except sqlite3.Error as error:
            print("Ошибка при добавлении/редактировании данных:", error)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec_())
