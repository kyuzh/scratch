import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QVBoxLayout, QWidget

class BlocNoteApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Bloc-Notes")
        self.setGeometry(100, 100, 800, 600)

        self.text_widget = QTextEdit(self)
        self.setCentralWidget(self.text_widget)

        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("Fichier")

        new_action = QAction("Nouveau", self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Ouvrir", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Enregistrer", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Enregistrer sous...", self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

    def new_file(self):
        self.text_widget.clear()

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(filter="Fichiers texte (*.txt)")
        if file_path:
            with open(file_path, "r") as file:
                self.text_widget.setPlainText(file.read())

    def save_file(self):
        # Save the content of the text widget to the same file it was opened from (if any)
        pass

    def save_file_as(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(filter="Fichiers texte (*.txt)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_widget.toPlainText())

