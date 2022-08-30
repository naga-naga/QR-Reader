import PySimpleGUI as sg
from PIL import ImageGrab

def main():
    filename = "screenshot.png"
    img = ImageGrab.grab(all_screens=True)
    img_resized = img.resize((int(img.width / 2), int(img.height / 2)))
    img_resized.save(filename)

    layout = [
        [sg.Image(filename)]
    ]

    window = sg.Window("title", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

    window.close()

if __name__ == "__main__":
    main()
