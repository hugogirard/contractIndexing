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
     "address": "1 Microsoft Way, Redmond, Washington, 98058",
     "reference": "Contoso"},
    {"name": "Fabrikam Inc", "rep": "Sarah Johnson", "title": "VP Operations",
     "address": "123 Tech Drive, Seattle, Washington, 98101",
     "reference": "Fabrikam"},
    {"name": "Northwind Traders", "rep": "Michael Chen", "title": "Director",
     "address": "456 Commerce Street, Bellevue, Washington, 98004",
     "reference": "Northwind"},
    {"name": "Fourth Coffee", "rep": "Emily Davis", "title": "CFO",
     "address": "789 Business Ave, Tacoma, Washington, 98402",
     "reference": "FourthCoffee"},
    {"name": "Woodgrove Bank", "rep": "Robert Taylor", "title": "Operations Manager",
     "address": "555 Finance Plaza, Redmond, Washington, 98052",
     "reference": "Woodgrove"},
]

VENDORS = [
    {"name": "AdventureWorks Cycles", "rep": "Aaron Smith", "title": "Sales Manager",
     "address": "98 NW 76st Street, Suite 54, Bellevue, Washington, 98007",
     "reference": "AdventureWorks"},
    {"name": "TechServe Solutions", "rep": "David Martinez", "title": "Account Manager",
     "address": "321 Service Road, Redmond, Washington, 98052",
     "reference": "TechServe"},
    {"name": "CloudHost Systems", "rep": "Lisa Anderson", "title": "Business Development",
     "address": "654 Cloud Lane, Seattle, Washington, 98103",
     "reference": "CloudHost"},
    {"name": "DataCenter Pro", "rep": "James Wilson", "title": "Director of Sales",
     "address": "987 Server Drive, Suite 200, Kirkland, Washington, 98033",
     "reference": "DataCenter"},
    {"name": "Alpine Ski House", "rep": "Patricia Moore", "title": "General Manager",
     "address": "777 Mountain Road, Bellevue, Washington, 98006",
     "reference": "Alpine"},
]

CONTRACT_TYPES = [
    {
        "title": "WEB HOSTING AGREEMENT",
        "type": "hosting",
        "services": "web hosting services",
        "jurisdiction_region": "Washington",
        "jurisdiction_clause": "This Agreement shall be governed by and construed in accordance with the internal laws of the State of Washington applicable to agreements made and to be performed entirely within such state."
    },
    {
        "title": "CLOUD SERVICES AGREEMENT",
        "type": "cloud",
        "services": "cloud computing and storage services",
        "jurisdiction_region": "Washington",
        "jurisdiction_clause": "This Agreement shall be governed by and construed in accordance with the internal laws of the State of Washington applicable to agreements made and to be performed entirely within such state."
    },
    {
        "title": "SOFTWARE LICENSE AGREEMENT",
        "type": "license",
        "services": "software licensing and support services",
        "jurisdiction_region": "California",
        "jurisdiction_clause": "This Agreement shall be governed by and construed in accordance with the internal laws of the State of California applicable to agreements made and to be performed entirely within such state."
    },
    {
        "title": "MAINTENANCE AND SUPPORT AGREEMENT",
        "type": "support",
        "services": "technical support and maintenance services",
        "jurisdiction_region": "Washington",
        "jurisdiction_clause": "This Agreement shall be governed by and construed in accordance with the internal laws of the State of Washington applicable to agreements made and to be performed entirely within such state."
    },
    {
        "title": "DATA PROCESSING AGREEMENT",
        "type": "data",
        "services": "data processing and analytics services",
        "jurisdiction_region": "New York",
        "jurisdiction_clause": "This Agreement shall be governed by and construed in accordance with the internal laws of the State of New York applicable to agreements made and to be performed entirely within such state."
    },
]


def generate_contract_dates():
    """Generate random contract effective and expiration dates"""
    # Effective date within the last 3 years
    days_ago = random.randint(0, 1095)
    effective_date = datetime.now() - timedelta(days=days_ago)
    
    # Expiration date: 12, 24, or 36 months from effective date
    contract_duration_months = random.choice([12, 24, 36])
    expiration_date = effective_date + timedelta(days=contract_duration_months * 30)
    
    return effective_date, expiration_date, contract_duration_months


def create_contract_pdf(filename, company, vendor, contract_type, effective_date, expiration_date, contract_duration):
    """Generate a PDF contract with all required fields"""
    doc = SimpleDocTemplate(filename, pagesize=letter,
                          rightMargin=0.75*inch, leftMargin=0.75*inch,
                          topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles with colors
    styles = getSampleStyleSheet()
    
    # Define color scheme - using blue tones like the sample
    primary_color = colors.HexColor('#1E3A8A')  # Deep blue
    accent_color = colors.HexColor('#3B82F6')   # Bright blue
    highlight_color = colors.HexColor('#FFA500') # Orange for highlights
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.white,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        backColor=primary_color,
        borderPadding=(10, 10, 10, 10)
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14,
        textColor=colors.HexColor('#1F2937')
    )
    
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=6,
        textColor=colors.HexColor('#374151')
    )
    
    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=11,
        textColor=primary_color,
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    # Title with colored background
    title_text = f'<para align="center" backColor="{primary_color.hexval()}" ' \
                 f'textColor="white" spaceAfter="10" spaceBefore="10">' \
                 f'<b>{contract_type["title"]}</b></para>'
    title = Paragraph(title_text, title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Introduction paragraph with proper party structure and colored highlights
    effective_date_str = effective_date.strftime("%d day of %B, %Y")
    intro_text = f"""This {contract_type["title"].title()} is entered as of the <font color="{highlight_color.hexval()}"><b>{effective_date_str}</b></font> 
    ("<b>Effective Date</b>") by and between <font color="{primary_color.hexval()}"><b>{company['name']}</b></font>, a Washington corporation, 
    having its principal place of business at {company['address']} ("<b>{company['reference']}</b>") 
    and <font color="{primary_color.hexval()}"><b>{vendor['name']}</b></font>, a Washington corporation, having its principal place of business at 
    {vendor['address']} ("<b>{vendor['reference']}</b>")."""
    
    elements.append(Paragraph(intro_text, body_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Contract term and expiration with colored highlights
    expiration_date_str = expiration_date.strftime("%B %d, %Y")
    term_text = f"""This agreement shall remain in effect for a period of <font color="{accent_color.hexval()}"><b>{contract_duration} months</b></font> 
    from the Effective Date and shall expire on <font color="{highlight_color.hexval()}"><b>{expiration_date_str}</b></font> unless terminated earlier 
    in accordance with the terms set forth herein."""
    elements.append(Paragraph(term_text, body_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Terms paragraph
    terms_text = f"""This agreement shall void and nullify any and all previous agreements to this 
    date between <font color="{primary_color.hexval()}"><b>{company['reference']}</b></font> and <font color="{primary_color.hexval()}"><b>{vendor['reference']}</b></font>."""
    elements.append(Paragraph(terms_text, body_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Generate dynamic contract terms
    access_limit = random.randint(200000, 600000)
    overage_fee = round(random.uniform(0.005, 0.02), 3)
    response_time = random.choice(["24 hours", "12 hours", "48 hours"])
    
    # Fees paragraph with colored highlights
    fees_text = f"""There shall be no additional fees of any kind paid to <font color="{primary_color.hexval()}"><b>{company['reference']}</b></font>, 
    other than those listed within this agreement for <font color="{accent_color.hexval()}"><b>{contract_type['services']}</b></font> and/or bandwidth usage. 
    The initial term of this contract is for <b>{contract_duration} months</b> with a maximum of 
    <font color="{highlight_color.hexval()}"><b>{access_limit:,}</b></font> accesses thereafter payment shall be <font color="{highlight_color.hexval()}"><b>${overage_fee}</b></font> 
    (one-half cent) per access. <font color="{primary_color.hexval()}"><b>{vendor['reference']}</b></font> must monitor and remit this amount to 
    <font color="{primary_color.hexval()}"><b>{company['reference']}</b></font> by no later than Wednesday for accesses used from the previous week 
    (Monday thru Sunday)."""
    elements.append(Paragraph(fees_text, body_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Support paragraph with colored highlights
    support_text = f"""<font color="{primary_color.hexval()}"><b>{company['reference']}</b></font> must provide a person(s) to correct any technical 
    problems (Server being down or slow, <font color="{accent_color.hexval()}"><b>{response_time}</b></font> per day, 7 days per week. 
    This person(s) must be available by beeper or telephone. <font color="{primary_color.hexval()}"><b>{vendor['reference']}</b></font> shall provide 
    this same 24 hour support at the broadcast location."""
    elements.append(Paragraph(support_text, body_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Governing law paragraph - Jurisdictions section with colored text
    gov_text = f"""<font color="{primary_color.hexval()}"><b>Governing Law:</b></font> {contract_type["jurisdiction_clause"]}"""
    elements.append(Paragraph(gov_text, body_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Final agreement paragraph
    final_text = f"""All parties have read and fully agree to all terms and conditions as set forth 
    in this <font color="{accent_color.hexval()}"><b>{contract_type["title"].title()}</b></font>."""
    elements.append(Paragraph(final_text, body_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Signature section with proper party names and colored styling
    sig_data = [
        [Paragraph(f'<font color="{primary_color.hexval()}"><b>{company["name"]}</b></font>', signature_style), 
         Paragraph(f'<font color="{primary_color.hexval()}"><b>{vendor["name"]}</b></font>', signature_style)],
        [Paragraph(f"By: {company['rep']}", signature_style), 
         Paragraph(f"By: {vendor['rep']}", signature_style)],
        [Paragraph(f"Title: {company['title']}", signature_style), 
         Paragraph(f"Title: {vendor['title']}", signature_style)],
        [Paragraph(f'<font name="Courier" color="{accent_color.hexval()}">{company["rep"]}</font>', signature_style), 
         Paragraph(f'<font name="Courier" color="{accent_color.hexval()}">{vendor["rep"]}</font>', signature_style)],
    ]
    
    sig_table = Table(sig_data, colWidths=[3.25*inch, 3.25*inch])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LINEABOVE', (0, 3), (-1, 3), 1, primary_color),  # Signature line
        ('TOPPADDING', (0, 3), (-1, 3), 10),
    ]))
    
    elements.append(sig_table)
    
    # Build PDF
    doc.build(elements)
    print(f"Generated: {filename}")
    
    # Return contract metadata for logging
    return {
        "filename": filename,
        "title": contract_type["title"],
        "type": contract_type["type"],
        "effective_date": effective_date.strftime("%Y-%m-%d"),
        "expiration_date": expiration_date.strftime("%Y-%m-%d"),
        "parties": [
            {
                "name": company['name'],
                "address": company['address'],
                "reference": company['reference'],
                "representative": company['rep'],
                "title": company['title']
            },
            {
                "name": vendor['name'],
                "address": vendor['address'],
                "reference": vendor['reference'],
                "representative": vendor['rep'],
                "title": vendor['title']
            }
        ],
        "jurisdiction": contract_type["jurisdiction_region"]
    }


def main():
    """Generate multiple contract PDFs"""
    print("Starting contract PDF generation...")
    print("=" * 60)
    
    # Create output directory if it doesn't exist
    output_dir = "generated_contracts"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate 8-12 random contracts
    num_contracts = random.randint(8, 12)
    
    contracts_metadata = []
    
    for i in range(num_contracts):
        # Randomly select company, vendor, and contract type
        company = random.choice(COMPANIES)
        vendor = random.choice(VENDORS)
        
        # Ensure company and vendor are different
        while company['name'] == vendor['name']:
            vendor = random.choice(VENDORS)
        
        contract_type = CONTRACT_TYPES[i % len(CONTRACT_TYPES)]
        effective_date, expiration_date, contract_duration = generate_contract_dates()
        
        # Generate filename with contract type
        filename = os.path.join(
            output_dir, 
            f"contract_{i+1:03d}_{contract_type['type']}_{company['reference']}_{effective_date.strftime('%Y%m%d')}.pdf"
        )
        
        # Create the contract and get metadata
        metadata = create_contract_pdf(
            filename, company, vendor, contract_type, 
            effective_date, expiration_date, contract_duration
        )
        contracts_metadata.append(metadata)
        
        # Print contract summary
        print(f"\nContract #{i+1}:")
        print(f"  Type: {metadata['type']} - {metadata['title']}")
        print(f"  Effective: {metadata['effective_date']}")
        print(f"  Expires: {metadata['expiration_date']}")
        print(f"  Party 1: {metadata['parties'][0]['name']} ({metadata['parties'][0]['reference']})")
        print(f"  Party 2: {metadata['parties'][1]['name']} ({metadata['parties'][1]['reference']})")
        print(f"  Jurisdiction: {metadata['jurisdiction']}")
    
    print("\n" + "=" * 60)
    print(f"Successfully generated {num_contracts} contracts in '{output_dir}' directory!")
    print("\nContract Type Summary:")
    type_counts = {}
    for metadata in contracts_metadata:
        contract_type = metadata['type']
        type_counts[contract_type] = type_counts.get(contract_type, 0) + 1
    
    for ctype, count in sorted(type_counts.items()):
        print(f"  {ctype}: {count} contract(s)")


if __name__ == "__main__":
    main()