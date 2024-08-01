import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# Function to create a PDF receipt
def create_pdf_receipt(filename, items, total, interest, grand_total):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setLineWidth(.3)
    c.setFont('Helvetica', 12)

    c.drawString(30, 750, 'FuelFlex Receipt')
    c.drawString(30, 735, '------------------------------------------')

    c.drawString(30, 705, 'Item')
    c.drawString(250, 705, 'Cost')
    c.drawString(500, 705, 'Total')

    line_height = 690
    for item, cost in items.items():
        c.drawString(30, line_height, item)
        c.drawString(250, line_height, f'R {cost}')
        line_height -= 15

    c.drawString(30, line_height, '------------------------------------------')
    line_height -= 15
    c.drawString(30, line_height, f'Subtotal: R {total}')
    line_height -= 15
    c.drawString(30, line_height, f'Interest (11.5%): R {interest}')
    line_height -= 15
    c.drawString(30, line_height, f'Grand Total: R {grand_total}')
    line_height -= 15

    c.save()

# Example usage
items = {'Fuel': 500}
total = 500
interest = total * INTEREST_RATE
grand_total = total + interest

create_pdf_receipt('receipt.pdf', items, total, interest, grand_total)