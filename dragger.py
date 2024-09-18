class Dragger:
    def __init__(self, canvas):
        pass

    def drag_start(event):
        global initial_position
        global drag_data
        item = event.widget.find_closest(event.x, event.y)
        item_type = event.widget.type(item)
        if item_type == 'rectangle':  # Check if the clicked item is a rectangle
            return  # Ignore rectangles
        drag_data = {'x': event.x, 'y': event.y, 'item': item}
        initial_position = {'x': event.x, 'y': event.y, 'item': item}

    def drag_motion(event, canvas):
        global drag_data
        if drag_data:
            x, y = event.x - drag_data['x'], event.y - drag_data['y']
            canvas.move(drag_data['item'], x, y)
            drag_data['x'], drag_data['y'] = event.x, event.y

    def drag_stop(event):
        global drag_data
    # if drag_data:
    # if drag_data['x']
