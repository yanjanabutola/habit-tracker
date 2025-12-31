import PySimpleGUI as sg
from frontend.constants import PET_IMAGE_SIZE
from frontend.themes import THEMES, DEFAULT_THEME

def pet_view(pet_image_path, health):
    theme = THEMES[DEFAULT_THEME]

    layout = [
        [sg.Image(pet_image_path, size=PET_IMAGE_SIZE)],
        [sg.Text(f"Health: {health}%", 
                 text_color=theme["fg"], 
                 background_color=theme["bg"],
                 font=theme["font"])]
    ]

    return sg.Frame(
        "Your Pet",
        layout,
        background_color=theme["bg"],
        title_color=theme["accent"]
    )
