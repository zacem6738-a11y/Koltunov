import os
import random 
import tkinter as tk
from tkinter import ttk, messagebox

from models import (all_users, find_user, user_by_login, login_exist,
                    add_user, update_user, delete_user,
                    unlock_user, register_fail, reset_attempts)

CURRENT_USER= None
CURRENT_EDIT= None
ENTRY_LOGIN=None

BG="#f9f1e5"
FIELD_BG="#ffffff"
FIELD_FG="#22262b"

FONT_TITLE=("Arial",16,"bold")
FONT_LABEL=("Arial",11,"bold")
FONT_BUTTON=("Arial",12,"bold")

root= tk.Tk()
root.tittle("Учебное приложение")
root.geometry("720x640")
root.configure(bg=BG)

container= tk.Frame(root, bg=BG)
container.pack(fill="both",expand=True,padx=20,pady=20)

def clear_screen():
    for w in container.winfo_children():
        w.destroy()

def make_title(text):
    return tk.Label(container, text=text, bg=BG, fg=FIELD_FG, font=FONT_TITLE)

def make_label(text):
   return tk.Label(container, text=text, bg=BG, fg=FIELD_FG,
                   font=FONT_LABEL, anchor="w")

def make_entry(password=False):
    entry= tk.Entry(container, font=FONT_BUTTON, bg=FIELD_BG, fg=FIELD_FG,
                    insertbackground=FIELD_FG, relief="solid", borderwidth=1)
    if password:
        entry.configure(show="*")
    return entry

def make_button(text, command, parent=None):
    host= container if parent is None else parent
    return tk.Button(host,text=text, command=command, font=FONT_BUTTON)

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
CAPTCHA_DIR=os.path.join(BASE_DIR,"captcha")
CORRECT_ORDER=[1, 2, 3, 4]
PIECE_SIZE=90

captcha_images={}
captcha_empty=None
captcha_host=None
captcha_slots=[]
captcha_piece_buttons={}
captcha_placed=[]
captcha_shuffled=[]
captcha_passed= False
capthca_fails=0

def load_captcha_images():
    global captcha_images, captcha_empty
    captcha_images={}
    for piece in(1, 2, 3, 4):
        path=os.path.join(CAPTCHA_DIR,"piece_"+str(piece)+".png")
        captcha_images[piece]=tk.PhotoImage(file=path).subsample(8)
    captcha_empty= tk.PhotoImage(width=PIECE_SIZE, height=PIECE_SIZE)

def build_captcha(host):
    global captcha_slots, captcha_piece_buttons, captcha_placed, captcha_shuffled
    for w in host.winfo_children():
        w.destroy()
    captca_slots=[]
    captcha_piece_buttons={}
    captcha_placed=[]
    captcha_shuffled= CORRECT_ORDER[:]
    random.shuffle(captcha_shuffled)
    while captcha_shuffled == CORRECT_ORDER:
        random.shuffle(captcha_shuffled)
    tk.Label(host, text="Соберите картинку: кликайте фрагменты по порядку",
             bg=BG, fg=FIELD_FG, font=FONT_LABEL, anchor="w").pack(fill="x")
    board= tk.Frame(host, bg=BG)
    board.pack(pady=(6, 6))
    for index in range(4):
        slot=tk.Label(board, image=captcha_empty,
                      bg=FIELD_BG,relief="solid",borderwidth=1)
        slot.grid(row=index // 2, column=index % 2)
        captcha_slots.append(slot)
    pieces= tk.Frame(host,bg=BG)
    pieces.pack(pady=(0, 6))
    for piece in captcha_shuffled:
        btn= tk.Button(pieces, image=captcha_images[piece],
                       relief="solid", borderwidth=1, cursor="hand2",
                       command=lambda p=piece: place_piece(p))
        btn.pack(side="left", padx=3)
        captcha_piece_buttons[piece] =btn
    make_button("Сбросить капчу", new_captcha_round,
                parent=host).pack(ipadx=16, ipady=3)
    
def new_captcha_round():
    global captcha_passed
    captcha_passed= False
    build_captcha(captcha_host)

def place_piece(piece):
    if captcha_passed or len(captcha_placed)>=4:
        return
    captcha_placed.append(piece)
    captcha_piece_buttons[piece].configure(state="disabled")
    captcha_slots[len(captcha_placed)-1].configure(image=captcha_images[piece])
    if len(captcha_placed) ==4:
        check_captcha()

def check_captcha():
    global captcha_passed, capthca_fails
    login=ENTRY_LOGIN.get().strip()
    if captcha_placed == CORRECT_ORDER:
        captcha_passed= True
        messagebox.showinfo("Капча",
                            "Пазл собран верно. Теперь можно нажимать <<Войти>>.")
        return
    if login_exist(login):
        became_locked =register_fail(login)
        if became_locked:
            messagebox.showerror("Блокировка"
                             "Вы заблокированы.Обратитесь к администратору")
        else:
            messagebox.showerror("Капча",
                             "Пазл собран неверно.Попробуйте сбрать еще раз,"
                             "ореинтируясь на продолжение рисунка.")
    else:
        capthca_fails=capthca_fails+1
        if capthca_fails >= 3:
            messagebox.showerror("Блокировка",
                                 "Третья неверная сборка капчи подряд."
                                 "При входе учётная запись будет заблокирована.")
        else:
            messagebox.showerror("Капча,"
                                 "Пазл собран неверно.Попробуйте собрать еще раз")
    new_captcha_round()

def try_login(login, password):
    global CURRENT_USER,capthca_fails
    login=login.strip()
    if not login or not password:
        messagebox.showwarning("Внимание","Заполните логин и пароль.")
        return
    if capthca_fails > 0: