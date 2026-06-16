import tkinter as tk
from tkinter import ttk, messagebox
import requests
import xml.etree.ElementTree as ET

# --- Λογική και Δεδομένα ---
provlima_diktyou = False

def anaktisi_isotimion():
    global provlima_diktyou
    times = {"Ευρώ (EUR)": 1.0}
    try:
        # Λήψη δεδομένων από την Ευρωπαϊκή Κεντρική Τράπεζα
        apantisi = requests.get("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml", timeout=5)
        apantisi.raise_for_status()
        tree = ET.fromstring(apantisi.content)
        namespaces = {'default': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
        cube = tree.find('.//default:Cube/default:Cube', namespaces)
        
        for stoixeio in cube.findall('default:Cube', namespaces):
            nomisma = stoixeio.attrib['currency']
            isotimia = float(stoixeio.attrib['rate'])
            if nomisma in ["USD", "GBP", "JPY", "MXN"]:
                onoma = {"USD": "Δολάριο ΗΠΑ (USD)", "GBP": "Λίρα Αγγλίας (GBP)", 
                         "JPY": "Γιεν Ιαπωνίας (JPY)", "MXN": "Πέσο Μεξικού (MXN)"}[nomisma]
                times[onoma] = isotimia
        provlima_diktyou = False
        return times
    except Exception:
        provlima_diktyou = True
        # Στατικές τιμές σε περίπτωση που δεν υπάρχει ίντερνετ
        return {
            "Ευρώ (EUR)": 1.0,
            "Δολάριο ΗΠΑ (USD)": 1.08,
            "Λίρα Αγγλίας (GBP)": 0.86,
            "Γιεν Ιαπωνίας (JPY)": 165.0,
            "Πέσο Μεξικού (MXN)": 18.5,
        }

# Ονόματα μονάδων για τα μενού
onomata_monadon = {
    "Μήκος": {"Μέτρα": "m", "Χιλιόμετρα": "km", "Εκατοστά": "cm", "Μίλια": "mi"},
    "Βάρος": {"Κιλά": "kg", "Γραμμάρια": "g", "Λίβρες": "lb", "Ουγγιές": "oz"},
    "Ταχύτητα": {"Μέτρα/δευτ": "m/s", "Χλμ/ώρα": "km/h", "Μίλια/ώρα": "mph", "Κόμβοι": "knots"},
    "Θερμοκρασία": {"Κελσίου": "C", "Φαρενάιτ": "F", "Κέλβιν": "K"},
}

# Συντελεστές μετατροπής βάσει μετρικού συστήματος
metriko_systima = {
    "Μήκος": {"m": 1, "km": 1000, "cm": 0.01, "mi": 1609.34},
    "Βάρος": {"kg": 1, "g": 0.001, "lb": 0.453592, "oz": 0.0283495},
    "Ταχύτητα": {"m/s": 1, "km/h": 0.277778, "mph": 0.44704, "knots": 0.514444},
}

# --- Ρύθμιση Παραθύρου (GUI) ---
parathyro = tk.Tk()
parathyro.title("Ο Δικός μου Μετατροπέας")
parathyro.geometry("450x550")
parathyro.configure(bg="#f5f5f5")

style = ttk.Style()
style.theme_use('clam')

istoriko = []
isotimies = anaktisi_isotimion()

# Μεταβλητές ελέγχου
katigoria_var = tk.StringVar(value="Μήκος")
monada_eisodou_var = tk.StringVar()
monada_exodou_var = tk.StringVar()
apotelesma_var = tk.StringVar(value="Αποτέλεσμα: ---")

def ektelesi_metatropis():
    katigoria = katigoria_var.get()
    apo_monada = monada_eisodou_var.get()
    pros_monada = monada_exodou_var.get()
    timi_eisodou = entry_timi.get()

    try:
        arithmos = float(timi_eisodou)
    except ValueError:
        messagebox.showerror("Σφάλμα", "Παρακαλώ βάλε έναν σωστό αριθμό!")
        return

    if katigoria == "Νόμισμα":
        is_apo = isotimies.get(apo_monada, 1)
        is_pros = isotimies.get(pros_monada, 1)
        apotelesma = arithmos * (is_pros / is_apo)
    elif katigoria == "Θερμοκρασία":
        m1 = onomata_monadon[katigoria][apo_monada]
        m2 = onomata_monadon[katigoria][pros_monada]
        if m1 == m2: apotelesma = arithmos
        elif m1 == "C": apotelesma = arithmos + 273.15 if m2 == "K" else (arithmos * 9/5) + 32
        elif m1 == "K": apotelesma = arithmos - 273.15 if m2 == "C" else ((arithmos - 273.15) * 9/5) + 32
        elif m1 == "F": apotelesma = (arithmos - 32) * 5/9 if m2 == "C" else ((arithmos - 32) * 5/9) + 273.15
    else:
        monades = metriko_systima[katigoria]
        kodikos_apo = onomata_monadon[katigoria][apo_monada]
        kodikos_pros = onomata_monadon[katigoria][pros_monada]
        apotelesma = arithmos * monades[kodikos_apo] / monades[kodikos_pros]

    teliko_keimeno = f"{apotelesma:.4f}"
    apotelesma_var.set(f"Αποτέλεσμα: {teliko_keimeno}")
    istoriko.append(f"{arithmos} {apo_monada} = {teliko_keimeno} {pros_monada}")

def ananeosi_monadon(*args):
    katigoria = katigoria_var.get()
    if katigoria == "Νόμισμα":
        listes = list(isotimies.keys())
    else:
        listes = list(onomata_monadon[katigoria].keys())
    
    monada_eisodou_var.set(listes[0])
    monada_exodou_var.set(listes[1])
    
    input_menu['values'] = listes
    output_menu['values'] = listes

# --- Σχεδίαση Interface ---
perieXomeno = ttk.Frame(parathyro, padding="20")
perieXomeno.pack(expand=True, fill="both")

ttk.Label(perieXomeno, text="ΜΕΤΑΤΡΟΠΕΑΣ ΜΟΝΑΔΩΝ", font=("Segoe UI", 16, "bold")).pack(pady=15)

# Επιλογή Κατηγορίας
ttk.Label(perieXomeno, text="Διάλεξε κατηγορία:").pack(anchor="w")
menu_katigorias = ttk.Combobox(perieXomeno, textvariable=katigoria_var, state="readonly", 
                               values=["Μήκος", "Βάρος", "Ταχύτητα", "Θερμοκρασία", "Νόμισμα"])
menu_katigorias.pack(fill="x", pady=5)
menu_katigorias.bind("<<ComboboxSelected>>", ananeosi_monadon)

# Πεδίο Εισαγωγής
ttk.Label(perieXomeno, text="Πληκτρολόγησε την τιμή:").pack(anchor="w", pady=(10, 0))
entry_timi = ttk.Entry(perieXomeno, font=("Segoe UI", 12))
entry_timi.pack(fill="x", pady=5)

# Από / Προς
frame_monadon = ttk.Frame(perieXomeno)
frame_monadon.pack(fill="x", pady=10)

ttk.Label(frame_monadon, text="Από:").grid(row=0, column=0, sticky="w")
input_menu = ttk.Combobox(frame_monadon, textvariable=monada_eisodou_var, state="readonly", width=18)
input_menu.grid(row=1, column=0, padx=(0, 10))

ttk.Label(frame_monadon, text="Σε:").grid(row=0, column=1, sticky="w")
output_menu = ttk.Combobox(frame_monadon, textvariable=monada_exodou_var, state="readonly", width=18)
output_menu.grid(row=1, column=1)

# Κουμπί Υπολογισμού
ttk.Button(perieXomeno, text="ΥΠΟΛΟΓΙΣΜΟΣ", command=ektelesi_metatropis).pack(fill="x", pady=20)

label_apotelesma = ttk.Label(perieXomeno, textvariable=apotelesma_var, font=("Segoe UI", 13, "bold"), foreground="#1b5e20")
label_apotelesma.pack(pady=10)

# Ιστορικό
def deixe_istoriko():
    keimeno_istorikou = "\n".join(istoriko[-10:]) if istoriko else "Δεν υπάρχουν ακόμα μετατροπές."
    messagebox.showinfo("Ιστορικό Μετατροπών", keimeno_istorikou)

ttk.Button(perieXomeno, text="Προβολή Ιστορικού", command=deixe_istoriko).pack(side="bottom", pady=10)

if provlima_diktyou:
    ttk.Label(perieXomeno, text="⚠️ Προσοχή: Χρήση παλιών ισοτιμιών (Offline)", foreground="red").pack(side="bottom")

ananeosi_monadon()
parathyro.mainloop()