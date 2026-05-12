from PySide6.QtWidgets import QDockWidget, QWidget, QFormLayout, QLineEdit, QComboBox, QVBoxLayout, QStackedWidget, QHBoxLayout, QListWidget, QPushButton
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt

class PropertiesDock(QDockWidget):
    def __init__(self, controller):
        super().__init__("Propriétés de l'élément")
        self.controller = controller
        self.setAllowedAreas(Qt.RightDockWidgetArea)
        
        # On définit une largeur minimale correcte, sans bloquer le redimensionnement
        self.setMinimumWidth(260)

        # --- STYLESHEET (Design) ---
        # Calqué sur le style de la DeclarationDialog
        self.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF; /* Force le fond du champ en blanc */
                color: #000000;            /* Force le texte en noir */
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 5px 8px;
            }
            QLineEdit:hover {
                border: 1px solid #AAAAAA;
            }
            QLineEdit:focus {
                border: 1px solid #0D99FF; /* Bordure bleu électrique au focus */
            }
            QLineEdit:read-only {
                background-color: #EBEBEB; /* Fond grisé pour signifier qu'on ne peut pas l'éditer */
                color: #555555;
                border: 1px solid #EBEBEB;
            }
            QListWidget {
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #EBEBEB;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
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
        
        # --- NOUVEAU : Éditeur d'invariant (Horloge, Opérateur, Valeur) ---
        self.node_inv_layout = QHBoxLayout()
        self.node_inv_clock = QComboBox()
        self.node_inv_op = QComboBox()
        self.node_inv_op.addItems(["<=", ">="])
        self.node_inv_value = QLineEdit()
        self.node_inv_value.setPlaceholderText("Valeur")
        self.node_inv_value.setValidator(QDoubleValidator(0.0, float('inf'), 4, self)) # Interdit le texte et le négatif
        
        self.btn_add_inv = QPushButton("+")
        
        self.node_inv_layout.addWidget(self.node_inv_clock)
        self.node_inv_layout.addWidget(self.node_inv_op)
        self.node_inv_layout.addWidget(self.node_inv_value)
        self.node_inv_layout.addWidget(self.btn_add_inv)
        
        self.inv_list_widget = QListWidget()
        self.btn_remove_inv = QPushButton("Supprimer l'invariant")
        
        self.node_layout.addRow("ID :", self.node_id_field)
        self.node_layout.addRow("Nouvel Inv. :", self.node_inv_layout)
        self.node_layout.addRow("Invariants :", self.inv_list_widget)
        self.node_layout.addRow("", self.btn_remove_inv)
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
        
        # Signaux pour le noeud (Invariant)
        self.btn_add_inv.clicked.connect(self._on_add_invariant)
        self.node_inv_value.returnPressed.connect(self._on_add_invariant)
        self.btn_remove_inv.clicked.connect(self._on_remove_invariant)

    def show_node_props(self, node_id, data, available_clocks):
        self.node_id_field.setText(node_id)
        
        # Bloquer les signaux pendant la mise à jour UI (pour ne pas déclencher la sauvegarde à tort)
        self.node_inv_clock.blockSignals(True)
        self.node_inv_op.blockSignals(True)
        self.node_inv_value.blockSignals(True)
        
        self.node_inv_clock.clear()
        self.node_inv_clock.addItem("Aucune")
        self.node_inv_clock.addItems(available_clocks)
        
        self.node_inv_clock.setCurrentText("Aucune")
        self.node_inv_op.setCurrentText("<=")
        self.node_inv_value.clear()
        
        # Remplir la liste des invariants existants
        self.inv_list_widget.clear()
        invariants = data.get("invariants", [])
        for inv in invariants:
            inv_text = f"{inv.get('clock')} {inv.get('operator')} {inv.get('value')}"
            self.inv_list_widget.addItem(inv_text)
        
        self.node_inv_clock.blockSignals(False)
        self.node_inv_op.blockSignals(False)
        self.node_inv_value.blockSignals(False)

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

    def _on_add_invariant(self):
        node_id = self.node_id_field.text()
        clock = self.node_inv_clock.currentText()
        op = self.node_inv_op.currentText()
        val = self.node_inv_value.text()
        
        if node_id and clock != "Aucune" and val.strip():
            self.controller.add_node_invariant(node_id, clock, op, val)

    def _on_remove_invariant(self):
        node_id = self.node_id_field.text()
        current_row = self.inv_list_widget.currentRow()
        
        if node_id and current_row >= 0:
            self.controller.remove_node_invariant(node_id, current_row)