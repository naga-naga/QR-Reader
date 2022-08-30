import os
import PySimpleGUI as sg
from PIL import ImageGrab

def main():
    RESIZE_RATIO = 2.5
    FILENAME = os.path.join(os.getenv("TEMP"), "screenshot.png")

    img = ImageGrab.grab(all_screens=True)
    img_resized = img.resize((int(img.width / RESIZE_RATIO), int(img.height / RESIZE_RATIO)))
    img_resized.save(FILENAME)

    layout = [
        [sg.Image(FILENAME)]
    ]

    window = sg.Window("QR Reader", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

    window.close()

if __name__ == "__main__":
    main()
