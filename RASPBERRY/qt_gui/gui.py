# Qt5 based GUI for 7-seg say
from PyQt5.QtWidgets import *
import PyQt5.QtGui

seg_say_string ="""
____________________________________________________
    ____                                            
   /    /                                           
-------/--------__----__----__-------__----__-------
      /   ===  (_ ` /___) /   )     (_ ` /   ) /   /
_____/________(__)_(___ _(___/_____(__)_(___(_(___/_
                            /                    /  
                        (_ /                 (_ /   
                                                    
"""

class gui(QWidget):
    def __init__(self):
        super().__init__()
        self.state = "IDLE"
        self.initUI()

    def initUI(self):
        self.setWindowTitle("7-seg say")

        self.label = QLabel(self)
        self.line = QLineEdit(self)
        self.button = QPushButton("SAY", self)

        font = PyQt5.QtGui.QFont("Monospace")
        static_label = QLabel(seg_say_string, self)
        static_label.setFont(font)

        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        h_layout.addWidget(self.line)
        h_layout.addWidget(self.button)
        v_layout.addWidget(static_label)
        v_layout.addWidget(self.label)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)

        # Make things bigger
        font = self.line.font()
        font.setPointSize(font.pointSize() + 10)
        self.line.setFont(font)
        self.label.setFont(font)
        self.button.setFont(font)

        # Events
        self.button.clicked.connect(self.sayMessage)
        self.line.returnPressed.connect(self.sayMessage)

        self.messageCompleted()

        self.show()

    def sayMessage(self):
        self.label.setText("Saying:")
        self.button.setEnabled(False)
        self.line.setEnabled(False)

        text = self.line.text()
        if len(text) > 0:
            print(text)

        self.messageCompleted()

    def messageCompleted(self):
        self.label.setText("What do you want me to say?")
        self.button.setEnabled(True)
        self.line.setEnabled(True)
        self.line.setText("")
        self.line.setFocus()

app = QApplication([])
app.setStyle('Fusion')
window = gui()
app.exec_()
