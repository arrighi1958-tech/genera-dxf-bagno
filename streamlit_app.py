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
    
    # Layer dedicati
    doc.layers.add('MURI_ESTERNI', color=7)
    doc.layers.add('PARETI_INTERNE', color=3)
    doc.layers.add('SANITARI', color=5)
    doc.layers.add('TESTI', color=1)
    
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
    
    # Perimetro interno netto (247x215)
    msp.add_lwpolyline([
        (x0, y0), (x0 + w_netto, y0), 
        (x0 + w_netto, y0 + h_netto), (x0, y0 + h_netto)
    ], close=True, dxfattribs={'layer': 'PARETI_INTERNE'})
    
    # Bagno piccolo in basso a destra (105 x 90 cm)
    bp_w, bp_h = 105.0, 90.0
    bp_x, bp_y = x0 + w_netto - bp_w, y0
    msp.add_lwpolyline([
        (bp_x, bp_y), (bp_x + bp_w, bp_y), 
        (bp_x + bp_w, bp_y + bp_h), (bp_x, bp_y + bp_h)
    ], close=True, dxfattribs={'layer': 'PARETI_INTERNE'})
    
    # Colonna scarico E2 (centro-superiore)
    msp.add_lwpolyline([
        (100, y0 + h_netto - 35), (170, y0 + h_netto - 35),
        (170, y0 + h_netto), (100, y0 + h_netto)
    ], close=True, dxfattribs={'layer': 'PARETI_INTERNE'})

    # Doccia a raso (132 x 82 cm) in alto a destra
    doc_w, doc_h = 132.0, 82.0
    doc_x = bp_x - doc_w
    doc_y = y0 + h_netto - doc_h
    msp.add_lwpolyline([
        (doc_x, doc_y), (doc_x + doc_w, doc_y), 
        (doc_x + doc_w, doc_y + doc_h), (doc_x, doc_y + doc_h)
    ], close=True, dxfattribs={'layer': 'SANITARI'})

    # Sanitari Bagno Principale (Parete Sinistra / D)
    msp.add_lwpolyline([(x0, y0 + h_netto - 70), (x0 + 38, y0 + h_netto - 70), (x0 + 38, y0 + h_netto - 20), (x0, y0 + h_netto - 20)], close=True, dxfattribs={'layer': 'SANITARI'}) # WC
    msp.add_lwpolyline([(x0, y0 + h_netto - 130), (x0 + 38, y0 + h_netto - 130), (x0 + 38, y0 + h_netto - 80), (x0, y0 + h_netto - 80)], close=True, dxfattribs={'layer': 'SANITARI'}) # Bidet
    msp.add_lwpolyline([(x0, y0 + 30), (x0 + 42, y0 + 30), (x0 + 42, y0 + 100), (x0, y0 + 100)], close=True, dxfattribs={'layer': 'SANITARI'}) # Lavabo

    # Sanitari Bagno Piccolo
    msp.add_lwpolyline([(bp_x + 15, bp_y + 45), (bp_x + 52, bp_y + 45), (bp_x + 52, bp_y + 80), (bp_x + 15, bp_y + 80)], close=True, dxfattribs={'layer': 'SANITARI'}) # WC piccolo
    msp.add_lwpolyline([(bp_x + 60, bp_y + 45), (bp_x + 95, bp_y + 45), (bp_x + 95, bp_y + 80), (bp_x + 60, bp_y + 80)], close=True, dxfattribs={'layer': 'SANITARI'}) # Bidet piccolo

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

# Anteprima Grafica Dettagliata
st.subheader("Anteprima Grafica - Distribuzione Interna")
fig, ax = plt.subplots(figsize=(8, 7))
ax.set_xlim(-25, 272)
ax.set_ylim(-25, 240)
ax.set_aspect('equal')

# Muri perimetrali
ax.add_patch(plt.Rectangle((0, 0), 247, 215, edgecolor='#212529', facecolor='#f8f9fa', lw=2))
# Bagno piccolo (105x90)
ax.add_patch(plt.Rectangle((247-105, 0), 105, 90, edgecolor='#2b9348', facecolor='#d8f3dc', lw=1.5))
# Colonna E2
ax.add_patch(plt.Rectangle((100, 215-35), 70, 35, edgecolor='#495057', facecolor='#adb5bd', lw=1))
# Doccia a raso (132x82)
ax.add_patch(plt.Rectangle((247-105-132, 215-82), 132, 82, edgecolor='#0077b6', facecolor='#caf0f8', lw=1.5))

# Sanitari parete sinistra
ax.add_patch(plt.Rectangle((0, 215-70), 38, 50, edgecolor='#3a0ca3', facecolor='#e0aaff', lw=1)) # WC
ax.add_patch(plt.Rectangle((0, 215-130), 38, 50, edgecolor='#3a0ca3', facecolor='#e0aaff', lw=1)) # Bidet
ax.add_patch(plt.Rectangle((0, 30), 42, 70, edgecolor='#3a0ca3', facecolor='#e0aaff', lw=1)) # Lavabo

# Testi descrittivi
ax.text(80, 130, "BAGNO PRINCIPALE\n(247 x 215 cm)", ha='center', va='center', fontsize=9, fontweight='bold', color='#1d3557')
ax.text(247-52.5, 45, "Bagno Piccolo\n105x90 cm", ha='center', va='center', fontsize=8, color='#2b9348', fontweight='bold')
ax.text(247-105-66, 215-41, "Doccia a raso\n132 x 82 cm", ha='center', va='center', fontsize=8, color='#0077b6', fontweight='bold')
ax.text(135, 215-17, "Colonna E2", ha='center', va='center', fontsize=7, color='white', fontweight='bold')

# Quote perimetrali
ax.text(123.5, 223, "Parete A: 247 cm", ha='center', va='bottom', fontsize=8, color='black')
ax.text(123.5, -8, "Parete C: 247 cm", ha='center', va='top', fontsize=8, color='black')
ax.text(-8, 107.5, "Parete D: 215 cm", ha='right', va='center', rotation=90, fontsize=8, color='black')
ax.text(255, 107.5, "Parete B: 215 cm", ha='left', va='center', rotation=270, fontsize=8, color='black')

ax.axis('off')
st.pyplot(fig)
