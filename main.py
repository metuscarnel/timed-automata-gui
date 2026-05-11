import sys
from PySide6.QtWidgets import QApplication

# 1. Imports stricts de l'architecture
from model import AutomatonModel
from controller import MainController

# 2. On importe UNIQUEMENT la fenêtre principale depuis le sous-dossier
from View.window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Forcer l'affichage en noir sur blanc avec la police Verdana pour toute l'application
    app.setStyleSheet("""
        /* Style global : blanc un peu terne et noir pas très foncé */
        QWidget {
            font-family: 'Verdana';
            background-color: #FAFAFA;
            color: #2C2C2C;
        }
        
        /* Barre de menu */
        QMenuBar {
            background-color: #FAFAFA;
            border-bottom: 1px solid #E5E5E5; /* bordure très fine */
        }
        QMenuBar::item {
            background-color: transparent;
            padding: 6px 12px;
        }
        QMenuBar::item:selected {
            background-color: #EBEBEB;
            border-radius: 4px;
        }
        
        /* Menus déroulants */
        QMenu {
            background-color: #FFFFFF;
            border: 1px solid #D5D5D5;
        }
        QMenu::item {
            padding: 6px 25px 6px 20px;
        }
        QMenu::item:selected {
            background-color: #EBEBEB;
        }
        
        /* Barre d'outils et ses boutons */
        QToolBar {
            background-color: #FAFAFA;
            border-bottom: 1px solid #E5E5E5;
            spacing: 8px;
            padding: 4px;
        }
        QToolButton {
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 4px;
            padding: 6px;
        }
        QToolButton:hover {
            background-color: #EBEBEB;
            border: 1px solid #D5D5D5;
        }
        QToolButton:pressed, QToolButton:checked {
            background-color: #E0E0E0;
            border: 1px solid #CCCCCC;
        }
    """)
    
    # Instanciation de la mécanique (Le Buffer)
    model = AutomatonModel()
    
    # Instanciation de l'Arbitre (Le Contrôleur)
    controller = MainController(model)
    
    # Instanciation de l'Interface (La Fenêtre)
    window = MainWindow(controller)
    
    # On lie la vue au contrôleur pour qu'il puisse lui donner des ordres (ex: ouvrir le dock)
    controller.set_view(window)
    
    # Affichage
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()