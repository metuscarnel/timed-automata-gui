from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout
from PySide6.QtCore import Signal, Qt, QEvent
from PySide6.QtGui import QFocusEvent

class InlineAddPopup(QWidget):
    """
    Une petite popup avec un QLineEdit pour une saisie rapide.
    - Valide avec 'Entrée'.
    - Annule avec 'Échap' ou perte de focus.
    """
    validated = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # --- Fenêtre sans bordure, qui reste au-dessus ---
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_DeleteOnClose) # Se détruit à la fermeture
        self.setAttribute(Qt.WA_TranslucentBackground) # Nécessaire pour afficher les coins arrondis proprement

        # --- Layout et Contenu ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0) # On enlève les marges pour que le QLineEdit remplisse tout
        self.line_edit = QLineEdit(self)
        layout.addWidget(self.line_edit)

        # --- Style ---
        self.setStyleSheet("""
            QLineEdit {
                border: 0.3px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px 10px;
                background-color: #FFFFFF;
                color: #0D99FF;
                font-family: 'IBM Plex Mono';
                font-size: 14pt;
                font-style: italic;
            }
        """)

        # --- Connexions ---
        self.line_edit.returnPressed.connect(self._on_validate)
        
        # Installer un filtre d'événements pour la touche Échap
        self.installEventFilter(self)

    def eventFilter(self, watched, event):
        # Fermer avec la touche Échap
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Escape:
            self.close()
            return True
        return super().eventFilter(watched, event)

    def focusOutEvent(self, event: QFocusEvent):
        # Fermer si on perd le focus
        self.close()
        super().focusOutEvent(event)

    def _on_validate(self):
        text = self.line_edit.text().strip()
        if text:
            self.validated.emit(text)
        self.close()

    def show_at(self, pos):
        """Affiche la popup à une position globale et donne le focus au QLineEdit."""
        self.move(pos)
        self.show()
        self.line_edit.setFocus()