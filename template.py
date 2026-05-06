import sys
from PySide6.QtWidgets import (QMainWindow, QApplication, QGraphicsView, 
                             QGraphicsScene, QDockWidget, QWidget, 
                             QLineEdit, QFormLayout, QMessageBox)
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtCore import Qt

class EditorInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Éditeur d'Automates")
        self.resize(1100, 700)

        # Configuration de la barre de menu pour macOS
        self.menuBar().setNativeMenuBar(False)

        # Zone Centrale (La Vue graphique)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # Initialisation des composants
        self.create_actions()
        self.create_menus()
        self.create_toolbar()
        self.create_properties_panel()

    def create_actions(self):
        # --- FICHIER ---
        self.new_act = QAction("Nouveau", self)
        self.new_act.setShortcut(QKeySequence.New)
        
        self.open_act = QAction("Ouvrir", self)
        self.open_act.setShortcut(QKeySequence.Open)
        
        self.save_act = QAction("Enregistrer", self)
        self.save_act.setShortcut(QKeySequence.Save)

        # --- AIDE ---
        self.about_act = QAction("À propos", self)
        self.about_act.triggered.connect(self.show_about)

    def create_menus(self):
        # Menu Fichier
        file_menu = self.menuBar().addMenu("&Fichier")
        file_menu.addAction(self.new_act)
        file_menu.addAction(self.open_act)
        file_menu.addAction(self.save_act)

        # Menu Aide
        help_menu = self.menuBar().addMenu("&?")
        help_menu.addAction(self.about_act)

    def create_toolbar(self):
        # Barre d'outils avec les actions principales[cite: 1]
        toolbar = self.addToolBar("toolbar")
        toolbar.addAction("Nouvelle Localité")
        toolbar.addAction("Nouvelle Transition")        
        toolbar.addSeparator()
        toolbar.addAction(

    def create_properties_panel(self):
        # Panneau latéral droit[cite: 1]
        dock = QDockWidget("Propriétés de l'élément", self)
        dock.setAllowedAreas(Qt.RightDockWidgetArea)
        
        container = QWidget()
       
        
        dock.setWidget(container)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

    def show_about(self):
        QMessageBox.about(self, "À propos", 
                         "Éditeur d'automates simplifié\nProjet Stage 2026")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditorInterface()
    window.show()
    sys.exit(app.exec())