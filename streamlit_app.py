import streamlit as st
import ezdxf
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Progetto Esecutivo - Stato di Fatto", layout="centered")
st.title("Progetto Esecutivo - Stato di Fatto (Rilievo)")
st.markdown("Pianta basata sulle dimensioni reali: **215 x 247 cm** (Pareti A/C = 215 cm, Pareti B/D = 247 cm).")

def genera_dxf_bytes():
    doc = ezdxf.new(dxfversion='AC1024')
    msp = doc.modelspace()
    
    doc.layers.add('MURI_ESTERNI', color=7)
    doc.layers.add('PARETI_INTERNE', color=3)
    doc.layers.add('SANITARI', color=5)
    doc.layers.add('CAVEDIO', color=2)
    doc.layers.add('APERTURE', color=4)
    
    x0, y0 = 0.0, 0.0
    w_netto, h_netto = 215.0, 247.0  # A/C = 215, B/D = 247[cite: 14]
    spessore = 10.0
    
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
    
    # Cavedio / Pilastro (54 x 16 cm) attaccato alla Parete B[cite: 14]
    cav_w, cav_h = 16.0, 54.0
    cav_x, cav_y = w_netto - cav_w, 123.0
    msp.add_lwpolyline([
        (cav_x, cav_y), (cav_x + cav_w, cav_y),
        (cav_x + cav_w, cav_y + cav_h), (cav_x, cav_y + cav_h)
    ], close=True, dxfattribs={'layer': 'CAVEDIO'})

    stream = io.StringIO()
    doc.write(stream)
    return stream.getvalue().encode('utf-8')

# Pulsante Download DXF
dxf_data = genera_dxf_bytes()
st.download_button(
    label="📥 Scarica il file DXF Ufficiale (215x247 cm)",
    data=dxf_data,
    file_name="bagno_215_247_esecutivo.dxf",
    mime="application/dxf"
)

# Anteprima Grafica con orientamento e dettagli reali
st.subheader("Anteprima Grafica - Disposizione Spazi e Aperture")
fig, ax = plt.subplots(figsize=(7, 8))
ax.set_xlim(-20, 235)
ax.set_ylim(-20, 267)
ax.set_aspect('equal')

# Contenitore principale (215 x 247)[cite: 14]
ax.add_patch(plt.Rectangle((0, 0), 215, 247, edgecolor='#212529', facecolor='#f8f9fa', lw=2))

# Cavedio / Pilastro (54 x 16 cm) sulla Parete B[cite: 14]
ax.add_patch(plt.Rectangle((215 - 16, 123), 16, 54, edgecolor='#d90429', facecolor='#ffccd5', lw=1.5))
ax.text(215 - 8, 150, "Cavedio E2\n16x54 cm", ha='center', va='center', fontsize=6, color='#d90429', fontweight='bold', rotation=90)

# Porta su Parete D (70 cm, posizionata a 90.5 cm dall'angolo C-D)[cite: 14]
ax.plot([0, 0], [90.5, 90.5 + 70], color='#fb8500', lw=4)
ax.text(-10, 90.5 + 35, "Porta 70 cm", ha='right', va='center', rotation=90, fontsize=7, color='#fb8500', fontweight='bold')

# Finestra 1 su Parete B (63 cm, a 4.5 cm dall'angolo A-B)[cite: 14]
ax.plot([215, 215], [247 - 4.5, 247 - 4.5 - 63], color='#0077b6', lw=4)
ax.text(223, 247 - 36, "Finestra 1 (63 cm)", ha='left', va='center', fontsize=7, color='#0077b6', fontweight='bold')

# Finestra 2 su Parete B (65 cm, a 51 cm dall'angolo C-B)[cite: 14]
ax.plot([215, 215], [51, 51 + 65], color='#0077b6', lw=4)
ax.text(223, 51 + 32.5, "Finestra 2 (65 cm)", ha='left', va='center', fontsize=7, color='#0077b6', fontweight='bold')

# Etichetta centrale
ax.text(107.5, 123.5, "STATO DI FATTO\n(215 x 247 cm)", ha='center', va='center', fontsize=9, fontweight='bold', color='#1d3557', alpha=0.4)

# Quote perimetrali corrette
ax.text(107.5, 253, "Parete A: 215 cm", ha='center', va='bottom', fontsize=8, color='black')
ax.text(107.5, -6, "Parete C: 215 cm", ha='center', va='top', fontsize=8, color='black')
ax.text(-6, 123.5, "Parete D: 247 cm", ha='right', va='center', rotation=90, fontsize=8, color='black')
ax.text(221, 123.5, "Parete B: 247 cm", ha='left', va='center', rotation=270, fontsize=8, color='black')

ax.axis('off')
st.pyplot(fig)
