import streamlit as st
import io
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="Generador de Pasajes", page_icon="🚌", layout="wide")
st.title("🚌 Generador de Pasajes de Colectivo")

with st.form("form_pasaje"):
    col_emp, col_pas, col_vía = st.columns(3)
    with col_emp:
        empresa = st.text_input("Empresa", value="FLECHA BUS")
        se_anuncia_a = st.text_input("Se anuncia a", value="CHEVALLIER A MENDOZA")
        forma_pago = st.selectbox("Forma de Pago", ["EFEC Efectivo", "TARJETA Débito", "TARJETA Crédito"])
        fecha_emision = st.text_input("Emisión", value="26/07/2026 19:15")
        codigo_pasaje = st.text_input("Código", value="22526669")
    with col_pas:
        pasajero_nombre = st.text_input("Nombre", value="VARGAS, SEBASTIAN")
        pasajero_doc = st.text_input("Documento", value="DNI 31737613")
        pasajero_nac = st.text_input("Nacionalidad", value="ARGENTINA")
    with col_vía:
        origen = st.text_input("Origen", value="RETIRO Buenos Aires")
        destino = st.text_input("Destino", value="San Martin (MZA)")
        fecha_salida = st.text_input("Fecha Salida", value="26/07/2026")
        dia_semana = st.text_input("Día", value="Domingo")
        hora_salida = st.text_input("Hora Salida", value="18:00")
        asiento = st.text_input("Asiento", value="65")
        precio = st.text_input("Precio", value="$ 131000.00")

    btn_generar = st.form_submit_button("🔥 GENERAR PASAJE PDF", use_container_width=True)

def crear_columna_cuerpo(titulo, datos, styles):
    style_emp = ParagraphStyle('Emp', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.HexColor('#1a365d'), alignment=1)
    style_tag = ParagraphStyle('Tag', fontName='Helvetica-Bold', fontSize=8.5, leading=10, alignment=1, textColor=colors.HexColor('#2b6cb0'))
    style_lbl = ParagraphStyle('Lbl', fontName='Helvetica-Bold', fontSize=7.5, leading=9, textColor=colors.HexColor('#718096'))
    style_val = ParagraphStyle('Val', fontName='Helvetica-Bold', fontSize=8.5, leading=10.5, textColor=colors.HexColor('#1a365d'))
    style_txt = ParagraphStyle('Txt', fontName='Helvetica', fontSize=8, leading=10, textColor=colors.HexColor('#2d3748'))

    filas = [
        [Paragraph(f"<b>{datos['empresa']}</b>", style_emp)],
        [Paragraph(f"<b>*** {titulo} ***</b>", style_tag)],
        [Spacer(1, 4)],
        [Paragraph("PASAJERO", style_lbl)],
        [Paragraph(f"{datos['pasajero_nombre']}", style_val)],
        [Paragraph(f"DOC: {datos['pasajero_doc']} ({datos['pasajero_nac']})", style_txt)],
        [Spacer(1, 4)],
        [Paragraph("ORIGEN - DESTINO", style_lbl)],
        [Paragraph(f"{datos['origen']}", style_val)],
        [Paragraph(f"➜ {datos['destino']}", style_val)],
        [Spacer(1, 4)],
        [Paragraph("FECHA Y HORA DE SALIDA", style_lbl)],
        [Paragraph(f"{datos['fecha_salida']} ({datos['dia_semana']}) - {datos['hora_salida']} hs", style_val)],
        [Spacer(1, 4)],
        [Paragraph(f"ASIENTO: <font size=11 color='#1a365d'><b>{datos['asiento']}</b></font>", style_val)],
        [Paragraph(f"PRECIO: <font size=10 color='#1a365d'><b>{datos['precio']}</b></font>", style_val)],
        [Spacer(1, 4)],
        [Paragraph(f"PAGO: {datos['forma_pago']}", style_txt)],
        [Paragraph(f"CÓDIGO: <b>{datos['codigo_pasaje']}</b>", style_txt)],
        [Paragraph(f"ANUNCIO: {datos['se_anuncia_a']}", style_txt)],
        [Paragraph(f"EMISIÓN: {datos['fecha_emision']}", style_txt)],
    ]

    t = Table(filas, colWidths=[255])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    return t

if btn_generar:
    datos = {
        "empresa": empresa, "se_anuncia_a": se_anuncia_a, "pasajero_nombre": pasajero_nombre,
        "pasajero_doc": pasajero_doc, "pasajero_nac": pasajero_nac, "origen": origen,
        "destino": destino, "fecha_salida": fecha_salida, "dia_semana": dia_semana,
        "hora_salida": hora_salida, "asiento": asiento, "precio": precio,
        "forma_pago": forma_pago, "fecha_emision": fecha_emision, "codigo_pasaje": codigo_pasaje
    }
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=14, leftMargin=14, topMargin=14, bottomMargin=14)
    styles = getSampleStyleSheet()

    c1 = crear_columna_cuerpo("TALÓN EMPRESA", datos, styles)
    c2 = crear_columna_cuerpo("TALÓN GUARDA", datos, styles)
    c3 = crear_columna_cuerpo("TALÓN PASAJERO", datos, styles)
    div_v = Paragraph("<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|", ParagraphStyle('Div', fontName='Helvetica', fontSize=8, textColor=colors.gray, alignment=1))

    tabla_principal = Table([[c1, div_v, c2, div_v, c3]], colWidths=[257, 10, 257, 10, 257])
    tabla_principal.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))

    doc.build([tabla_principal])
    buffer.seek(0)

    st.success("¡Pasaje listo!")
    st.download_button(label="📥 DESCARGAR PASAJE PDF", data=buffer, file_name=f"pasaje_{pasajero_nombre.replace(' ', '_')}.pdf", mime="application/pdf", use_container_width=True)