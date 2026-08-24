"""24 点提示界面。"""
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..cards import face_name
from ..hint import HintModel, hint_message

CARD_VALUES = list(range(1, 14))  # A,2,...,10,J,Q,K → 1..13


class HintWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("game24 — 24 点提示")
        self.model = HintModel()
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        boxes = QHBoxLayout()
        self.slot_buttons = []
        for i in range(4):
            b = QPushButton("")
            b.setFixedSize(64, 64)
            b.clicked.connect(lambda checked=False, idx=i: self._on_clear(idx))
            boxes.addWidget(b)
            self.slot_buttons.append(b)
        layout.addLayout(boxes)

        grid = QGridLayout()
        for i, v in enumerate(CARD_VALUES):
            b = QPushButton(face_name(v))
            b.clicked.connect(lambda checked=False, val=v: self._on_pick(val))
            grid.addWidget(b, i // 7, i % 7)
        layout.addLayout(grid)

        btn_row = QHBoxLayout()
        self.hint_btn = QPushButton("提示")
        self.hint_btn.clicked.connect(self._on_hint)
        self.clear_btn = QPushButton("清空")
        self.clear_btn.clicked.connect(self._on_clear_all)
        btn_row.addWidget(self.hint_btn)
        btn_row.addWidget(self.clear_btn)
        layout.addLayout(btn_row)

        self.result_label = QLabel()
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

    def _on_pick(self, value):
        if self.model.pick(value):
            self._refresh()

    def _on_clear(self, index):
        self.model.clear(index)
        self._refresh()

    def _on_clear_all(self):
        self.model.clear_all()
        self._refresh()

    def _on_hint(self):
        self.result_label.setText(hint_message(self.model))

    def _refresh(self):
        for i, b in enumerate(self.slot_buttons):
            v = self.model.selected[i]
            b.setText(face_name(v) if v is not None else "")
        self.result_label.setText("")
