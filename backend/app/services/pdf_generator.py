import os
from io import BytesIO
from datetime import datetime
from typing import Dict, Any, List

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class MedicalReportPDFGenerator:
    """
    Generates professional-grade medical consultation & triage reports in PDF format.
    Fulfills all Module 9 specifications.
    """

    NAVY = colors.HexColor("#102A43")
    MEDICAL_BLUE = colors.HexColor("#247BA0")
    TEAL = colors.HexColor("#20B2AA")
    SLATE = colors.HexColor("#627D98")
    LIGHT_BG = colors.HexColor("#F0F4F8")
    EMERGENCY_RED = colors.HexColor("#D64545")
    SUCCESS_GREEN = colors.HexColor("#2E9D72")

    @classmethod
    def generate_assessment_pdf(cls, assessment_data: Dict[str, Any], patient_data: Dict[str, Any], nearby_facilities: List[Dict[str, Any]] = None) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Custom Styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=cls.NAVY
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=cls.SLATE
        )
        section_heading = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=cls.MEDICAL_BLUE,
            spaceBefore=10,
            spaceAfter=4
        )
        body_style = ParagraphStyle(
            "BodyDark",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=cls.NAVY
        )
        bold_label = ParagraphStyle(
            "BoldLabel",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=13,
            textColor=cls.NAVY
        )
        disclaimer_style = ParagraphStyle(
            "Disclaimer",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#486581")
        )

        elements = []

        # 1. Header Banner
        header_text = [
            [
                Paragraph("<b>MEDIGUIDE AI CLINICAL TRIAGE REPORT</b>", title_style),
                Paragraph(f"<b>Date:</b> {datetime.utcnow().strftime('%d %b %Y, %H:%M UTC')}<br/><b>Report ID:</b> MG-{assessment_data.get('id', 'NEW')}", subtitle_style)
            ]
        ]
        header_table = Table(header_text, colWidths=[380, 160])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT')
        ]))
        elements.append(header_table)
        elements.append(HRFlowable(width="100%", thickness=1.5, color=cls.MEDICAL_BLUE, spaceBefore=6, spaceAfter=10))

        # 2. Patient Information
        elements.append(Paragraph("1. PATIENT DEMOGRAPHICS & CLINICAL CONTEXT", section_heading))
        patient_info = [
            [
                Paragraph("<b>Full Name:</b>", bold_label),
                Paragraph(patient_data.get("full_name", "Anonymous"), body_style),
                Paragraph("<b>Age / Gender:</b>", bold_label),
                Paragraph(f"{patient_data.get('age', 'N/A')} yrs / {patient_data.get('gender', 'Unspecified')}", body_style)
            ],
            [
                Paragraph("<b>Location:</b>", bold_label),
                Paragraph(patient_data.get("location", "Chennai, Tamil Nadu"), body_style),
                Paragraph("<b>Allergies / Meds:</b>", bold_label),
                Paragraph(patient_data.get("allergies", "None reported"), body_style)
            ]
        ]
        pt_table = Table(patient_info, colWidths=[100, 170, 100, 170])
        pt_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), cls.LIGHT_BG),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D9E2EC")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(pt_table)
        elements.append(Spacer(1, 10))

        # 3. Urgency Assessment Banner
        is_emergency = assessment_data.get("is_emergency", False)
        urg_color = cls.EMERGENCY_RED if is_emergency else cls.SUCCESS_GREEN
        urg_title = "CRITICAL EMERGENCY ALERT - DIAL 112" if is_emergency else "ROUTINE CLINICAL EVALUATION"
        urg_desc = assessment_data.get("red_flag_reason") if is_emergency else "No acute emergency red flags detected. Scheduled outpatient consultation recommended."

        urgency_box = [
            [
                Paragraph(f"<b>TRIAGE STATUS: {urg_title}</b><br/>{urg_desc}", ParagraphStyle("Urg", parent=body_style, textColor=colors.white, fontName="Helvetica-Bold"))
            ]
        ]
        urg_table = Table(urgency_box, colWidths=[540])
        urg_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), urg_color),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(urgency_table := urg_table)
        elements.append(Spacer(1, 10))

        # 4. Reported Symptoms & NLP Extraction
        elements.append(Paragraph("2. REPORTED SYMPTOMS & NLP CLINICAL EXTRACTION", section_heading))
        symptoms_list = assessment_data.get("symptoms", [])
        sym_names = [s.get("symptom_name", s.get("name", "Unknown")) for s in symptoms_list]

        nlp_info = [
            [Paragraph("<b>Primary Complaint:</b>", bold_label), Paragraph(assessment_data.get("chief_complaint", "General Discomfort"), body_style)],
            [Paragraph("<b>Reported Symptoms:</b>", bold_label), Paragraph(", ".join(sym_names) if sym_names else "None listed", body_style)],
            [Paragraph("<b>Duration & Severity:</b>", bold_label), Paragraph(f"{assessment_data.get('duration_days', 1)} days | Severity: {assessment_data.get('severity', 'Moderate')}", body_style)],
            [Paragraph("<b>Raw Input Narrative:</b>", bold_label), Paragraph(f'"{assessment_data.get("raw_input_text", "Direct selection")}"', body_style)],
        ]
        nlp_table = Table(nlp_info, colWidths=[130, 410])
        nlp_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D9E2EC")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(nlp_table)
        elements.append(Spacer(1, 10))

        # 5. Possible Conditions & Compatibility Scores
        elements.append(Paragraph("3. KNOWLEDGE BASE COMPATIBILITY ASSESSMENT", section_heading))
        results = assessment_data.get("results", []) or assessment_data.get("top_conditions", [])
        
        cond_rows = [
            [
                Paragraph("<b>Rank</b>", bold_label),
                Paragraph("<b>Possible Condition</b>", bold_label),
                Paragraph("<b>Compatibility Score</b>", bold_label),
                Paragraph("<b>Specialty</b>", bold_label),
                Paragraph("<b>Clinical Reasoning (XAI)</b>", bold_label)
            ]
        ]
        for idx, res in enumerate(results[:4]):
            name = res.get("condition_name", "Condition")
            score = res.get("compatibility_score", 0)
            spec = res.get("recommended_specialty", "General Physician")
            why = res.get("why_considered", "")
            cond_rows.append([
                Paragraph(str(idx + 1), body_style),
                Paragraph(f"<b>{name}</b>", body_style),
                Paragraph(f"{score}/100", ParagraphStyle("Score", parent=body_style, fontName="Helvetica-Bold", textColor=cls.MEDICAL_BLUE)),
                Paragraph(spec, body_style),
                Paragraph(why, ParagraphStyle("Why", parent=body_style, fontSize=8, leading=10))
            ])

        cond_table = Table(cond_rows, colWidths=[35, 125, 75, 95, 210])
        cond_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), cls.LIGHT_BG),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D9E2EC")),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(cond_table)
        elements.append(Spacer(1, 10))

        # 6. Doctor Specialization Recommendation
        elements.append(Paragraph("4. DOCTOR SPECIALIZATION RECOMMENDATION", section_heading))
        doc_rec = assessment_data.get("doctor_recommendation", {})
        spec_name = assessment_data.get("recommended_specialty") or doc_rec.get("primary_specialty", "General Physician")
        rec_match = assessment_data.get("doctor_recommendation_match") or doc_rec.get("recommendation_match", 88)
        rec_reason = assessment_data.get("doctor_recommendation_reason") or doc_rec.get("reason", "Appropriate for initial baseline evaluation.")

        doc_box = [
            [
                Paragraph("<b>Recommended Specialty:</b>", bold_label),
                Paragraph(f"<b>{spec_name}</b>", ParagraphStyle("Sp", parent=body_style, fontName="Helvetica-Bold", textColor=cls.MEDICAL_BLUE)),
                Paragraph("<b>Match Score:</b>", bold_label),
                Paragraph(f"<b>{rec_match}/100</b>", body_style)
            ],
            [
                Paragraph("<b>Recommendation Rationale:</b>", bold_label),
                Paragraph(rec_reason, body_style, 3)
            ]
        ]
        doc_table = Table(doc_box, colWidths=[130, 160, 90, 160])
        doc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), cls.LIGHT_BG),
            ('SPAN', (1, 1), (3, 1)),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D9E2EC")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(doc_table)
        elements.append(Spacer(1, 10))

        # 7. Nearby Healthcare Facilities (Chennai)
        if nearby_facilities:
            elements.append(Paragraph("5. VERIFIED NEARBY HEALTHCARE FACILITIES (CHENNAI)", section_heading))
            hosp_rows = [
                [
                    Paragraph("<b>Hospital / Clinic Name</b>", bold_label),
                    Paragraph("<b>Locality</b>", bold_label),
                    Paragraph("<b>Distance</b>", bold_label),
                    Paragraph("<b>Contact & Fee</b>", bold_label)
                ]
            ]
            for h in nearby_facilities[:3]:
                dist_str = f"{h.get('distance_km', 'N/A')} km" if 'distance_km' in h else "Chennai"
                fee_str = h.get('consultation_fee', 'Call to confirm')
                phone_str = h.get('phone', 'N/A')
                hosp_rows.append([
                    Paragraph(f"<b>{h.get('name', 'Hospital')}</b>", body_style),
                    Paragraph(h.get('locality', 'Chennai'), body_style),
                    Paragraph(dist_str, body_style),
                    Paragraph(f"Ph: {phone_str}<br/>Fee: {fee_str}", ParagraphStyle("HFee", parent=body_style, fontSize=8, leading=10))
                ])
            hosp_table = Table(hosp_rows, colWidths=[190, 95, 75, 180])
            hosp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), cls.LIGHT_BG),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#D9E2EC")),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(hosp_table)
            elements.append(Spacer(1, 10))

        # 8. Clinical Disclaimer (Mandatory)
        elements.append(HRFlowable(width="100%", thickness=1, color=cls.SLATE, spaceBefore=4, spaceAfter=6))
        elements.append(Paragraph(
            "<b>IMPORTANT CLINICAL SAFETY NOTICE:</b> "
            "This application provides preliminary AI-assisted health information and healthcare navigation. "
            "It does not provide a confirmed medical diagnosis or replace consultation with a qualified healthcare professional. "
            "Condition Compatibility Scores represent pattern compatibility with the medical knowledge base, not a clinical disease probability. "
            "Do not initiate, discontinue, or alter any medical treatment or medication without direct clinical consultation. "
            "In any acute medical emergency, call 112 (India) immediately or go to the nearest hospital casualty.",
            disclaimer_style
        ))

        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
