import tree
from PyQt5.QtWidgets import (
   QMainWindow,
   QVBoxLayout,
   QLabel,
   QPushButton,
   QLineEdit,
   QWidget,
   QFileDialog,
)

class OrthoDBGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tree")
        layout = QVBoxLayout()
        label = QLabel(
            'Enter <a href="https://www.orthodb.org/">OrthoDB v12</a> Group ID:'
        )
        label.setOpenExternalLinks(True)
        layout.addWidget(label)

        self.text_edit = QLineEdit()
        layout.addWidget(self.text_edit)

        button = QPushButton("Create iTOL Dataset")
        button.clicked.connect(self.create_click)
        layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def create_click(self):
        group_id = self.text_edit.text().strip()
        file_dialog = QFileDialog()
        options = QFileDialog.Options()
        file_path, _ = file_dialog.getSaveFileName(
            self,
            "Save iTOL Dataset",
            "",
            "Text Files (*.txt)",
            options=options,
        )
        tree.writeiTol(file_path, tree.retrieve_organism_names(group_id), group_id)
