import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
import os

# ================== WINDOW ==================
root = tk.Tk()
root.title("Habit Tracker - HabiPet 🐾")
root.geometry("420x780")
root.configure(bg="#1a1a2e")

# ================== DATE & TIME ==================
time_label = tk.Label(root, font=("Arial", 10), fg="white", bg="#1a1a2e")
time_label.pack(pady=(10, 0))

def update_time():
    now = datetime.now().strftime("📅 %d %b %Y   ⏰ %I:%M %p")
    time_label.config(text=now)
    root.after(1000, update_time)

update_time()

# ================== TITLE ==================
tk.Label(
    root, text="HabiPet 🐾",
    font=("Arial", 22, "bold"),
    fg="white", bg="#1a1a2e"
).pack(pady=10)

# ================== PET IMAGE ==================
image_frame = tk.Frame(root, bg="#1a1a2e")
image_frame.pack(pady=10)

pet_label = tk.Label(image_frame, bg="#1a1a2e")
pet_label.pack()

current_photo = None

def load_pet(pet_name):
    global current_photo
    path = f"assets/pets/{pet_name}.jpeg"
    if os.path.exists(path):
        img = Image.open(path).resize((150, 150))
        current_photo = ImageTk.PhotoImage(img)
        pet_label.config(image=current_photo)

load_pet("cat")

# ================== PET BUTTONS ==================
button_frame = tk.Frame(root, bg="#1a1a2e")
button_frame.pack(pady=8)

pets = ["cat", "dog", "dino", "owl", "rhino"]
for i, pet in enumerate(pets):
    tk.Button(
        button_frame, text=pet.capitalize(), width=8,
        bg="#16c784", fg="white",
        activebackground="#12a870",
        command=lambda p=pet: load_pet(p)
    ).grid(row=0, column=i, padx=4)

# ================== PET HEALTH ==================
health_frame = tk.Frame(root, bg="#1a1a2e")
health_frame.pack(pady=15)

health_value = 75

tk.Label(
    health_frame,
    text=f"Pet Health: {health_value} / 100",
    font=("Arial", 12, "bold"),
    fg="white",
    bg="#1a1a2e"
).pack()

health_bar_bg = tk.Frame(health_frame, bg="#444", width=200, height=15)
health_bar_bg.pack(pady=5)
health_bar_bg.pack_propagate(False)

health_bar = tk.Frame(
    health_bar_bg,
    bg="#2ecc71",
    width=int(2 * health_value),
    height=15
)
health_bar.pack(side="left")

status_text = "Healthy" if health_value >= 70 else "Weak" if health_value >= 40 else "Critical"

tk.Label(
    health_frame,
    text=f"Status: {status_text}",
    font=("Arial", 11),
    fg="#2ecc71" if status_text == "Healthy" else "#f1c40f" if status_text == "Weak" else "#e74c3c",
    bg="#1a1a2e"
).pack()

# Completion Rate
tk.Label(
    health_frame,
    text="Completion Rate: 75%",
    font=("Arial", 11),
    fg="white",
    bg="#1a1a2e"
).pack(pady=(10, 0))

tk.Label(
    health_frame,
    text="Current Streak: 5 days 🔥",
    font=("Arial", 11),
    fg="white",
    bg="#1a1a2e"
).pack()

# ================== MAIN CONTAINER (2-COLUMN) ==================
main_container = tk.Frame(root, bg="#1a1a2e")
main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# LEFT: DAILY HABITS
left_panel = tk.Frame(main_container, bg="#0d0d1a", relief=tk.SUNKEN, bd=1)
left_panel.pack(side="left", fill=tk.BOTH, expand=True, padx=(0, 10))

tk.Label(
    left_panel, text="Daily Habits",
    font=("Arial", 12, "bold"),
    fg="white", bg="#0d0d1a"
).pack(pady=10)

habit_input_frame = tk.Frame(left_panel, bg="#0d0d1a")
habit_input_frame.pack(pady=5, padx=5)

habit_entry = tk.Entry(habit_input_frame, width=15)
habit_entry.pack(side="left", padx=3)

habits_frame = tk.Frame(left_panel, bg="#0d0d1a")
habits_frame.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

def add_habit():
    text = habit_entry.get().strip()
    if text:
        var = tk.BooleanVar()
        tk.Checkbutton(
            habits_frame,
            text=text,
            variable=var,
            fg="white",
            bg="#0d0d1a",
            selectcolor="#0d0d1a",
            activebackground="#0d0d1a"
        ).pack(anchor="w", fill=tk.X, padx=5, pady=2)
        habit_entry.delete(0, tk.END)

add_btn = tk.Button(
    habit_input_frame, text="Add",
    bg="#3498db", fg="white", width=4, command=add_habit
)
add_btn.pack(side="left", padx=2)

# RIGHT: WEEKLY PROGRESS
right_panel = tk.Frame(main_container, bg="#1a1a2e")
right_panel.pack(side="left", fill=tk.BOTH, expand=True)

tk.Label(
    right_panel, text="Week 1 Progress",
    font=("Arial", 14, "bold"),
    fg="white", bg="#1a1a2e"
).pack(pady=(10, 10))

week_frame = tk.Frame(right_panel, bg="#1a1a2e")
week_frame.pack(pady=10)

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
day_states = {}

def toggle_day(day):
    lbl = day_states[day]
    if lbl.cget("text") == "❌":
        lbl.config(text="✔", fg="#2ecc71")
    else:
        lbl.config(text="❌", fg="#e74c3c")

for i, day in enumerate(days):
    frame = tk.Frame(week_frame, bg="#1a1a2e")
    frame.grid(row=0, column=i, padx=4)

    tk.Label(frame, text=day, fg="white", bg="#1a1a2e").pack()
    lbl = tk.Label(frame, text="❌", font=("Arial", 14), fg="#e74c3c", bg="#1a1a2e", cursor="hand2")
    lbl.pack()
    lbl.bind("<Button-1>", lambda e, d=day: toggle_day(d))
    day_states[day] = lbl

# ================== EXIT BUTTON ==================
tk.Button(
    root, text="Exit",
    font=("Arial", 11), width=12,
    bg="#e74c3c", fg="white",
    command=root.destroy
).pack(pady=20)

root.mainloop()
tk.Button(
    root, text="Exit",
    font=("Arial", 11),
    width=12,
    bg="#e74c3c",
    fg="white",
    command=root.destroy
).pack(pady=20)

root.mainloop()
