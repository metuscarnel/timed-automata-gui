import sys
from PySide6.QtWidgets import QApplication
from View.view import AutomataView

def main():
    app = QApplication(sys.argv)
    
    # On lance juste la vue seule
    window = AutomataView()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()