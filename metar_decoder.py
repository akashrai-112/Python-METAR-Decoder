import tkinter as tk
from tkinter import ttk, messagebox

airports_codes = {
    "VEBN": "Lal Bahadur Shastri International Airport, Varanasi",
    "VIDP": "Indira Gandhi International Airport, Delhi",
    "VABB": "Chhatrapati Shivaji Maharaj International Airport, Mumbai",
    "VOBL": "Kempegowda International Airport, Bengaluru",
    "VOMM": "Chennai International Airport, Chennai",
    "VECC": "Netaji Subhas Chandra Bose International Airport, Kolkata",
    "VOHS": "Rajiv Gandhi International Airport, Hyderabad",
    "VAAH": "Sardar Vallabhbhai Patel International Airport, Ahmedabad",
    "VAGO": "Manohar International Airport, Goa",
    "VOGA": "Goa International Airport (Dabolim)",
    "VIJP": "Jaipur International Airport, Jaipur",
    "VILK": "Chaudhary Charan Singh International Airport, Lucknow",
    "VANP": "Dr. Babasaheb Ambedkar International Airport, Nagpur",
    "VEPT": "Jay Prakash Narayan Airport, Patna",
    "VEGT": "Lokpriya Gopinath Bordoloi International Airport, Guwahati",
    "VOTV": "Trivandrum International Airport, Thiruvananthapuram",
    "VOCB": "Coimbatore International Airport, Coimbatore",
    "VOCI": "Cochin International Airport, Kochi",
    "VOCL": "Calicut International Airport, Kozhikode",
    "VOPB": "Veer Savarkar International Airport, Port Blair",
    "VAAU": "Aurangabad Airport",
    "VAID": "Devi Ahilyabai Holkar Airport, Indore",
    "VAJU": "Juhu Aerodrome, Mumbai",
    "VARK": "Maharana Pratap Airport, Udaipur",
    "VIBK": "Kushok Bakula Rimpochee Airport, Leh",
    "VISR": "Srinagar International Airport, Srinagar",
    "VEIM": "Imphal International Airport, Imphal",
    "VYBK": "Pakyong Airport, Gangtok",
    "VEJR": "Veer Surendra Sai Airport, Jharsuguda",
    "VOPN": "Sri Sathya Sai Airport, Puttaparthi",
}

weather_codes = {
    "RA": "Rain",
    "FG": "Fog",
    "TS": "Thunderstorm",
    "HZ": "Haze",
    "SN": "Snow",
    "DZ": "Drizzle",
    "BR": "Mist",
    "FU": "Smoke",
    "SA": "Sand",
    "DU": "Dust",
}

WEATHER_ICONS = {
    "Rain": "🌧",
    "Fog": "🌫",
    "Thunderstorm": "⛈",
    "Haze": "🌁",
    "Snow": "❄️",
    "Drizzle": "🌦",
    "Mist": "🌫",
    "Smoke": "💨",
    "Sand": "🏜",
    "Dust": "💨",
}

# ── palette ──────────────────────────────────────────────────────────────────
BG        = "#0b0f1a"   # deep night sky
PANEL     = "#131929"   # card surface
ACCENT    = "#00b4d8"   # radar-screen cyan
ACCENT2   = "#0077b6"   # darker cyan for gradients
TEXT      = "#e0f4ff"   # soft white
SUBTEXT   = "#8ab4c8"   # muted label
ENTRY_BG  = "#1a2540"
BORDER    = "#1e3a5f"
SUCCESS   = "#22d3a5"
WARNING   = "#f4a261"
ERROR_CLR = "#e63946"
ROW_ALT   = "#0f1e35"


def decode_metar():
    raw = entry_metar.get().strip()
    if not raw:
        messagebox.showwarning("Input Required", "Please enter a METAR string.")
        return

    parts = raw.split()
    if len(parts) < 9:
        messagebox.showerror(
            "Invalid METAR",
            "METAR string seems too short. Expected at least 9 fields.",
        )
        return

    # clear previous results
    for widget in result_frame.winfo_children():
        widget.destroy()

    try:
        rows = []

        # Airport
        icao = parts[0]
        airport_name = airports_codes.get(icao, "Unknown Airport")
        rows.append(("✈  Airport", f"{icao} — {airport_name}"))

        # Date/Time
        dt = parts[1]
        day  = dt[:2]
        hour = dt[2:4]
        mins = dt[4:6]
        rows.append(("🕐  Date/Time", f"Day {day}, {hour}:{mins} UTC"))

        # Wind
        wind = parts[2]
        wind_dir   = wind[:3]
        wind_spd   = wind[3:5]
        wind_gust  = ""
        if "G" in wind:
            g_idx     = wind.index("G")
            wind_spd  = wind[3:g_idx]
            wind_gust = f"  |  Gust: {wind[g_idx+1:g_idx+3]} kt"
        rows.append(("💨  Wind Direction", f"{wind_dir}°"))
        rows.append(("🌬  Wind Speed", f"{wind_spd} knots{wind_gust}"))

        # Visibility
        rows.append(("👁  Visibility", f"{parts[3]} m"))

        # Weather
        wx_raw  = parts[4]
        wx_name = weather_codes.get(wx_raw, wx_raw)
        wx_icon = WEATHER_ICONS.get(wx_name, "")
        rows.append(("🌤  Weather", f"{wx_icon}  {wx_name}" if wx_icon else wx_name))

        # Temp / Dew
        temp_dew = parts[7]
        temperature, dewpoint = temp_dew.split("/")
        rows.append(("🌡  Temperature", f"{temperature} °C"))
        rows.append(("💧  Dew Point", f"{dewpoint} °C"))

        # Pressure
        pressure = parts[8][1:]
        rows.append(("🔵  Pressure (QNH)", f"{pressure} hPa"))

        # ── render rows ──────────────────────────────────────────────────────
        result_frame.columnconfigure(0, weight=1, minsize=220)
        result_frame.columnconfigure(1, weight=2)

        for i, (label, value) in enumerate(rows):
            bg = PANEL if i % 2 == 0 else ROW_ALT

            lbl = tk.Label(
                result_frame,
                text=label,
                font=("Consolas", 10, "bold"),
                fg=SUBTEXT,
                bg=bg,
                anchor="w",
                padx=14,
                pady=10,
            )
            lbl.grid(row=i, column=0, sticky="nsew")

            val = tk.Label(
                result_frame,
                text=value,
                font=("Consolas", 10),
                fg=TEXT,
                bg=bg,
                anchor="w",
                padx=14,
                pady=10,
            )
            val.grid(row=i, column=1, sticky="nsew")

        status_var.set("✔  Decoded successfully")
        status_lbl.config(fg=SUCCESS)

    except Exception as exc:
        messagebox.showerror("Decode Error", f"Could not parse METAR:\n{exc}")
        status_var.set("✘  Decode failed")
        status_lbl.config(fg=ERROR_CLR)


def clear_all():
    entry_metar.delete(0, tk.END)
    for widget in result_frame.winfo_children():
        widget.destroy()
    status_var.set("")


def paste_sample():
    entry_metar.delete(0, tk.END)
    entry_metar.insert(0, "VIJP 141630Z 27015KT 4000 HZ FEW030 SCT100 38/22 Q1004 NOSIG")


# ── root window ──────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("METAR Decoder")
root.configure(bg=BG)
root.resizable(True, True)
root.geometry("780x640")
root.minsize(640, 520)

# ── title bar ────────────────────────────────────────────────────────────────
header = tk.Frame(root, bg=ACCENT2, pady=0)
header.pack(fill="x")

title_lbl = tk.Label(
    header,
    text="  ✈  METAR DECODER",
    font=("Consolas", 16, "bold"),
    fg=TEXT,
    bg=ACCENT2,
    pady=14,
    anchor="w",
    padx=20,
)
title_lbl.pack(side="left")

sub_lbl = tk.Label(
    header,
    text="Aviation Weather Report Parser  |  India Edition",
    font=("Consolas", 9),
    fg="#b0d8f0",
    bg=ACCENT2,
    pady=14,
    anchor="e",
    padx=20,
)
sub_lbl.pack(side="right")

# ── input section ────────────────────────────────────────────────────────────
input_outer = tk.Frame(root, bg=BG, pady=14, padx=20)
input_outer.pack(fill="x")

input_card = tk.Frame(input_outer, bg=PANEL, bd=0, relief="flat")
input_card.pack(fill="x", ipady=14, ipadx=14)

tk.Label(
    input_card,
    text="METAR STRING",
    font=("Consolas", 8, "bold"),
    fg=SUBTEXT,
    bg=PANEL,
    anchor="w",
).pack(anchor="w", padx=14, pady=(10, 2))

entry_metar = tk.Entry(
    input_card,
    font=("Consolas", 12),
    bg=ENTRY_BG,
    fg=TEXT,
    insertbackground=ACCENT,
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=ACCENT,
)
entry_metar.pack(fill="x", padx=14, pady=(0, 10), ipady=8)
entry_metar.bind("<Return>", lambda e: decode_metar())

# ── button row ───────────────────────────────────────────────────────────────
btn_frame = tk.Frame(input_card, bg=PANEL)
btn_frame.pack(anchor="w", padx=14, pady=(0, 8))

def make_btn(parent, text, cmd, color=ACCENT, fg_col=BG):
    return tk.Button(
        parent,
        text=text,
        command=cmd,
        font=("Consolas", 10, "bold"),
        bg=color,
        fg=fg_col,
        activebackground=ACCENT2,
        activeforeground=TEXT,
        relief="flat",
        cursor="hand2",
        padx=18,
        pady=6,
        bd=0,
    )

make_btn(btn_frame, "  DECODE  ", decode_metar).pack(side="left", padx=(0, 8))
make_btn(btn_frame, "  SAMPLE  ", paste_sample, color=ACCENT2, fg_col=TEXT).pack(side="left", padx=(0, 8))
make_btn(btn_frame, "  CLEAR  ", clear_all, color="#1e3a5f", fg_col=SUBTEXT).pack(side="left")

# ── status bar ───────────────────────────────────────────────────────────────
status_var = tk.StringVar()
status_lbl = tk.Label(
    input_card,
    textvariable=status_var,
    font=("Consolas", 9),
    fg=SUCCESS,
    bg=PANEL,
    anchor="w",
    padx=14,
)
status_lbl.pack(anchor="w", pady=(0, 4))

# ── results section ──────────────────────────────────────────────────────────
res_outer = tk.Frame(root, bg=BG, padx=20, pady=0)
res_outer.pack(fill="both", expand=True, pady=(0, 14))

tk.Label(
    res_outer,
    text="DECODED OUTPUT",
    font=("Consolas", 8, "bold"),
    fg=SUBTEXT,
    bg=BG,
    anchor="w",
).pack(anchor="w", pady=(0, 6))

canvas = tk.Canvas(res_outer, bg=PANEL, highlightthickness=0, bd=0)
scrollbar = ttk.Scrollbar(res_outer, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

result_frame = tk.Frame(canvas, bg=PANEL)
canvas_window = canvas.create_window((0, 0), window=result_frame, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_canvas_configure(event):
    canvas.itemconfig(canvas_window, width=event.width)

result_frame.bind("<Configure>", on_frame_configure)
canvas.bind("<Configure>", on_canvas_configure)

# mousewheel scrolling
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# ── footer ───────────────────────────────────────────────────────────────────
footer = tk.Frame(root, bg=ACCENT2, pady=4)
footer.pack(fill="x", side="bottom")
tk.Label(
    footer,
    text="Supports Indian ICAO codes  •  Press Enter or click DECODE  •  Try SAMPLE for a demo",
    font=("Consolas", 8),
    fg="#b0d8f0",
    bg=ACCENT2,
).pack()

root.mainloop()
