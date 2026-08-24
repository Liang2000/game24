"""主菜单。"""
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from .challenge_window import ChallengeWindow
from .hint_window import HintWindow


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("game24")
        layout = QVBoxLayout(self)

        title = QLabel("24 点益智小游戏")
        title.setStyleSheet("font-size: 24px;")
        layout.addWidget(title)

        row = QHBoxLayout()
        self.challenge_btn = QPushButton("单人挑战")
        self.hint_btn = QPushButton("24 点提示")
        row.addWidget(self.challenge_btn)
        row.addWidget(self.hint_btn)
        layout.addLayout(row)

        self.challenge_btn.clicked.connect(self._open_challenge)
        self.hint_btn.clicked.connect(self._open_hint)

        self._challenge_window = None
        self._hint_window = None

    def _open_challenge(self):
        if self._challenge_window is None:
            self._challenge_window = ChallengeWindow()
        self._challenge_window.show()

    def _open_hint(self):
        if self._hint_window is None:
            self._hint_window = HintWindow()
        self._hint_window.show()
