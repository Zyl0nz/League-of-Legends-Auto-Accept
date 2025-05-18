from PIL import ImageFont

try:
    font_path = r"C:\Users\Zyl0nz\Desktop\League Of Legends Auto Accept\BeaufortforLOL-medium.ttf"
    font = ImageFont.truetype(font_path, 12)
    print("Font loaded successfully.")
    print("Font name:", font.getname())
except Exception as e:
    print("Error loading font:", e)
