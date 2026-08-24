"""单人挑战界面。"""
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..cards import SUITS, face_name
from ..challenge import MESSAGES, ChallengeGame
from ..storage import append_record, default_path, load_records


class ChallengeWindow(QWidget):
    def __init__(self, records_path=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("game24 — 单人挑战")
        self.records_path = records_path or default_path()
        self.game = ChallengeGame()
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        self.cards_label = QLabel()
        self.cards_label.setStyleSheet("font-size: 28px;")
        layout.addWidget(self.cards_label)

        self.input = QLineEdit()
        self.input.setPlaceholderText("输入算式，如 3*8*(9-8)")
        self.input.returnPressed.connect(self._on_submit)
        layout.addWidget(self.input)

        row = QHBoxLayout()
        self.submit_btn = QPushButton("提交")
        self.nosolution_btn = QPushButton("无解")
        self.skip_btn = QPushButton("跳过")
        self.highlight_btn = QPushButton("高光时刻")
        for b in (self.submit_btn, self.nosolution_btn, self.skip_btn, self.highlight_btn):
            row.addWidget(b)
        layout.addLayout(row)

        self.feedback_label = QLabel()
        layout.addWidget(self.feedback_label)

        self.submit_btn.clicked.connect(self._on_submit)
        self.nosolution_btn.clicked.connect(self._on_nosolution)
        self.skip_btn.clicked.connect(self._on_skip)
        self.highlight_btn.clicked.connect(self._on_highlight)

    def _refresh(self):
        g = self.game
        self.status_label.setText(f"第 {g.level} 关   第 {g.question_number}/10 题   得分 {g.score}")
        self.cards_label.setText("  ".join(f"{face_name(v)}{SUITS[0]}" for v in g.hand))
        self.input.clear()
        self.input.setFocus()

    def _on_submit(self):
        expr = self.input.text().strip()
        if not expr:
            return
        self._handle(self.game.submit(expr))

    def _on_nosolution(self):
        self._handle(self.game.declare_no_solution())

    def _on_skip(self):
        self._handle(self.game.skip())

    def _handle(self, out):
        if out.level_over:
            self._finish_level(out)
            return
        self._refresh()
        self.feedback_label.setText(MESSAGES.get(out.feedback, ""))

    def _finish_level(self, out):
        rec = self.game.finish()
        append_record(self.records_path, rec)
        if out.passed:
            self.game = ChallengeGame(level=self.game.level + 1)
            msg = f"恭喜过关！进入第 {self.game.level} 关。"
        else:
            self.game = ChallengeGame(level=self.game.level)
            msg = f"闯关失败（得分 {rec['score']}）。已重置本关。"
        self._refresh()
        self.feedback_label.setText(msg)

    def _on_highlight(self):
        records = load_records(self.records_path)
        if not records:
            QMessageBox.information(self, "高光时刻", "暂无游戏记录。")
            return
        lines = []
        for r in records:
            state = "过关" if r.get("passed") else "失败"
            lines.append(
                f"{r.get('timestamp', '')}  第 {r.get('level', '?')} 关  "
                f"得分 {r.get('score', '?')}  {state}  用时 {r.get('duration', '?')}s"
            )
        QMessageBox.information(self, "高光时刻", "\n".join(lines))
