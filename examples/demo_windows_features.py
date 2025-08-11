#!/usr/bin/env python3
"""
Simple visual demo for Windows features: DPI awareness and corner rounding.
Focus on visual appearance only - no debug prints or complex info.
"""

import tkinter as tk
import tkface
import sys

def main():
    root = tk.Tk()
    root.title("tkface Windows Features - Visual Demo")
    
    # Apply DPI scaling
    tkface.win.dpi(root)
    
    # Set window size
    root.geometry("600x520+100+100")
    
    # Disable corner rounding (Windows 11)
    if sys.platform.startswith("win"):
        tkface.win.unround(root)
    
    # Main container
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(expand=True, fill='both')
    
    # Header
    header = tk.Label(main_frame, text="tkface Windows Features Demo")
    header.pack(pady=(0, 20))
    
    # DPI Scaling Test Section
    dpi_frame = tk.LabelFrame(main_frame, text="DPI Scaling Test", 
                             font=('Arial', 12, 'bold'), padx=15, pady=15)
    dpi_frame.pack(fill='x', pady=(0, 15))
    
    # Test buttons with different padding
    button_frame = tk.Frame(dpi_frame)
    button_frame.pack()
    
    buttons = [
        ("Small", 5, 2, '#e74c3c'),
        ("Medium", 10, 5, '#3498db'),
        ("Large", 20, 10, '#2ecc71'),
    ]
    
    for text, padx, pady, color in buttons:
        container = tk.Frame(button_frame, bg=color, relief='solid', bd=2)
        container.pack(side='left', padx=padx, pady=pady)
        
        btn = tk.Button(container, text=f"{text}\nPadding", 
                       width=12, height=2, bg='white', relief='raised',
                       font=('Arial', 10))
        btn.pack(padx=2, pady=2)
    
    # Font Scaling Test Section
    font_frame = tk.LabelFrame(main_frame, text="Font Scaling Test", 
                              font=('Arial', 12, 'bold'), padx=15, pady=15)
    font_frame.pack(fill='x', pady=(0, 15))
    
    # Different font sizes
    sizes = [8, 12, 16, 20]
    for size in sizes:
        label = tk.Label(font_frame, text=f"Font Size {size}", 
                        font=('Arial', size))
        label.pack(side='left', padx=10)
    
    # Window Features Test Section
    features_frame = tk.LabelFrame(main_frame, text="Window Features", 
                                  font=('Arial', 12, 'bold'), padx=15, pady=15)
    features_frame.pack(fill='x')
    
    # Feature indicators
    features = [
        ("DPI Aware", "✓ Enabled" if hasattr(root, 'DPI_scaling') else "✗ Disabled"),
        ("Corner Rounding", "✓ Disabled" if sys.platform.startswith("win") else "N/A"),
        ("Scaling Factor", f"{getattr(root, 'DPI_scaling', 1.0):.2f}x"),
    ]
    
    for feature, status in features:
        feature_label = tk.Label(features_frame, text=f"{feature}: {status}", 
                                font=('Arial', 10))
        feature_label.pack(anchor='w', pady=2)
    
    root.mainloop()

if __name__ == "__main__":
    main()
