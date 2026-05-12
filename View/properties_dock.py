from PySide6.QtWidgets import QDockWidget, QWidget, QFormLayout, QLineEdit, QComboBox, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Qt

class PropertiesDock(QDockWidget):
    def __init__(self, controller):
        super().__init__("Propriétés de l'élément")
        self.controller = controller
        self.setAllowedAreas(Qt.RightDockWidgetArea)

        # --- STYLESHEET (Design) ---
        # Calqué sur le style de la DeclarationDialog
        self.setStyleSheet("""
            QLineEdit, QComboBox {
                background-color: #FFFFFF; /* Force le fond du champ en blanc */
                color: #000000;            /* Force le texte en noir */
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 4px;
            }
            QLineEdit:read-only {
                background-color: #EBEBEB; /* Fond grisé pour signifier qu'on ne peut pas l'éditer */
                color: #555555;
            }
        """)

        # Conteneur principal
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.stacked_widget = QStackedWidget()
        
        self.layout.addWidget(self.stacked_widget)
        self.layout.addStretch() # Pousse le formulaire vers le haut
        self.setWidget(self.container)

        # --- PANNEAU LOCALITÉ ---
        self.node_panel = QWidget()
        self.node_layout = QFormLayout(self.node_panel)
        
        self.node_id_field = QLineEdit()
        self.node_id_field.setReadOnly(True)
        self.node_inv_combo = QComboBox()
        self.node_inv_combo.addItem("Aucun") # Placeholder en attendant les vrais Invariants
        
        self.node_layout.addRow("ID :", self.node_id_field)
        self.node_layout.addRow("Invariant :", self.node_inv_combo)
        self.stacked_widget.addWidget(self.node_panel)

        # --- PANNEAU TRANSITION ---
        self.trans_panel = QWidget()
        self.trans_layout = QFormLayout(self.trans_panel)
        
        self.trans_source_field = QLineEdit()
        self.trans_source_field.setReadOnly(True)
        self.trans_target_field = QLineEdit()
        self.trans_target_field.setReadOnly(True)
        self.trans_action_combo = QComboBox()
        
        self.trans_layout.addRow("Source :", self.trans_source_field)
        self.trans_layout.addRow("Cible :", self.trans_target_field)
        self.trans_layout.addRow("Action :", self.trans_action_combo)
        self.stacked_widget.addWidget(self.trans_panel)

        # Signaux
        self.trans_action_combo.currentTextChanged.connect(self._on_action_changed)

    def show_node_props(self, node_id, data):
        self.node_id_field.setText(node_id)
        self.stacked_widget.setCurrentWidget(self.node_panel)
        self.show()

    def show_transition_props(self, source_id, target_id, data, available_actions):
        self.trans_source_field.setText(source_id)
        self.trans_target_field.setText(target_id)
        
        # On bloque les signaux pendant le rafraîchissement du menu déroulant
        self.trans_action_combo.blockSignals(True)
        self.trans_action_combo.clear()
        self.trans_action_combo.addItem("Aucune")
        self.trans_action_combo.addItems(available_actions)
        current_action = data.get("action", "Aucune") or "Aucune"
        self.trans_action_combo.setCurrentText(current_action)
        self.trans_action_combo.blockSignals(False)

        self.stacked_widget.setCurrentWidget(self.trans_panel)
        self.show()

    def _on_action_changed(self, new_action):
        source_id = self.trans_source_field.text()
        target_id = self.trans_target_field.text()
        if source_id and target_id:
            self.controller.update_transition_action(source_id, target_id, new_action)