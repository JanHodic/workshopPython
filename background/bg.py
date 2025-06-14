def draw_parallax_background(screen, layers):
    for layer in layers:
        speed = layer["speed"]
        y = layer["y"]
        layer["x1"] -= speed
        layer["x2"] -= speed

        img = layer["image"]
        img_width = img.get_width()

        if layer["x1"] <= -img_width:
            layer["x1"] = layer["x2"] + img_width
        if layer["x2"] <= -img_width:
            layer["x2"] = layer["x1"] + img_width

        # vykresli obě kopie vrstvy na dané Y souřadnici
        screen.blit(img, (layer["x1"], y))
        screen.blit(img, (layer["x2"], y))