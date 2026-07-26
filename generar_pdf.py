from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def crear_columna_cuerpo(titulo, datos, styles):
    """
    Crea un cuerpo/talón con altura fija y sin datos innecesarios.
    Apto para A4 o Impresora Térmica Epson.
    """
    
    style_emp = ParagraphStyle('Emp', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor('#1a365d'), alignment=1)
    style_tag = ParagraphStyle('Tag', fontName='Helvetica-Bold', fontSize=7.5, leading=9, alignment=1, textColor=colors.HexColor('#2b6cb0'))
    
    style_lbl = ParagraphStyle('Lbl', fontName='Helvetica', fontSize=7, leading=8.5, textColor=colors.HexColor('#4a5568'))
    style_val = ParagraphStyle('Val', fontName='Helvetica-Bold', fontSize=7.5, leading=9, textColor=colors.HexColor('#1a365d'))
    style_big = ParagraphStyle('Big', fontName='Helvetica-Bold', fontSize=11, leading=13, textColor=colors.HexColor('#1a365d'))

    filas = [
        # Encabezado del cuerpo
        [Paragraph(f"<b>{datos['empresa']}</b>", style_emp)],
        [Paragraph(f"<b>*** {titulo} ***</b>", style_tag)],
        [Spacer(1, 4)],
        
        # Pasajero
        [Paragraph("PASAJERO", style_lbl)],
        [Paragraph(f"{datos['pasajero_nombre']}", style_val)],
        [Paragraph(f"DOC: {datos['pasajero_doc']} ({datos['pasajero_nac']})", style_lbl)],
        [Spacer(1, 4)],
        
        # Recorrido
        [Paragraph("ORIGEN - DESTINO", style_lbl)],
        [Paragraph(f"{datos['origen']}", style_val)],
        [Paragraph(f"➜ {datos['destino']}", style_val)],
        [Spacer(1, 4)],
        
        # Salida
        [Paragraph("FECHA Y HORA DE SALIDA", style_lbl)],
        [Paragraph(f"{datos['fecha_salida']} ({datos['dia_semana']}) - {datos['hora_salida']} hs", style_val)],
        [Spacer(1, 4)],
        
        # Asiento y Precio
        [Paragraph(f"ASIENTO: <font size=10 color='#1a365d'><b>{datos['asiento']}</b></font>", style_val)],
        [Paragraph(f"PRECIO: <font size=9 color='#1a365d'><b>{datos['precio']}</b></font>", style_val)],
        [Spacer(1, 4)],
        
        # Control / Datos emisor
        [Paragraph(f"PAGO: {datos['forma_pago']}", style_lbl)],
        [Paragraph(f"CÓDIGO: <b>{datos['codigo_pasaje']}</b>", style_lbl)],
        [Paragraph(f"ANUNCIO: {datos['se_anuncia_a']}", style_lbl)],
        [Paragraph(f"EMISIÓN: {datos['fecha_emision']}", style_lbl)],
    ]

    # Tabla con ancho y altura uniforme para todas las columnas
    t = Table(filas, colWidths=[240])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#cbd5e0')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    return t

def generar_pasaje_simetrico(datos, salida="pasaje_horizontal.pdf"):
    # Hoja A4 Horizontal
    doc = SimpleDocTemplate(
        salida,
        pagesize=landscape(A4),
        rightMargin=15, leftMargin=15, topMargin=15, bottomMargin=15
    )
    styles = getSampleStyleSheet()

    # Generar los 3 cuerpos EXACTAMENTE IGUALES
    c1 = crear_columna_cuerpo("TALÓN EMPRESA", datos, styles)
    c2 = crear_columna_cuerpo("TALÓN GUARDA", datos, styles)
    c3 = crear_columna_cuerpo("TALÓN PASAJERO", datos, styles)

    # Línea vertical de corte punteada
    div_v = Paragraph("<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|<br/>|", 
                      ParagraphStyle('Div', fontName='Helvetica', fontSize=8, textColor=colors.gray, alignment=1))

    # Poner las 3 columnas alineadas en paralelo con la misma altura
    tabla_principal = Table(
        [[c1, div_v, c2, div_v, c3]], 
        colWidths=[245, 12, 245, 12, 245]
    )
    tabla_principal.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 1),
        ('RIGHTPADDING', (0,0), (-1,-1), 1),
    ]))

    doc.build([tabla_principal])
    print("¡Pasaje térmico / A4 generado con éxito!")

# --- DATOS LIMPIOS Y SIMPLIFICADOS ---
mis_datos = {
    "empresa": "R.U. SRL y Otros - UTE",
    "se_anuncia_a": "CHEVALLIER A MENDOZA",
    
    "pasajero_nombre": "VARGAS, SEBASTIAN",
    "pasajero_doc": "DNI 31737613",
    "pasajero_nac": "ARGENTINA",
    
    "origen": "RETIRO Buenos Aires",
    "destino": "San Martin (MZA)",
    "fecha_salida": "23/07/2026",
    "dia_semana": "Jueves",
    "hora_salida": "18:00",
    "asiento": "65",
    
    "precio": "$ 131000.00",
    "forma_pago": "EFEC Efectivo",
    "fecha_emision": "21/07/2026 14:52",
    "codigo_pasaje": "22526669"
}

if __name__ == "__main__":
    generar_pasaje_simetrico(mis_datos)