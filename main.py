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
        # 画像をクリックしたとき
        elif event == "GRAPH_Press":
            drag_from = values["GRAPH"]
            print(drag_from)
        # 画像をドラッグしているとき
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
        # クリックをやめたとき
        elif event == "GRAPH_Release":
            print("-----")

            # 元の縮尺に戻す
            # また，y 座標は上下反転しているので，それも戻す
            start_x = drag_from[0] * RESIZE_RATIO
            start_y = img.height - drag_from[1] * RESIZE_RATIO
            end_x = cursor_pos[0] * RESIZE_RATIO
            end_y = img.height - cursor_pos[1] * RESIZE_RATIO

            # 始点の座標が終点の座標より大きいとトリミングの際にエラーとなるため
            # 該当する場合は入れ替えておく
            if start_x > end_x:
                start_x, end_x = end_x, start_x
            if start_y > end_y:
                start_y, end_y = end_y, start_y
            print(start_x, start_y, end_x, end_y)

            qr_image = img.crop((start_x, start_y, end_x, end_y))
            qr_image.save("qr.png")

    window.close()

if __name__ == "__main__":
    main()
