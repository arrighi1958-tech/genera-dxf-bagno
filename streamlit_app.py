import streamlit as st
import ezdxf
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Progetto Esecutivo - Doppia Sala da Bagno", layout="centered")
st.title("Progetto Esecutivo - Doppia Sala da Bagno")
st.markdown("Generatore DXF e anteprima grafica basati sul rilievo ufficiale (**247 x 215 cm**).")

def genera_dxf_bytes():
    doc = ezdxf.new(dxfversion='AC1024')
    msp = doc.modelspace()
    
    doc.layers.add('MURI_ESTERNI', color=7)
    doc.layers.add('PARETI_INTERNE', color=3)
    doc.layers.add('SANITARI', color=5)
    
    x0, y0 = 0.0, 0.0
    w_netto, h_netto = 247.0, 215.0
    spessore = 16.0
    
    # Muri esterni
    msp.add_lwpolyline([
        (x0 - spessore, y0 - spessore),
        (x0 + w_netto + spessore, y0 - spessore),
        (x0 + w_netto + spessore, y0 + h_netto + spessore),
        (x0 - spessore, y0 + h_netto + spessore)
    ], close=True, dxfattribs={'layer': 'MURI_ESTERNI'})
    
    # Perimetro interno (247x215)
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

    # Doccia a raso ruotata (82 x 132 cm) in alto a destra
    doc_w, doc_h = 82.0, 132.0
    doc_x = bp_x - doc_w
    doc_y = y0 + h_netto - doc_h
    msp.add_lwpolyline([
        (doc_x, doc_y), (doc_x + doc_w, doc_y), 
        (doc_x + doc_w, doc_y + doc_h), (doc_x, doc_y + doc_h)
    ], close=True, dxfattribs={'layer': 'SANITARI'})

    stream = io.StringIO()
    doc.write(stream)
    return stream.getvalue().encode('utf-8')

# Pulsante Download DXF
dxf_data = genera_dxf_bytes()
st.download_button(
    label="📥 Scarica il file DXF Esecutivo Definitivo",
    data=dxf_data,
    file_name="bagno_esecutivo_definitivo.dxf",
    mime="application/dxf"
)

# Anteprima Grafica Corretta
st.subheader("Anteprima Grafica - Distribuzione Interna")
fig, ax = plt.subplots(figsize=(8, 7))
ax.set_xlim(-20, 267)
ax.set_ylim(-20, 235)
ax.set_aspect('equal')

# Contenitore principale (247 x 215)
ax.add_patch(plt.Rectangle((0, 0), 247, 215, edgecolor='#212529', facecolor='#f8f9fa', lw=2))

# Bagno piccolo in basso a destra (90 x 110)
ax.add_patch(plt.Rectangle((247-90, 0), 90, 110, edgecolor='#2b9348', facecolor='#d8f3dc', lw=1.5))
ax.text(247-45, 55, "Bagno Piccolo\n90 x 110 cm", ha='center', va='center', fontsize=8, color='#2b9348', fontweight='bold')

# Doccia a raso ruotata in alto a destra (82 x 132)
ax.add_patch(plt.Rectangle((247-90-82, 215-132), 82, 132, edgecolor='#0077b6', facecolor='#caf0f8', lw=1.5))
ax.text(247-90-41, 215-66, "Doccia a raso\n(82 x 132 cm)", ha='center', va='center', fontsize=7, color='#0077b6', fontweight='bold')

# Sanitari Bagno Principale (Parete Sinistra D - ben distanziati)
# WC (in alto)
ax.add_patch(plt.Rectangle((0, 215 - 55), 38, 40, edgecolor='#3a0ca3', facecolor='#e0aaff', lw=1))
ax.text(19, 215 - 35, "WC", ha='center', va='center', fontsize=7, color='#3a0ca3', fontweight='bold')

# Bidet (al centro)
ax.add_patch(plt.Rectangle((0, 215 - 120), 38, 40, edgecolor='#3a0ca3', facecolor='#e0aaff', lw=1))
ax.text(19, 215 - 100, "Bidet", ha='center', va='center', fontsize=7, color='#3a0ca3', fontweight='bold')

# Lavabo (in basso)
ax.add_patch(plt.Rectangle((0, 25), 42, 65, edgecolor='#3a0ca3', facecolor='#e0aaff', lw=1))
ax.text(21, 57.5, "Lavabo", ha='center', va='center', fontsize=7, color='#3a0ca3', fontweight='bold')

# Etichetta centrale bagno principale
ax.text(100, 120, "BAGNO PRINCIPALE", ha='center', va='center', fontsize=10, fontweight='bold', color='#1d3557')

# Quote perimetrali esterne
ax.text(123.5, 221, "Parete A: 247 cm", ha='center', va='bottom', fontsize=8, color='black')
ax.text(123.5, -6, "Parete C: 247 cm", ha='center', va='top', fontsize=8, color='black')
ax.text(-6, 107.5, "Parete D: 215 cm", ha='right', va='center', rotation=90, fontsize=8, color='black')
ax.text(253, 107.5, "Parete B: 215 cm", ha='left', va='center', rotation=270, fontsize=8, color='black')

ax.axis('off')
st.pyplot(fig)
