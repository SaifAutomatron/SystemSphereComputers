from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import datetime
import boto3

class InvoiceGenerator:
    def __init__(self, customer_name, items, transaction_id, total, order_date):
        self.customer_name = customer_name
        self.items = items
        self.transaction_id = transaction_id
        self.total = total
        self.order_date = order_date

    def generate_invoice(self, output_path='invoice.pdf'):
        # Create a PDF document
        doc = SimpleDocTemplate(output_path)

        # Create story for PDF content
        story = []

        # Add content to the story
        styles = getSampleStyleSheet()
        invoice_title = Paragraph("<u>Invoice</u>", styles['Title'])
        customer_info = Paragraph(f"Customer: {self.customer_name}<br/>Transaction ID: {self.transaction_id}<br/>Order Date: {self.format_date(self.order_date)}", styles['Normal'])

        story.extend([invoice_title, customer_info])

        # Create a table for items and total
        table_data = [['Item', 'Price', 'Quantity', 'Subtotal']]
        for item in self.items:
            subtotal = item['price'] * item['quantity']
            table_data.append([item['name'], f"€{item['price']}", item['quantity'], f"€{subtotal}"])

        # Add a row for the total
        table_data.append(['Total', '', '', f'€{self.total}'])

        item_table = Table(table_data, colWidths=[200, 100, 100, 100])
        item_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                        ('SPAN', (0, -1), (-2, -1)),
                                        ('VALIGN', (0, -1), (-2, -1), 'MIDDLE')]))

        story.append(item_table)

        # Build the PDF document
        doc.build(story)
        print("Invoice generated")

    def format_date(self, date_str):
        # Format date in a readable way
        try:
            date_obj = datetime.datetime.strptime(date_str, '%d-%m-%Y')
            return date_obj.strftime('%B %d, %Y')
        except ValueError:
            return date_str
    
    def upload_to_s3(self, bucket_name, s3_key):
        # Connect to S3
        s3_client = boto3.client('s3', region_name='us-east-1')  

        # Upload the generated PDF to S3
        with open('invoice.pdf', 'rb') as file:
            s3_client.upload_fileobj(file, bucket_name, s3_key)

        print(f"Invoice uploaded to S3: s3://{bucket_name}/{s3_key}")

