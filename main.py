from ctypes import resize
import os
import PySimpleGUI as sg
from PIL import ImageGrab

def main():
    RESIZE_RATIO = 2.5
    FILENAME = os.path.join(os.getenv("TEMP"), "screenshot.png")

    img = ImageGrab.grab(all_screens=True)
    resized_width = int(img.width / RESIZE_RATIO)
    resized_height = int(img.height / RESIZE_RATIO)
    resized_size = (resized_width, resized_height)
    resized_img = img.resize(resized_size)
    resized_img.save(FILENAME)

    layout = [
        [
            sg.Graph(
                canvas_size=resized_size,
                graph_bottom_left=(0, 0),
                graph_top_right=resized_size,
                background_color="white",
                enable_events=True,
                drag_submits=True,
                key="GRAPH"
            ),
        ],
    ]

    window = sg.Window("QR Reader", layout, finalize=True)
    graph: sg.Graph = window["GRAPH"]
    graph.draw_image(filename=FILENAME, location=(0, resized_height))
    graph.update()
    graph.bind("<ButtonPress-1>", "_Press")
    graph.bind("<Button1-Motion>", "_Motion")
    graph.bind("<ButtonRelease-1>", "_Release")

    drag_from = None
    cursor_pos = None
    prev_rectangle = None

    while True:
        event, values = window.read()
        # print(event, values)

        if event == sg.WINDOW_CLOSED:
            break
        elif event == "GRAPH_Press":
            drag_from = values["GRAPH"]
            print(drag_from)
        elif event == "GRAPH_Motion":
            cursor_pos = values["GRAPH"]
            print(cursor_pos)

            if prev_rectangle is not None:
                graph.delete_figure(prev_rectangle)

            prev_rectangle = graph.draw_rectangle(
                top_left=drag_from,
                bottom_right=cursor_pos,
                line_color="red",
                line_width=3)
            graph.update()
        elif event == "GRAPH_Release":
            print("-----")

    window.close()

if __name__ == "__main__":
    main()
