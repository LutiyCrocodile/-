import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QComboBox, QVBoxLayout, QWidget


class OlympicResultsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data = self.loadData()
        self.schools = self.getUniqueSchools()
        self.classes = self.getUniqueClasses()
        self.populateComboBoxes()

    def initUI(self):
        self.setWindowTitle('Olympic Results')

        self.table = QTableWidget()
        self.schoolComboBox = QComboBox()
        self.classComboBox = QComboBox()

        self.schoolComboBox.currentIndexChanged.connect(self.filterData)
        self.classComboBox.currentIndexChanged.connect(self.filterData)

        layout = QVBoxLayout()
        layout.addWidget(self.schoolComboBox)
        layout.addWidget(self.classComboBox)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def loadData(self):
        with open('results.csv', newline='') as csvfile:
            return list(csv.DictReader(csvfile))

    def getUniqueSchools(self):
        return sorted(set(row['school'] for row in self.data))

    def getUniqueClasses(self):
        return sorted(set(row['class'] for row in self.data))

    def populateComboBoxes(self):
        self.schoolComboBox.addItems(self.schools)
        self.classComboBox.addItems(self.classes)

    def filterData(self):
        school = self.schoolComboBox.currentText()
        class_ = self.classComboBox.currentText()
        filtered_data = [row for row in self.data if
                         (row['school'] == school or not school) and
                         (row['class'] == class_ or not class_)]
        self.updateTable(filtered_data)

    def updateTable(self, filtered_data):
        self.table.setRowCount(len(filtered_data))
        self.table.setColumnCount(len(filtered_data[0]))  # или общее количество колонок
        for row_index, row_data in enumerate(filtered_data):
            for column_index, (key, value) in enumerate(row_data.items()):
                self.table.setItem(row_index, column_index, QTableWidgetItem(value))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OlympicResultsApp()
    ex.show()
    sys.exit(app.exec_())
