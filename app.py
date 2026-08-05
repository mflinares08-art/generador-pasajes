import streamlit as st
import io
from datetime import datetime
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="Generador de Pasajes", page_icon="🚌", layout="wide")
st.title("🚌 Generador de Pasajes de Colectivo")

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def obtener_dia_semana(fecha_str):
    try:
        fecha_dt = datetime.strptime(fecha_str.strip(), "%d/%m/%Y")
        return DIAS_SEMANA[fecha_dt.weekday()]
    except Exception:
        return "Día inválido"

# Subidor de logo en la barra lateral o dentro del form
st.sidebar.header("🎨 Personalización")
logo_file = st.sidebar.file_uploader("Subir Logo de Empresa (PNG o JPG)", type=["png", "jpg", "jpeg"])

with st.form("form_pasaje"):
    col_emp, col_pas, col_vía = st.columns(3)
    with col_emp:
        empresa = st.text_input("Empresa", value="FLECHA BUS")
        se_anuncia_a = st.text_input("Se anuncia a", value="CHEVALLIER A MENDOZA")
        forma_pago = st.selectbox("Forma de Pago", ["EFEC Efectivo", "TARJETA Débito", "TARJETA Crédito"])
        numero_pasaje = st.text_input("Número de Pasaje", value="22526669")
    with col_pas:
        pasajero_nombre = st.text_input("Nombre del Pasajero", value="VARGAS, SEBASTIAN")
        pasajero_doc = st.text_input("Documento", value="DNI 31737613")
        pasajero_nac = st.text_input("Nacionalidad", value="ARGENTINA")
    with col_vía:
        origen = st.text_input("Origen", value="RETIRO Buenos Aires")
        destino = st.text_input("Destino", value="San Martin (MZA)")
        fecha_salida = st.text_input("Fecha Salida (DD/MM/AAAA)", value="26/07/2026")
        hora_salida = st.text_input("Hora Salida", value="18:00")
        asiento = st.text_input("Asiento", value="65")
        precio = st.text_input("Precio", value="$ 131000.00")

    dia_detectado = obtener_dia_semana(fecha_salida)
    st.info(f"📅 **Día de la semana detectado automáticamente:** {dia_detectado}")

    btn_generar = st.form_submit_button("🔥 GENERAR PASAJE PDF", use_container_width=True)

def crear_columna_cuerpo(titulo_talon, datos, logo_img, styles):
    style_emp = ParagraphStyle('Emp', fontName='Helvetica-Bold', fontSize=10, leading=12, alignment=1, textColor=colors.black)
    style_val = ParagraphStyle('Val', fontName='Helvetica-Bold', fontSize=8.5, leading=10, textColor=colors.black)
    style_txt = ParagraphStyle('Txt', fontName='Helvetica', fontSize=8, leading=9.5, textColor=colors.black)
    style_talon = ParagraphStyle('Talon', fontName='Helvetica-Bold', fontSize=6.5, leading=8, alignment=1, textColor=colors.black)

    # Si hay logo cargado, creamos el elemento de imagen para ReportLab
    img_element = ""
    if logo_img:
        # Guardar la imagen temporalmente en memoria para ReportLab
        img_buffer = io.BytesIO()
        logo_img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        # Escalamos la imagen a un tamaño adecuado para el ticket
        img_element = RLImage(img_buffer, width=80, height=30)

    filas = [
        # Encabezado: Logo (si hay) y Nombre de la Empresa
        [img_element if img_element else Paragraph(f"<b>{datos['empresa']}</b>", style_emp), 
         Paragraph(f"<b>{datos['empresa']}</b>" if img_element else "", style_emp)],
        
        [Spacer(1, 2), Spacer(1, 2)],
        
        # Pasajero y Documento
        [Paragraph(f"<b>PASAJERO:</b> {datos['pasajero_nombre']}", style_val), 
         Paragraph(f"<b>DOC:</b> {datos['pasajero_doc']} ({datos['pasajero_nac']})", style_txt)],
        
        # Origen y Destino
        [Paragraph(f"<b>ORIGEN:</b> {datos['origen']}", style_txt), 
         Paragraph(f"<b>DESTINO:</b> {datos['destino']}", style_val)],
        
        # Salida y Asiento
        [Paragraph(f"<b>SALIDA:</b> {datos['fecha_salida']} ({datos['dia_semana']}) - {datos['hora_salida']} hs", style_val),
         Paragraph(f"<b>ASIENTO:</b> <font size=10><b>{datos['asiento']}</b></font>", style_val)],
        
        # Precio, Pago y Nro Pasaje
        [Paragraph(f"<b>PRECIO:</b> <font size=9.5><b>{datos['precio']}</b></font>", style_val),
         Paragraph(f"<b>PAGO:</b> {datos['forma_pago']}", style_txt)],
        
        [Paragraph(f"<b>Nº PASAJE:</b> <b>{datos['numero_pasaje']}</b>", style_txt),
         Paragraph(f"<b>ANUNCIO:</b> {datos['se_anuncia_a']}", style_txt)],
        
        [Spacer(1, 4), Spacer(1, 4)],
        # Leyenda de comprobante y talón al final de cada cuerpo
        [Paragraph(f"<b>{titulo_talon}<br/>COMPROBANTE DE BOLETO - SOLO VALIDO PARA ABORDAR</b>", style_talon), Paragraph("", style_talon)]
    ]

    t = Table(filas, colWidths=[140, 115])
    t.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)) if not img_element else ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('SPAN', (0, 7), (1, 7)),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('PADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t

if btn_generar:
    # Cargar la imagen del logo si el usuario la subió
    logo_img = None
    if logo_file is not None:
        logo_img = Image.open(logo_file)

    datos = {
        "empresa": empresa, "se_anuncia_a": se_anuncia_a, "pasajero_nombre": pasajero_nombre,
        "pasajero_doc": pasajero_doc, "pasajero_nac": pasajero_nac, "origen": origen,
        "destino": destino, "fecha_salida": fecha_salida, "dia_semana": dia_detectado,
        "hora_salida": hora_salida, "asiento": asiento, "precio": precio,
        "forma_pago": forma_pago, "numero_pasaje": numero_pasaje
    }
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=10, leftMargin=10, topMargin=10, bottomMargin=10)
    styles = getSampleStyleSheet()

    c1 = crear_columna_cuerpo("TALÓN EMPRESA", datos, logo_img, styles)
    c2 = crear_columna_cuerpo("TALÓN GUARDA", datos, logo_img, styles)
    c3 = crear_columna_cuerpo("TALÓN PASAJERO", datos, logo_img, styles)
    div_v = Paragraph("<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|", ParagraphStyle('Div', fontName='Helvetica', fontSize=7, textColor=colors.black, alignment=1))

    tabla_principal = Table([[c1, div_v, c2, div_v, c3]], colWidths=[257, 10, 257, 10, 257])
    tabla_principal.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0)
    ]))

    doc.build([tabla_principal])
    buffer.seek(0)

    st.success("¡Pasaje generado con leyenda de abordaje!")
    st.download_button(label="📥 DESCARGAR PASAJE PDF", data=buffer, file_name=f"pasaje_{pasajero_nombre.replace(' ', '_')}.pdf", mime="application/pdf", use_container_width=True)