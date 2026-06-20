import tkinter as tk
from tkinter import ttk, messagebox
import requests
import xml.etree.ElementTree as ET

# --- Λογική ---
provlima_diktyou = False

def anaktisi_isotimion():
    global provlima_diktyou
    times = {"Ευρώ (EUR)": 1.0}
    try:
        apantisi = requests.get("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml", timeout=5)
        apantisi.raise_for_status()
        tree = ET.fromstring(apantisi.content)
        namespaces = {'default': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
        cube = tree.find('.//default:Cube/default:Cube', namespaces)
        for stoixeio in cube.findall('default:Cube', namespaces):
            nomisma = stoixeio.attrib['currency']
            isotimia = float(stoixeio.attrib['rate'])
            if nomisma in ["USD", "GBP", "JPY", "MXN"]:
                onoma = {"USD": "Δολάριο (USD)", "GBP": "Λίρα (GBP)", "JPY": "Γιεν (JPY)", "MXN": "Πέσο (MXN)"}[nomisma]
                times[onoma] = isotimia
        return times
    except:
        provlima_diktyou = True
        return {"Ευρώ (EUR)": 1.0, "Δολάριο (USD)": 1.08, "Λίρα (GBP)": 0.86, "Γιεν (JPY)": 165.0, "Πέσο (MXN)": 18.5}

# Δεδομένα
onomata_monadon = {
    "Μήκος": {"Μέτρα": "m", "Χιλιόμετρα": "km", "Εκατοστά": "cm", "Μίλια": "mi"},
    "Βάρος": {"Κιλά": "kg", "Γραμμάρια": "g", "Λίβρες": "lb", "Ουγγιές": "oz"},
    "Ταχύτητα": {"Μέτρα/δευτ": "m/s", "Χλμ/ώρα": "km/h", "Μίλια/ώρα": "mph", "Κόμβοι": "knots"},
    "Θερμοκρασία": {"Κελσίου": "C", "Φαρενάιτ": "F", "Κέλβιν": "K"},
    "Νόμισμα": {}
}

metriko_systima = {
    "Μήκος": {"m": 1, "km": 1000, "cm": 0.01, "mi": 1609.34},
    "Βάρος": {"kg": 1, "g": 0.001, "lb": 0.453592, "oz": 0.0283495},
    "Ταχύτητα": {"m/s": 1, "km/h": 0.277778, "mph": 0.44704, "knots": 0.514444},
}

# --- GUI ---
parathyro = tk.Tk()
parathyro.title("Unit Converter Pro")
parathyro.geometry("420x650")
parathyro.configure(bg="#2c3e50")

isotimies = anaktisi_isotimion()
onomata_monadon["Νόμισμα"] = {k: k for k in isotimies.keys()}

def format_number(val):
    # Εμφάνιση με 4 δεκαδικά και κόμμα
    return f"{val:,.4f}".replace('.', ',')

def ektelesi_metatropis():
    try:
        val = float(entry_timi.get().replace(',', '.'))
        kat = katigoria_var.get()
        m1, m2 = monada_eisodou_var.get(), monada_exodou_var.get()
        
        if kat == "Νόμισμα":
            res = val * (isotimies[m2] / isotimies[m1])
        elif kat == "Θερμοκρασία":
            val_c = val if m1 == "Κελσίου" else ((val-32)*5/9 if m1=="Φαρενάιτ" else val-273.15)
            res = val_c if m2 == "Κελσίου" else (val_c*9/5+32 if m2=="Φαρενάιτ" else val_c+273.15)
        else:
            code1, code2 = onomata_monadon[kat][m1], onomata_monadon[kat][m2]
            res = val * metriko_systima[kat][code1] / metriko_systima[kat][code2]
            
        apotelesma_var.set(format_number(res))
    except:
        messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε έγκυρο αριθμό")

# --- UI Styling & Components ---
style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", padding=5)

frame = tk.Frame(parathyro, bg="#34495e", padx=25, pady=25)
frame.pack(expand=True, fill="both", padx=15, pady=15)

# Τίτλος
tk.Label(frame, text="UNIT CONVERTER", font=("Segoe UI", 20, "bold"), bg="#34495e", fg="#f1c40f").pack(pady=(0, 10))
ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=10)

katigoria_var = tk.StringVar(value="Μήκος")
monada_eisodou_var = tk.StringVar()
monada_exodou_var = tk.StringVar()
apotelesma_var = tk.StringVar(value="0,0000")

def ananeosi_monadon(*args):
    kat = katigoria_var.get()
    listes = list(onomata_monadon[kat].keys())
    input_menu['values'] = listes
    output_menu['values'] = listes
    monada_eisodou_var.set(listes[0])
    output_menu.set(listes[1] if len(listes) > 1 else listes[0])

# Επιλογή Κατηγορίας
tk.Label(frame, text="Επιλογή Κατηγορίας", bg="#34495e", fg="#bdc3c7", font=("Segoe UI", 9)).pack(anchor="w")
menu = ttk.Combobox(frame, textvariable=katigoria_var, values=list(onomata_monadon.keys()), state="readonly")
menu.pack(fill="x", pady=(5, 15))
menu.bind("<<ComboboxSelected>>", ananeosi_monadon)

# Ποσότητα
tk.Label(frame, text="Ποσότητα", bg="#34495e", fg="#bdc3c7", font=("Segoe UI", 9)).pack(anchor="w")
entry_timi = tk.Entry(frame, font=("Segoe UI", 16), justify="center", bd=0, highlightthickness=1, highlightbackground="#7f8c8d")
entry_timi.pack(fill="x", pady=(5, 15), ipady=8)

# Dual Columns
cols = tk.Frame(frame, bg="#34495e")
cols.pack(fill="x", pady=10)
input_menu = ttk.Combobox(cols, textvariable=monada_eisodou_var, state="readonly", width=10)
input_menu.pack(side="left", expand=True, fill="x")
tk.Label(cols, text=" ➔ ", bg="#34495e", fg="#3498db", font=("Segoe UI", 14, "bold")).pack(side="left", padx=10)
output_menu = ttk.Combobox(cols, textvariable=monada_exodou_var, state="readonly", width=10)
output_menu.pack(side="right", expand=True, fill="x")

# Κουμπί
btn = tk.Button(frame, text="ΜΕΤΑΤΡΟΠΗ", command=ektelesi_metatropis, bg="#27ae60", fg="white", 
                font=("Segoe UI", 12, "bold"), relief="flat", cursor="hand2", activebackground="#2ecc71")
btn.pack(fill="x", pady=25, ipady=10)

# Αποτέλεσμα
tk.Label(frame, text="ΑΠΟΤΕΛΕΣΜΑ", bg="#34495e", fg="#95a5a6", font=("Segoe UI", 8, "bold")).pack()
tk.Label(frame, textvariable=apotelesma_var, font=("Segoe UI", 36, "bold"), bg="#34495e", fg="#2ecc71").pack(pady=5)

ananeosi_monadon()
parathyro.mainloop()