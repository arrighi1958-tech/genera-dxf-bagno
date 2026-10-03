import io
import ezdxf
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Progetto Esecutivo - Doppia Sala da Bagno", layout="centered"
)
st.title("Progetto Esecutivo - Doppia Sala da Bagno (247x215 cm)")
st.markdown(
    "Pianta esecutiva completa con distribuzione dei sanitari in entrambi i"
    " bagni, cavedio E2 e note tecniche normative."
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
    label="📥 Scarica il file DXF Esecutivo Completo",
    data=dxf_data,
    file_name="bagno_doppio_definitivo.dxf",
    mime="application/dxf",
)

# Anteprima Grafica Completa
st.subheader(
    "Anteprima Grafica - Modifica Bagno (Proposta di Distribuzione - Variante"
    " 2)"
)
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

# Cavedio E2 (105 x 90 interno / 115 x 100 esterno -> rappresentato come blocco tecnico)
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
    "E2 - Colonna Scarico",
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
    "Finestra (63 cm)",
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
    "Finestra (61 cm)",
    ha="center",
    va="bottom",
    fontsize=7,
    color="#0077b6",
    fontweight="bold",
)

# Porte sulla Parete C (P1: 52 a 122 | P2: 167 a 237)
ax.plot([52, 122], [0, 0], color="#fb8500", lw=4)
ax.text(
    87,
    -8,
    "P1 (70 cm)",
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
    "P2 (70 cm)",
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
    75,
    "Bagno Piccolo\n90 x 110 cm",
    ha="center",
    va="center",
    fontsize=7,
    color="#2b9348",
    fontweight="bold",
)

# Sanitari Bagno Piccolo (WC, Bidet sulla parete superiore del bagno piccolo, Lavabo a sinistra)
# WC piccolo
ax.add_patch(
    plt.Rectangle(
        (bp_x + 12, 110 - 38),
        32,
        38,
        edgecolor="#2b9348",
        facecolor="#ffffff",
        lw=1,
    )
)
ax.text(
    bp_x + 28,
    110 - 19,
    "WC",
    ha="center",
    va="center",
    fontsize=6,
    color="#2b9348",
    fontweight="bold",
)

# Bidet piccolo
ax.add_patch(
    plt.Rectangle(
        (bp_x + 48, 110 - 38),
        32,
        38,
        edgecolor="#2b9348",
        facecolor="#ffffff",
        lw=1,
    )
)
ax.text(
    bp_x + 64,
    110 - 19,
    "Bidet",
    ha="center",
    va="center",
    fontsize=6,
    color="#2b9348",
    fontweight="bold",
)

# Lavabo piccolo
ax.add_patch(
    plt.Rectangle(
        (bp_x, 35), 28, 40, edgecolor="#2b9348", facecolor="#ffffff", lw=1
    )
)
ax.text(
    bp_x + 14,
    55,
    "Lav.",
    ha="center",
    va="center",
    fontsize=6,
    color="#2b9348",
    fontweight="bold",
)

# Doccia a raso pavimento in alto a destra (132 x 82 adattata o 80x105)
ax.add_patch(
    plt.Rectangle(
        (247 - 82, 215 - 110),
        82,
        110,
        edgecolor="#0077b6",
        facecolor="#caf0f8",
        lw=1.5,
    )
)
ax.text(
    247 - 41,
    215 - 55,
    "Doccia\n132x82 cm",
    ha="center",
    va="center",
    fontsize=6,
    color="#0077b6",
    fontweight="bold",
)

# Sanitari Bagno Principale (Parete D)
h_san = 38.0
w_san = 35.0
y_wc = 215.0 - 15 - h_san
y_bidet = y_wc - 12 - h_san
y_lavabo = y_bidet - 20 - 50  # lavabo principale più ampio

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
        (0, 15), 42, 55, edgecolor="#3a0ca3", facecolor="#e0aaff", lw=1
    )
)
ax.text(
    21,
    42.5,
    "Lavabo",
    ha="center",
    va="center",
    fontsize=7,
    color="#3a0ca3",
    fontweight="bold",
)

# Spazio di manovra centrale
ax.add_patch(
    plt.Circle((115, 107.5), 25, color="#adb5bd", fill=False, ls="--", lw=1.5)
)
ax.text(
    115,
    107.5,
    "Ø 120 cm\nSpazio manovra",
    ha="center",
    va="center",
    fontsize=6,
    color="#495057",
)

# Etichetta Bagno Principale
ax.text(
    75,
    130,
    "BAGNO PRINCIPALE",
    ha="center",
    va="center",
    fontsize=8,
    fontweight="bold",
    color="#1d3557",
)

ax.axis("off")
st.pyplot(fig)
