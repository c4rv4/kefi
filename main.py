import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import ttkbootstrap
import io

def get_weather(city):
    API_key = "015a47b3533022e26b8a6a5886383308"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)
    
    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    weather = res.json()
    icon_id = weather["weather"][0]["icon"]
    temperature = weather["main"]["temp"] - 273.15
    description = weather["weather"][0]["description"]
    city_name = weather["name"]
    country = weather["sys"]["country"]
    
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}.png"
    return (icon_url, temperature, description, city_name, country)

def search():
    city = c_e.get()
    result = get_weather(city)
    if result is None:
        return
    
    icon_url, temperature, description, city_name, country = result
    
    lab_coun.configure(text=f"{city_name}, {country}")
    
    icon_data = requests.get(icon_url).content
    icon = ImageTk.PhotoImage(Image.open(io.BytesIO(icon_data)))
    icon_lab.configure(image=icon)
    icon_lab.image = icon
    
    temp_lab.configure(text=f"Temperature: {temperature:.2f}°C")
    info_label.configure(text=f"Description: {description}")

root = ttkbootstrap.Window(themename="flatly")
root.title("KEFI")
root.geometry("400x400")

c_e = ttkbootstrap.Entry(root, font="Helvetica, 18")
c_e.pack(pady=10)

s_b = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
s_b.pack(pady=10)

lab_coun = tk.Label(root, font="Helvetica, 25")
lab_coun.pack(pady=20)

icon_lab = tk.Label(root)
icon_lab.pack()

temp_lab = tk.Label(root, font="Helvetica, 20")
temp_lab.pack()

info_label = tk.Label(root, font="Helvetica, 20")
info_label.pack()

root.mainloop()
