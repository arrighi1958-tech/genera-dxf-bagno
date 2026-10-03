import io
import ezdxf
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Progetto Esecutivo - Doppia Sala da Bagno", layout="centered"
)
st.title("Progetto Esecutivo - Doppia Sala da Bagno (247x215 cm)")
st.markdown(
    "Pianta esecutiva aggiornata: sanitari del bagno piccolo riposizionati (WC e"
    " bidet in alto a parete, lavandino a sinistra verso la parete D)."
)


def genera_dxf_bytes():
  doc = ezdxf.new(dxfversion="AC1024")
  msp = doc.modelspace()

  doc.layers.add("MURI_ESTERNI", color=7)
  doc.layers.add("PARETI_INTERNE", color=3)
  doc.layers.add("SANITARI", color=5)
  doc.layers.add("CAVEDIO", color=2)
  doc.layers.add("APERTURE", color=4)

  x0, y0 = 0.0, 0.0
  w_netto, h_netto = 247.0, 215.0
  spessore = 16.0

  # Muri esterni
  msp.add_lwpolyline(
      [
          (x0 - spessore, y0 - spessore),
          (x0 + w_netto + spessore, y0 - spessore),
          (x0 + w_netto + spessore, y0 + h_netto + spessore),
          (x0 - spessore, y0 + h_netto + spessore),
      ],
      close=True,
      dxfattribs={"layer": "MURI_ESTERNI"},
  )

  # Perimetro interno (247 x 215)
  msp.add_lwpolyline(
      [(x0, y0), (x0 + w_netto, y0), (x0 + w_netto, y0 + h_netto), (x0, y0 + h_netto)],
      close=True,
      dxfattribs={"layer": "PARETI_INTERNE"},
  )

  # Bagno piccolo in basso a destra (90 x 110 cm)
  bp_w, bp_h = 90.0, 110.0
  bp_x, bp_y = x0 + w_netto - bp_w, y0
  msp.add_lwpolyline(
      [
          (bp_x, bp_y),
          (bp_x + bp_w, bp_y),
          (bp_x + bp_w, bp_y + bp_h),
          (bp_x, bp_y + bp_h),
      ],
      close=True,
      dxfattribs={"layer": "PARETI_INTERNE"},
  )

  stream = io.StringIO()
  doc.write(stream)
  return stream.getvalue().encode("utf-8")


# Pulsante Download DXF
dxf_data = genera_dxf_bytes()
st.download_button(
    label="📥 Scarica il file DXF Esecutivo Aggiornato",
    data=dxf_data,
    file_name="bagno_doppio_aggiornato.dxf",
    mime="application/dxf",
)

# Anteprima Grafica Completa
st.subheader("Anteprima Grafica - Nuova Disposizione Sanitari Bagno Piccolo")
fig, ax = plt.subplots(figsize=(9, 8))
ax.set_xlim(-25, 272)
ax.set_ylim(-25, 240)
ax.set_aspect("equal")

# Contenitore principale (247 x 215)
ax.add_patch(
    plt.Rectangle(
        (0, 0), 247, 215, edgecolor="#212529", facecolor="#f8f9fa", lw=2
    )
)

# Cavedio E2 (larghezza 56.5 cm, spessore 16 cm)
cav_x, cav_w, cav_h = 70.0, 56.5, 16.0
cav_y = 215 - cav_h
ax.add_patch(
    plt.Rectangle(
        (cav_x, cav_y),
        cav_w,
        cav_h,
        edgecolor="#d90429",
        facecolor="#ffccd5",
        lw=1.5,
    )
)
ax.text(
    cav_x + cav_w / 2,
    cav_y + cav_h / 2,
    "Cavedio E2",
    ha="center",
    va="center",
    fontsize=6,
    color="#d90429",
    fontweight="bold",
)

# Finestre sulla Parete A
ax.plot([4.5, 67.5], [215, 215], color="#0077b6", lw=4)
ax.text(
    36.0,
    223,
    "Finestra 2 (63 cm)",
    ha="center",
    va="bottom",
    fontsize=7,
    color="#0077b6",
    fontweight="bold",
)

ax.plot([134.5, 195.5], [215, 215], color="#0077b6", lw=4)
ax.text(
    165.0,
    223,
    "Finestra 1 (61 cm)",
    ha="center",
    va="bottom",
    fontsize=7,
    color="#0077b6",
    fontweight="bold",
)

# Porte sulla Parete C (P1: 77 a 147 | P2: 167 a 237)
ax.plot([77, 147], [0, 0], color="#fb8500", lw=4)
ax.text(
    112,
    -8,
    "Porta Bagno Princ. (70 cm)",
    ha="center",
    va="top",
    fontsize=7,
    color="#fb8500",
    fontweight="bold",
)

ax.plot([167, 237], [0, 0], color="#fb8500", lw=4)
ax.text(
    202,
    -8,
    "Porta Bagno Piccolo (70 cm)",
    ha="center",
    va="top",
    fontsize=7,
    color="#fb8500",
    fontweight="bold",
)

# Bagno piccolo in basso a destra (90 x 110)
bp_x = 247 - 90
ax.add_patch(
    plt.Rectangle((bp_x, 0), 90, 110, edgecolor="#2b9348", facecolor="#d8f3dc", lw=1.5)
)
ax.text(
    bp_x + 45,
    95,
    "Bagno Piccolo\n90 x 110 cm",
    ha="center",
    va="center",
    fontsize=7,
    color="#2b9348",
    fontweight="bold",
)

# Doccia in alto a destra sopra il bagno piccolo (80 x 105)
ax.add_patch(
    plt.Rectangle(
        (247 - 80, 215 - 105),
        80,
        105,
        edgecolor="#0077b6",
        facecolor="#caf0f8",
        lw=1.5,
    )
)
ax.text(
    247 - 40,
    215 - 52.5,
    "Doccia\n(80x105 cm)",
    ha="center",
    va="center",
    fontsize=7,
    color="#0077b6",
    fontweight="bold",
)

# Sanitari Bagno Piccolo (aggiornati secondo le nuove indicazioni)
# WC piccolo (traslato in alto a parete verso la doccia/lato A)
ax.add_patch(
    plt.Rectangle(
        (bp_x + 10, 62), 32, 38, edgecolor="#2b9348", facecolor="#ffffff", lw=1
    )
)
ax.text(
    bp_x + 26,
    81,
    "WC",
    ha="center",
    va="center",
    fontsize=6,
    color="#2b9348",
    fontweight="bold",
)

# Bidet piccolo (traslato in alto a parete verso la doccia/lato A)
ax.add_patch(
    plt.Rectangle(
        (bp_x + 48, 62), 32, 38, edgecolor="#2b9348", facecolor="#ffffff", lw=1
    )
)
ax.text(
    bp_x + 64,
    81,
    "Bidet",
    ha="center",
    va="center",
    fontsize=6,
    color="#2b9348",
    fontweight="bold",
)

# Lavabo piccolo (traslato a parete verso sinistra, vicino al confine con il bagno principale / parete D)
ax.add_patch(
    plt.Rectangle(
        (bp_x + 4, 30), 28, 40, edgecolor="#2b9348", facecolor="#ffffff", lw=1
    )
)
ax.text(
    bp_x + 18,
    50,
    "Lav.",
    ha="center",
    va="center",
    fontsize=6,
    color="#2b9348",
    fontweight="bold",
)

# Sanitari Bagno Principale (Parete D: 215 cm)
h_san = 35.0
w_san = 38.0
spazio_utile = 215.0
gap = (spazio_utile - (3 * h_san)) / 4.0

y_wc = 215.0 - gap - h_san
y_bidet = y_wc - gap - h_san
y_lavabo = y_bidet - gap - h_san

# WC Principale
ax.add_patch(
    plt.Rectangle(
        (0, y_wc), w_san, h_san, edgecolor="#3a0ca3", facecolor="#e0aaff", lw=1
    )
)
ax.text(
    w_san / 2,
    y_wc + h_san / 2,
    "WC",
    ha="center",
    va="center",
    fontsize=7,
    color="#3a0ca3",
    fontweight="bold",
)

# Bidet Principale
ax.add_patch(
    plt.Rectangle(
        (0, y_bidet),
        w_san,
        h_san,
        edgecolor="#3a0ca3",
        facecolor="#e0aaff",
        lw=1,
    )
)
ax.text(
    w_san / 2,
    y_bidet + h_san / 2,
    "Bidet",
    ha="center",
    va="center",
    fontsize=7,
    color="#3a0ca3",
    fontweight="bold",
)

# Lavabo Principale
ax.add_patch(
    plt.Rectangle(
        (0, y_lavabo),
        w_san,
        h_san,
        edgecolor="#3a0ca3",
        facecolor="#e0aaff",
        lw=1,
    )
)
ax.text(
    w_san / 2,
    y_lavabo + h_san / 2,
    "Lavabo",
    ha="center",
    va="center",
    fontsize=7,
    color="#3a0ca3",
    fontweight="bold",
)

# Etichetta centrale bagno principale
ax.text(
    75,
    115,
    "BAGNO PRINCIPALE",
    ha="center",
    va="center",
    fontsize=9,
    fontweight="bold",
    color="#1d3557",
)

# Quote perimetrali esterne
ax.text(
    123.5,
    231,
    "Parete A: 247 cm",
    ha="center",
    va="bottom",
    fontsize=8,
    color="black",
)
ax.text(
    123.5,
    -15,
    "Parete C: 247 cm",
    ha="center",
    va="top",
    fontsize=8,
    color="black",
)
ax.text(
    -12,
    107.5,
    "Parete D: 215 cm",
    ha="right",
    va="center",
    rotation=90,
    fontsize=8,
    color="black",
)
ax.text(
    259,
    107.5,
    "Parete B: 215 cm",
    ha="left",
    va="center",
    rotation=270,
    fontsize=8,
    color="black",
)

ax.axis("off")
st.pyplot(fig)
