# tree.py v0.1
# michael.gilmore@umu.se

import sys
import subprocess
import csv
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QLineEdit, QWidget, QFileDialog

class OrthoDBGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tree")

        layout = QVBoxLayout()

        label = QLabel("Enter <a href=\"https://www.orthodb.org/\">OrthoDB v11</a> Group ID:")
        label.setOpenExternalLinks(True)
        layout.addWidget(label)

        self.text_edit = QLineEdit()
        layout.addWidget(self.text_edit)

        button = QPushButton("Create iTOL Dataset")
        button.clicked.connect(self.retrieve_organism_names)
        layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def run_curl_command(self, curl_command):
        try:
            result = subprocess.check_output(curl_command, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8').split("\n", 3)[-1]
        except subprocess.CalledProcessError as e:
            print(f"Error executing curl command: {e.output.decode('utf-8')}")
            return None

    def retrieve_organism_names(self):
        group_id = self.text_edit.text().strip()

        curl_command = f'curl -X GET "https://data.orthodb.org/current/tab?id={group_id}"'
        response = self.run_curl_command(curl_command)

        if response:
            # Remove initial lines
            tsv_data = response.split("\n", 3)[-1]

            # Parse TSV data
            reader = csv.reader(tsv_data.splitlines(), delimiter='\t')
            next(reader)  # Skip the header row

            organism_names = []
            for row in reader:
                if len(row) >= 5:
                    organism_name = row[4]
                    organism_name = organism_name.replace(" ", "_")
                    organism_names.append(organism_name)

            file_dialog = QFileDialog()
            options = QFileDialog.Options()
            file_path, _ = file_dialog.getSaveFileName(self, "Save iTOL Dataset", "", "Text Files (*.txt)", options=options)

            if file_path:
                with open(file_path, "w") as file:
                    file.write("DATASET_GRADIENT\n")
                    file.write("#Dataset created using tree.py\n\n")
                    file.write("SEPARATOR TAB\n")
                    file.write("DATASET_LABEL\t{}\n".format(group_id))
                    file.write("COLOR\t#00ff00\n")
                    file.write("COLOR_MIN\t#00ff00\n")
                    file.write("COLOR_MAX\t#0000ff\n\n")
                    file.write("DATA\n")
                    for organism_name in organism_names:
                        file.write(f"{organism_name}\t1\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrthoDBGUI()
    window.show()
    sys.exit(app.exec_())
