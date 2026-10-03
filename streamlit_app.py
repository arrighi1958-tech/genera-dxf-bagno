import io
import ezdxf
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Progetto Esecutivo - Doppia Sala da Bagno", layout="centered"
)
st.title("Progetto Esecutivo - Doppia Sala da Bagno (247x215 cm)")
st.markdown(
    "Pianta esecutiva completa e definitiva: ora il file DXF scaricabile"
    " contiene tutti i dettagli geometrici (muri, cavedio, doccia e"
    " sanitari)."
)


def genera_dxf_bytes():
  doc = ezdxf.new(dxfversion="AC1024")
  msp = doc.modelspace()

  doc.layers.add("MURI_ESTERNI", color=7)
  doc.layers.add("PARETI_INTERNE", color=3)
  doc.layers.add("SANITARI", color=5)
  doc.layers.add("CAVEDIO", color=2)
  doc.layers.add("DOCCIA", color=4)

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

  # Cavedio E2
  cav_x, cav_w, cav_h = 70.0, 56.5, 16.0
  cav_y = 215 - cav_h
  msp.add_lwpolyline(
      [
          (cav_x, cav_y),
          (cav_x + cav_w, cav_y),
          (cav_x + cav_w, cav_y + cav_h),
          (cav_x, cav_y + cav_h),
      ],
      close=True,
      dxfattribs={"layer": "CAVEDIO"},
  )

  # Doccia (80x105)
  doc_x, doc_y, doc_w, doc_h = 247 - 80, 215 - 105, 80, 105
  msp.add_lwpolyline(
      [
          (doc_x, doc_y),
          (doc_x + doc_w, doc_y),
          (doc_x + doc_w, doc_y + doc_h),
          (doc_x, doc_y + doc_h),
      ],
      close=True,
      dxfattribs={"layer": "DOCCIA"},
  )

  # Sanitari Bagno Piccolo
  # WC Piccolo
  wcp_x, wcp_y, wcp_w, wcp_h = bp_x + 6, 72, 34, 38
  msp.add_lwpolyline(
      [
          (wcp_x, wcp_y),
          (wcp_x + wcp_w, wcp_y),
          (wcp_x + wcp_w, wcp_y + wcp_h),
          (wcp_x, wcp_y + wcp_h),
      ],
      close=True,
      dxfattribs={"layer": "SANITARI"},
  )

  # Bidet Piccolo
  bidp_x, bidp_y, bidp_w, bidp_h = bp_x + 46, 72, 34, 38
  msp.add_lwpolyline(
      [
          (bidp_x, bidp_y),
          (bidp_x + bidp_w, bidp_y),
          (bidp_x + bidp_w, bidp_y + bidp_h),
          (bidp_x, bidp_y + bidp_h),
      ],
      close=True,
      dxfattribs={"layer": "SANITARI"},
  )

  # Lavabo Piccolo (spostato in basso verso la parete C)
  lavp_x, lavp_y, lavp_w, lavp_h = bp_x, 6, 28, 42
  msp.add_lwpolyline(
      [
          (lavp_x, lavp_y),
          (lavp_x + lavp_w, lavp_y),
          (lavp_x + lavp_w, lavp_y + lavp_h),
          (lavp_x, lavp_y + lavp_h),
      ],
      close=True,
      dxfattribs={"layer": "SANITARI"},
  )

  # Sanitari Bagno Principale (Parete D: 215 cm)
  h_san = 35.0
  w_san = 38.0
  gap = (215.0 - (3 * h_san)) / 4.0
  y_wc = 215.0 - gap - h_san
  y_bidet = y_wc - gap - h_san
  y_lavabo = y_bidet - gap - h_san

  for y_s in [y_wc, y_bidet, y_lavabo]:
    msp.add_lwpolyline(
        [(0, y_s), (w_san, y_s), (w_san, y_s + h_san), (0, y_s + h_san)],
        close=True,
        dxfattribs={"layer": "SANITARI"},
    )

  stream = io.StringIO()
  doc.write(stream)
  return stream.getvalue().encode("utf-8")


# Pulsante Download DXF
dxf_data = genera_dxf_bytes()
st.download_button(
    label="📥 Scarica il file DXF Esecutivo Completo",
    data=dxf_data,
    file_name="bagno_doppio_completo.dxf",
    mime="application/dxf",
)

# Anteprima Grafica Completa (Streamlit)
st.subheader("Anteprima Grafica - Configurazione Completa")
fig, ax = plt.subplots(figsize=(9, 8))
ax.set_xlim(-25, 272)
ax.set_ylim(-25, 240)
ax.set_aspect("equal")

ax.add_patch(
    plt.Rectangle(
        (0, 0), 247, 215, edgecolor="#212529", facecolor="#f8f9fa", lw=2
    )
)

# Cavedio E2
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

# Porte sulla Parete C
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

# Bagno piccolo
bp_x = 247 - 90
ax.add_patch(
    plt.Rectangle((bp_x, 0), 90, 110, edgecolor="#2b9348", facecolor="#d8f3dc", lw=1.5)
)
ax.text(
    bp_x + 45,
    55,
    "Bagno Piccolo\n90 x 110 cm",
    ha="center",
    va="center",
    fontsize=7,
    color="#2b9348",
    fontweight="bold",
)

# Doccia
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

# Sanitari Bagno Piccolo
ax.add_patch(
    plt.Rectangle(
        (bp_x + 6, 72), 34, 38, edgecolor="#2b9348", facecolor="#ffffff", lw=1
    )
)
ax.text(
    bp_x + 23,
    91,
    "WC",
    ha="center",
    va="center",
    fontsize=6,
    color="#2b9348",
    fontweight="bold",
)
ax.add_patch(
    plt.Rectangle(
        (bp_x + 46, 72), 34, 38, edgecolor="#2b9348", facecolor="#ffffff", lw=1
    )
)
ax.text(
    bp_x + 63,
    91,
    "Bidet",
    ha="center",
    va="center",
    fontsize=6,
    color="#2b9348",
    fontweight="bold",
)
ax.add_patch(
    plt.Rectangle(
        (bp_x, 6), 28, 42, edgecolor="#2b9348", facecolor="#ffffff", lw=1
    )
)
ax.text(
    bp_x + 14,
    27,
    "Lav.",
    ha="center",
    va="center",
    fontsize=6,
    color="#2b9348",
    fontweight="bold",
)

# Sanitari Bagno Principale
h_san = 35.0
w_san = 38.0
gap = (215.0 - (3 * h_san)) / 4.0
y_wc = 215.0 - gap - h_san
y_bidet = y_wc - gap - h_san
y_lavabo = y_bidet - gap - h_san

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

ax.axis("off")
st.pyplot(fig)
