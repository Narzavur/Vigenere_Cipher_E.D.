import os
import sys
import subprocess

# If run directly on Windows with python.exe, relaunch with pythonw.exe so double-clicking 
# opens the GUI without a console window
if __name__ == "__main__" and sys.platform == "win32":
    if sys.executable.endswith("python.exe"):
        pyw = sys.executable.replace("python.exe", "pythonw.exe")
        if os.path.exists(pyw):
            subprocess.Popen([pyw, sys.argv[0]] + sys.argv[1:])
            sys.exit(0)

import tkinter as tk
from tkinter import messagebox, filedialog, font
import webbrowser

def key_to_shifts(key: str):
    if not key:
        raise ValueError("Keyword is empty")
    shifts = []
    for ch in key:
        if ch.isalpha():
            shifts.append(ord(ch.lower()) - ord('a'))
        else:
            raise ValueError("Keyword must contain only letters A-Z")
    return shifts

def vigenere_encrypt(plain: str, key: str) -> str:
    shifts = key_to_shifts(key)
    out = []
    k = 0
    for ch in plain:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = shifts[k % len(shifts)]
            out.append(chr((ord(ch) - base + shift) % 26 + base))
            k += 1
        else:
            out.append(ch)
    return ''.join(out)

def vigenere_decrypt(cipher: str, key: str) -> str:
    shifts = key_to_shifts(key)
    out = []
    k = 0
    for ch in cipher:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = shifts[k % len(shifts)]
            out.append(chr((ord(ch) - base - shift) % 26 + base))
            k += 1
        else:
            out.append(ch)
    return ''.join(out)

# ---------------- UI SETTINGS ----------------
# Black background, darkish-gray typing areas for better contrast
BG = "#000000"      # black background
PANEL = "#2b2b2b"   # darkish gray for text panels
FIELD = "#2b2b2b"   # darkish gray for entry fields
FG = "#FFFFFF"      # white foreground / text
# Buttons: slightly lighter black than the background so they are distinguishable
ACCENT = "#1a1a1a"  # slightly lighter black for buttons
BTN_ACTIVE = "#0a0a0a"  # active -> a bit darker when pressed
ERROR_BG = BG

# Fonts & scaling for crisper text
base_font = ("Segoe UI", 11)
label_font = ("Segoe UI Semibold", 11)
mono_font = ("Consolas", 12)

# Configure some default named fonts to improve consistency
try:
    font.nametofont("TkDefaultFont").configure(family=base_font[0], size=base_font[1])
    font.nametofont("TkTextFont").configure(family=mono_font[0], size=mono_font[1])
except Exception:
    pass

root = tk.Tk()
root.title("Vigenère Cipher")
root.geometry("760x500")
root.resizable(True, True)
root.configure(bg=BG)

# Create frames for different pages
welcome_frame = tk.Frame(root, bg=BG)
main_frame = tk.Frame(root, bg=BG)

# ================ WELCOME PAGE ================
def create_welcome_page():
    """Create and display the welcome page"""
    # Clear the welcome frame
    for widget in welcome_frame.winfo_children():
        widget.destroy()
    
    # Title
    title = tk.Label(welcome_frame, text="Vigenère Cipher", 
                     bg=BG, fg=FG, font=("Segoe UI", 28, "bold"))
    title.pack(pady=(40, 20))
    
    # Summary text with scrolling
    summary_text = """The Vigenère Cipher is a method of encrypting
text using a keyword to shift letters.
Unlike the Caesar cipher which uses a fixed shift,
the Vigenère cipher uses a repeating keyword
to shift each letter by a different amount.

Each letter is assigned a numerical value.
The keyword repeats to match the plaintext length,
and each letter is shifted by the corresponding
numerical value from the keyword. The resulting
ciphertext retains the original case, and
non-alphabetic characters are not modified.

Learn more about the Vigenère Cipher →"""
    
    # Create scrollable text frame
    text_frame = tk.Frame(welcome_frame, bg="#000000" )
    text_frame.pack(pady=(0, 20), padx=20, fill="both", expand=True)
    
    # Create scrollbar
    scrollbar = tk.Scrollbar(text_frame, bg="#000000" , troughcolor="#000000" , highlightthickness=0, highlightcolor="#000000" )
    scrollbar.pack(side="right", fill="y")
    
    summary = tk.Text(text_frame, height=10, width=65, wrap="word",
                      bg="#000000" , fg=FG, font=("Segoe UI", 11),
                      relief="flat", bd=0, highlightthickness=0,
                      yscrollcommand=scrollbar.set)
    summary.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=summary.yview)
    
    summary.insert("1.0", summary_text)
    
    # Configure text alignment to center
    summary.tag_configure("center", justify="center")
    summary.tag_add("center", "1.0", "end")
    
    # Configure link tag
    summary.tag_configure("link", foreground="#64B5F6", underline=True)
    
    # Apply link tag to the "Learn more" text
    link_text = "Learn more about the Vigenère Cipher →"
    start_idx = summary.search(link_text, "1.0")
    if start_idx:
        end_idx = f"{start_idx}+{len(link_text)}c"
        summary.tag_add("link", start_idx, end_idx)
    
    def on_link_enter(event):
        summary.config(cursor="hand2")
        summary.tag_config("link", foreground="#90CAF9")
    
    def on_link_leave(event):
        summary.config(cursor="")
        summary.tag_config("link", foreground="#64B5F6")
    
    def on_link_click(event):
        webbrowser.open("https://en.wikipedia.org/wiki/Vigenère_cipher")
    
    summary.tag_bind("link", "<Enter>", on_link_enter)
    summary.tag_bind("link", "<Leave>", on_link_leave)
    summary.tag_bind("link", "<Button-1>", on_link_click)
    
    summary.config(state="disabled")  # Make read-only
    
    # Start button
    start_btn = tk.Button(welcome_frame, text="Start", 
                          command=transition_to_main,
                          bg=ACCENT, fg=FG,
                          activebackground=BTN_ACTIVE, activeforeground=FG,
                          bd=0, relief="flat", padx=40, pady=12,
                          font=("Segoe UI", 12))
    start_btn.pack(pady=(20, 40))
    
    welcome_frame.pack(fill="both", expand=True)

def transition_to_main():
    """Transition from welcome page to main UI"""
    welcome_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

# ================ MAIN UI ================
frm_top = tk.Frame(main_frame, bg=BG)
frm_top.pack(padx=10, pady=8, anchor="w", fill="x")

# Create a frame for keyword and how to use
keyword_frame = tk.Frame(frm_top, bg=BG)
keyword_frame.pack(side="left")

lbl_key = tk.Label(keyword_frame, text="Keyword:", bg=BG, fg=FG, font=label_font)
lbl_key.grid(row=0, column=0, sticky="w")
entry_key = tk.Entry(keyword_frame, width=30, bg=FIELD, fg=FG, insertbackground=FG, font=base_font,
                     relief="solid", bd=1)
entry_key.grid(row=0, column=1, padx=(6, 12))
entry_key.focus_set()

# Add "How to use" text on the right side
frm_help = tk.Frame(frm_top, bg=BG)
frm_help.pack(side="right", padx=(20, 0))

lbl_how_to_use = tk.Label(frm_help, text="How to use", bg=BG, fg="#64B5F6", 
                           font=("Segoe UI", 10, "underline"), cursor="hand2")
lbl_how_to_use.pack()

def open_how_to_use_popup():
    """Create and display the how to use popup overlay with fade-in effect"""
    # Create overlay frame
    overlay = tk.Frame(root, bg="#000000", relief="solid", bd=1, highlightthickness=2, highlightcolor="#666666")
    overlay.place(relx=0.5, rely=0.5, anchor="center", width=480, height=280)
    
    # Bring overlay to front
    overlay.lift()
    
    # Create top frame for close button
    top_frame = tk.Frame(overlay, bg="#4a4a4a")
    top_frame.pack(fill="x", padx=15, pady=(12, 8))
    
    # Title label
    title_label = tk.Label(top_frame, text="How to Use", bg="#4a4a4a", fg=FG, 
                           font=("Segoe UI", 12, "bold"))
    title_label.pack(side="left")
    
    # Close button (X) on the right
    def close_popup():
        overlay.destroy()
    
    close_btn = tk.Label(top_frame, text="✕", bg="#4a4a4a", fg=FG, 
                         font=("Segoe UI", 14, "bold"), cursor="hand2", padx=2)
    close_btn.pack(side="right")
    close_btn.bind("<Button-1>", lambda e: close_popup())
    close_btn.bind("<Enter>", lambda e: close_btn.config(fg="#FF5252"))
    close_btn.bind("<Leave>", lambda e: close_btn.config(fg=FG))
    
    # Content frame
    content_frame = tk.Frame(overlay, bg="#4a4a4a")
    content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 12))
    
    instructions_text = tk.Text(content_frame, wrap="word", bg="#3a3a3a", fg=FG,
                                font=("Segoe UI", 9), relief="flat", bd=0,
                                highlightthickness=0)
    instructions_text.pack(fill="both", expand=True)
    
    instructions = """First, enter your chosen keyword into the keyword field. Then, in the input field, enter the sentence you would like to encrypt. Then press the encrypt button to get your encrypted text. To decrypt, put the keyword in the keyword field and the encrypted text in the input field, then press decrypt to get the original message. To maximise user comfort, I have added a swap fields button to switch quickly between the two."""
    
    instructions_text.insert("1.0", instructions)
    instructions_text.config(state="disabled")  # Make read-only
    
    # Fade-in effect
    overlay.attributes('alpha', 0) if hasattr(overlay, 'attributes') else None
    
    # Simple fade-in by adjusting opacity (works for the frame)
    alpha = 0
    def fade_in():
        nonlocal alpha
        if alpha < 1:
            alpha += 0.15
            overlay.after(30, fade_in)
    
    fade_in()

lbl_how_to_use.bind("<Button-1>", lambda e: open_how_to_use_popup())
lbl_how_to_use.bind("<Enter>", lambda e: lbl_how_to_use.config(fg="#90CAF9"))
lbl_how_to_use.bind("<Leave>", lambda e: lbl_how_to_use.config(fg="#64B5F6"))

def show_error(msg):
    messagebox.showerror("Error", msg)

# Core operations
def do_encrypt():
    key = entry_key.get().strip()
    text = txt_input.get("1.0", "end-1c")
    try:
        res = vigenere_encrypt(text, key)
    except ValueError as e:
        show_error(str(e))
        return
    txt_output.delete("1.0", "end")
    txt_output.insert("1.0", res)

def do_decrypt():
    key = entry_key.get().strip()
    text = txt_input.get("1.0", "end-1c")
    try:
        res = vigenere_decrypt(text, key)
    except ValueError as e:
        show_error(str(e))
        return
    txt_output.delete("1.0", "end")
    txt_output.insert("1.0", res)

def do_clear():
    entry_key.delete(0, "end")
    txt_input.delete("1.0", "end")
    txt_output.delete("1.0", "end")

def copy_output():
    out = txt_output.get("1.0", "end-1c")
    root.clipboard_clear()
    root.clipboard_append(out)
    messagebox.showinfo("Copied", "Output copied to clipboard.")

def save_output():
    out = txt_output.get("1.0", "end-1c")
    if not out:
        show_error("No output to save.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text files","*.txt"), ("All files","*.*")])
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        messagebox.showinfo("Saved", f"Output saved to:\n{path}")

def swap_fields():
    # Move output into input to speed up subsequent decrypt/encrypt cycles.
    out = txt_output.get("1.0", "end-1c")
    if not out:
        show_error("No output to swap into input.")
        return
    txt_input.delete("1.0", "end")
    txt_input.insert("1.0", out)
    txt_output.delete("1.0", "end")
    entry_key.focus_set()
    txt_input.focus_set()

# Buttons
btn_frame = tk.Frame(main_frame, bg=BG)
btn_frame.pack(padx=10, pady=(0,8), anchor="w")

def make_button(text, cmd):
    # smaller buttons: smaller padding and slightly smaller font
    btn_font = ("Segoe UI", 9)
    return tk.Button(btn_frame, text=text, command=cmd,
                     bg=ACCENT, fg=FG,
                     activebackground=BTN_ACTIVE, activeforeground=FG,
                     bd=0, relief="flat", padx=8, pady=4, font=btn_font)

btn_encrypt = make_button("Encrypt →", do_encrypt)
btn_encrypt.grid(row=0, column=0, padx=6)
btn_decrypt = make_button("← Decrypt", do_decrypt)
btn_decrypt.grid(row=0, column=1, padx=6)
btn_swap = make_button("Swap Fields", swap_fields)
btn_swap.grid(row=0, column=2, padx=6)
btn_copy = make_button("Copy Output", copy_output)
btn_copy.grid(row=0, column=3, padx=6)
btn_save = make_button("Save Output", save_output)
btn_save.grid(row=0, column=4, padx=6)
btn_clear = make_button("Clear All", do_clear)
btn_clear.grid(row=0, column=5, padx=6)

# Text areas
txt_frame = tk.Frame(main_frame, bg=BG)
txt_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))

# Configure grid to make text areas resizable
txt_frame.grid_rowconfigure(1, weight=1)
txt_frame.grid_columnconfigure(0, weight=1)
txt_frame.grid_columnconfigure(1, weight=1)

lbl_in = tk.Label(txt_frame, text="Input (plain text or cipher text):", bg=BG, fg=FG, font=label_font)
lbl_in.grid(row=0, column=0, sticky="w")
lbl_out = tk.Label(txt_frame, text="Output:", bg=BG, fg=FG, font=label_font)
lbl_out.grid(row=0, column=1, sticky="w", padx=(12,0))

txt_input = tk.Text(txt_frame, wrap="word", bg=PANEL, fg=FG,
                    insertbackground=FG, font=mono_font, relief="solid", bd=1, highlightthickness=0)
txt_input.grid(row=1, column=0, padx=(0,8), pady=6, sticky="nsew")
txt_output = tk.Text(txt_frame, wrap="word", bg=PANEL, fg=FG,
                     insertbackground=FG, font=mono_font, relief="solid", bd=1, highlightthickness=0)
txt_output.grid(row=1, column=1, padx=(8,0), pady=6, sticky="nsew")

# Selection appearance for better visibility (darkish-gray fields)
txt_input.configure(selectbackground="#FFFFFF", selectforeground=BG)
txt_output.configure(selectbackground="#FFFFFF", selectforeground=BG)

# Keyboard shortcuts
root.bind_all("<Control-e>", lambda e: do_encrypt())
root.bind_all("<Control-d>", lambda e: do_decrypt())
root.bind_all("<Control-c>", lambda e: copy_output())
root.bind_all("<Control-Shift-s>", lambda e: swap_fields())

# Initialize and start the application
create_welcome_page()
root.mainloop()