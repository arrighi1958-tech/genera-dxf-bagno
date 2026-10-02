import streamlit as st
import ezdxf
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Progetto Esecutivo - Doppia Sala da Bagno", layout="centered")
st.title("Progetto Esecutivo - Doppia Sala da Bagno")
st.markdown("Pianta esecutiva basata sulle dimensioni reali: **215 x 247 cm** (Pareti A/C = 215 cm, B/D = 247 cm).")

def genera_dxf_bytes():
    doc = ezdxf.new(dxfversion='AC1024')
    msp = doc.modelspace()
    
    doc.layers.add('MURI_ESTERNI', color=7)
    doc.layers.add('PARETI_INTERNE', color=3)
    doc.layers.add('SANITARI', color=5)
    doc.layers.add('CAVEDIO', color=2)
    
    x0, y0 = 0.0, 0.0
    w_netto, h_netto = 215.0, 247.0  # A/C = 215 cm, B/D = 247 cm[cite: 11]
    spessore = 16.0
    
    # Muri esterni
    msp.add_lwpolyline([
        (x0 - spessore, y0 - spessore),
        (x0 + w_netto + spessore, y0 - spessore),
        (x0 + w_netto + spessore, y0 + h_netto + spessore),
        (x0 - spessore, y0 + h_netto + spessore)
    ], close=True, dxfattribs={'layer': 'MURI_ESTERNI'})
    
    # Perimetro interno (215 x 247)
    msp.add_lwpolyline([
        (x0, y0), (x0 + w_netto, y0), 
        (x0 + w_netto, y0 + h_netto), (x0, y0 + h_netto)
    ], close=True, dxfattribs={'layer': 'PARETI_INTERNE'})
    
    # Bagno piccolo in basso a destra (90 x 110 cm)
    bp_w, bp_h = 90.0, 110.0
    bp_x, bp_y = x0 + w_netto - bp_w, y0
    msp.add_lwpolyline([
        (bp_x, bp_y), (bp_x + bp_w, bp_y), 
        (bp_x + bp_w, bp_y + bp_h), (bp_x, bp_y + bp_h)
    ], close=True, dxfattribs={'layer': 'PARETI_INTERNE'})

    # Doccia in alto a destra sopra il bagno piccolo (80 x 105 cm)
    doc_w, doc_h = 80.0, 105.0
    doc_x = x0 + w_netto - doc_w
    doc_y = y0 + h_netto - doc_h
    msp.add_lwpolyline([
        (doc_x, doc_y), (doc_x + doc_w, doc_y), 
        (doc_x + doc_w, y0 + h_netto), (x0, y0 + h_netto)
    ], close=True, dxfattribs={'layer': 'SANITARI'})

    stream = io.StringIO()
    doc.write(stream)
    return stream.getvalue().encode('utf-8')

# Pulsante Download DXF
dxf_data = genera_dxf_bytes()
st.download_button(
    label="📥 Scarica il file DXF Esecutivo Corretto",
    data=dxf_data,
    file_name="bagno_esecutivo_orientato.dxf",
    mime="application/dxf"
)

# Anteprima Grafica Completa
st.subheader("Anteprima Grafica - Distribuzione Interna e Aperture")
fig, ax = plt.subplots(figsize=(7, 8))
ax.set_xlim(-20, 235)
ax.set_ylim(-20, 267)
ax.set_aspect('equal')

# Contenitore principale (215 x 247)[cite: 11]
ax.add_patch(plt.Rectangle((0, 0), 215, 247, edgecolor='#212529', facecolor='#f8f9fa', lw=2))

# Cavedio / Pilastro sulla Parete B (16 x 54 cm)
ax.add_patch(plt.Rectangle((215 - 16, 123), 16, 54, edgecolor='#d90429', facecolor='#ffccd5', lw=1.5))
ax.text(215 - 8, 150, "Cavedio E2", ha='center', va='center', fontsize=6, color='#d90429', fontweight='bold', rotation=90)

# Porta sulla Parete D (70 cm a 90.5 cm dall'angolo C-D)
ax.plot([0, 0], [90.5, 90.5 + 70], color='#fb8500', lw=4)
ax.text(-10, 90.5 + 35, "Porta 70 cm", ha='right', va='center', rotation=90, fontsize=7, color='#fb8500', fontweight='bold')

# Finestra 1 sulla Parete B (63 cm a 4.5 cm dall'angolo A-B)
ax.plot([215, 215], [247 - 4.5, 247 - 4.5 - 63], color='#0077b6', lw=4)
ax.text(223, 247 - 36, "Finestra 1", ha='left', va='center', fontsize=7, color='#0077b6', fontweight='bold')

# Finestra 2 sulla Parete B (65 cm a 51 cm dall'angolo C-B)
ax.plot([215, 215], [51, 51 + 65], color='#0077b6', lw=4)
ax.text(223, 51 + 32.5, "Finestra 2", ha='left', va='center', fontsize=7, color='#0077b6', fontweight='bold')

# Bagno piccolo in basso a destra (90 x 110)
ax.add_patch(plt.Rectangle((215-90, 0), 90, 110, edgecolor='#2b9348', facecolor='#d8f3dc', lw=1.5))
ax.text(215-45, 55, "Bagno Piccolo\n90 x 110 cm", ha='center', va='center', fontsize=8, color='#2b9348', fontweight='bold')

# Doccia in alto a destra sopra il bagno piccolo (80 x 105)
ax.add_patch(plt.Rectangle((215-80, 247-105), 80, 105, edgecolor='#0077b6', facecolor='#caf0f8', lw=1.5))
ax.text(215-40, 247-52.5, "Doccia\n(80x105 cm)", ha='center', va='center', fontsize=7, color='#0077b6', fontweight='bold')

# Sanitari equidistanti lungo la parete sinistra (Parete D: 247 cm)[cite: 11]
h_san = 40.0
w_san = 38.0
gap = (247.0 - (3 * h_san)) / 4.0

y_wc = 247.0 - gap - h_san
y_bidet = y_wc - gap - h_san
y_lavabo = y_bidet - gap - h_san

# WC
ax.add_patch(plt.Rectangle((0, y_wc), w_san, h_san, edgecolor='#3a0ca3', facecolor='#e0aaff', lw=1))
ax.text(w_san/2, y_wc + h_san/2, "WC", ha='center', va='center', fontsize=7, color='#3a0ca3', fontweight='bold')

# Bidet
ax.add_patch(plt.Rectangle((0, y_bidet), w_san, h_san, edgecolor='#3a0ca3', facecolor='#e0aaff', lw=1))
ax.text(w_san/2, y_bidet + h_san/2, "Bidet", ha='center', va='center', fontsize=7, color='#3a0ca3', fontweight='bold')

# Lavabo
ax.add_patch(plt.Rectangle((0, y_lavabo), w_san, h_san, edgecolor='#3a0ca3', facecolor='#e0aaff', lw=1))
ax.text(w_san/2, y_lavabo + h_san/2, "Lavabo", ha='center', va='center', fontsize=7, color='#3a0ca3', fontweight='bold')

# Etichetta centrale bagno principale
ax.text(65, 123.5, "BAGNO PRINCIPALE", ha='center', va='center', fontsize=9, fontweight='bold', color='#1d3557')

# Quote perimetrali esterne corrette
ax.text(107.5, 253, "Parete A: 215 cm", ha='center', va='bottom', fontsize=8, color='black')
ax.text(107.5, -6, "Parete C: 215 cm", ha='center', va='top', fontsize=8, color='black')
ax.text(-6, 123.5, "Parete D: 247 cm", ha='right', va='center', rotation=90, fontsize=8, color='black')
ax.text(221, 123.5, "Parete B: 247 cm", ha='left', va='center', rotation=270, fontsize=8, color='black')

ax.axis('off')
st.pyplot(fig)
