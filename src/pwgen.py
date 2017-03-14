'''
Created on May 24, 2016

@author: jon
'''

import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import random
from tkinter.constants import DISABLED

import dialog


title = "Secure Password & Keyfile Generator"
ascii_min = 33
ascii_max = 126
divide_text = "- -  - -  - -  - -  - -  - -  - -  - -"
def_pw_length = 20




def new_pw():
    pw = ""
    while len(pw) < pw_length.get():
        i = random.SystemRandom().randint(ascii_min, ascii_max)
        s = str(chr(i))
        if is_allowed_byte(i):
            pw += s
        
    return pw

def is_allowed_byte(byte):
    if byte >= 48 and byte <= 57:
        return digits_check.get()
    elif byte >= 65 and byte <= 90:
        return uppercase_check.get()
    elif byte >= 97 and byte <= 122:
        return lowercase_check.get()
    elif byte >= ascii_min and byte <= ascii_max:
        return special_check.get()
    else:
        return 0


def key_file_gen():
    file_size_mb = float(key_file_size.get())
    file_size_bytes = int(file_size_mb * 1024 * 1024)

    try:
        path = filedialog.askopenfile(mode='r', initialdir="~").name
        
    except:
        return
        
    if path == "":
        return

    file = open(path, 'w')
    
    key_file_button["state"] = DISABLED
    
    time_start = time.time()
    
    for i in range(file_size_bytes):
        file.write(chr(random.SystemRandom().randint(ascii_min, ascii_max)))
        
    time_end = time.time()
    total_time = time_end - time_start
            
    key_file_button["state"] = "active"
    
    message = "Created keyfile at: %s" % path
    message += "\n"
    message += "size: %f mb, %d bytes" % (file_size_mb, file_size_bytes)
    message += "\n"
    message += "total time: %f seconds" % float(total_time)
    dialog.Dialog(frame, message)
    
    

def signal_handler(signum, frame):
    raise Exception("Reached timeout")

def clear_clipboard():
#     signal.signal(signal.SIGALRM, signal_handler)
#     signal.alarm(0.5)
    
    try:
        import os
        if os.name == 'nt':
            from ctypes import windll
            if windll.user32.OpenClipboard(None):
                windll.user32.EmptyClipboard()
                windll.user32.CloseClipboard()    
        elif os.name == 'posix':
            os.system("xsel -bc")
            #
            #    use subprocess module
            #
            
    except:
        None
    
    
    
def copy_to_clip():
    frame.clipboard_clear()
    frame.clipboard_append(password["text"])
    
    
def create_pwgen():
    
    clip = tk.Button(frame, text="copy to clip", command=copy_to_clip)
    clip.grid(row=0, column=0)
    
    refresh = tk.Button(frame, text="refresh", command=regen)
    refresh.grid(row=0, column=1)
    
    clear = tk.Button(frame, text="clear clipboard", command=clear_clipboard)
    clear.grid(row=0, column=2)
    
    global password 
    password = tk.Label(frame)
    password.grid(row=1, column=0, columnspan=2)
    
    global pw_length
    pw_length = tk.IntVar(frame)
    pw_selector = tk.Spinbox(frame, from_=1, to=64, textvariable=pw_length)
    pw_length.set(def_pw_length)
    pw_selector.grid(row=1, column=2, columnspan=2)
    
    global digits_check
    digits_check = tk.IntVar(frame)
    digits = tk.Checkbutton(frame, text="digits", variable=digits_check)
    digits_check.set(1)
    digits.grid(row=2, column=0)
    
    global lowercase_check
    lowercase_check = tk.IntVar(frame)
    lowercase = tk.Checkbutton(frame, text="lowercase", variable=lowercase_check)
    lowercase_check.set(1)
    lowercase.grid(row=2, column=1)

    global uppercase_check
    uppercase_check = tk.IntVar(frame)
    uppercase = tk.Checkbutton(frame, text="uppercase", variable=uppercase_check)
    uppercase_check.set(1)
    uppercase.grid(row=2, column=2)
    
    global special_check
    special_check = tk.IntVar(frame)
    special = tk.Checkbutton(frame, text="special", variable=special_check)
    special_check.set(1)
    special.grid(row=2, column=3)
    
    
    
    
def create_widgets():
    
    create_pwgen()
    
    divider = ttk.Label(frame, text=divide_text)
    divider.grid(row=3, column=0)
    
    tk.Label(frame, text="**keyfile generation will OVERWRITE an existing file**").grid(row=4, column=0)

    
    key_file_desc = tk.Label(frame, text="keyfile size (mb): expect 6 seconds per mb")
    key_file_desc.grid(row=5, column=0)
    
    
    global key_file_size
    key_file_size = tk.StringVar(frame)
    key_file = tk.Entry(frame, textvariable=key_file_size)
    key_file_size.set("0.5")
    key_file.grid(row=6, column=0)
    
    global key_file_button
    key_file_button = tk.Button(frame, text="generate keyfile", command=key_file_gen)
    key_file_button.grid(row=7, column=0)
    
def regen():
    password["text"] = new_pw()

def create_gui():
    global frame
    frame = tk.Tk()
    frame.wm_title(title)
    create_widgets()
    regen()
    frame.mainloop()



if __name__ == '__main__':
    create_gui()
    
    
    
    
    
    
    