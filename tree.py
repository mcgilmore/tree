import sys
import subprocess
import csv
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QTextEdit, QWidget

class OrthoDBGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OrthoDB GUI")
        self.setGeometry(200, 200, 400, 400)

        layout = QVBoxLayout()

        label = QLabel("Enter OrthoDB Group ID:")
        layout.addWidget(label)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        button = QPushButton("Retrieve Organism Names")
        button.clicked.connect(self.retrieve_organism_names)
        layout.addWidget(button)

        self.result_text_edit = QTextEdit()
        layout.addWidget(self.result_text_edit)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def run_curl_command(self, curl_command):
        try:
            result = subprocess.check_output(curl_command, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8').split("\n", 3)[-1]  # Convert bytes to string
        except subprocess.CalledProcessError as e:
            print(f"Error executing curl command: {e.output.decode('utf-8')}")
            return None

    def retrieve_organism_names(self):
        group_id = self.text_edit.toPlainText()

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
                    organism_name = row[4]  # Column 5 (0-based index)
                    organism_names.append(organism_name)
                    print(row)

            self.result_text_edit.setPlainText('\n'.join(organism_names))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrthoDBGUI()
    window.show()
    sys.exit(app.exec_())
