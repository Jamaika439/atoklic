import pyautogui
import time
import threading
import keyboard
import tkinter as tk
from tkinter import ttk, messagebox
import random

class MouseAutoklicker:
    def __init__(self):
        self.clicking = False
        self.mouse_following = False
        self.click_delay = 0.1
        self.area_defined = False
        self.area_x1 = 0
        self.area_y1 = 0
        self.area_x2 = 0
        self.area_y2 = 0
        self.fixed_x = 0
        self.fixed_y = 0
        self.random_clicks = False
        self.enabled = True  # Ein/Aus Schalter
        
        # GUI erstellen
        self.root = tk.Tk()
        self.root.title("Mouse Autoklicker v2.0")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        self.create_gui()
        self.setup_hotkeys()
        
    def create_gui(self):
        # Haupttitel
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🖱️ Mouse Autoklicker", 
                              font=('Arial', 14, 'bold'), fg='white', bg='#2c3e50')
        title_label.place(relx=0.5, rely=0.5, anchor='center')
        
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Ein/Aus Schalter
        power_frame = tk.Frame(main_frame, bg='#ecf0f1')
        power_frame.pack(pady=10)
        
        self.power_var = tk.BooleanVar(value=True)
        power_check = tk.Checkbutton(power_frame, text="🔌 Autoklicker aktiviert", 
                                    variable=self.power_var, font=('Arial', 11, 'bold'),
                                    bg='#ecf0f1', fg='#27ae60', command=self.toggle_power)
        power_check.pack()
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Klick-Geschwindigkeit
        speed_frame = tk.LabelFrame(main_frame, text="⚡ Klick-Geschwindigkeit", 
                                   font=('Arial', 10, 'bold'), bg='#ecf0f1')
        speed_frame.pack(pady=10, fill='x')
        
        speed_inner = tk.Frame(speed_frame, bg='#ecf0f1')
        speed_inner.pack(pady=10)
        
        tk.Label(speed_inner, text="Intervall (Sekunden):", bg='#ecf0f1').pack()
        self.delay_var = tk.StringVar(value="0.1")
        delay_entry = tk.Entry(speed_inner, textvariable=self.delay_var, width=10, justify='center')
        delay_entry.pack(pady=5)
        
        tk.Button(speed_inner, text="✓ Aktualisieren", command=self.update_delay,
                 bg='#3498db', fg='white', font=('Arial', 9)).pack(pady=5)
        
        # Klick-Modi
        mode_frame = tk.LabelFrame(main_frame, text="🎯 Klick-Modus", 
                                  font=('Arial', 10, 'bold'), bg='#ecf0f1')
        mode_frame.pack(pady=10, fill='x')
        
        mode_inner = tk.Frame(mode_frame, bg='#ecf0f1')
        mode_inner.pack(pady=10)
        
        self.mode_var = tk.StringVar(value="fixed")
        
        tk.Radiobutton(mode_inner, text="📌 Feste Position", 
                      variable=self.mode_var, value="fixed", bg='#ecf0f1').pack(anchor='w', pady=2)
        tk.Radiobutton(mode_inner, text="🔲 Bereich klicken", 
                      variable=self.mode_var, value="area", bg='#ecf0f1').pack(anchor='w', pady=2)
        tk.Radiobutton(mode_inner, text="🖱️ Maus verfolgen", 
                      variable=self.mode_var, value="follow", bg='#ecf0f1').pack(anchor='w', pady=2)
        
        # Bereich-Info und Buttons
        area_frame = tk.LabelFrame(main_frame, text="📏 Bereichs-Auswahl", 
                                  font=('Arial', 10, 'bold'), bg='#ecf0f1')
        area_frame.pack(pady=10, fill='x')
        
        area_inner = tk.Frame(area_frame, bg='#ecf0f1')
        area_inner.pack(pady=10)
        
        self.area_info_var = tk.StringVar(value="Noch kein Bereich definiert")
        area_label = tk.Label(area_inner, textvariable=self.area_info_var, 
                             font=('Arial', 9), wraplength=350, bg='#ecf0f1', fg='#7f8c8d')
        area_label.pack(pady=5)
        
        # Bereich-Buttons
        area_btn_frame = tk.Frame(area_inner, bg='#ecf0f1')
        area_btn_frame.pack(pady=5)
        
        tk.Button(area_btn_frame, text="🔲 Bereich markieren (F8)", 
                 command=self.mark_area_friendly, bg='#e74c3c', fg='white',
                 font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(area_btn_frame, text="🗑️ Bereich löschen", 
                 command=self.clear_area, bg='#95a5a6', fg='white',
                 font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        
        # Zufällige Klicks
        self.random_var = tk.BooleanVar()
        random_check = tk.Checkbutton(area_inner, text="🎲 Zufällige Positionen im Bereich", 
                                     variable=self.random_var, bg='#ecf0f1')
        random_check.pack(pady=5)
        
        # Status
        status_frame = tk.LabelFrame(main_frame, text="📊 Status", 
                                    font=('Arial', 10, 'bold'), bg='#ecf0f1')
        status_frame.pack(pady=10, fill='x')
        
        self.status_var = tk.StringVar(value="Bereit - Drücke F6 zum Starten")
        status_label = tk.Label(status_frame, textvariable=self.status_var, 
                               font=('Arial', 10), fg='#2980b9', bg='#ecf0f1')
        status_label.pack(pady=10)
        
        # Haupt-Buttons
        button_frame = tk.Frame(main_frame, bg='#ecf0f1')
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="▶️ Start/Stop (F6)", 
                 command=self.toggle_clicking, bg='#27ae60', fg='white',
                 font=('Arial', 11, 'bold'), width=18).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="🛑 Notfall-Stop (F7)", 
                 command=self.emergency_stop, bg='#e74c3c', fg='white',
                 font=('Arial', 11, 'bold'), width=18).pack(side=tk.LEFT, padx=5)
        
        # Zusätzliche Buttons
        extra_button_frame = tk.Frame(main_frame, bg='#ecf0f1')
        extra_button_frame.pack(pady=5)
        
        tk.Button(extra_button_frame, text="🖱️ Mausverfolgung (F9)", 
                 command=self.toggle_mouse_follow, bg='#9b59b6', fg='white',
                 font=('Arial', 10), width=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(extra_button_frame, text="📍 Aktuelle Position", 
                 command=self.get_current_pos, bg='#f39c12', fg='white',
                 font=('Arial', 10), width=20).pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Hotkey-Übersicht
        hotkey_frame = tk.LabelFrame(main_frame, text="⌨️ Hotkeys", 
                                    font=('Arial', 10, 'bold'), bg='#ecf0f1')
        hotkey_frame.pack(pady=5, fill='x')
        
        hotkeys_text = """F6 = Start/Stop Klicken    F7 = Notfall-Stop    F8 = Bereich markieren
F9 = Mausverfolgung    F10 = Ein/Aus    Esc = Programm beenden"""
        
        tk.Label(hotkey_frame, text=hotkeys_text, font=('Arial', 8), 
                bg='#ecf0f1', fg='#7f8c8d', justify='center').pack(pady=5)
        
    def setup_hotkeys(self):
        keyboard.add_hotkey('f6', self.toggle_clicking)
        keyboard.add_hotkey('f7', self.emergency_stop)
        keyboard.add_hotkey('f8', self.mark_area_friendly)
        keyboard.add_hotkey('f9', self.toggle_mouse_follow)
        keyboard.add_hotkey('f10', self.toggle_power)
        keyboard.add_hotkey('esc', self.close_app)
        
    def toggle_power(self):
        self.enabled = self.power_var.get()
        if not self.enabled:
            self.emergency_stop()
            self.status_var.set("🔴 Autoklicker deaktiviert")
        else:
            self.status_var.set("🟢 Autoklicker aktiviert - Bereit")
            
    def update_delay(self):
        try:
            new_delay = float(self.delay_var.get())
            if new_delay < 0.001:
                new_delay = 0.001
            elif new_delay > 60:
                new_delay = 60
            self.click_delay = new_delay
            self.status_var.set(f"✅ Klick-Intervall auf {new_delay:.3f}s gesetzt")
        except ValueError:
            self.status_var.set("❌ Fehler: Ungültiger Delay-Wert")
            
    def toggle_clicking(self):
        if not self.enabled:
            self.status_var.set("⚠️ Erst Autoklicker aktivieren!")
            return
            
        if self.clicking:
            self.clicking = False
            self.status_var.set("⏸️ Klicken gestoppt")
        else:
            mode = self.mode_var.get()
            
            if mode == "follow":
                self.mouse_following = True
                self.status_var.set("🖱️ Mausverfolgung aktiv...")
            elif mode == "area" and not self.area_defined:
                self.status_var.set("⚠️ Erst Bereich markieren! (F8)")
                return
            elif mode == "fixed":
                self.fixed_x, self.fixed_y = pyautogui.position()
                self.status_var.set(f"📌 Klicke an fester Position ({self.fixed_x},{self.fixed_y})")
            else:
                self.status_var.set("🔲 Klicke in definiertem Bereich...")
            
            self.clicking = True
            self.random_clicks = self.random_var.get()
            
            # Klick-Thread starten
            self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
            self.click_thread.start()
            
    def emergency_stop(self):
        self.clicking = False
        self.mouse_following = False
        self.status_var.set("🛑 NOTFALL-STOP - Alles gestoppt!")
        
    def toggle_mouse_follow(self):
        if not self.enabled:
            self.status_var.set("⚠️ Erst Autoklicker aktivieren!")
            return
            
        self.mouse_following = not self.mouse_following
        if self.mouse_following:
            self.mode_var.set("follow")
            self.status_var.set("🖱️ Mausverfolgung: EIN")
        else:
            self.status_var.set("🖱️ Mausverfolgung: AUS")
            
    def get_current_pos(self):
        x, y = pyautogui.position()
        self.status_var.set(f"📍 Aktuelle Position: ({x}, {y})")
        
    def mark_area_friendly(self):
        if not self.enabled:
            self.status_var.set("⚠️ Erst Autoklicker aktivieren!")
            return
            
        # Benutzerfreundliche Bereich-Auswahl
        result = messagebox.showinfo("Bereich markieren", 
            "Bereich-Markierung startet in 3 Sekunden!\n\n" +
            "1️⃣ Klicke die ERSTE Ecke des Bereichs\n" +
            "2️⃣ Klicke die ZWEITE Ecke des Bereichs\n\n" +
            "💡 Tipp: Das Fenster wird automatisch minimiert")
        
        # 3 Sekunden Countdown
        for i in range(3, 0, -1):
            self.status_var.set(f"⏳ Bereich-Markierung startet in {i}...")
            self.root.update()
            time.sleep(1)
            
        # Fenster minimieren
        self.root.iconify()
        
        try:
            self.status_var.set("🎯 Klicke die ERSTE Ecke...")
            self.root.update()
            
            # Warten auf ersten Klick (mit Timeout)
            start_time = time.time()
            clicked = False
            
            while time.time() - start_time < 30:  # 30 Sekunden Timeout
                if keyboard.is_pressed('esc'):
                    self.status_var.set("❌ Bereich-Markierung abgebrochen")
                    self.root.deiconify()
                    return
                    
                # Maus-Klick erkennen
                if keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift'):
                    # Alternative: Ctrl+Shift für ersten Punkt
                    self.area_x1, self.area_y1 = pyautogui.position()
                    clicked = True
                    break
                    
                # Oder linke Maustaste (einfacher)
                try:
                    # Kurze Pause und dann Position checken bei Klick
                    current_pos = pyautogui.position()
                    time.sleep(0.05)
                    new_pos = pyautogui.position()
                    if current_pos == new_pos:  # Maus ist still, wahrscheinlich geklickt
                        time.sleep(0.1)
                        if keyboard.is_pressed('space'):  # Leertaste als Bestätigung
                            self.area_x1, self.area_y1 = current_pos
                            clicked = True
                            break
                except:
                    pass
                    
                time.sleep(0.05)
            
            if not clicked:
                # Einfachere Methode: Tastatur-basiert
                self.root.deiconify()
                pos_input = tk.simpledialog.askstring("Erste Ecke", 
                    "Bewege Maus zur ersten Ecke und drücke OK\n" +
                    f"Aktuelle Position: {pyautogui.position()}")
                self.area_x1, self.area_y1 = pyautogui.position()
                self.root.iconify()
            
            time.sleep(0.5)
            self.status_var.set("🎯 Klicke die ZWEITE Ecke...")
            
            # Warten auf zweiten Klick
            start_time = time.time()
            clicked = False
            
            while time.time() - start_time < 30:
                if keyboard.is_pressed('esc'):
                    self.status_var.set("❌ Bereich-Markierung abgebrochen")
                    self.root.deiconify()
                    return
                    
                if keyboard.is_pressed('space'):  # Leertaste für zweiten Punkt
                    self.area_x2, self.area_y2 = pyautogui.position()
                    clicked = True
                    break
                    
                time.sleep(0.05)
            
            if not clicked:
                # Fallback
                self.root.deiconify()
                pos_input = tk.simpledialog.askstring("Zweite Ecke", 
                    "Bewege Maus zur zweiten Ecke und drücke OK\n" +
                    f"Aktuelle Position: {pyautogui.position()}")
                self.area_x2, self.area_y2 = pyautogui.position()
            
            # Bereich normalisieren
            if self.area_x1 > self.area_x2:
                self.area_x1, self.area_x2 = self.area_x2, self.area_x1
            if self.area_y1 > self.area_y2:
                self.area_y1, self.area_y2 = self.area_y2, self.area_y1
                
            self.area_defined = True
            width = self.area_x2 - self.area_x1
            height = self.area_y2 - self.area_y1
            
            self.area_info_var.set(f"✅ Bereich: ({self.area_x1},{self.area_y1}) → ({self.area_x2},{self.area_y2}) | {width}×{height}px")
            self.status_var.set(f"✅ Bereich erfolgreich definiert! ({width}×{height}px)")
            self.mode_var.set("area")
            
        except Exception as e:
            self.status_var.set(f"❌ Fehler beim Markieren: {str(e)}")
        finally:
            self.root.deiconify()  # Fenster wieder anzeigen
            
    def clear_area(self):
        self.area_defined = False
        self.area_info_var.set("Noch kein Bereich definiert")
        self.status_var.set("🗑️ Bereich gelöscht")
        
    def click_loop(self):
        while self.clicking and self.enabled:
            try:
                mode = self.mode_var.get()
                
                if mode == "follow" or self.mouse_following:
                    pyautogui.click()
                    
                elif mode == "area" and self.area_defined:
                    if self.random_clicks:
                        rand_x = random.randint(self.area_x1, self.area_x2)
                        rand_y = random.randint(self.area_y1, self.area_y2)
                        pyautogui.click(rand_x, rand_y)
                    else:
                        center_x = self.area_x1 + (self.area_x2 - self.area_x1) // 2
                        center_y = self.area_y1 + (self.area_y2 - self.area_y1) // 2
                        pyautogui.click(center_x, center_y)
                        
                elif mode == "fixed":
                    pyautogui.click(self.fixed_x, self.fixed_y)
                    
                time.sleep(self.click_delay)
                
            except Exception as e:
                self.status_var.set(f"❌ Klick-Fehler: {str(e)}")
                break
                
    def close_app(self):
        self.clicking = False
        self.root.quit()
        
    def run(self):
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.close_app)
            self.root.mainloop()
        except KeyboardInterrupt:
            self.close_app()

if __name__ == "__main__":
    # PyAutoGUI Sicherheit
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.01
    
    print("🖱️ Mouse Autoklicker wird gestartet...")
    print("Hotkeys: F6=Start/Stop | F7=Notfall-Stop | F8=Bereich | F9=Mausverfolgung | F10=Ein/Aus | Esc=Exit")
    
    try:
        from tkinter import simpledialog
        klicker = MouseAutoklicker()
        klicker.run()
    except ImportError:
        print("❌ Fehler: tkinter nicht verfügbar. Installiere Python mit tkinter-Support.")
    except Exception as e:
        print(f"❌ Fehler beim Start: {e}")