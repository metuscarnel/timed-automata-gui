import sys
import signal
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
        /* Style global */
        QWidget {
            font-family: 'IBM Plex Mono';
            background-color: #FAFAFA;
            color: #2C2C2C;
        }
        
        /* Barre de menu */
        QMenuBar {
            background-color: #FAFAFA;
            border-bottom: 1px solid #E5E5E5;
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
            border: 0.3px solid #CCCCCC;
            border-radius: 4px;
            padding: 4px;
        }
        QMenu::item {
            padding: 6px 24px 6px 12px;
            border-radius: 4px;
            margin: 1px 4px;
        }
        QMenu::item:selected {
            background-color: #EBEBEB;
            color: #000000;
        }
        QMenu::separator {
            height: 1px;
            background-color: #EEEEEE;
            margin: 4px 8px;
        }
        
        /* Barre d'outils et ses boutons */
        QToolBar {
            background-color: #FAFAFA;
            border-bottom: 1px solid #E5E5E5;
            spacing: 10px;
            padding: 8px;
            min-height: 40px;
        }
        QToolButton {
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 4px;
            padding: 8px 12px;
        }
        QToolButton:hover {
            background-color: #EBEBEB;
            border: 1px solid #D5D5D5;
        }
        QToolButton:pressed, QToolButton:checked {
            background-color: #E0E0E0;
            border: 1px solid #CCCCCC;
        }
        QToolButton#miniAddBtn {
            padding: 2px;
            font-size: 16px;
            font-weight: bold;
        }
        
        /* --- QComboBox (Menus déroulants Flat Design) --- */
        QComboBox {
            background-color: #FFFFFF;
            color: #000000;
            border: 1px solid #CCCCCC;
            border-radius: 4px;
            padding: 5px 8px;
        }
        QComboBox:hover {
            border: 1px solid #AAAAAA;
        }
        QComboBox:focus {
            border: 1px solid #0D99FF;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 24px;
            border: none;
        }
        QComboBox::down-arrow {
            /* Flèche native sans contour extérieur */
        }
        QComboBox QAbstractItemView {
            background-color: #FFFFFF;
            color: #000000;
            border: 1px solid #CCCCCC;
            border-radius: 4px;
            selection-background-color: #E5F3FF;
            selection-color: #000000;
            outline: none;
        }
    """)
    
    # Instanciation du modèle
    model = AutomatonModel()
    
    # Instanciation du contrôleur
    controller = MainController(model)
    
    # Instanciation de la vue
    window = MainWindow(controller)
    
    # On lie la vue au contrôleur pour qu'il puisse lui donner des ordres (ex: ouvrir le dock)
    controller.set_view(window)
    
    # Affichage
    window.show()
    # Gestion de la fermeture via Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()