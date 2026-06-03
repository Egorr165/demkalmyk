import os
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )

RESOURCES_DIR = os.path.join(BASE_DIR, "import")
PHOTOS_DIR = os.path.join(RESOURCES_DIR, "photos")

ICON_ICO = os.path.join(RESOURCES_DIR, "icon.ico")
ICON_PNG = os.path.join(RESOURCES_DIR, "icon.png")
PICTURE_PNG = os.path.join(RESOURCES_DIR, "picture.png")

COLOR_WHITE = "#FFFFFF"
COLOR_SECOND = "#DAA520"
COLOR_ACCENT = "#B8860B"
COLOR_DISCOUNT_ROW = "#F4A460"
COLOR_ZERO_STOCK = "#ADD8E6"

FONT = "Calibri"
