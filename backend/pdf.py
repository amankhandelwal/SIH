
import pdfkit

config = pdfkit.configuration(wkhtmltopdf='/opt/wkhtmltox/bin/wkhtmltopdf')
pdfkit.from_file('challan.html', 'challan.pdf', configuration=config)

'''
from flask import Flask, request, Response ,jsonify, render_template, make_response

import pdfkit

#import wkhtmltopdf

#import numpy as np

app = Flask(__name__)



@app.route("/pdf")
def pdf_template():
	config = pdfkit.configuration(wkhtmltopdf='/opt/wkhtmltox/bin/wkhtmltopdf')
	pdf = pdfkit.from_file('templates/homepage.html', 'out.pdf', configuration=config)
	response = make_response(pdf)
	response.headers['Content-Type'] = 'application/pdf'
	response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
	return response



if __name__ == "__main__":
	app.run(host="127.0.0.2", port=5005, debug=True)

'''