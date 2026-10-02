import streamlit as st
import ezdxf
import matplotlib.pyplot as plt
import io

st.title("Generatore DXF - Proposta Bagno (247x215 cm)")
st.markdown("Questa applicazione genera il file DXF basato sulle proporzioni corrette con la doccia a raso e i sanitari.")

def genera_dxf_bytes():
    doc = ezdxf.new(dxfversion='AC1024')
    msp = doc.modelspace()
    
    doc.layers.add('MURI_ESTERNI', color=7)
    doc.layers.add('PARETI_INTERNE', color=3)
    doc.layers.add('SANITARI', color=5)
    
    x0, y0 = 0.0, 0.0
    w_netto, h_netto = 247.0, 215.0
    spessore = 16.0
    
    msp.add_lwpolyline([
        (x0 - spessore, y0 - spessore),
        (x0 + w_netto + spessore, y0 - spessore),
        (x0 + w_netto + spessore, y0 + h_netto + spessore),
        (x0 - spessore, y0 + h_netto + spessore)
    ], close=True, dxfattribs={'layer': 'MURI_ESTERNI'})
    
    msp.add_lwpolyline([
        (x0, y0), (x0 + w_netto, y0), 
        (x0 + w_netto, y0 + h_netto), (x0, y0 + h_netto)
    ], close=True, dxfattribs={'layer': 'PARETI_INTERNE'})
    
    bp_w, bp_h = 105.0, 90.0
    bp_x, bp_y = x0 + w_netto - bp_w, y0
    msp.add_lwpolyline([
        (bp_x, bp_y), (bp_x + bp_w, bp_y), 
        (bp_x + bp_w, bp_y + bp_h), (bp_x, bp_y + bp_h)
    ], close=True, dxfattribs={'layer': 'PARETI_INTERNE'})
    
    doc_w, doc_h = 132.0, 82.0
    doc_x, doc_y = bp_x - doc_w, y0 + h_netto - doc_h
    msp.add_lwpolyline([
        (doc_x, doc_y), (doc_x + doc_w, doc_y), 
        (doc_x + doc_w, doc_y + doc_h), (doc_x, doc_y + doc_h)
    ], close=True, dxfattribs={'layer': 'SANITARI'})

    stream = io.StringIO()
    doc.write(stream)
    return stream.getvalue().encode('utf-8')

dxf_data = genera_dxf_bytes()
st.download_button(
    label="📥 Scarica il file DXF per il CAD",
    data=dxf_data,
    file_name="proposta_bagno_variante2.dxf",
    mime="application/dxf"
)

st.subheader("Anteprima dello Schema Tecnico")
fig, ax = plt.subplots(figsize=(6, 5))
ax.set_xlim(-20, 267)
ax.set_ylim(-20, 235)
ax.set_aspect('equal')

ax.add_patch(plt.Rectangle((0, 0), 247, 215, edgecolor='black', facecolor='#f8f9fa', lw=1.5))
ax.add_patch(plt.Rectangle((247-105, 0), 105, 90, edgecolor='green', facecolor='#d8f3dc', lw=1.2))
ax.add_patch(plt.Rectangle((247-105-132, 215-82), 132, 82, edgecolor='blue', facecolor='#caf0f8', lw=1.2))
ax.text(123.5, 107.5, "Bagno Principale\n247 x 215 cm", ha='center', va='center', fontsize=9, fontweight='bold')
ax.text(247-52.5, 45, "Bagno\nPiccolo", ha='center', va='center', fontsize=7)
ax.text(247-105-66, 215-41, "Doccia a raso\n132x82 cm", ha='center', va='center', fontsize=7)

ax.axis('off')
st.pyplot(fig)
