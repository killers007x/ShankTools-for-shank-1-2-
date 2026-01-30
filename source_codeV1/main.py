#!/usr/bin/env python3
"""
TEX to PNG Converter App
Converts Shank 2 TEX files to PNG images and vice versa
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading

from shank2_ktex_v4 import KTEXConverter


class TexConverterApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("TEX - PNG Converter")
        self.window.geometry("520x500")
        self.window.resizable(False, False)
        
        self.converter = KTEXConverter()
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title = tk.Label(
            self.window,
            text="Shank 2 TEX Converter",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=15)
        
        # Extract Frame (TEX to PNG)
        extract_frame = tk.LabelFrame(
            self.window,
            text="Extract (TEX to PNG)",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        extract_frame.pack(pady=10, padx=20, fill="x")
        
        btn_extract_single = tk.Button(
            extract_frame,
            text="Extract Single File",
            font=("Arial", 10),
            width=18,
            command=self.extract_single
        )
        btn_extract_single.pack(side="left", padx=10, pady=5)
        
        btn_extract_folder = tk.Button(
            extract_frame,
            text="Extract Entire Folder",
            font=("Arial", 10),
            width=18,
            command=self.extract_folder
        )
        btn_extract_folder.pack(side="right", padx=10, pady=5)
        
        # Rebuild Frame (PNG to TEX)
        rebuild_frame = tk.LabelFrame(
            self.window,
            text="Rebuild (PNG to TEX)",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        rebuild_frame.pack(pady=10, padx=20, fill="x")
        
        btn_rebuild_single = tk.Button(
            rebuild_frame,
            text="Rebuild Single File",
            font=("Arial", 10),
            width=18,
            command=self.rebuild_single
        )
        btn_rebuild_single.pack(side="left", padx=10, pady=5)
        
        btn_rebuild_folder = tk.Button(
            rebuild_frame,
            text="Rebuild Entire Folder",
            font=("Arial", 10),
            width=18,
            command=self.rebuild_folder
        )
        btn_rebuild_folder.pack(side="right", padx=10, pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.window,
            length=450,
            mode='determinate'
        )
        self.progress.pack(pady=15)
        
        # Status label
        self.status = tk.Label(
            self.window,
            text="Ready",
            font=("Arial", 10)
        )
        self.status.pack(pady=5)
        
        # Log text box
        self.log = tk.Text(
            self.window,
            height=10,
            width=58,
            font=("Consolas", 9)
        )
        self.log.pack(pady=10)
    
    def log_message(self, msg):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
    
    def reset_ui(self):
        self.log.delete(1.0, tk.END)
        self.progress['value'] = 0
        self.status.config(text="Processing...")
    
    # ==================== EXTRACT ====================
    
    def extract_single(self):
        file_path = filedialog.askopenfilename(
            title="Select TEX File",
            filetypes=[("TEX files", "*.tex"), ("All files", "*.*")]
        )
        
        if file_path:
            self.reset_ui()
            self.progress['value'] = 50
            
            try:
                result = self.converter.extract(Path(file_path))
                
                if result.success:
                    self.log_message(f"Success: {result.output_path.name}")
                    messagebox.showinfo("Success", "Extraction completed!")
                else:
                    self.log_message(f"Failed: {result.error}")
                    messagebox.showerror("Error", result.error)
            
            except Exception as e:
                self.log_message(f"Error: {e}")
                messagebox.showerror("Error", str(e))
            
            self.progress['value'] = 100
            self.status.config(text="Done")
    
    def extract_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder with TEX Files")
        
        if folder_path:
            folder = Path(folder_path)
            tex_files = list(folder.glob("*.tex"))
            
            if not tex_files:
                messagebox.showwarning("Warning", "No TEX files found in this folder!")
                return
            
            self.reset_ui()
            self.log_message(f"Found {len(tex_files)} TEX files")
            self.log_message("-" * 40)
            
            thread = threading.Thread(
                target=self.process_files,
                args=(tex_files, "extract")
            )
            thread.start()
    
    # ==================== REBUILD ====================
    
    def rebuild_single(self):
        file_path = filedialog.askopenfilename(
            title="Select PNG File",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if file_path:
            self.reset_ui()
            self.progress['value'] = 50
            
            try:
                result = self.converter.rebuild(Path(file_path))
                
                if result.success:
                    self.log_message(f"Success: {result.output_path.name}")
                    messagebox.showinfo("Success", "Rebuild completed!")
                else:
                    self.log_message(f"Failed: {result.error}")
                    messagebox.showerror("Error", result.error)
            
            except Exception as e:
                self.log_message(f"Error: {e}")
                messagebox.showerror("Error", str(e))
            
            self.progress['value'] = 100
            self.status.config(text="Done")
    
    def rebuild_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder with PNG Files")
        
        if folder_path:
            folder = Path(folder_path)
            png_files = list(folder.glob("*.png"))
            
            if not png_files:
                messagebox.showwarning("Warning", "No PNG files found in this folder!")
                return
            
            self.reset_ui()
            self.log_message(f"Found {len(png_files)} PNG files")
            self.log_message("-" * 40)
            
            thread = threading.Thread(
                target=self.process_files,
                args=(png_files, "rebuild")
            )
            thread.start()
    
    # ==================== PROCESS ====================
    
    def process_files(self, files, mode):
        total = len(files)
        success = 0
        
        for i, file in enumerate(files):
            try:
                if mode == "extract":
                    result = self.converter.extract(file)
                else:
                    result = self.converter.rebuild(file)
                
                if result.success:
                    self.log_message(f"OK: {file.name}")
                    success += 1
                else:
                    self.log_message(f"FAIL: {file.name}")
            
            except Exception as e:
                self.log_message(f"FAIL: {file.name}: {e}")
            
            progress = ((i + 1) / total) * 100
            self.progress['value'] = progress
            self.window.update_idletasks()
        
        self.log_message("-" * 40)
        self.log_message(f"Completed: {success}/{total}")
        self.status.config(text=f"Done ({success}/{total})")
        
        action = "Extracted" if mode == "extract" else "Rebuilt"
        messagebox.showinfo("Done", f"{action} {success} of {total} files")
    
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = TexConverterApp()
    app.run()