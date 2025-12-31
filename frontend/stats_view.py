import PySimpleGUI as sg
from frontend.themes import THEMES, DEFAULT_THEME

def stats_view(daily_pct, weekly_pct, monthly_pct):
    theme = THEMES[DEFAULT_THEME]

    layout = [
        [sg.Text("Stats", font=theme["title_font"], 
                 background_color=theme["bg"], text_color=theme["accent"])],
        [sg.Text(f"Today: {daily_pct}%", background_color=theme["bg"], text_color=theme["fg"])],
        [sg.Text(f"This Week: {weekly_pct}%", background_color=theme["bg"], text_color=theme["fg"])],
        [sg.Text(f"This Month: {monthly_pct}%", background_color=theme["bg"], text_color=theme["fg"])]
    ]

    return sg.Frame(
        "Progress",
        layout,
        background_color=theme["bg"],
        title_color=theme["accent"]
    )
