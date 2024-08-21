from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont

"""
QFont::Light (25): 非常细的字体，适用于需要强调细字体的场合。
QFont::Normal (50): 标准的字体粗细，适用于大多数文本。
QFont::DemiBold (63): 半粗体，比标准字体稍粗。
QFont::Bold (75): 粗体，用于标题或需要强调的文本。
QFont::Black (87): 非常粗的字体，适用于需要强烈视觉冲击的文本。
"""


class FontWeight:

    Normal = QFont.Weight.Normal
    DemiBold = QFont.Weight.DemiBold
    Bold = QFont.Weight.Bold
    Black = QFont.Weight.Black


def setFont(label: QLabel, fontSize: int, fontWeight: FontWeight):

    font = QFont()
    font.setFamilies(["HarmonyOS Sans SC", "Microsoft YaHei"])
    font.setPointSize(fontSize)
    font.setWeight(fontWeight)

    label.setFont(font)
