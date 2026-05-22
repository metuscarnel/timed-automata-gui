from PySide6.QtWidgets import QDockWidget, QWidget, QFormLayout, QLineEdit, QComboBox, QVBoxLayout, QStackedWidget, QHBoxLayout, QListWidget, QPushButton
from PySide6.QtGui import QDoubleValidator, QIntValidator
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
            padding: 6px 12px;
            }
            QPushButton#deleteBtn {
                background-color: #FFEBEE;
                color: #D32F2F;
                border: 1px solid #EF9A9A;
                font-weight: bold;
            padding: 8px 12px; /* Un peu plus grand pour les actions de suppression */
            }
            QPushButton#deleteBtn:hover {
                background-color: #FFCDD2;
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
        self.node_inv_op.addItems(["<=", ">=", "=="]) # Nouvelle règle métier
        
        self.node_inv_clock_target = QComboBox()
        
        self.node_inv_value = QLineEdit()
        self.node_inv_value.setPlaceholderText("Valeur (0)")
        self.node_inv_value.setValidator(QIntValidator(-9999, 9999, self))
        
        self.btn_add_inv = QPushButton("+")
        
        self.node_inv_layout.addWidget(self.node_inv_clock)
        self.node_inv_layout.addWidget(self.node_inv_op)
        self.node_inv_layout.addWidget(self.node_inv_clock_target)
        self.node_inv_layout.addWidget(self.node_inv_value)
        self.node_inv_layout.addWidget(self.btn_add_inv)
        
        self.inv_list_widget = QListWidget()
        self.btn_remove_inv = QPushButton("Supprimer l'invariant")
        
        self.btn_delete_node = QPushButton("Supprimer la localité")
        self.btn_delete_node.setObjectName("deleteBtn") # Application du style d'avertissement (Rouge)
        
        self.node_layout.addRow("ID :", self.node_id_field)
        self.node_layout.addRow("Nouvel Inv. :", self.node_inv_layout)
        self.node_layout.addRow("Invariants :", self.inv_list_widget)
        self.node_layout.addRow("", self.btn_remove_inv)
        self.node_layout.addRow("", QWidget()) # Espace pour aérer
        self.node_layout.addRow("", self.btn_delete_node)
        self.stacked_widget.addWidget(self.node_panel)

        # --- PANNEAU TRANSITION ---
        self.trans_panel = QWidget()
        self.trans_layout = QFormLayout(self.trans_panel)
        
        self.trans_source_field = QLineEdit()
        self.trans_source_field.setReadOnly(True)
        self.trans_target_field = QLineEdit()
        self.trans_target_field.setReadOnly(True)
        self.trans_action_combo = QComboBox()
        
        # --- NOUVEAU : Éditeur de garde (Horloge, Opérateur, Valeur) ---
        self.trans_guard_layout = QHBoxLayout()
        self.trans_guard_clock = QComboBox()
        self.trans_guard_op = QComboBox()
        self.trans_guard_op.addItems(["<=", ">=", "=="]) # Même règle métier que pour les nœuds
        
        self.trans_guard_clock_target = QComboBox()
        
        self.trans_guard_value = QLineEdit()
        self.trans_guard_value.setPlaceholderText("Valeur (0)")
        self.trans_guard_value.setValidator(QIntValidator(-9999, 9999, self))
        
        self.btn_add_guard = QPushButton("+")
        self.trans_guard_layout.addWidget(self.trans_guard_clock)
        self.trans_guard_layout.addWidget(self.trans_guard_op)
        self.trans_guard_layout.addWidget(self.trans_guard_clock_target)
        self.trans_guard_layout.addWidget(self.trans_guard_value)
        self.trans_guard_layout.addWidget(self.btn_add_guard)
        
        self.guard_list_widget = QListWidget()
        self.btn_remove_guard = QPushButton("Supprimer la garde")
        
        self.btn_delete_trans = QPushButton("Supprimer la transition")
        self.btn_delete_trans.setObjectName("deleteBtn") # Application du style d'avertissement (Rouge)
        
        self.trans_layout.addRow("Source :", self.trans_source_field)
        self.trans_layout.addRow("Cible :", self.trans_target_field)
        self.trans_layout.addRow("Action :", self.trans_action_combo)
        self.trans_layout.addRow("Nouv. Garde :", self.trans_guard_layout)
        self.trans_layout.addRow("Gardes :", self.guard_list_widget)
        self.trans_layout.addRow("", self.btn_remove_guard)
        self.trans_layout.addRow("", QWidget()) # Espace pour aérer
        self.trans_layout.addRow("", self.btn_delete_trans)
        self.stacked_widget.addWidget(self.trans_panel)

        # Signaux
        self.trans_action_combo.currentTextChanged.connect(self._on_action_changed)
        
        # Signaux pour la transition (Gardes)
        self.btn_add_guard.clicked.connect(self._on_add_guard)
        self.trans_guard_value.returnPressed.connect(self._on_add_guard)
        self.btn_remove_guard.clicked.connect(self._on_remove_guard)
        
        self.trans_guard_clock.currentIndexChanged.connect(self._validate_guard_add_btn)
        self.trans_guard_clock_target.currentIndexChanged.connect(self._validate_guard_add_btn)

        # Signaux pour le noeud (Invariant)
        self.btn_add_inv.clicked.connect(self._on_add_invariant)
        self.node_inv_value.returnPressed.connect(self._on_add_invariant)
        self.btn_remove_inv.clicked.connect(self._on_remove_invariant)
        
        
        self.node_inv_clock_target.currentIndexChanged.connect(self._validate_inv_add_btn)
        
        self.btn_delete_node.clicked.connect(self._on_delete_node)
        self.btn_delete_trans.clicked.connect(self._on_delete_trans)
        self.inv_list_widget.itemDoubleClicked.connect(self._on_edit_invariant)
        self.guard_list_widget.itemDoubleClicked.connect(self._on_edit_guard)
        
    def show_node_props(self, node_id, data, available_clocks):
        self.node_id_field.setText(node_id)
        
        # Bloquer les signaux pendant la mise à jour UI (pour ne pas déclencher la sauvegarde à tort)
        self.node_inv_clock.blockSignals(True)
        self.node_inv_op.blockSignals(True)
        self.node_inv_value.blockSignals(True)
        
        self.node_inv_clock.clear()
        self.node_inv_clock.addItem("Aucune")
        self.node_inv_clock.addItems(available_clocks)
        
        self.node_inv_clock_target.blockSignals(True)
        self.node_inv_clock_target.clear()
        self.node_inv_clock_target.addItem("---")
        self.node_inv_clock_target.addItems(available_clocks)
        self.node_inv_clock_target.blockSignals(False)
        
        self.node_inv_clock.setCurrentText("Aucune")
        self.node_inv_op.setCurrentText("<=")
        self.node_inv_clock_target.setCurrentText("---")
        self.node_inv_value.clear()
        
        # Remplir la liste des invariants existants
        self.inv_list_widget.clear()
        invariants = data.get("invariants", [])
        for inv in invariants:
            c1 = inv.get('clock')
            op = inv.get('operator')
            t_type = inv.get('type')
            t_val = inv.get('value')
            if t_type == "clock":
                offset = inv.get('offset', 0)
                if offset > 0:
                    inv_text = f"{c1} {op} {t_val} + {offset}"
                elif offset < 0:
                    inv_text = f"{c1} {op} {t_val} - {abs(offset)}"
                else:
                    inv_text = f"{c1} {op} {t_val}"
            else:
                inv_text = f"{c1} {op} {t_val}"
            self.inv_list_widget.addItem(inv_text)
        
        self.node_inv_clock.blockSignals(False)
        self.node_inv_op.blockSignals(False)
        self.node_inv_value.blockSignals(False)
        
        self._validate_inv_add_btn()

        self.stacked_widget.setCurrentWidget(self.node_panel)
        self.show()

    def show_transition_props(self, source_id, target_id, data, available_actions, available_clocks):
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

        # --- Rafraîchissement des Gardes ---
        self.trans_guard_clock.blockSignals(True)
        self.trans_guard_op.blockSignals(True)
        self.trans_guard_value.blockSignals(True)
        
        self.trans_guard_clock.clear()
        self.trans_guard_clock.addItem("Aucune")
        self.trans_guard_clock.addItems(available_clocks)
        
        self.trans_guard_clock_target.blockSignals(True)
        self.trans_guard_clock_target.clear()
        self.trans_guard_clock_target.addItem("---")
        self.trans_guard_clock_target.addItems(available_clocks)
        self.trans_guard_clock_target.blockSignals(False)
        
        self.trans_guard_clock.setCurrentText("Aucune")
        self.trans_guard_op.setCurrentText("<=")
        self.trans_guard_clock_target.setCurrentText("---")
        self.trans_guard_value.clear()
        
        self.guard_list_widget.clear()
        guards = data.get("guards", [])
        for guard in guards:
            c1 = guard.get('clock')
            op = guard.get('operator')
            t_type = guard.get('type')
            t_val = guard.get('value')
            if t_type == "clock":
                offset = guard.get('offset', 0)
                if offset > 0:
                    guard_text = f"{c1} {op} {t_val} + {offset}"
                elif offset < 0:
                    guard_text = f"{c1} {op} {t_val} - {abs(offset)}"
                else:
                    guard_text = f"{c1} {op} {t_val}"
            else:
                guard_text = f"{c1} {op} {t_val}"
            self.guard_list_widget.addItem(guard_text)
            
        self.trans_guard_clock.blockSignals(False)
        self.trans_guard_op.blockSignals(False)
        self.trans_guard_value.blockSignals(False)
        
        self._validate_guard_add_btn()

        self.stacked_widget.setCurrentWidget(self.trans_panel)
        self.show()

    def _validate_inv_add_btn(self):
        clock1 = self.node_inv_clock.currentText()
        clock2 = self.node_inv_clock_target.currentText()
        if clock1 == "Aucune" or (clock1 == clock2 and clock2 != "---"):
            self.btn_add_inv.setEnabled(False)
        else:
            self.btn_add_inv.setEnabled(True)

    def _validate_guard_add_btn(self):
        clock1 = self.trans_guard_clock.currentText()
        clock2 = self.trans_guard_clock_target.currentText()
        if clock1 == "Aucune" or (clock1 == clock2 and clock2 != "---"):
            self.btn_add_guard.setEnabled(False)
        else:
            self.btn_add_guard.setEnabled(True)

    def _on_action_changed(self, new_action):
        source_id = self.trans_source_field.text()
        target_id = self.trans_target_field.text()
        if source_id and target_id:
            self.controller.update_transition_action(source_id, target_id, new_action)

    def _on_add_invariant(self):
        node_id = self.node_id_field.text()
        clock1 = self.node_inv_clock.currentText()
        op = self.node_inv_op.currentText()
        clock2 = self.node_inv_clock_target.currentText()
        val_text = self.node_inv_value.text().strip()
        
        if not node_id or clock1 == "Aucune":
            return
            
        offset_val = int(val_text) if val_text else 0
        
        if clock2 == "---":
            t_type = "value"
            t_val = str(offset_val)
            offset = 0
        else:
            if clock1 == clock2:
                return
            t_type = "clock"
            t_val = clock2
            offset = offset_val
            
        self.controller.add_node_invariant(node_id, clock1, op, t_type, t_val, offset)

    def _on_add_guard(self):
        source_id = self.trans_source_field.text()
        target_id = self.trans_target_field.text()
        clock1 = self.trans_guard_clock.currentText()
        op = self.trans_guard_op.currentText()
        clock2 = self.trans_guard_clock_target.currentText()
        val_text = self.trans_guard_value.text().strip()
        
        if not source_id or not target_id or clock1 == "Aucune":
            return
            
        offset_val = int(val_text) if val_text else 0
        
        if clock2 == "---":
            t_type = "value"
            t_val = str(offset_val)
            offset = 0
        else:
            if clock1 == clock2:
                return
            t_type = "clock"
            t_val = clock2
            offset = offset_val
            
        self.controller.add_transition_guard(source_id, target_id, clock1, op, t_type, t_val, offset)

    def _on_remove_guard(self):
        source_id = self.trans_source_field.text()
        target_id = self.trans_target_field.text()
        current_row = self.guard_list_widget.currentRow()
        
        if source_id and target_id and current_row >= 0:
            self.controller.remove_transition_guard(source_id, target_id, current_row)

    def _on_remove_invariant(self):
        node_id = self.node_id_field.text()
        current_row = self.inv_list_widget.currentRow()
        
        if node_id and current_row >= 0:
            self.controller.remove_node_invariant(node_id, current_row)

    def _on_delete_node(self):
        node_id = self.node_id_field.text()
        if node_id:
            self.controller.handle_delete_node(node_id)

    def _on_delete_trans(self):
        source_id = self.trans_source_field.text()
        target_id = self.trans_target_field.text()
        if source_id and target_id:
            self.controller.handle_delete_transition(source_id, target_id)
   

    def _on_edit_invariant(self, item):
        print("Invariant edit")
        self.btn_add_guard.setText("v")
        print(self.btn_add_guard.text())
    def _on_edit_guard(self, item):
        print("Guard editing")
