import streamlit as st
import ezdxf
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Rilievo Stato Attuale - Bagno", layout="centered")
st.title("Stato di Fatto - Rilievo Bagno")
st.markdown("Generatore DXF e anteprima grafica basati sulla scheda di rilievo ufficiale (**247 x 215 cm**).")

def genera_dxf_bytes():
    doc = ezdxf.new(dxfversion='AC1024')
    msp = doc.modelspace()
    
    doc.layers.add('MURI_ESTERNI', color=7)
    doc.layers.add('PARETI_INTERNE', color=3)
    doc.layers.add('SANITARI', color=5)
    doc.layers.add('CAVEDIO', color=2)
    
    x0, y0 = 0.0, 0.0
    w_netto, h_netto = 247.0, 215.0  # Pareti D/B = 247, A/C = 215
    spessore = 10.0
    
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
    
    # Cavedio / Pilastro (54 x 16 cm) da scheda rilievo[cite: 14]
    cav_w, cav_h = 54.0, 16.0
    cav_x, cav_y = 70.0, 123.0
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
    label="📥 Scarica il file DXF Stato Attuale",
    data=dxf_data,
    file_name="bagno_stato_attuale.dxf",
    mime="application/dxf"
)

# Anteprima Grafica con i dati della scheda
st.subheader("Anteprima Grafica - Stato di Fatto (Rilievo)")
fig, ax = plt.subplots(figsize=(8, 7))
ax.set_xlim(-20, 267)
ax.set_ylim(-20, 235)
ax.set_aspect('equal')

# Contenitore principale (Parete D/B = 247, A/C = 215)
ax.add_patch(plt.Rectangle((0, 0), 247, 215, edgecolor='#212529', facecolor='#f8f9fa', lw=2))

# Cavedio / Pilastro (54 x 16 cm)[cite: 14]
ax.add_patch(plt.Rectangle((70, 123), 54, 16, edgecolor='#d90429', facecolor='#ffccd5', lw=1.5))
ax.text(97, 131, "Cavedio / Pilastro\n54 x 16 cm", ha='center', va='center', fontsize=6, color='#d90429', fontweight='bold')

# Finestra 1 su Parete B (63 cm, a 4.5 cm dall'angolo A-B)[cite: 14]
ax.plot([247, 247], [215 - 4.5, 215 - 4.5 - 63], color='#0077b6', lw=4)
ax.text(253, 215 - 36, "Finestra 1\n63 cm", ha='left', va='center', fontsize=7, color='#0077b6', fontweight='bold')

# Finestra 2 su Parete B (65 cm, a 51 cm dall'angolo C-B)[cite: 14]
ax.plot([247, 247], [51, 51 + 65], color='#0077b6', lw=4)
ax.text(253, 51 + 32.5, "Finestra 2\n65 cm", ha='left', va='center', fontsize=7, color='#0077b6', fontweight='bold')

# Porta su Parete D (70 cm)[cite: 14]
ax.plot([0, 0], [86.5, 86.5 + 70], color='#fb8500', lw=4)
ax.text(-12, 86.5 + 35, "Porta 70 cm", ha='right', va='center', rotation=90, fontsize=7, color='#fb8500', fontweight='bold')

# Sanitari ed elementi esistenti (da scheda)[cite: 14]
ax.add_patch(plt.Rectangle((10, 150), 37, 55, edgecolor='#3a0ca3', facecolor='#e0aaff', lw=1))
ax.text(28.5, 177.5, "WC", ha='center', va='center', fontsize=7, color='#3a0ca3', fontweight='bold')

ax.add_patch(plt.Rectangle((10, 85), 37, 55, edgecolor='#3a0ca3', facecolor='#e0aaff', lw=1))
ax.text(28.5, 112.5, "Bidet", ha='center', va='center', fontsize=7, color='#3a0ca3', fontweight='bold')

ax.add_patch(plt.Rectangle((10, 20), 63, 52, edgecolor='#3a0ca3', facecolor='#e0aaff', lw=1))
ax.text(41.5, 46, "Lavabo", ha='center', va='center', fontsize=7, color='#3a0ca3', fontweight='bold')

ax.add_patch(plt.Rectangle((120, 20), 73, 120, edgecolor='#0077b6', facecolor='#caf0f8', lw=1))
ax.text(156.5, 80, "Doccia\n73 x 120 cm", ha='center', va='center', fontsize=7, color='#0077b6', fontweight='bold')

ax.add_patch(plt.Rectangle((150, 150), 60, 65, edgecolor='#432818', facecolor='#dda15e', lw=1))
ax.text(180, 182.5, "Lavatrice\n60x65 cm", ha='center', va='center', fontsize=7, color='#432818', fontweight='bold')

# Etichetta generale
ax.text(123.5, 107.5, "STATO ATTUALE (RILIEVO)", ha='center', va='center', fontsize=9, fontweight='bold', color='#1d3557', alpha=0.3)

# Quote perimetrali
ax.text(123.5, 221, "Parete A: 215 cm", ha='center', va='bottom', fontsize=8, color='black')
ax.text(123.5, -6, "Parete C: 215 cm", ha='center', va='top', fontsize=8, color='black')
ax.text(-6, 107.5, "Parete D: 247 cm", ha='right', va='center', rotation=90, fontsize=8, color='black')
ax.text(253, 107.5, "Parete B: 247 cm", ha='left', va='center', rotation=270, fontsize=8, color='black')

ax.axis('off')
st.pyplot(fig)
