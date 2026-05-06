class AutomataModel:
    def __init__(self):
        self.data = {"locations": [], "init": ""}

    def add_location(self, loc_id, x, y):
        """Stocke la localité selon ton format JSON final"""
        self.data["locations"].append(loc_id)
        self.data[loc_id] = {
            "node_pos": {"x": x, "y": y},
            "name_pos": {"x": x, "y": y},
            "invariant": [[0, "inf", "inf"], ["val", 0, "inf"], ["val", "inf", 0]],
            "invariant_pos": {"x": x, "y": y},
            "transitions": [],
            "transitions_layout": {}
        }