import pdfkit

config = pdfkit.configuration(wkhtmltopdf='/opt/wkhtmltox/bin/wkhtmltopdf')
pdfkit.from_file('templates/homepage.html', 'ou.pdf', configuration=config)