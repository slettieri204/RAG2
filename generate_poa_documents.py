"""
generate_poa_documents.py

Generates realistic (but fictional) Power of Attorney PDF documents
for Pennsylvania and Illinois, based on each state's actual statutory
form structure. Uses fictional names and addresses.

These are for TESTING/DEMONSTRATION purposes only — not legal documents.

Usage:
    pip install reportlab
    python generate_poa_documents.py

Output:
    docs/PA_Durable_Power_of_Attorney.pdf
    docs/PA_Healthcare_Power_of_Attorney.pdf
    docs/IL_Statutory_Short_Form_POA_Property.pdf
    docs/IL_Statutory_Short_Form_POA_Healthcare.pdf
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.lib import colors

os.makedirs("docs", exist_ok=True)

# ─── Shared Styles ───────────────────────────────────────────────────────────

def get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="DocTitle", fontSize=14, leading=18, alignment=TA_CENTER,
        spaceAfter=6, spaceBefore=12, fontName="Helvetica-Bold"
    ))
    styles.add(ParagraphStyle(
        name="SectionHead", fontSize=11, leading=14, spaceBefore=14,
        spaceAfter=6, fontName="Helvetica-Bold"
    ))
    styles.add(ParagraphStyle(
        name="BodyText2", fontSize=10, leading=13, alignment=TA_JUSTIFY,
        spaceAfter=6, fontName="Helvetica"
    ))
    styles.add(ParagraphStyle(
        name="NoticeText", fontSize=9, leading=12, alignment=TA_JUSTIFY,
        spaceAfter=4, fontName="Helvetica"
    ))
    styles.add(ParagraphStyle(
        name="NoticeTextBold", fontSize=9, leading=12, alignment=TA_JUSTIFY,
        spaceAfter=4, fontName="Helvetica-Bold"
    ))
    styles.add(ParagraphStyle(
        name="SignatureLine", fontSize=10, leading=20, spaceBefore=20,
        spaceAfter=4, fontName="Helvetica"
    ))
    styles.add(ParagraphStyle(
        name="SmallText", fontSize=8, leading=10, alignment=TA_LEFT,
        spaceAfter=2, fontName="Helvetica-Oblique", textColor=colors.grey
    ))
    styles.add(ParagraphStyle(
        name="Centered", fontSize=10, leading=13, alignment=TA_CENTER,
        spaceAfter=6, fontName="Helvetica"
    ))
    styles.add(ParagraphStyle(
        name="IndentBody", fontSize=10, leading=13, alignment=TA_JUSTIFY,
        spaceAfter=4, fontName="Helvetica", leftIndent=36
    ))
    return styles


def hr():
    return HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=6, spaceAfter=6)


def signature_block(name, role, date_str, styles):
    """Generate a signature block with a line and typed name."""
    return [
        Spacer(1, 18),
        Paragraph(f"____________________________________", styles["SignatureLine"]),
        Paragraph(f"{name}", styles["BodyText2"]),
        Paragraph(f"{role}", styles["SmallText"]),
        Paragraph(f"Date: {date_str}", styles["BodyText2"]),
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# DOCUMENT 1: Pennsylvania Durable Power of Attorney (Financial/Property)
# Based on 20 Pa.C.S. Section 5601 et seq.
# ═══════════════════════════════════════════════════════════════════════════════

def generate_pa_financial_poa():
    filename = "docs/PA_Durable_Power_of_Attorney.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            topMargin=0.75*inch, bottomMargin=0.75*inch,
                            leftMargin=1*inch, rightMargin=1*inch)
    styles = get_styles()
    story = []

    # Header
    story.append(Paragraph("COMMONWEALTH OF PENNSYLVANIA", styles["Centered"]))
    story.append(Paragraph("DURABLE GENERAL POWER OF ATTORNEY", styles["DocTitle"]))
    story.append(Paragraph("Pursuant to 20 Pa.C.S. Chapter 56", styles["Centered"]))
    story.append(hr())

    # Statutory Notice (required by 20 Pa.C.S. Section 5601(c))
    story.append(Paragraph("NOTICE", styles["SectionHead"]))
    story.append(Paragraph(
        "THE PURPOSE OF THIS POWER OF ATTORNEY IS TO GIVE THE PERSON YOU DESIGNATE "
        "(YOUR \"AGENT\") BROAD POWERS TO HANDLE YOUR PROPERTY, WHICH MAY INCLUDE "
        "POWERS TO PLEDGE, SELL, OR OTHERWISE DISPOSE OF ANY REAL OR PERSONAL "
        "PROPERTY WITHOUT ADVANCE NOTICE TO YOU OR APPROVAL BY YOU. THIS POWER OF "
        "ATTORNEY DOES NOT IMPOSE A DUTY ON YOUR AGENT TO EXERCISE GRANTED POWERS, "
        "BUT WHEN POWERS ARE EXERCISED, YOUR AGENT MUST USE DUE CARE TO ACT FOR YOUR "
        "BENEFIT AND IN ACCORDANCE WITH THIS POWER OF ATTORNEY.",
        styles["NoticeTextBold"]
    ))
    story.append(Paragraph(
        "YOUR AGENT MAY EXERCISE THE POWERS GIVEN HERE THROUGHOUT YOUR LIFETIME, EVEN "
        "AFTER YOU BECOME INCAPACITATED, UNLESS YOU EXPRESSLY LIMIT THE DURATION OF "
        "THESE POWERS OR YOU REVOKE THESE POWERS OR A COURT ACTING ON YOUR BEHALF "
        "TERMINATES OR MODIFIES YOUR AGENT'S AUTHORITY.",
        styles["NoticeTextBold"]
    ))
    story.append(Paragraph(
        "YOUR AGENT MUST ACT IN ACCORDANCE WITH YOUR REASONABLE EXPECTATIONS TO THE "
        "EXTENT ACTUALLY KNOWN BY YOUR AGENT AND, OTHERWISE, IN YOUR BEST INTEREST, "
        "ACT IN GOOD FAITH AND ACT ONLY WITHIN THE SCOPE OF AUTHORITY GRANTED BY YOU "
        "IN THIS POWER OF ATTORNEY.",
        styles["NoticeTextBold"]
    ))
    story.append(Paragraph(
        "THE POWERS AND DUTIES OF AN AGENT UNDER A POWER OF ATTORNEY ARE EXPLAINED "
        "MORE FULLY IN 20 Pa.C.S. Ch. 56. IF THERE IS ANYTHING ABOUT THIS FORM THAT "
        "YOU DO NOT UNDERSTAND, YOU SHOULD ASK A LAWYER OF YOUR OWN CHOOSING TO "
        "EXPLAIN IT TO YOU.",
        styles["NoticeTextBold"]
    ))
    story.append(Paragraph(
        "I HAVE READ OR HAD EXPLAINED TO ME THIS NOTICE AND I UNDERSTAND ITS CONTENTS.",
        styles["NoticeTextBold"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "_______________________________ &nbsp;&nbsp;&nbsp;&nbsp; Date: March 15, 2025",
        styles["BodyText2"]
    ))
    story.append(Paragraph("Margaret A. Whitfield (Principal)", styles["SmallText"]))
    story.append(hr())

    # Principal and Agent Designation
    story.append(Paragraph("ARTICLE I: DESIGNATION OF PRINCIPAL AND AGENT", styles["SectionHead"]))
    story.append(Paragraph(
        "I, <b>Margaret A. Whitfield</b>, of 742 Elmhurst Drive, Apt. 3B, Philadelphia, "
        "Pennsylvania 19103, born on June 14, 1958, Social Security Number ending in "
        "XXX-XX-4728, being of sound mind and under no constraint or undue influence, "
        "do hereby appoint the following individual as my Attorney-in-Fact (hereinafter "
        "referred to as my \"Agent\"):",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Primary Agent:</b> Robert J. Whitfield (Son)<br/>"
        "Address: 1584 Oakmont Boulevard, Pittsburgh, Pennsylvania 15213<br/>"
        "Telephone: (412) 555-0193<br/>"
        "Email: rjwhitfield@email.example.com",
        styles["IndentBody"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Successor Agent:</b> In the event that my Primary Agent is unable or unwilling "
        "to serve or continue to serve, I designate the following individual as my "
        "Successor Agent:",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "Patricia L. Donovan (Daughter)<br/>"
        "Address: 239 Cherry Lane, Harrisburg, Pennsylvania 17101<br/>"
        "Telephone: (717) 555-0847",
        styles["IndentBody"]
    ))

    # Durability
    story.append(Paragraph("ARTICLE II: DURABILITY PROVISION", styles["SectionHead"]))
    story.append(Paragraph(
        "Pursuant to 20 Pa.C.S. Section 5604, this Power of Attorney is DURABLE and shall "
        "not be affected by my subsequent disability, incapacity, or incompetence. It shall "
        "remain in full force and effect until my death or until I revoke it in writing, or "
        "until a court of competent jurisdiction modifies or terminates the authority granted "
        "herein. This Power of Attorney shall be effective immediately upon execution.",
        styles["BodyText2"]
    ))

    # Powers Granted
    story.append(Paragraph("ARTICLE III: POWERS GRANTED", styles["SectionHead"]))
    story.append(Paragraph(
        "I grant my Agent general authority to act for me with respect to the following "
        "subjects as defined in 20 Pa.C.S. Section 5602:",
        styles["BodyText2"]
    ))

    powers = [
        ("A", "Real Property Transactions", "To buy, sell, lease, exchange, mortgage, grant options, collect rent, and in all ways manage my real property, including but not limited to any residential property located at 742 Elmhurst Drive, Philadelphia, PA 19103."),
        ("B", "Tangible Personal Property Transactions", "To buy, sell, lease, exchange, and otherwise manage my tangible personal property, including vehicles, furniture, equipment, and personal effects."),
        ("C", "Stock, Bond, and Securities Transactions", "To buy, sell, exchange, and manage stocks, bonds, mutual funds, and other securities held in any brokerage or investment account in my name."),
        ("D", "Banking and Financial Institution Transactions", "To conduct any and all banking transactions, including opening and closing accounts, making deposits and withdrawals, writing checks, accessing safe deposit boxes, and obtaining loans or lines of credit on my behalf."),
        ("E", "Insurance and Annuity Transactions", "To purchase, modify, surrender, collect benefits from, and make claims under any insurance policies or annuity contracts, whether life, health, disability, casualty, or other type."),
        ("F", "Retirement Plan Transactions", "To contribute to, withdraw from, change beneficiary designations on, and manage all retirement plans, pensions, IRAs, 401(k) plans, and similar accounts."),
        ("G", "Tax Matters", "To prepare, sign, file, and amend federal, state, and local tax returns; receive confidential tax information; contest tax assessments; and claim refunds on my behalf."),
        ("H", "Government Benefits", "To apply for, manage, and maintain eligibility for all government benefits, including Social Security, Medicare, Medicaid, Veterans Affairs benefits, and any other federal, state, or local programs."),
        ("I", "Legal Actions and Proceedings", "To initiate, defend, settle, or otherwise participate in legal, administrative, or arbitration proceedings on my behalf, and to retain legal counsel as necessary."),
        ("J", "Personal and Family Maintenance", "To pay for my personal care, support, maintenance, and the maintenance of my dependents from my assets."),
    ]

    for letter_code, title, desc in powers:
        story.append(Paragraph(
            f"<b>({letter_code}) {title}.</b> {desc}",
            styles["IndentBody"]
        ))

    # Special Instructions
    story.append(Paragraph("ARTICLE IV: SPECIAL INSTRUCTIONS AND LIMITATIONS", styles["SectionHead"]))
    story.append(Paragraph(
        "The following special instructions and limitations shall apply to the authority "
        "granted under this Power of Attorney:",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "(1) My Agent shall not have the authority to make gifts of my property exceeding "
        "$5,000 per recipient per calendar year, subject to the limitations of 20 Pa.C.S. "
        "Section 5601.2.",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "(2) My Agent shall not have the authority to change any beneficiary designation on "
        "any of my life insurance policies or retirement accounts, except to name my "
        "grandchildren as contingent beneficiaries.",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "(3) My Agent shall maintain detailed records of all transactions conducted on my "
        "behalf and shall provide an accounting to my Successor Agent or to any court of "
        "competent jurisdiction upon request.",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "(4) Under no circumstances shall my Agent use my assets for the personal benefit "
        "of the Agent, except as reasonable compensation for services rendered in the "
        "administration of this Power of Attorney, not to exceed $500 per month.",
        styles["IndentBody"]
    ))

    # Third Party Reliance
    story.append(Paragraph("ARTICLE V: THIRD-PARTY RELIANCE", styles["SectionHead"]))
    story.append(Paragraph(
        "Any third party who receives a copy of this Power of Attorney may rely upon it. "
        "Revocation of this Power of Attorney is not effective as to a third party until the "
        "third party has actual knowledge of the revocation. I agree to indemnify and hold "
        "harmless any third party who acts in good faith reliance upon the authority granted "
        "in this Power of Attorney.",
        styles["BodyText2"]
    ))

    # Guardian Nomination
    story.append(Paragraph("ARTICLE VI: GUARDIAN NOMINATION", styles["SectionHead"]))
    story.append(Paragraph(
        "If a court decides that it is necessary to appoint a guardian of my estate or "
        "guardian of my person, I hereby nominate my Agent, Robert J. Whitfield, to serve "
        "in that capacity. If Robert J. Whitfield is unable or unwilling to serve, I "
        "nominate Patricia L. Donovan as an alternative guardian.",
        styles["BodyText2"]
    ))

    # Revocation
    story.append(Paragraph("ARTICLE VII: REVOCATION", styles["SectionHead"]))
    story.append(Paragraph(
        "I reserve the right to revoke this Power of Attorney at any time by providing "
        "written notice to my Agent and to any third parties who may have received a copy "
        "of this document. Upon revocation, all authority granted herein shall immediately "
        "cease, subject to the protections afforded to third parties under 20 Pa.C.S. "
        "Section 5608.",
        styles["BodyText2"]
    ))

    story.append(PageBreak())

    # Execution
    story.append(Paragraph("EXECUTION", styles["SectionHead"]))
    story.append(Paragraph(
        "IN WITNESS WHEREOF, I have hereunto set my hand this 15th day of March, 2025.",
        styles["BodyText2"]
    ))
    story.extend(signature_block("Margaret A. Whitfield", "Principal", "March 15, 2025", styles))

    # Witnesses
    story.append(Paragraph("WITNESSES", styles["SectionHead"]))
    story.append(Paragraph(
        "The foregoing instrument was signed, sealed, and declared by the above-named "
        "Principal as her Power of Attorney, in our presence, and we, at her request and "
        "in her presence and in the presence of each other, have subscribed our names as "
        "witnesses thereto.",
        styles["BodyText2"]
    ))
    story.extend(signature_block("Jennifer M. Kowalski", "Witness #1 - 891 Pine Street, Philadelphia, PA 19107", "March 15, 2025", styles))
    story.extend(signature_block("David R. Thompson", "Witness #2 - 4520 Walnut Street, Philadelphia, PA 19139", "March 15, 2025", styles))

    # Notary
    story.append(Paragraph("NOTARY ACKNOWLEDGMENT", styles["SectionHead"]))
    story.append(Paragraph(
        "COMMONWEALTH OF PENNSYLVANIA<br/>"
        "COUNTY OF PHILADELPHIA",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "On this 15th day of March, 2025, before me, a Notary Public, personally appeared "
        "Margaret A. Whitfield, known to me (or satisfactorily proven) to be the person "
        "whose name is subscribed to the within instrument, and acknowledged that she "
        "executed the same for the purposes therein contained.",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "IN WITNESS WHEREOF, I have hereunto set my hand and notarial seal.",
        styles["BodyText2"]
    ))
    story.extend(signature_block("Anna C. Rodriguez", "Notary Public\nMy Commission Expires: December 31, 2027\nNotary ID: 2019-PA-041582", "March 15, 2025", styles))

    # Agent Acknowledgment (required by 20 Pa.C.S. Section 5601(d))
    story.append(PageBreak())
    story.append(Paragraph("AGENT'S ACKNOWLEDGMENT", styles["SectionHead"]))
    story.append(Paragraph(
        "Pursuant to 20 Pa.C.S. Section 5601(d)",
        styles["SmallText"]
    ))
    story.append(Paragraph(
        "I, Robert J. Whitfield, have read the Power of Attorney dated March 15, 2025, "
        "and am the person identified as the Agent for the Principal, Margaret A. Whitfield. "
        "I hereby acknowledge that when I act as Agent:",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "I shall act in accordance with the Principal's reasonable expectations to the "
        "extent actually known by me and, otherwise, in the Principal's best interest, "
        "act in good faith and act only within the scope of authority granted to me by "
        "the Principal in the Power of Attorney.",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "I shall not act in any manner that is contrary to the Principal's known wishes "
        "or in any manner that would constitute self-dealing, unless specifically "
        "authorized by the Principal in the Power of Attorney document.",
        styles["IndentBody"]
    ))
    story.extend(signature_block("Robert J. Whitfield", "Agent", "March 15, 2025", styles))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "DISCLAIMER: This document is a sample generated for demonstration and testing "
        "purposes only. It is NOT a valid legal document and should NOT be used for any "
        "legal purpose. All names, addresses, and identifying information are fictional.",
        styles["SmallText"]
    ))

    doc.build(story)
    print(f"  Created: {filename}")


# ═══════════════════════════════════════════════════════════════════════════════
# DOCUMENT 2: Pennsylvania Healthcare Power of Attorney
# Based on 20 Pa.C.S. Section 5451 et seq.
# ═══════════════════════════════════════════════════════════════════════════════

def generate_pa_healthcare_poa():
    filename = "docs/PA_Healthcare_Power_of_Attorney.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            topMargin=0.75*inch, bottomMargin=0.75*inch,
                            leftMargin=1*inch, rightMargin=1*inch)
    styles = get_styles()
    story = []

    story.append(Paragraph("COMMONWEALTH OF PENNSYLVANIA", styles["Centered"]))
    story.append(Paragraph("HEALTH CARE POWER OF ATTORNEY", styles["DocTitle"]))
    story.append(Paragraph("Pursuant to 20 Pa.C.S. Sections 5451-5465<br/>(Health Care Agents and Representatives)", styles["Centered"]))
    story.append(hr())

    story.append(Paragraph("PART I: APPOINTMENT OF HEALTH CARE AGENT", styles["SectionHead"]))
    story.append(Paragraph(
        "I, <b>Margaret A. Whitfield</b>, of 742 Elmhurst Drive, Apt. 3B, Philadelphia, "
        "Pennsylvania 19103, born June 14, 1958, being of sound mind, willfully and "
        "voluntarily appoint the following individual as my Health Care Agent to make "
        "health care decisions for me if I become unable to make or communicate my own "
        "health care decisions:",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>Health Care Agent:</b> Patricia L. Donovan (Daughter)<br/>"
        "Address: 239 Cherry Lane, Harrisburg, Pennsylvania 17101<br/>"
        "Telephone: (717) 555-0847<br/>"
        "Email: pldonovan@email.example.com",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "<b>Alternate Health Care Agent:</b> Robert J. Whitfield (Son)<br/>"
        "Address: 1584 Oakmont Boulevard, Pittsburgh, Pennsylvania 15213<br/>"
        "Telephone: (412) 555-0193",
        styles["IndentBody"]
    ))

    story.append(Paragraph("PART II: AUTHORITY GRANTED", styles["SectionHead"]))
    story.append(Paragraph(
        "I grant my Health Care Agent full authority to make any and all health care "
        "decisions on my behalf, including but not limited to the following:",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "(a) To consent to, refuse, or withdraw consent to any medical treatment, "
        "surgical procedure, diagnostic test, or therapeutic intervention, including "
        "experimental treatments;<br/>"
        "(b) To authorize my admission to or discharge from any hospital, nursing home, "
        "assisted living facility, rehabilitation center, hospice, or other medical facility;<br/>"
        "(c) To access, obtain copies of, and authorize the release of my medical records "
        "and personal health information, including information protected under the Health "
        "Insurance Portability and Accountability Act of 1996 (HIPAA);<br/>"
        "(d) To retain and dismiss health care providers, physicians, nurses, therapists, "
        "and other medical professionals;<br/>"
        "(e) To authorize the administration of pain relief medication or palliative care, "
        "even if such treatment may hasten my death;<br/>"
        "(f) To make decisions regarding organ donation and the disposition of my remains "
        "after death, in accordance with my wishes expressed herein or previously communicated.",
        styles["IndentBody"]
    ))

    story.append(Paragraph("PART III: INSTRUCTIONS AND WISHES", styles["SectionHead"]))
    story.append(Paragraph(
        "I provide the following guidance to my Health Care Agent regarding my preferences "
        "for medical treatment:",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>End-of-Life Care:</b> If I have a terminal condition with no reasonable "
        "expectation of recovery, or if I am in a persistent vegetative state, I do NOT "
        "wish to be kept alive by artificial means, including mechanical ventilation, "
        "artificial nutrition and hydration, or cardiopulmonary resuscitation. I request "
        "that all comfort measures be provided to keep me pain-free and comfortable.",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "<b>Pain Management:</b> I wish to receive adequate pain medication to maintain my "
        "comfort, even if such medication may cloud my consciousness or hasten my death.",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "<b>Organ Donation:</b> Upon my death, I wish to donate any usable organs and "
        "tissues for the purpose of transplantation and medical research.",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "<b>Religious Considerations:</b> I am of the Roman Catholic faith. While I "
        "respect the teachings of my Church, my Health Care Agent should prioritize "
        "the medical guidance provided above, which reflects my personal wishes after "
        "careful consideration.",
        styles["IndentBody"]
    ))

    story.append(Paragraph("PART IV: EFFECTIVE DATE AND DURABILITY", styles["SectionHead"]))
    story.append(Paragraph(
        "This Health Care Power of Attorney shall become effective upon a determination "
        "by my attending physician that I am unable to make or communicate health care "
        "decisions for myself. This power is durable and shall not be affected by my "
        "subsequent disability or incapacity. This document shall remain in effect until "
        "I revoke it in writing or by oral declaration in the presence of two witnesses.",
        styles["BodyText2"]
    ))

    story.append(Paragraph("PART V: HIPAA AUTHORIZATION", styles["SectionHead"]))
    story.append(Paragraph(
        "I intend for my Health Care Agent to be treated as I would be with respect to "
        "my rights regarding the use and disclosure of my individually identifiable health "
        "information and other medical records. This release authority applies to any "
        "information governed by HIPAA and its implementing regulations.",
        styles["BodyText2"]
    ))

    # Execution
    story.append(Paragraph("EXECUTION", styles["SectionHead"]))
    story.append(Paragraph(
        "IN WITNESS WHEREOF, I have hereunto set my hand this 15th day of March, 2025.",
        styles["BodyText2"]
    ))
    story.extend(signature_block("Margaret A. Whitfield", "Principal", "March 15, 2025", styles))

    story.append(Paragraph("WITNESSES", styles["SectionHead"]))
    story.extend(signature_block("Jennifer M. Kowalski", "Witness #1 - 891 Pine Street, Philadelphia, PA 19107", "March 15, 2025", styles))
    story.extend(signature_block("David R. Thompson", "Witness #2 - 4520 Walnut Street, Philadelphia, PA 19139", "March 15, 2025", styles))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "DISCLAIMER: This document is a sample generated for demonstration and testing "
        "purposes only. It is NOT a valid legal document and should NOT be used for any "
        "legal purpose. All names, addresses, and identifying information are fictional.",
        styles["SmallText"]
    ))

    doc.build(story)
    print(f"  Created: {filename}")


# ═══════════════════════════════════════════════════════════════════════════════
# DOCUMENT 3: Illinois Statutory Short Form POA for Property
# Based on 755 ILCS 45/3-3
# ═══════════════════════════════════════════════════════════════════════════════

def generate_il_property_poa():
    filename = "docs/IL_Statutory_Short_Form_POA_Property.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            topMargin=0.75*inch, bottomMargin=0.75*inch,
                            leftMargin=1*inch, rightMargin=1*inch)
    styles = get_styles()
    story = []

    # Cover Sheet: Notice to Individual (required by 755 ILCS 45/3-3)
    story.append(Paragraph("STATE OF ILLINOIS", styles["Centered"]))
    story.append(Paragraph("NOTICE TO THE INDIVIDUAL SIGNING THE", styles["Centered"]))
    story.append(Paragraph("ILLINOIS STATUTORY SHORT FORM<br/>POWER OF ATTORNEY FOR PROPERTY", styles["DocTitle"]))
    story.append(Paragraph("755 ILCS 45/3-3", styles["Centered"]))
    story.append(hr())

    story.append(Paragraph(
        "PLEASE READ THIS NOTICE CAREFULLY. The form that you will be signing is a legal "
        "document. It is governed by the Illinois Power of Attorney Act. If there is "
        "anything about this form that you do not understand, you should ask a lawyer to "
        "explain it to you.",
        styles["NoticeTextBold"]
    ))
    story.append(Paragraph(
        "The purpose of this Power of Attorney is to give your designated \"agent\" broad "
        "powers to handle your financial affairs, which may include the power to pledge, "
        "sell, or dispose of any of your real or personal property, even without your "
        "consent or any advance notice to you.",
        styles["NoticeText"]
    ))
    story.append(Paragraph(
        "When using the Statutory Short Form, you may name successor agents, but you may "
        "not name co-agents. This form does not impose a duty upon your agent to handle "
        "your financial affairs, so it is important that you select an agent who will agree "
        "to do this for you. It is also important to select an agent whom you trust, since "
        "you are giving that agent control over your financial assets and property.",
        styles["NoticeText"]
    ))
    story.append(Paragraph(
        "If you name a successor agent, the successor agent may act for you only after "
        "the first agent is no longer able to act or is no longer willing to act for you. "
        "Any agent, whether named in the statutory short form or in another power of "
        "attorney form, may be subject to the requirements of the Illinois Power of "
        "Attorney Act regarding the duties of agents.",
        styles["NoticeText"]
    ))
    story.append(Paragraph(
        "The agent is required to use the property for your benefit and is prohibited from "
        "making gifts of your property unless you have specifically granted that power in "
        "paragraph 3 of the form. Otherwise, your agent may use your property for the "
        "benefit of your agent or others only if such use has previously been established "
        "by you or by a court order. The agent is required to keep records of receipts, "
        "disbursements, and significant actions taken as your agent.",
        styles["NoticeText"]
    ))
    story.append(Paragraph(
        "This Power of Attorney does not authorize your agent to appear in court for you "
        "as an attorney-at-law or otherwise engage in the practice of law. This Power of "
        "Attorney will not give your agent any authority over your health care decisions.",
        styles["NoticeText"]
    ))
    story.append(Paragraph(
        "This Power of Attorney may be amended or revoked by you at any time and in any "
        "manner. Absent amendment or revocation, the authority granted in this Power of "
        "Attorney will become effective at the time this Power is signed and will remain "
        "in effect until your death. A revocation of this Power of Attorney is not "
        "effective as to your agent or any third party until the agent or third party "
        "receives actual notice of the revocation.",
        styles["NoticeText"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Please place your initials on the following line indicating that you have read "
        "this Notice: &nbsp;&nbsp;&nbsp; <b>T.R.C.</b> &nbsp;&nbsp; Principal's initials",
        styles["BodyText2"]
    ))

    story.append(PageBreak())

    # The Form Itself
    story.append(Paragraph("ILLINOIS STATUTORY SHORT FORM", styles["Centered"]))
    story.append(Paragraph("POWER OF ATTORNEY FOR PROPERTY", styles["DocTitle"]))
    story.append(hr())

    story.append(Paragraph(
        "1. I, <b>Thomas R. Castellano</b>, residing at 2847 North Lakewood Avenue, "
        "Chicago, Illinois 60614, hereby revoke all prior statutory powers of attorney "
        "for property executed by me and appoint:",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>Agent:</b> Maria E. Castellano (Spouse)<br/>"
        "Address: 2847 North Lakewood Avenue, Chicago, Illinois 60614<br/>"
        "Telephone: (312) 555-0726",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "as my attorney-in-fact (my \"agent\") to act for me and in my name (in any way "
        "I could act in person) with respect to the following powers, as defined in "
        "Section 3-4 of the \"Statutory Short Form Power of Attorney for Property Law\" "
        "(755 ILCS 45/3-4), including all amendments, but subject to any limitations on "
        "or additions to the specified powers inserted in paragraph 3 below:",
        styles["BodyText2"]
    ))

    # Powers List
    story.append(Paragraph(
        "2. <b>POWERS GRANTED</b> (NOTE: The following categories of powers are authorized. "
        "None have been struck out.)",
        styles["BodyText2"]
    ))

    il_powers = [
        ("(a)", "Real estate transactions"),
        ("(b)", "Financial institution transactions"),
        ("(c)", "Stock and bond transactions"),
        ("(d)", "Tangible personal property transactions"),
        ("(e)", "Safe deposit box transactions"),
        ("(f)", "Insurance and annuity transactions"),
        ("(g)", "Retirement plan transactions"),
        ("(h)", "Social Security, employment, and military service benefits"),
        ("(i)", "Tax matters"),
        ("(j)", "Claims and litigation"),
        ("(k)", "Commodity and option transactions"),
        ("(l)", "Business operations transactions"),
        ("(m)", "Borrowing transactions"),
        ("(n)", "Estate transactions"),
    ]

    for code, power in il_powers:
        story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{code} {power}", styles["BodyText2"]))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "3. <b>LIMITATIONS ON AND ADDITIONS TO THE AGENT'S POWERS.</b> The powers "
        "granted above shall be subject to the following limitations and additions:",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "(i) My Agent may make gifts of my property to my spouse, children, and "
        "grandchildren in amounts not exceeding $3,000 per person per calendar year, "
        "provided that such gifts do not impair my ability to meet my own financial needs "
        "and obligations.",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "(ii) My Agent shall not have the authority to change the beneficiary designations "
        "on any life insurance policy or retirement account without my prior written consent, "
        "unless I am incapacitated at the time.",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "(iii) My Agent shall deposit all funds collected on my behalf into my primary "
        "checking account at First National Bank of Illinois, account number ending in 7842.",
        styles["IndentBody"]
    ))

    # Successor Agent
    story.append(Paragraph(
        "4. <b>SUCCESSOR AGENT.</b> If my Agent named above is unable or unwilling to "
        "serve or continue to serve as my Agent, I appoint the following person to serve "
        "as my Successor Agent:",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>Successor Agent:</b> Anthony D. Castellano (Brother)<br/>"
        "Address: 519 West Barry Avenue, Unit 4, Chicago, Illinois 60657<br/>"
        "Telephone: (312) 555-1394",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "<b>Second Successor Agent:</b> Lisa K. Ferraro (Sister)<br/>"
        "Address: 1205 South Ridgeland Avenue, Oak Park, Illinois 60302<br/>"
        "Telephone: (708) 555-0215",
        styles["IndentBody"]
    ))

    # Effective Date
    story.append(Paragraph(
        "5. <b>EFFECTIVE DATE AND DURABILITY.</b> This Power of Attorney is effective "
        "immediately and shall continue in force until my death or revocation, and shall "
        "not be affected by my disability or incapacity. This is a durable power of "
        "attorney under 755 ILCS 45/2-5.",
        styles["BodyText2"]
    ))

    # Execution
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "I, Thomas R. Castellano, the Principal, sign my name to this Statutory Short "
        "Form Power of Attorney for Property on January 22, 2025, and, being first "
        "duly sworn, do hereby declare that I sign and execute this instrument as my "
        "Power of Attorney and that I sign it willingly, and that I execute it as my "
        "free and voluntary act for the purposes therein expressed.",
        styles["BodyText2"]
    ))
    story.extend(signature_block("Thomas R. Castellano", "Principal", "January 22, 2025", styles))

    # Witness
    story.append(Paragraph("WITNESS", styles["SectionHead"]))
    story.append(Paragraph(
        "I, the undersigned witness, declare under penalty of perjury that the person "
        "who signed this document, or asked another to sign for him or her, did so in my "
        "presence, that the Principal appeared to be of sound mind and under no duress, "
        "fraud, or undue influence.",
        styles["BodyText2"]
    ))
    story.extend(signature_block("Sandra J. Okonkwo", "Witness - 1120 West Diversey Parkway, Chicago, IL 60614", "January 22, 2025", styles))

    # Notary
    story.append(Paragraph("NOTARY ACKNOWLEDGMENT", styles["SectionHead"]))
    story.append(Paragraph(
        "STATE OF ILLINOIS<br/>COUNTY OF COOK",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "On this 22nd day of January, 2025, before me, a Notary Public in and for said "
        "County and State, personally appeared Thomas R. Castellano, known to me to be "
        "the person whose name is subscribed to the within instrument, and acknowledged "
        "that he executed the same of his own free will.",
        styles["BodyText2"]
    ))
    story.extend(signature_block("Michael P. Harrington", "Notary Public, State of Illinois\nMy Commission Expires: August 14, 2027\nNotary Seal No. 2022-IL-NP-884210", "January 22, 2025", styles))

    story.append(PageBreak())

    # Agent's Acceptance / Notice to Agent (per 755 ILCS 45/3-3)
    story.append(Paragraph("NOTICE TO AGENT", styles["SectionHead"]))
    story.append(Paragraph(
        "By accepting appointment as Agent under this Power of Attorney, you become "
        "obligated to the Principal to use the powers granted in the Principal's best "
        "interest, to keep the Principal's property separate from yours unless the "
        "property is jointly owned, and to exercise reasonable caution and prudence. "
        "A violation of your duties may subject you to criminal prosecution.",
        styles["NoticeTextBold"]
    ))
    story.append(Paragraph(
        "If you are also a health care representative for the Principal, you may not "
        "use the Principal's property for your own benefit unless the Principal or a "
        "court authorizes it. This Power of Attorney for Property does not authorize "
        "you to make health care decisions for the Principal.",
        styles["NoticeText"]
    ))
    story.append(Paragraph("AGENT'S ACCEPTANCE", styles["SectionHead"]))
    story.append(Paragraph(
        "I, Maria E. Castellano, accept my appointment as Agent under this Statutory "
        "Short Form Power of Attorney for Property. I have read the Notice to Agent and "
        "understand my duties and obligations. I agree to act in the best interest of "
        "the Principal.",
        styles["BodyText2"]
    ))
    story.extend(signature_block("Maria E. Castellano", "Agent", "January 22, 2025", styles))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "DISCLAIMER: This document is a sample generated for demonstration and testing "
        "purposes only. It is NOT a valid legal document and should NOT be used for any "
        "legal purpose. All names, addresses, and identifying information are fictional.",
        styles["SmallText"]
    ))

    doc.build(story)
    print(f"  Created: {filename}")


# ═══════════════════════════════════════════════════════════════════════════════
# DOCUMENT 4: Illinois Statutory Short Form POA for Health Care
# Based on 755 ILCS 45/4-10
# ═══════════════════════════════════════════════════════════════════════════════

def generate_il_healthcare_poa():
    filename = "docs/IL_Statutory_Short_Form_POA_Healthcare.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            topMargin=0.75*inch, bottomMargin=0.75*inch,
                            leftMargin=1*inch, rightMargin=1*inch)
    styles = get_styles()
    story = []

    # Cover Sheet
    story.append(Paragraph("STATE OF ILLINOIS", styles["Centered"]))
    story.append(Paragraph("NOTICE TO THE INDIVIDUAL SIGNING THE", styles["Centered"]))
    story.append(Paragraph("ILLINOIS STATUTORY SHORT FORM<br/>POWER OF ATTORNEY FOR HEALTH CARE", styles["DocTitle"]))
    story.append(Paragraph("755 ILCS 45/4-10", styles["Centered"]))
    story.append(hr())

    story.append(Paragraph(
        "No one can predict when a serious illness or accident might occur. When it does, "
        "you may need someone else to speak or make health care decisions for you. If you "
        "plan now, you can increase the chances that the medical treatment you get will be "
        "the treatment you want.",
        styles["NoticeText"]
    ))
    story.append(Paragraph(
        "In Illinois, you can choose someone to be your \"health care agent.\" Your agent "
        "is the person you trust to make health care decisions for you if you are unable "
        "or do not want to make them yourself. These decisions should be based on your "
        "personal values and wishes.",
        styles["NoticeText"]
    ))
    story.append(Paragraph(
        "It is important to put your choice of agent in writing. The written form is "
        "often called an \"advance directive.\" You may use this form or another form, "
        "as long as it meets the legal requirements of Illinois. There are many written "
        "and online resources to guide you and your loved ones in having a conversation "
        "about these issues.",
        styles["NoticeText"]
    ))
    story.append(Paragraph(
        "The form that you will be signing is a legal document. It is governed by the "
        "Illinois Power of Attorney Act (755 ILCS 45/4-1 et seq.). If there is anything "
        "about this form that you do not understand, you should ask a lawyer to explain "
        "it to you.",
        styles["NoticeTextBold"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Please place your initials on the following line indicating that you have read "
        "this Notice: &nbsp;&nbsp;&nbsp; <b>T.R.C.</b> &nbsp;&nbsp; Principal's initials",
        styles["BodyText2"]
    ))

    story.append(PageBreak())

    # Main Form
    story.append(Paragraph("ILLINOIS STATUTORY SHORT FORM", styles["Centered"]))
    story.append(Paragraph("POWER OF ATTORNEY FOR HEALTH CARE", styles["DocTitle"]))
    story.append(hr())

    story.append(Paragraph(
        "1. I, <b>Thomas R. Castellano</b>, residing at 2847 North Lakewood Avenue, "
        "Chicago, Illinois 60614, hereby revoke all prior powers of attorney for health "
        "care executed by me and appoint:",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>Health Care Agent:</b> Maria E. Castellano (Spouse)<br/>"
        "Address: 2847 North Lakewood Avenue, Chicago, Illinois 60614<br/>"
        "Telephone: (312) 555-0726<br/>"
        "Email: mecastellano@email.example.com",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "as my attorney-in-fact (my \"agent\") to act for me and in my name (in any way "
        "I could act in person) to make any and all decisions for me concerning my personal "
        "care, medical treatment, hospitalization, and health care, and to require, withhold, "
        "or withdraw any type of medical treatment or procedure, even though my death may "
        "ensue. My agent shall have the same access to my medical records that I have, "
        "including the right to disclose the contents to others as my agent sees fit. "
        "This authorization applies to any information governed by the Health Insurance "
        "Portability and Accountability Act of 1996 (HIPAA).",
        styles["BodyText2"]
    ))

    # Successor Agent
    story.append(Paragraph(
        "2. <b>SUCCESSOR AGENT.</b> If the agent named above is unable or unwilling to "
        "serve, I appoint:",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "<b>Successor Health Care Agent:</b> Lisa K. Ferraro (Sister)<br/>"
        "Address: 1205 South Ridgeland Avenue, Oak Park, Illinois 60302<br/>"
        "Telephone: (708) 555-0215",
        styles["IndentBody"]
    ))

    # Health Care Instructions
    story.append(Paragraph(
        "3. <b>SPECIFIC INSTRUCTIONS AND LIMITATIONS</b> (pursuant to Section 4-10 "
        "of the Illinois Power of Attorney Act):",
        styles["BodyText2"]
    ))

    story.append(Paragraph("<b>End-of-Life Decisions:</b>", styles["BodyText2"]))
    story.append(Paragraph(
        "(a) If I am suffering from a terminal condition with no reasonable chance of "
        "recovery and am unable to communicate my wishes, I direct my agent to refuse "
        "or withdraw all life-sustaining treatment, including artificial nutrition and "
        "hydration, mechanical ventilation, and dialysis. I request that comfort care "
        "and pain management be provided.",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "(b) If I am in a persistent vegetative state or irreversible coma, I direct "
        "my agent to refuse or withdraw all life-sustaining treatment. I understand "
        "that this may result in my death.",
        styles["IndentBody"]
    ))

    story.append(Paragraph("<b>Organ and Tissue Donation:</b>", styles["BodyText2"]))
    story.append(Paragraph(
        "(c) Upon my death, I hereby authorize the donation of my organs and tissues "
        "for transplantation, therapy, or medical research, in accordance with the "
        "Illinois Revised Uniform Anatomical Gift Act (755 ILCS 50/).",
        styles["IndentBody"]
    ))

    story.append(Paragraph("<b>Disposition of Remains:</b>", styles["BodyText2"]))
    story.append(Paragraph(
        "(d) I direct that my remains be cremated. My ashes shall be interred at "
        "Holy Sepulchre Cemetery in Alsip, Illinois, in the Castellano family plot. "
        "All decisions made by my agent with respect to the disposition of my remains, "
        "including cremation, shall be binding pursuant to the Disposition of Remains "
        "Act, 755 ILCS 65/1 et seq.",
        styles["IndentBody"]
    ))

    story.append(Paragraph("<b>Mental Health Treatment:</b>", styles["BodyText2"]))
    story.append(Paragraph(
        "(e) I authorize my agent to consent to mental health treatment and to have "
        "access to my mental health records. However, my agent may NOT consent to my "
        "admission to a mental health facility for more than 17 days, nor consent to "
        "electroconvulsive therapy, psychosurgery, or other experimental procedures "
        "without a court order.",
        styles["IndentBody"]
    ))

    story.append(Paragraph("<b>Additional Wishes:</b>", styles["BodyText2"]))
    story.append(Paragraph(
        "(f) I wish to be treated at Northwestern Memorial Hospital in Chicago, Illinois "
        "whenever reasonably feasible. My primary care physician is Dr. Sarah M. Peterson, "
        "whose office is located at 680 North Lake Shore Drive, Suite 1240, Chicago, IL "
        "60611, phone (312) 555-8190.",
        styles["IndentBody"]
    ))
    story.append(Paragraph(
        "(g) I am of Italian heritage and Catholic faith. I request that if I am near "
        "death, a Catholic priest be contacted to administer the Sacrament of the Anointing "
        "of the Sick. My parish is St. Alphonsus, located at 1429 West Wellington Avenue, "
        "Chicago, IL 60657, phone (312) 555-6744.",
        styles["IndentBody"]
    ))

    # Effective Date
    story.append(Paragraph(
        "4. <b>EFFECTIVE DATE AND DURABILITY.</b> This Power of Attorney for Health Care "
        "shall be effective upon my inability to make or communicate health care decisions, "
        "as determined by my attending physician. It is durable and shall not be affected "
        "by my disability or incapacity.",
        styles["BodyText2"]
    ))

    story.append(Paragraph(
        "5. <b>REVOCATION.</b> I understand that I have the right to revoke this Power "
        "of Attorney at any time by communicating my intent to revoke to my agent and/or "
        "my attending physician, either in writing or by any other means.",
        styles["BodyText2"]
    ))

    # Execution
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "I, Thomas R. Castellano, the Principal, sign my name to this Statutory Short "
        "Form Power of Attorney for Health Care on January 22, 2025.",
        styles["BodyText2"]
    ))
    story.extend(signature_block("Thomas R. Castellano", "Principal", "January 22, 2025", styles))

    # Witness
    story.append(Paragraph("WITNESS", styles["SectionHead"]))
    story.append(Paragraph(
        "I declare under penalty of perjury under the laws of the State of Illinois that "
        "the person who signed this document, or asked another to sign for him, did so in "
        "my presence, and that to the best of my knowledge, the Principal is of sound mind "
        "and is not acting under duress, fraud, or undue influence. I am at least 18 years "
        "of age, and I am not the agent designated in this Power of Attorney.",
        styles["BodyText2"]
    ))
    story.extend(signature_block("Sandra J. Okonkwo", "Witness - 1120 West Diversey Parkway, Chicago, IL 60614", "January 22, 2025", styles))

    # Notary
    story.append(Paragraph("NOTARY ACKNOWLEDGMENT", styles["SectionHead"]))
    story.append(Paragraph("STATE OF ILLINOIS<br/>COUNTY OF COOK", styles["BodyText2"]))
    story.append(Paragraph(
        "On this 22nd day of January, 2025, before me, a Notary Public in and for said "
        "County and State, personally appeared Thomas R. Castellano, known to me to be "
        "the person whose name is subscribed to the within instrument, and acknowledged "
        "that he executed the same of his own free will, for the purposes therein stated.",
        styles["BodyText2"]
    ))
    story.extend(signature_block("Michael P. Harrington", "Notary Public, State of Illinois\nMy Commission Expires: August 14, 2027", "January 22, 2025", styles))

    # Agent Acceptance
    story.append(Paragraph("AGENT'S ACCEPTANCE", styles["SectionHead"]))
    story.append(Paragraph(
        "I, Maria E. Castellano, accept my appointment as Health Care Agent under this "
        "Statutory Short Form Power of Attorney for Health Care. I understand my "
        "responsibilities and agree to act in the best interest of the Principal, "
        "following the instructions and wishes set forth in this document.",
        styles["BodyText2"]
    ))
    story.extend(signature_block("Maria E. Castellano", "Health Care Agent", "January 22, 2025", styles))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "DISCLAIMER: This document is a sample generated for demonstration and testing "
        "purposes only. It is NOT a valid legal document and should NOT be used for any "
        "legal purpose. All names, addresses, and identifying information are fictional.",
        styles["SmallText"]
    ))

    doc.build(story)
    print(f"  Created: {filename}")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 55)
    print("  Generating sample Power of Attorney documents")
    print("  (All names and information are FICTIONAL)")
    print("=" * 55)
    print()

    generate_pa_financial_poa()
    generate_pa_healthcare_poa()
    generate_il_property_poa()
    generate_il_healthcare_poa()

    print()
    print("=" * 55)
    print("  Done! 4 documents created in the docs/ folder:")
    print("    1. PA_Durable_Power_of_Attorney.pdf")
    print("    2. PA_Healthcare_Power_of_Attorney.pdf")
    print("    3. IL_Statutory_Short_Form_POA_Property.pdf")
    print("    4. IL_Statutory_Short_Form_POA_Healthcare.pdf")
    print()
    print("  These documents use FICTIONAL names/data and")
    print("  are structured to match each state's statutory")
    print("  POA format for realistic testing.")
    print("=" * 55)
