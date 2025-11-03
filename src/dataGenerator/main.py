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
    """Generate random contract dates: execution, effective, expiration, and renewal"""
    # Execution date (when contract was signed) - within the last 3 years
    days_ago = random.randint(0, 1095)
    execution_date = datetime.now() - timedelta(days=days_ago)
    
    # Effective date: 0-30 days after execution
    days_after_execution = random.randint(0, 30)
    effective_date = execution_date + timedelta(days=days_after_execution)
    
    # Contract duration: 12, 24, or 36 months
    contract_duration_months = random.choice([12, 24, 36])
    
    # Expiration date: calculated from effective date
    expiration_date = effective_date + timedelta(days=contract_duration_months * 30)
    
    # Renewal date: 30-90 days before expiration
    days_before_expiration = random.randint(30, 90)
    renewal_date = expiration_date - timedelta(days=days_before_expiration)
    
    return execution_date, effective_date, expiration_date, renewal_date, contract_duration_months


def create_contract_pdf(filename, company, vendor, contract_type, effective_date, expiration_date, 
                       execution_date, renewal_date, contract_duration, contract_id):
    """Generate a PDF contract with all required fields"""
    doc = SimpleDocTemplate(filename, pagesize=letter,
                          rightMargin=0.5*inch, leftMargin=0.5*inch,
                          topMargin=0.5*inch, bottomMargin=0.5*inch)
    
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
        fontSize=13,
        textColor=colors.white,
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        backColor=primary_color,
        borderPadding=(8, 8, 8, 8)
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=9,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=11,
        textColor=colors.HexColor('#1F2937')
    )
    
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['BodyText'],
        fontSize=9,
        spaceAfter=4,
        textColor=colors.HexColor('#374151')
    )
    
    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=10,
        textColor=primary_color,
        spaceAfter=6,
        spaceBefore=6,
        fontName='Helvetica-Bold'
    )
    
    # Title with colored background
    title_text = f'<para align="center" backColor="{primary_color.hexval()}" ' \
                 f'textColor="white" spaceAfter="6" spaceBefore="6">' \
                 f'<b>{contract_type["title"]}</b></para>'
    title = Paragraph(title_text, title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.1*inch))
    
    # Contract ID header (small, subtle)
    contract_id_text = f'<para align="right"><font size="7" color="{primary_color.hexval()}">Contract ID: {contract_id}</font></para>'
    elements.append(Paragraph(contract_id_text, body_style))
    elements.append(Spacer(1, 0.08*inch))
    
    # Introduction paragraph with proper party structure and colored highlights
    effective_date_str = effective_date.strftime("%d day of %B, %Y")
    execution_date_str = execution_date.strftime("%B %d, %Y")
    
    intro_text = f"""This {contract_type["title"].title()} is executed on <font color="{highlight_color.hexval()}"><b>{execution_date_str}</b></font> 
    and entered into effect as of the <font color="{highlight_color.hexval()}"><b>{effective_date_str}</b></font> 
    ("<b>Effective Date</b>") by and between <font color="{primary_color.hexval()}"><b>{company['name']}</b></font>, a Washington corporation, 
    having its principal place of business at {company['address']} ("<b>{company['reference']}</b>") 
    and <font color="{primary_color.hexval()}"><b>{vendor['name']}</b></font>, a Washington corporation, having its principal place of business at 
    {vendor['address']} ("<b>{vendor['reference']}</b>")."""
    
    elements.append(Paragraph(intro_text, body_style))
    elements.append(Spacer(1, 0.08*inch))
    
    # Contract term and expiration with colored highlights
    expiration_date_str = expiration_date.strftime("%B %d, %Y")
    renewal_date_str = renewal_date.strftime("%B %d, %Y")
    
    term_text = f"""This agreement shall remain in effect for a period of <font color="{accent_color.hexval()}"><b>{contract_duration} months</b></font> 
    from the Effective Date and shall expire on <font color="{highlight_color.hexval()}"><b>{expiration_date_str}</b></font> unless terminated earlier 
    in accordance with the terms set forth herein. The contract is eligible for renewal on or before 
    <font color="{accent_color.hexval()}"><b>{renewal_date_str}</b></font>."""
    elements.append(Paragraph(term_text, body_style))
    elements.append(Spacer(1, 0.08*inch))
    
    # Terms paragraph
    terms_text = f"""This agreement shall void and nullify any and all previous agreements to this 
    date between <font color="{primary_color.hexval()}"><b>{company['reference']}</b></font> and <font color="{primary_color.hexval()}"><b>{vendor['reference']}</b></font>."""
    elements.append(Paragraph(terms_text, body_style))
    elements.append(Spacer(1, 0.08*inch))
    
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
    elements.append(Spacer(1, 0.08*inch))
    
    # Support paragraph with colored highlights
    support_text = f"""<font color="{primary_color.hexval()}"><b>{company['reference']}</b></font> must provide a person(s) to correct any technical 
    problems (Server being down or slow, <font color="{accent_color.hexval()}"><b>{response_time}</b></font> per day, 7 days per week. 
    This person(s) must be available by beeper or telephone. <font color="{primary_color.hexval()}"><b>{vendor['reference']}</b></font> shall provide 
    this same 24 hour support at the broadcast location."""
    elements.append(Paragraph(support_text, body_style))
    elements.append(Spacer(1, 0.08*inch))
    
    # Governing law paragraph - Jurisdictions section with colored text
    gov_text = f"""<font color="{primary_color.hexval()}"><b>Governing Law:</b></font> {contract_type["jurisdiction_clause"]}"""
    elements.append(Paragraph(gov_text, body_style))
    elements.append(Spacer(1, 0.08*inch))
    
    # Final agreement paragraph
    final_text = f"""All parties have read and fully agree to all terms and conditions as set forth 
    in this <font color="{accent_color.hexval()}"><b>{contract_type["title"].title()}</b></font>."""
    elements.append(Paragraph(final_text, body_style))
    elements.append(Spacer(1, 0.15*inch))
    
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
    
    sig_table = Table(sig_data, colWidths=[3.5*inch, 3.5*inch])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LINEABOVE', (0, 3), (-1, 3), 1, primary_color),  # Signature line
        ('TOPPADDING', (0, 3), (-1, 3), 6),
    ]))
    
    elements.append(sig_table)
    
    # Build PDF
    doc.build(elements)
    print(f"Generated: {filename}")
    
    # Return contract metadata for logging (matching Azure Search schema)
    return {
        "filename": filename,
        "id": contract_id,
        "docType": "contract",
        "title": contract_type["title"],
        "contractId": contract_id,
        "executionDate": execution_date.strftime("%Y-%m-%d"),
        "effectiveDate": effective_date.strftime("%Y-%m-%d"),
        "expirationDate": expiration_date.strftime("%Y-%m-%d"),
        "contractDuration": f"{contract_duration} months",
        "renewalDate": renewal_date.strftime("%Y-%m-%d"),
        "parties": [
            {
                "name": company['name'],
                "address": company['address'],
                "referenceName": company['reference'],
                "clause": f"{company['name']}, a Washington corporation, having its principal place of business at {company['address']} (\"{company['reference']}\")"
            },
            {
                "name": vendor['name'],
                "address": vendor['address'],
                "referenceName": vendor['reference'],
                "clause": f"{vendor['name']}, a Washington corporation, having its principal place of business at {vendor['address']} (\"{vendor['reference']}\")"
            }
        ],
        "jurisdictions": [contract_type["jurisdiction_region"]]
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
        execution_date, effective_date, expiration_date, renewal_date, contract_duration = generate_contract_dates()
        
        # Generate unique contract ID
        contract_id = f"CTR-{contract_type['type'].upper()}-{effective_date.strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        
        # Generate filename with contract type
        filename = os.path.join(
            output_dir, 
            f"contract_{i+1:03d}_{contract_type['type']}_{company['reference']}_{effective_date.strftime('%Y%m%d')}.pdf"
        )
        
        # Create the contract and get metadata
        metadata = create_contract_pdf(
            filename, company, vendor, contract_type, 
            effective_date, expiration_date, execution_date, renewal_date, 
            contract_duration, contract_id
        )
        contracts_metadata.append(metadata)
        
        # Print contract summary
        print(f"\nContract #{i+1}:")
        print(f"  ID: {metadata['contractId']}")
        print(f"  DocType: {metadata['docType']}")
        print(f"  Title: {metadata['title']}")
        print(f"  Execution Date: {metadata['executionDate']}")
        print(f"  Effective Date: {metadata['effectiveDate']}")
        print(f"  Expiration Date: {metadata['expirationDate']}")
        print(f"  Renewal Date: {metadata['renewalDate']}")
        print(f"  Duration: {metadata['contractDuration']}")
        print(f"  Party 1: {metadata['parties'][0]['name']} ({metadata['parties'][0]['referenceName']})")
        print(f"  Party 2: {metadata['parties'][1]['name']} ({metadata['parties'][1]['referenceName']})")
        print(f"  Jurisdictions: {', '.join(metadata['jurisdictions'])}")
    
    print("\n" + "=" * 60)
    print(f"Successfully generated {num_contracts} contracts in '{output_dir}' directory!")
    print("\nContract Type Summary:")
    type_counts = {}
    for metadata in contracts_metadata:
        # Extract type from title
        contract_title = metadata['title']
        type_counts[contract_title] = type_counts.get(contract_title, 0) + 1
    
    for ctype, count in sorted(type_counts.items()):
        print(f"  {ctype}: {count} contract(s)")


if __name__ == "__main__":
    main()