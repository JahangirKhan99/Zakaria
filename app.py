from flask import Flask, request, send_file, make_response
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io

app = Flask(__name__)

@app.route("/")
def home():
    return open("index.html").read()

@app.route("/generate", methods=["POST"])
def generate():
    name = request.form["name"]
    cnic = request.form["cnic"]
    bank = request.form["bank"]
    amount = request.form["amount"]
    date = request.form["date"]

    packet = io.BytesIO()
    c = canvas.Canvas(packet)
    c.setFont("Helvetica", 10)

    # ✅ Final safe coordinates
    c.drawString(80, 560, name)
    c.drawString(80, 535, cnic)
    c.drawString(80, 510, bank)
    c.drawRightString(470, 560, amount)
    c.drawString(420, 535, date)

    c.save()
    packet.seek(0)

    template = PdfReader("PassportChallanForm.pdf")
    overlay = PdfReader(packet)

    page = template.pages[0]
    page.merge_page(overlay.pages[0])

    writer = PdfWriter()
    writer.add_page(page)

    output = "Final_Challan.pdf"
    with open(output, "wb") as f:
        writer.write(f)

    response = make_response(send_file(output, mimetype="application/pdf"))
    response.headers["Content-Disposition"] = "inline; filename=Challan.pdf"
    return response

if __name__ == "__main__":
    app.run(debug=True)
