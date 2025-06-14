import pygame


def init_layers():
    layers = [
        {"image": pygame.image.load("src/images/layer-1.png").convert_alpha(), "speed": 0.2, "y": 0},
        {"image": pygame.image.load("src/images/layer-2.png").convert_alpha(), "speed": 0.5, "y": 100},
        {"image": pygame.image.load("src/images/layer-3.png").convert_alpha(), "speed": 1.0, "y": 0},
        {"image": pygame.image.load("src/images/layer-4.png").convert_alpha(), "speed": 2.0, "y": 100},
        {"image": pygame.image.load("src/images/layer-5.png").convert_alpha(), "speed": 3.0, "y": 100},
    ]

    for layer in layers:
        layer["x1"] = 0
        layer["x2"] = layer["image"].get_width()
    return layers


def draw_parallax_background(screen, layers, scroll_enabled=True):
    for layer in layers:
        if scroll_enabled:
            layer["x1"] -= layer["speed"]
            layer["x2"] -= layer["speed"]

        img = layer["image"]
        img_width = img.get_width()
        y = layer["y"]

        if layer["x1"] <= -img_width:
            layer["x1"] = layer["x2"] + img_width
        if layer["x2"] <= -img_width:
            layer["x2"] = layer["x1"] + img_width

        screen.blit(img, (layer["x1"], y))
        screen.blit(img, (layer["x2"], y))