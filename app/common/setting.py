# coding: utf-8
from pathlib import Path

# change DEBUG to False if you want to compile the code to exe
DEBUG = "__compiled__" not in globals()


YEAR = 2024
AUTHOR = "630"
VERSION = "v0.0.1"
APP_NAME = "Class Fee System"

REPO_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets"

CLASS_NAME = "安顺市第一高级中学 2026级3班"


CONFIG_FOLDER = Path("config").absolute()
CONFIG_FILE = CONFIG_FOLDER / "config.json"
DATA_FILE = CONFIG_FOLDER / "feeData.json"
IMG_FOLDER = CONFIG_FOLDER / "images"
