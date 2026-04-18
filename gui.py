from tkinter import *
from tkinter import ttk, messagebox
import pydirectinput, pyautogui
import threading, os
import win32gui
import cv2
from pynput import keyboard
from vision import Vision
from ekranyakala import ekranYakala
from time import sleep

# 🎨 TEMA RENKLERİ
BG = "#0b0b0b"
PANEL = "#141414"
ACCENT = "#8b0000"
TEXT = "#e0e0e0"
GREEN = "#00c853"
BLUE = "#2979ff"

class Window(Frame):
    def __init__(self, master=None, saniye=0):
        Frame.__init__(self, master)
        self.master = master
        self.saniye = saniye
        

        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # 🖼️ ARKA PLAN (opsiyonel)
        try:
            self.bg_img = PhotoImage(file=os.path.join(self.base_dir, "ui_bg.png"))
            bg_label = Label(self.master, image=self.bg_img)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            self.master.configure(bg=BG)

        # ===== AYARLAR PANEL =====
        F3 = Frame(self.master, bg=PANEL, bd=2, relief="ridge")
        F3.place(x=20, y=30, width=200, height=170)

        Label(F3, text="AYARLAR", fg="red", bg=PANEL,
              font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=5)

        self.ara = Button(F3, text="Ara",
            bg=ACCENT, fg="white",
            bd=0, cursor="hand2",
            command=self.ara)
        self.ara.pack(padx=10, pady=5, anchor="e")

        v1 = StringVar()

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TCombobox",
            fieldbackground=PANEL,
            background=PANEL,
            foreground=TEXT)

        self.windowName = ttk.Combobox(F3,
            width=15, textvariable=v1, state="readonly")
        self.windowName.pack(padx=10)

        Label(F3, text="Kesme Süresi",
              fg=TEXT, bg=PANEL).pack(anchor="w", padx=10)

        self.kesimsuresi = Spinbox(F3,
            from_=3, to=999,
            width=5,
            bg=PANEL,
            fg=TEXT,
            buttonbackground=ACCENT)
        self.kesimsuresi.pack(anchor="w", padx=10)

        self.var1 = IntVar(value=0)

        self.kilitle = Checkbutton(F3,
            text="Kilitle",
            fg=TEXT,
            bg=PANEL,
            selectcolor=BG,
            command=self.userKilit,
            variable=self.var1)
        self.kilitle.pack(anchor="w", padx=10)

        # ===== DURUM PANEL =====
        F2 = Frame(self.master, bg=PANEL, bd=2, relief="ridge")
        F2.place(x=230, y=30, width=160, height=120)

        Label(F2, text="DURUM", fg="red", bg=PANEL,
              font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=5)

        self.metinSayisi = 0

        self.durum = Label(F2, text="Pasif",
                           font=("Segoe UI", 11, "bold"),
                           fg="red", bg=PANEL)
        self.durum.pack(anchor="w", padx=10)

        self.bulunanMetin = Label(F2,
            text="Bulunan Metin: 0",
            fg=BLUE, bg=PANEL)
        self.bulunanMetin.pack(anchor="w", padx=10)

        self.zaman = Label(F2,
            text="Geçen Zaman: 00:00:00",
            fg=GREEN, bg=PANEL)
        self.zaman.pack(anchor="w", padx=10)

        # ===== BUTONLAR =====
        self.start = Button(self.master,
            text="BAŞLA",
            command=self.thread,
            bg=ACCENT,
            fg="white",
            activebackground="#b71c1c",
            font=("Segoe UI", 11, "bold"),
            bd=0,
            cursor="hand2",
            width=15)
        self.start.place(x=250, y=160)

        self.stop = Button(self.master,
            text="DURDUR",
            command=self.durdur,
            bg="#263238",
            fg=GREEN,
            activebackground="#37474f",
            font=("Segoe UI", 11, "bold"),
            bd=0,
            cursor="hand2",
            width=15)
        self.stop.place(x=250, y=200)

        # 🔥 HOVER EFEKT
        def hover_on(e):
            e.widget['bg'] = "#c62828"

        def hover_off(e):
            e.widget['bg'] = ACCENT

        self.start.bind("<Enter>", hover_on)
        self.start.bind("<Leave>", hover_off)

    # ===== FONKSİYONLAR (DEĞİŞMEDİ) =====

    def ara(self):
        liste = []
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title != "":
                    liste.append(title)
        win32gui.EnumWindows(winEnumHandler, None)
        self.windowName.config(values=liste)

    def userKilit(self):
        if self.var1.get() == 1:
            self.kesimsuresi.config(state="disabled")
            self.windowName.config(state="disabled")
            self.ara.config(state="disabled")
        else:
            self.kesimsuresi.config(state="normal")
            self.windowName.config(state="readonly")
            self.ara.config(state="normal")

    def zamanlayici(self):
        if self.sureBaslat:
            self.saniye += 1
            seconds = self.saniye % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            self.master.after(1000, self.zamanlayici)
            self.zaman.configure(
                text="Geçen Zaman: %02d:%02d:%02d" % (hour, minutes, seconds))

    def thread(self):
        threading.Thread(target=self.basla).start()

    def basla(self):
        try:
            if self.windowName.get() == "":
                messagebox.showwarning("Hata","Başlamadan Önce Oyun Ekranını Seç")
                return

            try:
                wincap = ekranYakala(self.windowName.get())
            except Exception as e:
                messagebox.showerror("Hata", f"Pencere bulunamadı\n{e}")
                return

            cascade_path = os.path.join(self.base_dir, "cascade", "cascade.xml")
            self.cascade = cv2.CascadeClassifier(cascade_path)

            if self.cascade.empty():
                messagebox.showerror("Hata", "cascade.xml yüklenemedi!")
                return

            self.vision = Vision(None)
            self.metine_vur = False
            self.s = 1
            self.saniye = 0

            self.start.config(state=DISABLED)
            self.kilitle.config(state="disabled")

            self.sureBaslat = True
            self.zamanlayici()
            self.durum["text"] = "Aktif"

            threading.Thread(
                target=self.saldir,
                args=(int(self.kesimsuresi.get()), wincap)
            ).start()

        except Exception as e:
            print("Hata:", e)

    def durdur(self):
        self.sureBaslat = False
        self.durum["text"] = "Pasif"
        self.start.config(state=NORMAL)
        self.kilitle.config(state="normal")

    def dur(self, key):
        if key == keyboard.Key.f11:
            self.durdur()
            return False

    def saldir(self, saniye, wincap):
        try:
            with keyboard.Listener(on_press=self.dur) as dur:
                while dur.running:
                    ss = wincap.get_screenshot()
                    gray = cv2.cvtColor(ss, cv2.COLOR_BGR2GRAY)
                    rectangles = self.cascade.detectMultiScale(gray, 1.1, 5)

                    if not self.metine_vur:
                        self.metine_vur = True
                        threading.Thread(
                            target=self.metinevur,
                            args=(rectangles, saniye, wincap)
                        ).start()

        except Exception as e:
            self.durdur()
            print("saldir hatası:", e)

    def metinevur(self,rectangles, metinKesmeSuresi, wincap):
        if len(rectangles) > 0:
            targets = self.vision.get_click_points(rectangles)
            target = wincap.get_screen_position(targets[0])

            pyautogui.moveTo(x=target[0], y=target[1]+5)
            pyautogui.click()

            self.bulunanMetin["text"] = f"Bulunan Metin: {self.s}"

            sleep(metinKesmeSuresi)
            self.s += 1
        else:
            pydirectinput.press("e", presses=6)
            pydirectinput.press("f", presses=6)

        self.metine_vur = False


# ===== ÇALIŞTIR =====
root = Tk()
root.title("Metin2 Farm Bot")
root.geometry("420x260")
root.resizable(False, False)

app = Window(root)
root.mainloop()
