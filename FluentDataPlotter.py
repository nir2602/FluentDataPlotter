from PySide6 import QtCore, QtWidgets, QtGui
import matplotlib.pyplot as plt 
import numpy as np

class FluentDataPlotter(QtWidgets.QMainWindow):

    MIN_BOX_WIDTH = 75
    MIN_BOX_HEIGHT = 35

    MAX_BOX_WIDTH = 75
    MAX_BOX_HEIGHT = 35


    def __init__(self):
        super().__init__()


        self.labels = ["No Labels Loaded"]


        self.file_path = None

        self.setWindowTitle("Fluent Data Plotter")
        self.setGeometry(200, 200, 800, 400)

        # Create the central widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a layout
        self.layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # align to the top
        # self.layout.setAlignment(QtCore.Qt.AlignTop)

        # Choose file Frame

        fileFrame = QtWidgets.QFrame()
        # fileFrame.setFrameShape(QtWidgets.QFrame.Box)
        fileFrame.setLineWidth(2)
        

        fileFrameLayout = QtWidgets.QVBoxLayout()

        # Open File button 
        self.open_file_button = QtWidgets.QPushButton("Open File")
        self.open_file_button.clicked.connect(self.open_file_dialog)
        self.open_file_button.setMinimumWidth(self.MIN_BOX_WIDTH)
        self.open_file_button.setMaximumWidth(self.MAX_BOX_WIDTH)
        self.open_file_button.setMinimumHeight(self.MIN_BOX_HEIGHT)

        # Label to display the selected file
        self.file_label = QtWidgets.QLabel("No file selected")
        fileFrameLayout.addWidget(self.file_label)

        fileFrameLayout.addWidget(self.open_file_button)



        fileFrame.setLayout(fileFrameLayout)

        self.layout.addWidget(fileFrame)

        labelsFrame = QtWidgets.QFrame()
        # labelsFrame.setFrameShape(QtWidgets.QFrame.Box)
        labelsFrame.setLineWidth(2)

        labelsFrameLayout = QtWidgets.QVBoxLayout()

        # Load labels button
        self.load_labels_button = QtWidgets.QPushButton("Load Labels")
        self.load_labels_button.clicked.connect(self.load_labels)
        self.layout.addWidget(self.load_labels_button)

        labelsFrameLayout.addWidget(self.load_labels_button)
        
        labelsFrameLayout.addWidget(QtWidgets.QLabel("Choose labels:"))


        # Label to display the labels
        self.x_label = QtWidgets.QComboBox()
        self.x_label.setPlaceholderText("X Label")

        self.y_label = QtWidgets.QComboBox()
        self.y_label.setPlaceholderText("Y Label")

        # labelsFrameLayout.addWidget(self.label_label, alignment=QtCore.Qt.AlignTop)
        labelsFrameLayout.addWidget(self.x_label, alignment=QtCore.Qt.AlignTop)
        labelsFrameLayout.addWidget(self.y_label, alignment=QtCore.Qt.AlignTop)


        
        labelsFrame.setLayout(labelsFrameLayout)

        self.layout.setContentsMargins(10, 10, 10, 10)

        self.layout.addWidget(labelsFrame)

        # Stretch final button to the bottom of the screen.
        self.layout.addStretch(1)

        # execute button
        self.execute_button = QtWidgets.QPushButton("Create graph")
        self.execute_button.clicked.connect(self.create_graph)
        self.layout.addWidget(self.execute_button, alignment=QtCore.Qt.AlignBottom)
        

    def open_file_dialog(self):
        # Open a file dialog and get the selected file path
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setNameFilter(".out files (*.out)")
        if file_dialog.exec():
            self.file_path = file_dialog.selectedFiles()[0]  # Get the selected file
            self.file_label.setText(f"Selected File: {self.file_path}")
        else:
            self.file_label.setText("No file selected")

    def load_labels(self):
        # Load the labels from the file
        if not self.file_path:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a file first!")
            return
        
        with open(self.file_path, "r") as file:
            # labels are located on the third line... seek to the third line
            for _ in range(2):
                next(file)
            
            # Read the lables
            # First: Strip the line of any extra characters
            # labels are in the format "('label1', 'label2', ...)"
            labels = file.readline().strip('').strip('(').strip(')').strip("'").split()
            self.labels = labels

        # Check if the file contains two columns of data
        if len(labels) < 2:
            QtWidgets.QMessageBox.warning(self, "Error", "File does not contain two columns of data")
            return
        
        # Display labels
        self.x_label.clear()
        self.y_label.clear()

        self.x_label.addItems(self.labels)
        self.y_label.addItems(self.labels)


        
    def create_graph(self):

        # no file is selected
        if not self.file_path:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a file first!")
            return
        
        try:
            # Load data from file 
            data = np.loadtxt(self.file_path, skiprows=3)

            # Get the selected labels
            x_label_index = self.labels.index(self.x_label.currentText())
            y_label_index = self.labels.index(self.y_label.currentText())

            x = data[:, x_label_index]
            y = data[:, y_label_index]

            # Create a plot
            plt.plot(x, y)
            plt.xlabel(f"{self.x_label.currentText()}")
            plt.ylabel(f"{self.y_label.currentText()}")
            plt.title(f"{self.y_label.currentText()} vs {self.x_label.currentText()}")
            plt.show()


        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to create graph: {e}")



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = FluentDataPlotter()
    window.show()
    app.exec()
