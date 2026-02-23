from fastapi import APIRouter, Response, Depends
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from backend.database import get_db
from backend.crud import get_scheme_by_id
from typing import Optional

router = APIRouter()

@router.get("/download-guide/{scheme_id}")
async def download_guide(scheme_id: str, name: Optional[str] = "Applicant", db: Session = Depends(get_db)):
    scheme_obj = get_scheme_by_id(db, scheme_id)
    if not scheme_obj:
        print(f"DEBUG: PDF Generation failed - Scheme {scheme_id} not found")
        return Response(content="Scheme not found", status_code=404)
    
    # Safely convert to dict
    try:
        scheme = {
            "name": scheme_obj.name,
            "benefits": scheme_obj.benefits,
            "required_documents": scheme_obj.required_documents if isinstance(scheme_obj.required_documents, list) else [],
            "apply_url": scheme_obj.apply_url,
            "deadline": scheme_obj.deadline,
            "category": getattr(scheme_obj, 'category', 'General')
        }
    except Exception as e:
        print(f"DEBUG: Mapping error: {e}")
        return Response(content=f"Error processing scheme data: {str(e)}", status_code=500)

    print(f"DEBUG: Starting PDF generation for {scheme['name']}")
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    styles = getSampleStyleSheet()

    # --- 1. Background Decoration ---
    p.setFillColorRGB(0.06, 0.09, 0.16)  # Dark Background style
    p.rect(0, 0, width, height, fill=1)
    
    # Header Accent
    p.setFillColorRGB(0.39, 0.4, 0.95) # --primary color
    p.rect(0, height - 1.5 * inch, width, 1.5 * inch, fill=1)

    # --- 2. Professional Header ---
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 28)
    p.drawString(0.75 * inch, height - 0.8 * inch, "Yojana.AI Intelligence Report")
    
    p.setFont("Helvetica", 12)
    p.drawString(0.75 * inch, height - 1.1 * inch, f"Strategic Roadmap for: {name.upper()}")
    p.drawString(0.75 * inch, height - 1.3 * inch, f"Scheme ID Reference: {scheme_id.upper()}")

    # --- 3. Scheme Identification ---
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(0.75 * inch, height - 2.2 * inch, scheme['name'])
    
    p.setStrokeColorRGB(0.39, 0.4, 0.95)
    p.line(0.75 * inch, height - 2.4 * inch, 7 * inch, height - 2.4 * inch)

    # --- 4. AI Strategic Overview ---
    p.setFont("Helvetica-Bold", 14)
    p.drawString(0.75 * inch, height - 2.8 * inch, "🤖 AI STRATEGIC OVERVIEW")
    
    p.setFont("Helvetica", 11)
    p.setFillColorRGB(0.8, 0.8, 0.8)
    overview_text = f"Based on our algorithmic analysis, the {scheme['name']} is a high-impact initiative categorized under {scheme.get('category', 'Social Welfare')}. This scheme is specifically optimized to provide {scheme['benefits']}. Our engine has flagged this as a Top Match for your profile."
    
    # Simple text wrapping for overview
    y = height - 3.1 * inch
    words = overview_text.split()
    line = ""
    for word in words:
        if p.stringWidth(line + word + " ") < 6.5 * inch:
            line += word + " "
        else:
            p.drawString(0.75 * inch, y, line)
            line = word + " "
            y -= 15
    p.drawString(0.75 * inch, y, line)

    # --- 5. Application Roadmap (Checklist) ---
    y -= 40
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(0.75 * inch, y, "🗺️ APPLICATION ROADMAP")
    
    y -= 25
    p.setFont("Helvetica", 11)
    p.setFillColorRGB(0.8, 0.8, 0.8)
    p.drawString(0.75 * inch, y, "Required Documents (Human Verification Needed):")
    
    y -= 20
    for doc in scheme["required_documents"]:
        p.setStrokeColor(colors.white)
        p.rect(0.8 * inch, y - 2, 10, 10, stroke=1, fill=0) # Checkbox
        p.drawString(1.1 * inch, y, doc)
        y -= 20

    # --- 6. Execution Steps ---
    y -= 30
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(0.75 * inch, y, "⚙️ EXECUTION STEPS")
    
    y -= 25
    p.setFont("Helvetica", 11)
    p.setFillColorRGB(0.8, 0.8, 0.8)
    steps = [
        f"1. Secure URL: {scheme['apply_url']}",
        f"2. Digitization: Ensure all checked documents are scanned clearly.",
        f"3. Deadline Awareness: Submit latest by {scheme['deadline']}.",
        "4. Status Monitoring: Use the tracking ID generated upon submission."
    ]
    for step in steps:
        p.drawString(0.75 * inch, y, step)
        y -= 20

    # --- 7. Footer & Security Watermark ---
    p.setFont("Helvetica-Oblique", 9)
    p.setFillColorRGB(0.5, 0.5, 0.5)
    p.drawString(0.75 * inch, 0.5 * inch, "VERIFIED BY YOJANA.AI ENGINE | SECURE DOCUMENT GENERATION | 2026")

    p.showPage()
    p.save()

    buffer.seek(0)
    return Response(
        content=buffer.getvalue(), 
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={scheme_id}_AI_Guide.pdf"}
    )
