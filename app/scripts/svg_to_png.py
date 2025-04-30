import cairosvg

# Caminho do SVG de entrada e do PNG de saída
svg_path = "entrada.svg"
png_path = "saida.png"

# Exporta como PNG com alta resolução (ex: 300 DPI equivalente)
cairosvg.svg2png(url="assets/GeofisicaApp.svg", write_to="assets/GeofisicaApp.png", output_width=3000, output_height=3000)


