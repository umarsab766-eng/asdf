import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageDraw
import os
from datetime import datetime
import numpy as np
from tkinter import font

class ModernButton(tk.Button):
    def __init__(self, master, **kwargs):
        
        kwargs.setdefault('relief', 'flat')
        kwargs.setdefault('bd', 0)
        kwargs.setdefault('font', ('Arial', 10, 'bold'))
        kwargs.setdefault('cursor', 'hand2')
        
        super().__init__(master, **kwargs)
        
        
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
        self.bind('<ButtonRelease-1>', self.on_release)
        
        self.original_bg = self.cget('bg') if self.cget('bg') != '' else '#4a90e2'
        self.hover_bg = self.lighten_color(self.original_bg, 20)
        self.pressed_bg = self.darken_color(self.original_bg, 20)
        
        self.config(bg=self.original_bg, fg='white')
    
    def lighten_color(self, color, percent):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c + (255 - c) * percent / 100)) for c in rgb)
        return '#%02x%02x%02x' % rgb
    
    def darken_color(self, color, percent):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(max(0, int(c * (1 - percent / 100))) for c in rgb)
        return '#%02x%02x%02x' % rgb
    
    def on_enter(self, event):
        self.config(bg=self.hover_bg)
    
    def on_leave(self, event):
        self.config(bg=self.original_bg)
    
    def on_click(self, event):
        self.config(bg=self.pressed_bg)
    
    def on_release(self, event):
        self.config(bg=self.hover_bg)

class DigitalCameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Digital Camera - 3D Edition")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
       
        self.setup_styles()
        
        
        self.cap = cv2.VideoCapture(0)
        self.current_image = None
        self.captured_images = []
        
        
        self.create_widgets()
        

        self.update_preview()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        
        style.configure('Card.TFrame', 
                       background='#34495e',
                       relief='raised',
                       borderwidth=2)
        
        style.configure('Dark.TLabelframe',
                       background='#34495e',
                       foreground='white',
                       borderwidth=3,
                       relief='raised')
        
        style.configure('Dark.TLabelframe.Label',
                       background='#34495e',
                       foreground='white',
                       font=('Arial', 11, 'bold'))
        
        
        style.configure('Dark.TListbox',
                       background='#2c3e50',
                       foreground='white',
                       selectbackground='#4a90e2',
                       borderwidth=2,
                       relief='sunken')
    
    def create_widgets(self):

        title_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        title_frame.pack(fill='x', pady=10)
        
        title_label = tk.Label(title_frame, 
                               text="📸 3D Digital Camera",
                               font=('Arial', 24, 'bold'),
                               bg='#2c3e50',
                               fg='#ecf0f1')
        title_label.pack()
        
        
        shadow_label = tk.Label(title_frame,
                                text="📸 3D Digital Camera",
                                font=('Arial', 24, 'bold'),
                                bg='#2c3e50',
                                fg='#1a252f')
        shadow_label.place(x=3, y=3)
        
        
        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        
        left_panel = tk.Frame(main_container, bg='#2c3e50')
        left_panel.pack(side='left', fill='both', expand=True)
        
        preview_container = tk.Frame(left_panel, bg='#34495e', relief='raised', bd=3)
        preview_container.pack(pady=10, padx=10, fill='both', expand=True)
        

        self.preview_label = tk.Label(preview_container, 
                                     bg='black',
                                     relief='sunken',
                                     bd=3)
        self.preview_label.pack(padx=5, pady=5, fill='both', expand=True)
        
        
        btn_container = tk.Frame(left_panel, bg='#2c3e50')
        btn_container.pack(pady=10)
       
        self.capture_btn = ModernButton(btn_container, 
                                       text="📷 Capture",
                                       bg='#e74c3c',
                                       width=12,
                                       command=self.capture_image)
        self.capture_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.save_btn = ModernButton(btn_container,
                                    text="💾 Save",
                                    bg='#27ae60',
                                    width=12,
                                    command=self.save_image)
        self.save_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.exit_btn = ModernButton(btn_container,
                                    text="🚪 Exit",
                                    bg='#95a5a6',
                                    width=12,
                                    command=self.exit_app)
        self.exit_btn.grid(row=0, column=2, padx=5, pady=5)
        
        
        right_panel = tk.Frame(main_container, bg='#2c3e50', width=300)
        right_panel.pack(side='right', fill='y', padx=(10, 0))
        right_panel.pack_propagate(False)
        
    
        filter_frame = ttk.LabelFrame(right_panel, text="🎨 Filters", style='Dark.TLabelframe')
        filter_frame.pack(pady=10, fill='x', padx=5)
        
        
        gallery_frame = ttk.LabelFrame(right_panel, text="🖼️ Gallery", style='Dark.TLabelframe')
        gallery_frame.pack(pady=10, fill='both', expand=True, padx=5)
        
        gallery_container = tk.Frame(gallery_frame, bg='#34495e')
        gallery_container.pack(padx=5, pady=5, fill='both', expand=True)
        
        
        listbox_frame = tk.Frame(gallery_container, bg='#2c3e50', relief='sunken', bd=2)
        listbox_frame.pack(fill='both', expand=True)
        
        self.gallery_listbox = tk.Listbox(listbox_frame,
                                        bg='#2c3e50',
                                        fg='white',
                                        selectbackground='#4a90e2',
                                        selectforeground='white',
                                        font=('Arial', 10),
                                        bd=0,
                                        highlightthickness=0)
        self.gallery_listbox.pack(fill='both', expand=True)
        self.gallery_listbox.bind('<<ListboxSelect>>', self.show_gallery_image)
        
        
        scrollbar = ttk.Scrollbar(listbox_frame, command=self.gallery_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.gallery_listbox.config(yscrollcommand=scrollbar.set)
    
    def create_3d_scale(self, parent, label, from_, to, initial):
        frame = tk.Frame(parent, bg='#34495e')
        
        label_widget = tk.Label(frame, text=label, bg='#34495e', fg='white', font=('Arial', 10))
        label_widget.pack()
        
        scale = tk.Scale(frame,
                        from_=from_,
                        to=to,
                        resolution=0.1,
                        orient="horizontal",
                        bg="#345d87",
                        fg='white',
                        troughcolor='#2c3e50',
                        activebackground='#4a90e2',
                        highlightbackground='#34495e',
                        bd=0,
                        relief='flat')
        scale.set(initial)
        scale.pack(fill='x')
        return scale
    
    def update_preview(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            
            img = Image.fromarray(frame)
            
        
            img.thumbnail((600, 400), Image.Resampling.LANCZOS)
            
            img = ImageTk.PhotoImage(image=img)
            
            self.preview_label.configure(image=img)
            self.preview_label.image = img
            self.current_image = np.array(img)
        
        self.root.after(10, self.update_preview)
    
    def capture_image(self):
        if self.current_image is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"📸 capture_{timestamp}.png"
            self.captured_images.append((filename, self.current_image))
            self.gallery_listbox.insert(tk.END, filename)
            
            
            self.preview_label.config(relief='raised')
            self.root.after(100, lambda: self.preview_label.config(relief='sunken'))
            
            messagebox.showinfo("Success", f"Captured: {filename}")
    
    def save_image(self):
        if not self.captured_images:
            messagebox.showwarning("No Image", "Capture an image first!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if filename:
            last_image = self.captured_images[-1][1]
            
            if len(last_image.shape) == 3:
                img_array = cv2.cvtColor(last_image, cv2.COLOR_RGB2BGR)
            else:
                img_array = last_image
            cv2.imwrite(filename, img_array)
            messagebox.showinfo("Success", f"Saved: {filename}")
    
    def apply_filter(self, filter_type):
        if self.current_image is None:
            return
        
       
        print(self.current_image)
        print(type(self.current_image))
        if len(self.current_image.shape) == 2:
            img = Image.fromarray(self.current_image, mode='L')
        else:
            img = Image.fromarray(self.current_image)
        
        if filter_type == "grayscale":
            img = img.convert("L")
        elif filter_type == "sepia":
            img = img.convert("RGB")
            
            pixels = np.array(img)
            sepia_filter = np.array([
                [0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]
            ])
            sepia_img = pixels.dot(sepia_filter.T)
            sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
            img = Image.fromarray(sepia_img)
        elif filter_type == "blur":
            img = img.filter(ImageFilter.BLUR)
        

        self.current_image = np.array(img)
        
        img_tk = ImageTk.PhotoImage(image=img)
        self.preview_label.configure(image=img_tk)
        self.preview_label.image = img_tk

    def apply_adjustments(self):
        if self.current_image is None:
            return
            
        img = Image.fromarray(self.current_image)
        
        
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(self.brightness.get())
        
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(self.contrast.get())
        
        self.current_image = np.array(img)
        
        
        img_tk = ImageTk.PhotoImage(image=img)
        self.preview_label.configure(image=img_tk)
        self.preview_label.image = img_tk
    
    def show_gallery_image(self, event):
        selection = self.gallery_listbox.curselection()
        if selection:
            idx = selection[0]
            filename, img_array = self.captured_images[idx]
            
            
            top = tk.Toplevel(self.root)
            top.title(filename)
            top.configure(bg='#2c3e50')
            top.geometry("600x500")
            
            
            title = tk.Label(top, text=filename, 
                           font=('Arial', 14, 'bold'),
                           bg='#2c3e50', fg='white')
            title.pack(pady=10)
            
            
            img_frame = tk.Frame(top, bg='#34495e', relief='raised', bd=3)
            img_frame.pack(padx=20, pady=10, fill='both', expand=True)
            
            
            img = Image.fromarray(img_array)
            img.thumbnail((550, 400), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            
            label = tk.Label(img_frame, image=img_tk, bg='black', relief='sunken', bd=2)
            label.image = img_tk
            label.pack(padx=5, pady=5, fill='both', expand=True)
            
            
            ModernButton(top, text="Close", bg='#e74c3c', 
                        command=top.destroy).pack(pady=10)
    
    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.cap.release()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalCameraApp(root)
    root.mainloop()