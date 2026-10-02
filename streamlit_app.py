import streamlit as st
import ezdxf
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Progetto Esecutivo - Doppia Sala da Bagno", layout="centered")
st.title("Progetto Esecutivo - Doppia Sala da Bagno")
st.markdown("Pianta esecutiva basata sulle dimensioni ufficiali: **247 x 215 cm** (Pareti A/C = 247 cm, Pareti B/D = 215 cm).")

def genera_dxf_bytes():
    doc = ezdxf.new(dxfversion='AC1024')
    msp = doc.modelspace()
    
    doc.layers.add('MURI_ESTERNI', color=7)
    doc.layers.add('PARETI_INTERNE', color=3)
    doc.layers.add('SANITARI', color=5)
    doc.layers.add('CAVEDIO', color=2)
    
    x0, y0 = 0.0, 0.0
    w_netto, h_netto = 247.0, 215.0  # A/C = 247 cm, B/D = 215 cm
    spessore = 16.0
    
    # Muri esterni
    msp.add_lwpolyline([
        (x0 - spessore, y0 - spessore),
        (x0 + w_netto + spessore, y0 - spessore),
        (x0 + w_netto + spessore, y0 + h_netto + spessore),
        (x0 - spessore, y0 + h_netto + spessore)
    ], close=True, dxfattribs={'layer': 'MURI_ESTERNI'})
    
    # Perimetro interno (247 x 215)
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

    # Cavedio / Colonna E2 (Parete Superiore A)
    cav_w, cav_h = 35.0, 22.0
    cav_x = 100.0
    cav_y = y0 + h_netto - cav_h
    msp.add_lwpolyline([
        (cav_x, cav_y), (cav_x + cav_w, cav_y),
        (cav_x + cav_w, y0 + h_netto), (cav_x, y0 + h_netto)
    ], close=True, dxfattribs={'layer': 'CAVEDIO'})

    # Doccia in alto a destra sopra il bagno piccolo (80 x 105 cm)
    doc_w, doc_h = 80.0, 105.0
    doc_x = x0 + w_netto - doc_w
    doc_y = y0 + h_netto - doc_h
    msp.add_lwpolyline([
        (doc_x, doc_y), (doc_x + doc_w, doc_y), 
        (doc_x + doc_w, y0 + h_netto), (doc_x, y0 + h_netto)
    ], close=True, dxfattribs={'layer': 'SANITARI'})

    stream = io.StringIO()
    doc.write(stream)
    return stream.getvalue().encode('utf-8')

# Pulsante Download DXF
dxf_data = genera_dxf_bytes()
st.download_button(
    label="📥 Scarica il file DXF Esecutivo Definitivo (247x215)",
    data=dxf_data,
    file_name="bagno_esecutivo_247_215.dxf",
    mime="application/dxf"
)

# Anteprima Grafica Pulita
st.subheader("Anteprima Grafica - Distribuzione Interna")
fig, ax = plt.subplots(figsize=(8, 7))
ax.set_xlim(-20, 267)
ax.set_ylim(-20, 235)
ax.set_aspect('equal')

# Contenitore principale (247 x 215)
ax.add_patch(plt.Rectangle((0, 0), 247, 215, edgecolor='#212529', facecolor='#f8f9fa', lw=2))

# Cavedio / Colonna E2 (Parete Superiore A)
ax.add_patch(plt.Rectangle((95, 215-25), 35, 25, edgecolor='#d90429', facecolor='#ffccd5', lw=1.5))
ax.text(112.5, 215-12.5, "Cavedio E2", ha='center', va='center', fontsize=6, color='#d90429', fontweight='bold')

# Bagno piccolo in basso a destra (90 x 110)
ax.add_patch(plt.Rectangle((247-90, 0), 90, 110, edgecolor='#2b9348', facecolor='#d8f3dc', lw=1.5))
ax.text(247-45, 55, "Bagno Piccolo\n90 x 110 cm", ha='center', va='center', fontsize=8, color='#2b9348', fontweight='bold')

# Doccia in alto a destra sopra il bagno piccolo (80 x 105)
ax.add_patch(plt.Rectangle((247-80, 215-105), 80, 105, edgecolor='#0077b6', facecolor='#caf0f8', lw=1.5))
ax.text(247-40, 215-52.5, "Doccia\n(80x105 cm)", ha='center', va='center', fontsize=7, color='#0077b6', fontweight='bold')

# Sanitari equidistanti lungo la parete sinistra (altezza totale 215 cm)
h_san = 40.0
w_san = 38.0
gap = (215.0 - (3 * h_san)) / 4.0

y_wc = 215.0 - gap - h_san
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
ax.text(80, 120, "BAGNO PRINCIPALE", ha='center', va='center', fontsize=10, fontweight='bold', color='#1d3557')

# Quote perimetrali esterne corrette (A e C = 247, B e D = 215)
ax.text(123.5, 221, "Parete A: 247 cm", ha='center', va='bottom', fontsize=8, color='black')
ax.text(123.5, -6, "Parete C: 247 cm", ha='center', va='top', fontsize=8, color='black')
ax.text(-6, 107.5, "Parete D: 215 cm", ha='right', va='center', rotation=90, fontsize=8, color='black')
ax.text(253, 107.5, "Parete B: 215 cm", ha='left', va='center', rotation=270, fontsize=8, color='black')

ax.axis('off')
st.pyplot(fig)
