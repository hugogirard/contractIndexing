from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
from datetime import datetime, timedelta
import random
import os

# Sample data for generating contracts
COMPANIES = [
    {"name": "Contoso Corporation", "rep": "Angel Brown", "title": "CTO", 
     "address": "1 Microsoft Way, Redmond, Washington 98045"},
    {"name": "Fabrikam Inc", "rep": "Sarah Johnson", "title": "VP Operations",
     "address": "123 Tech Drive, Seattle, Washington 98101"},
    {"name": "Northwind Traders", "rep": "Michael Chen", "title": "Director",
     "address": "456 Commerce Street, Bellevue, Washington 98004"},
    {"name": "Fourth Coffee", "rep": "Emily Davis", "title": "CFO",
     "address": "789 Business Ave, Tacoma, Washington 98402"},
]

VENDORS = [
    {"name": "AdventureWorks Cycles", "rep": "Aaron Smith", "title": "Sales Manager",
     "address": "98 NW Test Street, Suite 50, Bellevue, Washington 98007"},
    {"name": "TechServe Solutions", "rep": "David Martinez", "title": "Account Manager",
     "address": "321 Service Road, Redmond, Washington 98052"},
    {"name": "CloudHost Systems", "rep": "Lisa Anderson", "title": "Business Development",
     "address": "654 Cloud Lane, Seattle, Washington 98103"},
    {"name": "DataCenter Pro", "rep": "James Wilson", "title": "Director of Sales",
     "address": "987 Server Drive, Kirkland, Washington 98033"},
]

CONTRACT_TYPES = [
    {
        "title": "WEB HOSTING AGREEMENT",
        "services": "web hosting services",
        "access_limit": random.randint(200000, 600000),
        "overage_fee": round(random.uniform(0.005, 0.02), 3),
        "response_time": "24 hours"
    },
    {
        "title": "CLOUD SERVICES AGREEMENT",
        "services": "cloud computing and storage services",
        "access_limit": random.randint(500000, 1000000),
        "overage_fee": round(random.uniform(0.01, 0.03), 3),
        "response_time": "12 hours"
    },
    {
        "title": "SOFTWARE LICENSE AGREEMENT",
        "services": "software licensing and support services",
        "access_limit": random.randint(100000, 300000),
        "overage_fee": round(random.uniform(0.02, 0.05), 3),
        "response_time": "48 hours"
    },
    {
        "title": "MAINTENANCE AND SUPPORT AGREEMENT",
        "services": "technical support and maintenance services",
        "access_limit": random.randint(150000, 400000),
        "overage_fee": round(random.uniform(0.01, 0.025), 3),
        "response_time": "24 hours"
    },
]


def generate_contract_date():
    """Generate a random contract date within the last 3 years"""
    days_ago = random.randint(0, 1095)
    return datetime.now() - timedelta(days=days_ago)


def create_contract_pdf(filename, company, vendor, contract_type, contract_date):
    """Generate a PDF contract"""
    doc = SimpleDocTemplate(filename, pagesize=letter,
                          rightMargin=0.75*inch, leftMargin=0.75*inch,
                          topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.black,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14
    )
    
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Title
    title = Paragraph(contract_type["title"], title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Introduction paragraph
    date_str = contract_date.strftime("%d day of %B, %Y")
    intro_text = f"""This {contract_type["title"].title()} is entered as of the {date_str} 
    ("<b>Effective Date</b>") by and between <b>{company['name']}</b>, a corporation, 
    having its principal place of business at {company['address']} ("<b>{company['name'].split()[0]}</b>") 
    and <b>{vendor['name']}</b>, a corporation having its principal place of business at 
    {vendor['address']} ("<b>{vendor['name'].split()[0]}</b>")."""
    
    elements.append(Paragraph(intro_text, body_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Terms paragraph
    terms_text = f"""This agreement shall void and nullify any and all previous agreements to this 
    date between {company['name'].split()[0]} and {vendor['name'].split()[0]}."""
    elements.append(Paragraph(terms_text, body_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Fees paragraph
    fees_text = f"""There shall be no additional fees of any kind paid to {company['name'].split()[0]}, 
    other than those listed within this agreement for {contract_type['services']} and/or bandwidth usage. 
    The initial term of this contract is for {random.choice([12, 24, 36])} months with a maximum of 
    {contract_type['access_limit']:,} accesses thereafter payment shall be ${contract_type['overage_fee']} 
    (one-half cent) per access. {vendor['name'].split()[0]} must monitor and remit this amount to 
    {company['name'].split()[0]} by no later than Wednesday for accesses used from the previous week 
    (Monday thru Sunday)."""
    elements.append(Paragraph(fees_text, body_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Support paragraph
    support_text = f"""{company['name'].split()[0]} must provide a person(s) to correct any technical 
    problems (Server being down or slow, {contract_type['response_time']} per day, 7 days per week. 
    This person(s) must be available by beeper or telephone. {vendor['name'].split()[0]} shall provide 
    this same 24 hour support at the broadcast location."""
    elements.append(Paragraph(support_text, body_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Governing law paragraph
    gov_text = f"""This Agreement shall be governed by and construed in accordance with the internal 
    laws of the state of Washington. Such laws shall be applicable to this agreement without regard to 
    its conflicts of law provisions. Disputes arising out of or related to the performance (or the 
    alleged failure to perform) of either party must not be performed entirely within such state."""
    elements.append(Paragraph(gov_text, body_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Final agreement paragraph
    final_text = """All parties have read and fully agree to all terms and conditions as set forth 
    in this Web Hosting Agreement."""
    elements.append(Paragraph(final_text, body_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Signature section
    sig_data = [
        [Paragraph(f"<b>{company['name']}</b>", signature_style), 
         Paragraph(f"<b>{vendor['name']}</b>", signature_style)],
        [Paragraph(f"By: {company['rep']}", signature_style), 
         Paragraph(f"By: {vendor['rep']}", signature_style)],
        [Paragraph(f"Title: {company['title']}", signature_style), 
         Paragraph(f"Title: {vendor['title']}", signature_style)],
        [Paragraph(f"<font name='Courier'>{company['rep']}</font>", signature_style), 
         Paragraph(f"<font name='Courier'>{vendor['rep']}</font>", signature_style)],
    ]
    
    sig_table = Table(sig_data, colWidths=[3.25*inch, 3.25*inch])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    
    elements.append(sig_table)
    
    # Build PDF
    doc.build(elements)
    print(f"Generated: {filename}")


def main():
    """Generate multiple contract PDFs"""
    print("Starting contract PDF generation...")
    
    # Create output directory if it doesn't exist
    output_dir = "generated_contracts"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate 5-10 random contracts
    num_contracts = random.randint(5, 10)
    
    for i in range(num_contracts):
        # Randomly select company, vendor, and contract type
        company = random.choice(COMPANIES)
        vendor = random.choice(VENDORS)
        contract_type = CONTRACT_TYPES[i % len(CONTRACT_TYPES)]
        contract_date = generate_contract_date()
        
        # Generate filename
        filename = os.path.join(
            output_dir, 
            f"contract_{i+1:03d}_{company['name'].replace(' ', '_')}_{contract_date.strftime('%Y%m%d')}.pdf"
        )
        
        # Create the contract
        create_contract_pdf(filename, company, vendor, contract_type, contract_date)
    
    print(f"\nSuccessfully generated {num_contracts} contracts in '{output_dir}' directory!")


if __name__ == "__main__":
    main()