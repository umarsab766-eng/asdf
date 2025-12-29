from nicegui import ui
import tkinter as tk
from tkinter import messagebox

def convert_temperature():
    try:
        temp = float(entry_temp.get())
        from_unit = combo_from.get()
        
       
        if from_unit == "Celsius (°C)":
            f = (temp * 9/5) + 32
            k = temp + 273.15
            result_f.config(text=f"{f:.2f} °F")
            result_k.config(text=f"{k:.2f} K")
            
        elif from_unit == "Fahrenheit (°F)":
            c = (temp - 32) * 5/9
            k = c + 273.15
            result_c.config(text=f"{c:.2f} °C")
            result_k.config(text=f"{k:.2f} K")
            
        elif from_unit == "Kelvin (K)":
            c = temp - 273.15
            f = (c * 9/5) + 32
            result_c.config(text=f"{c:.2f} °C")
            result_f.config(text=f"{f:.2f} °F")

    except ValueError:
        messagebox.showerror("Error", "Kripya sahi number darj karein!")


root = tk.Tk()
root.title("Professional Temp Converter")
root.geometry("400x500")
root.resizable(False, False)

# Colors (Modern Dark Theme)
bg_color = "#1e1e2e"      
card_color = "#252535"     
text_color = "#c0caf5"     
accent_color = "#7aa2f7"   
entry_bg = "#16161e"      
btn_color = "#bb9af7"      

root.configure(bg=bg_color)

main_frame = tk.Frame(root, bg=card_color, padx=20, pady=20)
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=440)


title_label = tk.Label(main_frame, text="Temperature", font=("Helvetica", 18, "bold"), 
                       bg=card_color, fg=text_color)
title_label.pack(pady=(10, 5))

subtitle_label = tk.Label(main_frame, text="Converter", font=("Helvetica", 14), 
                          bg=card_color, fg=accent_color)
subtitle_label.pack(pady=(0, 20))


entry_temp = tk.Entry(main_frame, font=("Helvetica", 14), justify="center", 
                      bd=0, bg=entry_bg, fg="white", insertbackground="white")
entry_temp.pack(pady=10, ipady=10, fill="x")
entry_temp.insert(0, "0") 


units = ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"]
combo_from = tk.StringVar(value="Celsius (°C)")
option_menu = tk.OptionMenu(main_frame, combo_from, *units)
option_menu.config(font=("Helvetica", 10), bg=entry_bg, fg=text_color, 
                   bd=0, activebackground=accent_color, activeforeground="white", 
                   highlightthickness=0)
option_menu["menu"].config(bg=card_color, fg=text_color)
option_menu.pack(pady=10, fill="x")


convert_btn = tk.Button(main_frame, text="Convert Now", font=("Helvetica", 12, "bold"),
                        bg=btn_color, fg="#1a1b26", bd=0, pady=10, cursor="hand2",
                        activebackground="#ff9e64", activeforeground="white",
                        command=convert_temperature)
convert_btn.pack(pady=25, fill="x")


results_frame = tk.Frame(main_frame, bg=card_color)
results_frame.pack(fill="x", pady=10)


lbl_style = {"bg": card_color, "fg": text_color, "font": ("Helvetica", 10)}
val_style = {"bg": card_color, "fg": accent_color, "font": ("Helvetica", 14, "bold")}


tk.Label(results_frame, text="Celsius:", **lbl_style).grid(row=0, column=0, sticky="w")
result_c = tk.Label(results_frame, text="---", **val_style)
result_c.grid(row=0, column=1, sticky="e")


tk.Label(results_frame, text="Fahrenheit:", **lbl_style).grid(row=1, column=0, sticky="w")
result_f = tk.Label(results_frame, text="32.00 °F", **val_style) # Default example
result_f.grid(row=1, column=1, sticky="e")


tk.Label(results_frame, text="Kelvin:", **lbl_style).grid(row=2, column=0, sticky="w")
result_k = tk.Label(results_frame, text="273.15 K", **val_style) # Default example
result_k.grid(row=2, column=1, sticky="e")

results_frame.columnconfigure(0, weight=1)
results_frame.columnconfigure(1, weight=1)

root.mainloop()
ui.run()