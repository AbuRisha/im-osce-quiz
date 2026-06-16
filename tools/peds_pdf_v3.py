r"""
v3: Q+A card PDF. Question order driven by an explicit per-case list
(matches the original prompt PDF). Answers pulled from STUDY_GUIDE.md by
matching the section label nearest to each question's keyword.
Output -> C:\Users\erick\Downloads\Pediatrics_Study_Guide.pdf
"""
import os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from peds_model_answers import MODEL_ANSWERS

MD_SRC  = r"C:\Users\erick\.local\share\opencode\worktree\c5c8c88a20f46fcf5f705ed119d409d27fa4d470\nimble-circuit\learners\pediatrics_study_guide\STUDY_GUIDE.md"
OUT_PDF = r"C:\Users\erick\Downloads\Pediatrics_Study_Guide.pdf"
CHROME  = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# ----------------------------------------------------------------------
# CASES — verbatim question order from the source prompt PDF.
# Format: (case_num, title, stem, [ (question_text, answer_keyword_or_label), ... ])
# The "label" matches a section header in STUDY_GUIDE.md (case-insensitive,
# tolerant of trailing modifiers).
# ----------------------------------------------------------------------

CASES = [
    (1, "Cephalohematoma",
     "Newborn after assisted vaginal delivery; firm blood-filled swelling over parietal scalp that does NOT cross suture lines.",
     [("What is the finding?", "Finding / diagnosis"),
      ("Give 1 differential.", "Differential"),
      ("Give 2 risk factors.", "Risk factors"),
      ("Give 2 potential complications.", "Complications"),
      ("What is the management plan?", "Management")]),

    (2, "Down Syndrome (Trisomy 21)",
     "38-week spontaneous delivery, dysmorphic facial features.",
     [("What is the diagnosis?", "Diagnosis"),
      ("Give 3 characteristic dysmorphic features.", "Dysmorphic features"),
      ("Which investigations confirm the diagnosis?", "Investigations to confirm"),
      ("What is the genetic abnormality?", "Genetic abnormality"),
      ("Give 2 medical problems that can occur.", "Medical problems")]),

    (3, "Preseptal (Periorbital) Cellulitis",
     "9-month-old infant, 2-day history of fever, nasal congestion, left eye swollen / unable to close.",
     [("What is the diagnosis?", "Diagnosis"),
      ("Most likely causative organism?", "Most common organisms"),
      ("Give 1 differential.", "Differential"),
      ("Outline the management plan.", "Management")]),

    (4, "Neonatal Respiratory Distress Syndrome (RDS)",
     "Preterm neonate, grunting, cyanosis, increased work of breathing. CXR at 30 min of life; required ventilation.",
     [("Mention 2 X-ray findings.", "X-ray findings"),
      ("What is the diagnosis (preterm condition)?", "Diagnosis"),
      ("What is the cause?", "Cause"),
      ("Give 2 treatments.", "Treatment"),
      ("How can it be prevented?", "Prevention")]),

    (5, "Acute Lymphoblastic Leukemia (ALL)",
     "4-year-old: pallor, weakness, fever, generally unwell.",
     [("What is the abnormality in CBC and smear?", "CBC / smear"),
      ("Probable diagnosis?", "Diagnosis"),
      ("Confirmatory investigations?", "Investigations"),
      ("Treatment options?", "Treatment")]),

    (6, "Sickle Cell Anemia",
     "4-year-old with pallor, limb pain, jaundice; two packed RBC transfusions to date.",
     [("What is the diagnosis?", "Diagnosis"),
      ("Confirmatory investigations?", "Investigations"),
      ("Name 2 complications.", "Complications"),
      ("Long-term medication to reduce recurrence?", "Long-term medication"),
      ("How to prevent infections in these children?", "Infection prevention")]),

    (7, "Acute Chest Syndrome (Sickle Cell)",
     "14-year-old African-Caribbean girl with known sickle cell; chest and back pain, codeine not helping; SOB, bronchial breath sounds.",
     [("Most likely cause?", "Most likely cause"),
      ("How will you manage?", "Management"),
      ("Other complications of sickle cell?", "Other SCD complications"),
      ("How to prevent infections in sickle cell?", "Infection prevention in SCD")]),

    (8, "Beta-Thalassemia Major",
     "7-year-old with pallor; blood transfusions since birth. Microcytic hypochromic anemia on labs.",
     [("Identify the specific facies.", "Facies"),
      ("Probable diagnosis?", "Diagnosis"),
      ("Mode of inheritance?", "Inheritance"),
      ("Diagnostic investigations of choice?", "Investigations"),
      ("Management options?", "Management"),
      ("Mention 2 long-term complications.", "Complications")]),
]

CASES += [
    (9, "Iron Deficiency Anemia (IDA)",
     "2-year-old picky eater, drinks 800 mL milk/day, pale, eating paper (pica).",
     [("Describe the findings in CBC.", "CBC findings"),
      ("What is the diagnosis?", "Diagnosis"),
      ("What are the possible causes?", "Causes"),
      ("Further investigations to confirm.", "Investigations"),
      ("What is the treatment?", "Treatment")]),

    (10, "Nephrotic Syndrome",
     "3-year-old male: facial swelling, abdominal distension, bilateral scrotal swelling, pitting edema; urine dipstick 4+ protein, 2+ blood.",
     [("Primary diagnosis?", "Diagnosis"),
      ("Most common histopathological type in this age group?", "Most common histopathological type"),
      ("Cardinal features of the condition?", "Cardinal/diagnostic features"),
      ("Other investigations you would request?", "Investigations"),
      ("Treatment?", "Treatment")]),

    (11, "Meningococcemia",
     "2-year-old boy: 6 hr of fever, vomiting, rapidly spreading rash over limbs, tachycardia, non-blanching purpuric rash, capillary refill 4 s on legs and trunk.",
     [("Describe the rash and its clinical significance.", "Rash"),
      ("Most likely diagnosis?", "Diagnosis"),
      ("Causative organism?", "Causative organism"),
      ("Give 3 clinical features.", "Clinical features"),
      ("Outline immediate management priorities.", "Management"),
      ("Give 2 complications and 2 preventive measures.", ["Complications", "Prevention"])]),

    (12, "Henoch-Schönlein Purpura (HSP)",
     "5-year-old boy: non-blanching rash on buttocks and legs, abdominal pain; platelet count and bleeding time normal.",
     [("What is the diagnosis?", "Diagnosis"),
      ("Important bedside test?", "Bedside test"),
      ("Treatment lines?", "Treatment"),
      ("Name 2 complications.", "Complications")]),

    (13, "Varicella (Chickenpox)",
     "4-year-old, unvaccinated; fever and widespread itchy vesicular rash.",
     [("Most likely diagnosis?", "Diagnosis"),
      ("Organism?", "Organism"),
      ("Mode of transmission?", "Transmission"),
      ("Give 3 clinical features.", "Clinical features"),
      ("Management in an otherwise healthy child?", "Management"),
      ("Give 2 possible complications.", "Complications"),
      ("Preventive measures?", "Prevention")]),

    (14, "Measles",
     "4-year-old: high-grade fever, cough, coryza, conjunctivitis.",
     [("Diagnosis?", "Diagnosis"),
      ("Causative organism?", "Causative organism"),
      ("Give 2 complications.", "Complications"),
      ("How is it prevented?", "Prevention"),
      ("Management plan?", "Management")]),

    (15, "Roseola Infantum",
     "10-month-old: fever, diarrhea, pink rash, inflamed pharynx, mild conjunctival injection.",
     [("Diagnosis?", "Diagnosis"),
      ("Causative organism?", "Causative organism"),
      ("Describe the sequence of events.", "Sequence"),
      ("Give 2 differentials.", "Differential"),
      ("Outline 2 key management steps.", "Management")]),

    (16, "Hand-Foot-Mouth Disease (HFMD)",
     "4-year-old: low-grade fever, vomited once, maculopapular/papulovesicular rash with mouth sores.",
     [("Diagnosis?", "Diagnosis"),
      ("Causative organism?", "Cause"),
      ("Mode of transmission?", "Mode of transmission"),
      ("Prognosis?", "Prognosis"),
      ("Give 2 complications.", "Complications"),
      ("How to treat?", "Treatment")]),
]

CASES += [
    (17, "Scarlet Fever",
     "5-year-old girl: fever, sore throat, sandpaper rash.",
     [("Diagnosis?", "Diagnosis"),
      ("Organism?", "Organism"),
      ("Give 4 clinical features.", "Clinical features"),
      ("Name the toxin responsible for the rash.", "Toxin"),
      ("Investigations?", "Investigations"),
      ("Treatment?", "Treatment"),
      ("Complications after a 2-3 week latent period?", "Late complications")]),

    (18, "Kawasaki Disease",
     "3-year-old: high fever for 6 days not responding to antibiotics, non-purulent conjunctivitis, red cracked lips, strawberry tongue, polymorphous rash, swelling of hands and feet.",
     [("Diagnosis?", "Diagnosis"),
      ("Give 4 clinical (diagnostic) features.", "Diagnostic criteria"),
      ("Give 2 cardiovascular complications.", "CV complications"),
      ("Initial important investigations?", "Initial investigations"),
      ("Give 2 key management principles.", "Key principles of management")]),

    (19, "Mongolian Spots (Congenital Dermal Melanocytosis)",
     "3-day-old infant, feeding well; blue-gray macules over back and buttocks.",
     [("Describe the skin lesions.", "Skin lesions"),
      ("Diagnosis?", "Diagnosis"),
      ("Management?", "Management"),
      ("Prognosis?", "Prognosis"),
      ("Give 1 differential.", "Differential")]),

    (20, "Lobar Pneumonia",
     "4-year-old girl: high-grade fever, productive cough; CXR provided.",
     [("Radiological findings?", "Radiological findings"),
      ("Causative organism?", "Causative organism"),
      ("Diagnosis?", "Diagnosis"),
      ("Treatment?", "Treatment"),
      ("Give 2 possible complications.", "Complications"),
      ("(v2) Describe the CT.", "Radiological findings"),
      ("(v2) Give 2 clinical features.", "Clinical features"),
      ("(v2) Two most important management steps.", "Treatment")]),

    (21, "Foreign Body Inhalation",
     "2-year-old boy: cough and difficulty breathing started while playing with toys; RR 33, SpO2 88%, absent breath sounds on the right, high-pitched wheeze, nasal flaring.",
     [("Diagnosis?", "Diagnosis"),
      ("Give 2 clinical features.", "Clinical features"),
      ("Investigation to confirm and manage?", "Investigations to confirm and manage"),
      ("Give 2 possible complications if not treated promptly.", "Complications if not treated")]),

    (22, "Cystic Fibrosis (CF)",
     "6-year-old boy: recurrent chest infections, chronic cough, bulky foul-smelling stools, failure to thrive.",
     [("Diagnosis?", "Diagnosis"),
      ("Underlying genetic defect?", "Genetic defect"),
      ("Give 2 possible long-term complications.", "Long-term complications"),
      ("Findings shown in image?", "Image findings"),
      ("Investigation of choice?", "Investigation of choice"),
      ("Management?", "Management")]),

    (23, "Bacterial Meningitis",
     "5-year-old male: fever, tonic-clonic convulsions, increasing lethargy.",
     [("Diagnosis?", "Diagnosis"),
      ("Probable etiology?", "Etiology"),
      ("Essential investigations to arrive at diagnosis?", "Investigations"),
      ("Management options for the suspected diagnosis?", "Management"),
      ("Complications of the illness?", "Complications"),
      ("How can it be prevented in children?", "Prevention")]),

    (24, "Tetralogy of Fallot (TOF)",
     "5-year-old girl: bluish discoloration of lips and nail beds; clubbed fingers; CXR provided.",
     [("What is abnormal in the fingers?", "Finger abnormality"),
      ("Describe the X-ray.", "CXR description"),
      ("Diagnosis?", "Diagnosis"),
      ("Anatomical abnormalities detected by imaging?", "Four anatomical abnormalities"),
      ("Medical management of the cyanotic (tet) spells?", "Management of cyanotic")]),
]

CASES += [
    (25, "Neonatal Jaundice (ABO Incompatibility)",
     "3-day-old: yellowish discoloration of skin starting 24 h ago, sclerae yellow.",
     [("Name of the condition?", "Diagnosis"),
      ("Give 4 possible causes in the neonate.", "Causes"),
      ("Underlying cause in this infant?", "Underlying cause"),
      ("Immediate management — 2 interventions.", "Management"),
      ("Complications if not treated?", "Complications"),
      ("(v2) Clinical diagnosis?", "Clinical diagnosis"),
      ("(v2) Most important history questions?", "History"),
      ("(v2) Investigations?", "Investigations"),
      ("(v2) 3 different causes of this sign?", "Causes (v2)")]),

    (26, "Biliary Atresia",
     "6-week-old full-term male: persistent jaundice, dark urine + pale stool, palpable liver, cholestatic picture (direct bilirubin 7.6).",
     [("What type of jaundice?", "Type of jaundice"),
      ("Which labs?", "Labs"),
      ("Give 2 clinical features.", "Clinical features"),
      ("Give 2 investigations to confirm biliary atresia.", "Investigations"),
      ("Outline the definitive management.", "Definitive management")]),

    (27, "Congenital Diaphragmatic Hernia (CDH)",
     "Newborn: antenatal polyhydramnios, reduced air entry; CXR shows bowel loops in chest with mediastinal shift.",
     [("Describe the X-ray.", "CXR description"),
      ("Diagnosis?", "Diagnosis"),
      ("Pathophysiology leading to respiratory distress?", "Pathophysiology"),
      ("Give 2 key principles of management.", "Key principles of management"),
      ("Definitive management?", "Definitive management")]),

    (28, "Duodenal Atresia",
     "12-hour-old female neonate with Down syndrome features; abdominal X-ray shows the 'double bubble' sign.",
     [("What is the diagnosis?", "Diagnosis"),
      ("What does the X-ray show?", "X-ray finding"),
      ("Genetic abnormality underlying this?", "Genetic abnormality"),
      ("Associated complications?", "Associated anomalies"),
      ("Give 2 key principles of management.", "Key principles of management")]),

    (29, "Duchenne Muscular Dystrophy (DMD)",
     "4-year-old boy: delayed walking, waddling gait.",
     [("Diagnosis?", "Diagnosis"),
      ("Clinical signs?", "Clinical signs"),
      ("Screening serum enzyme investigation?", "Screening enzyme"),
      ("What other investigation?", "Other investigation"),
      ("Mode of inheritance?", "Inheritance")]),

    (30, "Becker Muscular Dystrophy (BMD)",
     "12-year-old previously healthy boy: muscle weakness over the past 4 weeks; maternal uncle with Becker MD.",
     [("What is the diagnosis?", "Diagnosis"),
      ("Mode of inheritance?", "Mode of inheritance"),
      ("Relevant family history significance?", "Significance of maternal uncle"),
      ("Investigation to confirm?", "Investigations to confirm"),
      ("How does this differ from Duchenne?", "How does BMD differ from DMD")]),

    (31, "Myelomeningocele",
     "Newborn: soft cystic swelling on the back covered by a thin membrane.",
     [("Diagnosis?", "Diagnosis"),
      ("Give 2 common neurological problems.", "Neurological problems"),
      ("Give 1 congenital associated anomaly.", "Associated anomaly"),
      ("Outline the management plan.", "Management"),
      ("One measure to help prevent this condition?", "Prevention")]),

    (32, "Hydrocephalus",
     "1-year-old: head growing larger, unable to move limbs well, vomits after feeding; CT brain provided.",
     [("Describe the findings in the picture.", "Findings"),
      ("Diagnosis?", "Diagnosis"),
      ("What is the treatment?", "Treatment"),
      ("Enumerate 2 other causes of a large skull.", "Other causes of large skull")]),
]

CASES += [
    (33, "Cerebral Palsy (CP)",
     "2-year-old girl: inability to use hands or walk; maternal fever during pregnancy.",
     [("Identify the clinical signs in the head and limbs.", "Clinical signs"),
      ("Diagnosis?", "Diagnosis"),
      ("One possible cause for this condition?", "Cause"),
      ("Treatment — mention 2.", "Treatment")]),

    (34, "Sturge-Weber Syndrome",
     "4½-year-old girl on antiepileptic drugs with intractable seizure disorder; facial red/port-wine rash; CT brain provided.",
     [("Cutaneous findings?", "Cutaneous findings"),
      ("Radiologic / intracranial imaging findings?", "Radiologic / intracranial findings"),
      ("What disease is she having?", "Disease"),
      ("Give 2 complications.", "Complications")]),

    (35, "Rickets",
     "3-year-old boy: delayed teething, delayed walking; X-ray and bowed legs on exam.",
     [("Diagnosis?", "Diagnosis"),
      ("Most common cause?", "Cause"),
      ("Name the lower-limb deformity.", "Deformity"),
      ("What is the main treatment?", "Treatment")]),

    (36, "Turner Syndrome",
     "14-year-old girl, shortest in her class.",
     [("Diagnosis?", "Diagnosis"),
      ("Associated features?", "Associated features"),
      ("Give 2 medical conditions that could be present.", "Medical conditions"),
      ("Treatment?", "Treatment")]),

    (37, "Marfan Syndrome",
     "16-year-old girl, tall stature; photos of hands demonstrating wrist sign and thumb sign.",
     [("Names of the signs?", "Names of signs"),
      ("Diagnosis?", "Diagnosis"),
      ("Genetic defect and mode of inheritance?", "Genetic defect"),
      ("Give 3 additional clinical features.", "Additional clinical features")]),

    (38, "Pyelonephritis",
     "6-year-old with fever 39.5°C, loin pain, vomiting; urine: hazy, pH 7, blood 1+, bacteria 3+, nitrite 1+, leukocyte esterase 3+.",
     [("Most striking urine profile abnormalities — mention 3.", "Urine abnormalities"),
      ("Suspected diagnosis?", "Diagnosis"),
      ("How will you confirm the diagnosis?", "Confirmation"),
      ("Mention 1 possible cause.", "Cause"),
      ("Most common organism?", "Organism")]),
]

STANDALONE = (
    "Standalone Topic",
    "Meningococcal Rash vs Viral Rash",
    "Differentiate between meningococcal rash and viral rash (clinical key points + reasoning).",
    [("Color / appearance?", "Color"),
     ("Blanching?", "Blanching"),
     ("Distribution?", "Distribution"),
     ("Associated systemic illness?", "Systemic illness"),
     ("Course / progression?", "Course"),
     ("Immediate action?", "Action")],
)

# ----------------------------------------------------------------------
# Markdown answer parser — pulls all "**Label:**" blocks out of each case
# in STUDY_GUIDE.md, keyed by case number, then by label.
# ----------------------------------------------------------------------

INLINE_BOLD = re.compile(r"\*\*(.+?)\*\*")
INLINE_ITAL = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)")
INLINE_CODE = re.compile(r"`([^`]+)`")

def inline_md(text):
    text = (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))
    text = INLINE_CODE.sub(r"<code>\1</code>", text)
    text = INLINE_BOLD.sub(r"<strong>\1</strong>", text)
    text = INLINE_ITAL.sub(r"<em>\1</em>", text)
    return text


def parse_md_answers(md):
    """Return {case_num(int): [(label, lead_html, ordered_bool, [items_html])]}"""
    cases = {}
    case_pat = re.compile(r"^(?:##\s*)?Case\s+(\d+)\s*[-\u2013\u2014]\s*(.+?)\s*$",
                          re.MULTILINE)
    matches = list(case_pat.finditer(md))
    for i, m in enumerate(matches):
        num = int(m.group(1))
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(md)
        body = md[start:end]
        body = re.sub(r"^\s*-{3,}\s*$", "", body, flags=re.MULTILINE).strip()
        # Skip stem line
        body = re.sub(r"^\*\*Stem:\*\*.*?(?=\n-|\n\n)", "", body, count=1, flags=re.DOTALL).strip()
        cases[num] = parse_sections(body)
    return cases


def parse_sections(body):
    sections = []
    lines = body.split("\n")
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        m = re.match(r"^-\s+\*\*(.+?):\*\*\s*(.*)$", line)
        if not m:
            i += 1
            continue
        label = m.group(1).strip()
        lead = m.group(2).strip()
        sub_lines = []
        i += 1
        while i < n:
            nxt = lines[i]
            if re.match(r"^-\s+\*\*", nxt):
                break
            if re.match(r"^\s+[-\d]", nxt):
                sub_lines.append(nxt)
                i += 1
                continue
            if nxt.strip() == "":
                i += 1
                continue
            if not sub_lines and not nxt.startswith("-"):
                lead = (lead + " " + nxt.strip()).strip()
                i += 1
                continue
            i += 1
        ordered, items = parse_sublist(sub_lines)
        sections.append((label, inline_md(lead), ordered, items))
    return sections


def parse_sublist(sub_lines):
    items, ordered = [], False
    for ln in sub_lines:
        s = ln.strip()
        if not s:
            continue
        mo = re.match(r"^(\d+)\.\s+(.*)$", s)
        if mo:
            ordered = True
            items.append(inline_md(mo.group(2)))
            continue
        mu = re.match(r"^[-*]\s+(.*)$", s)
        if mu:
            items.append(inline_md(mu.group(1)))
            continue
        if items:
            items[-1] += " " + inline_md(s)
    return ordered, items


def find_answer(case_sections, target_label):
    """Fuzzy-match a question's answer_label against the case's section labels."""
    if not case_sections:
        return None
    t = re.sub(r"[^a-z0-9 ]+", " ", target_label.lower()).strip()
    t_words = set(t.split())
    best, best_score = None, 0
    for sec in case_sections:
        lbl = sec[0]
        l = re.sub(r"[^a-z0-9 ]+", " ", lbl.lower()).strip()
        l_words = set(l.split())
        score = 0
        if t == l: score = 100
        elif t in l or l in t: score = 80
        else:
            overlap = len(t_words & l_words)
            if overlap > 0:
                score = 40 + 10 * overlap
        if score > best_score:
            best, best_score = sec, score
    return best if best_score >= 40 else None


# Word-number map for parsing "give two complications"
WORD_NUMS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
}

def parse_counts(qtext):
    """
    From a question like 'Give 2 complications and 2 preventive measures'
    return [2, 2]. From 'Give 3 clinical features' return [3].
    From a question with no number, return [None] (= show all, but cap at 5).
    Compound 'and'/'plus' questions return one count per clause.
    """
    # Split on ' and ' / ', and' / ' + ' (compound questions)
    parts = re.split(r"\s+(?:and|plus|\+)\s+", qtext, flags=re.IGNORECASE)
    counts = []
    for part in parts:
        # Look for a leading digit or number-word
        m = re.search(r"\b(\d+)\b", part)
        if m:
            counts.append(int(m.group(1)))
            continue
        wm = re.search(r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\b",
                       part, flags=re.IGNORECASE)
        if wm:
            counts.append(WORD_NUMS[wm.group(1).lower()])
            continue
        counts.append(None)
    return counts

# Section-style classifier — color per answer type
SECTION_STYLES = {
    "diagnosis":          ("#b91c1c", "#fef2f2", "DX"),
    "finding":            ("#b91c1c", "#fef2f2", "DX"),
    "features":           ("#7c3aed", "#f5f3ff", "FX"),
    "dysmorphic":         ("#7c3aed", "#f5f3ff", "FX"),
    "clinical features":  ("#7c3aed", "#f5f3ff", "FX"),
    "clinical signs":     ("#7c3aed", "#f5f3ff", "SG"),
    "signs":              ("#7c3aed", "#f5f3ff", "SG"),
    "symptoms":           ("#7c3aed", "#f5f3ff", "SX"),
    "investigations":     ("#0ea5e9", "#f0f9ff", "IX"),
    "investigation":      ("#0ea5e9", "#f0f9ff", "IX"),
    "labs":               ("#0ea5e9", "#f0f9ff", "LB"),
    "imaging":            ("#0ea5e9", "#f0f9ff", "IM"),
    "x-ray":              ("#0ea5e9", "#f0f9ff", "XR"),
    "ct":                 ("#0ea5e9", "#f0f9ff", "CT"),
    "radiological":       ("#0ea5e9", "#f0f9ff", "RAD"),
    "cbc":                ("#0ea5e9", "#f0f9ff", "LB"),
    "differential":       ("#f59e0b", "#fffbeb", "DDX"),
    "risk factors":       ("#d97706", "#fffbeb", "RF"),
    "complications":      ("#dc2626", "#fef2f2", "CX"),
    "complication":       ("#dc2626", "#fef2f2", "CX"),
    "medical problems":   ("#dc2626", "#fef2f2", "CX"),
    "cardiovascular":     ("#dc2626", "#fef2f2", "CV"),
    "management":         ("#059669", "#ecfdf5", "MX"),
    "treatment":          ("#059669", "#ecfdf5", "MX"),
    "prevention":         ("#0d9488", "#f0fdfa", "PV"),
    "preventive":         ("#0d9488", "#f0fdfa", "PV"),
    "prognosis":          ("#6366f1", "#eef2ff", "PG"),
    "genetic":            ("#7c3aed", "#f5f3ff", "GN"),
    "genetics":           ("#7c3aed", "#f5f3ff", "GN"),
    "etiology":           ("#7c3aed", "#f5f3ff", "ET"),
    "inheritance":        ("#7c3aed", "#f5f3ff", "GN"),
    "cause":              ("#7c3aed", "#f5f3ff", "ET"),
    "causes":             ("#7c3aed", "#f5f3ff", "ET"),
    "organism":           ("#7c3aed", "#f5f3ff", "ORG"),
    "causative organism": ("#7c3aed", "#f5f3ff", "ORG"),
    "transmission":       ("#0891b2", "#ecfeff", "TX"),
    "pathophysiology":    ("#7c3aed", "#f5f3ff", "PP"),
    "associated":         ("#0891b2", "#ecfeff", "AS"),
    "facies":             ("#7c3aed", "#f5f3ff", "FX"),
    "rash":               ("#7c3aed", "#f5f3ff", "FX"),
    "skin lesions":       ("#7c3aed", "#f5f3ff", "FX"),
    "deformity":          ("#7c3aed", "#f5f3ff", "FX"),
    "toxin":              ("#7c3aed", "#f5f3ff", "TX"),
    "sequence":           ("#0891b2", "#ecfeff", "SEQ"),
    "family history":     ("#0891b2", "#ecfeff", "HX"),
    "history":            ("#0891b2", "#ecfeff", "HX"),
    "bedside":            ("#0ea5e9", "#f0f9ff", "BS"),
    "urine":              ("#0ea5e9", "#f0f9ff", "UR"),
    "long-term":          ("#dc2626", "#fef2f2", "CX"),
    "late":               ("#dc2626", "#fef2f2", "CX"),
    "type of jaundice":   ("#b91c1c", "#fef2f2", "DX"),
    "underlying cause":   ("#7c3aed", "#f5f3ff", "ET"),
    "anatomical":         ("#0ea5e9", "#f0f9ff", "AN"),
    "vs duchenne":        ("#0891b2", "#ecfeff", "CMP"),
    "histopathology":     ("#7c3aed", "#f5f3ff", "PATH"),
    "cardinal":           ("#7c3aed", "#f5f3ff", "FX"),
    "screening":          ("#0ea5e9", "#f0f9ff", "IX"),
    "other":              ("#475569", "#f1f5f9", "OTH"),
    "definitive":         ("#059669", "#ecfdf5", "MX"),
}
DEFAULT_STYLE = ("#475569", "#f1f5f9", "::")

def classify(label):
    key = label.lower().strip().rstrip(":").strip()
    if key in SECTION_STYLES:
        return SECTION_STYLES[key]
    for k, v in SECTION_STYLES.items():
        if k in key:
            return v
    return DEFAULT_STYLE

# ----------------------------------------------------------------------
# CSS — same card aesthetic as v2, with Q-block + A-card layout
# ----------------------------------------------------------------------
CSS = r"""
@page { size: A4; margin: 12mm 11mm 14mm 11mm; }
* { box-sizing: border-box; }
html, body {
  font-family: -apple-system, "Segoe UI", system-ui, "Helvetica Neue", Arial, sans-serif;
  font-size: 9.5pt;
  line-height: 1.4;
  color: #1f2937;
  margin: 0;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

h1 {
  font-size: 22pt; color: #b91c1c;
  border-bottom: 3px solid #b91c1c;
  padding-bottom: 6px; margin: 0 0 10px;
}

.title-page { page-break-after: always; padding-top: 40mm; }
.title-page h1 { font-size: 32pt; text-align: center; border: none; }
.title-page .sub { text-align: center; color: #6b7280; font-size: 14pt; margin-top: 6px; }
.title-page .meta { text-align: center; margin-top: 30mm; color: #94a3b8; font-size: 10pt; }
.title-page .note { text-align: center; margin-top: 8mm; color: #374151; font-size: 10pt;
  max-width: 140mm; margin-left: auto; margin-right: auto; line-height: 1.5; }

.toc-page { page-break-after: always; }
.toc-page h2 {
  font-size: 16pt; color: #0c4a6e; margin: 0 0 12px;
  border-bottom: 2px solid #0c4a6e; padding-bottom: 4px;
}
.toc-grid { column-count: 2; column-gap: 18px; font-size: 9.5pt; line-height: 1.5; }
.toc-grid .toc-item { break-inside: avoid; padding: 2px 0; border-bottom: 1px dotted #cbd5e1; }
.toc-grid .toc-item .num { display: inline-block; width: 22px; color: #0c4a6e; font-weight: 700; }

.case { page-break-before: always; break-before: page; }
.case-header {
  background: linear-gradient(90deg, #0c4a6e 0%, #0ea5e9 100%);
  color: white; padding: 9px 14px; border-radius: 6px 6px 0 0;
  font-size: 13.5pt; font-weight: 700; letter-spacing: 0.2px;
}
.case-header .case-num {
  display: inline-block; background: rgba(255,255,255,0.22);
  padding: 2px 9px; border-radius: 4px; font-size: 10.5pt;
  margin-right: 10px; font-weight: 600;
}
.stem {
  background: #fff7ed; border: 1px solid #fed7aa;
  border-left: 4px solid #f59e0b;
  padding: 8px 12px; border-radius: 0 0 6px 6px;
  margin-bottom: 12px; font-size: 10pt;
}
.stem .lbl {
  color: #c2410c; font-weight: 700; margin-right: 6px;
  text-transform: uppercase; letter-spacing: 0.4px; font-size: 8.5pt;
}

.qa { margin: 0 0 9px; page-break-inside: avoid; break-inside: avoid; }
.q {
  display: flex; align-items: flex-start;
  background: #f1f5f9; border-left: 4px solid #0c4a6e;
  padding: 6px 10px; border-radius: 4px 4px 0 0;
  font-size: 10pt; color: #0c4a6e; font-weight: 600;
}
.q .qnum {
  display: inline-block; min-width: 22px;
  background: #0c4a6e; color: white;
  font-size: 9pt; font-weight: 700;
  padding: 1px 6px; margin-right: 8px;
  border-radius: 3px; text-align: center;
}
.a {
  border: 1px solid var(--accent, #cbd5e1);
  border-top: none;
  border-left: 4px solid var(--accent, #475569);
  background: var(--tint, #f8fafc);
  border-radius: 0 0 4px 4px;
  padding: 7px 12px 8px;
}
.a .sec-head {
  display: flex; align-items: center;
  font-size: 8.5pt; font-weight: 700;
  color: var(--accent, #475569);
  text-transform: uppercase; letter-spacing: 0.5px;
  margin-bottom: 4px;
}
.a .sec-head .tag {
  display: inline-block;
  background: var(--accent, #475569); color: white;
  font-size: 7.5pt; padding: 1px 5px; border-radius: 3px;
  margin-right: 6px; letter-spacing: 0.3px;
}
.a .lead { font-size: 9.5pt; color: #111827; margin: 0 0 3px; }
.a .lead strong { color: var(--accent, #b91c1c); }
.a ul, .a ol { padding-left: 20px; margin: 2px 0 0; font-size: 9.25pt; }
.a li { margin: 1px 0; line-height: 1.4; }
.a ul li::marker { color: var(--accent, #475569); }
.a ol li::marker { color: var(--accent, #475569); font-weight: 700; }
.a strong { color: #b91c1c; }
.a-missing {
  border: 1px dashed #cbd5e1; padding: 5px 10px;
  font-size: 8.5pt; color: #94a3b8; font-style: italic;
}

/* PICKS list mixes 'main picks' (★) and 'easy picks' (☆ safety net) */
.a ul.picks, .a ol.picks { padding-left: 20px; margin: 2px 0 0; }

.a ul.picks li.main-pick, .a ol.picks li.main-pick {
  font-weight: 500;
  color: #111827;
  padding: 2px 0;
}
.a ul.picks li.easy-pick, .a ol.picks li.easy-pick {
  font-weight: 400;
  color: #334155;
  padding: 2px 0;
  font-size: 9pt;
}
.a ul.picks li .star,
.a ol.picks li .star {
  color: var(--accent, #b91c1c);
  font-weight: 700;
  margin-right: 4px;
  font-size: 10pt;
}
.a ul.picks li .star.easy,
.a ol.picks li .star.easy {
  color: var(--accent, #b91c1c);
  opacity: 0.55;
  font-weight: 400;
}
.a ol.picks li.easy-pick::marker { color: #94a3b8; font-weight: 500; }
.a ol.picks li.main-pick::marker { font-weight: 800; color: var(--accent, #b91c1c); }

/* EXTRAS = backup options under a muted heading */
.extras-head {
  margin-top: 6px;
  font-size: 7.5pt;
  color: #94a3b8;
  font-style: italic;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  border-top: 1px dotted #cbd5e1;
  padding-top: 4px;
}
.a ul.extras {
  list-style: disc;
  padding-left: 20px;
  margin: 2px 0 0;
  font-size: 8.5pt;
  color: #6b7280;
}
.a ul.extras li { line-height: 1.35; margin: 1px 0; }
.a ul.extras li::marker { color: #cbd5e1; }
.a ul.extras strong { color: #6b7280; font-weight: 600; }

/* Compound 'X and Y' questions render as side-by-side cards */
.multi-a {
  display: flex;
  gap: 8px;
  align-items: stretch;
}
.multi-a-col {
  flex: 1 1 0;
  min-width: 0;
}
.multi-a-col .a { border-radius: 0 0 4px 4px; height: 100%; }

code { background: #f3f4f6; padding: 1px 4px; border-radius: 3px; font-size: 8.5pt; color: #b91c1c; }

/* --- MODEL ANSWERS block (end of every case) --------------------------- */
.model-answers {
  margin-top: 14px;
  padding: 10px 14px 12px;
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
  border-left: 5px solid #059669;
  border-radius: 6px;
  page-break-inside: avoid;
  break-inside: avoid;
}
.model-head {
  font-size: 11pt;
  font-weight: 800;
  color: #059669;
  letter-spacing: 0.3px;
  margin-bottom: 6px;
}
.model-head .ma-sub {
  font-weight: 500;
  font-size: 8.5pt;
  color: #6b7280;
  font-style: italic;
  letter-spacing: 0.2px;
}
.model-list {
  list-style: none;
  padding-left: 0;
  margin: 0;
  font-size: 9.5pt;
  line-height: 1.45;
  color: #111827;
}
.model-list li.ma-item {
  margin: 0 0 7px;
  padding: 0;
  page-break-inside: avoid;
  break-inside: avoid;
}
.model-list li.ma-item:last-child { margin-bottom: 0; }

.ma-qline {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-bottom: 2px;
}
.ma-qnum {
  display: inline-block;
  background: #059669;
  color: white;
  font-size: 8pt;
  font-weight: 800;
  padding: 1px 6px;
  border-radius: 3px;
  letter-spacing: 0.3px;
  flex: 0 0 auto;
}
.ma-qtext {
  color: #047857;
  font-size: 8.5pt;
  font-weight: 600;
  font-style: italic;
}
.ma-aline {
  padding-left: 28px;
  color: #111827;
}
.ma-aline strong { color: #0284c7; }   /* fallback if no hl-* class */

.pearl {
  margin-top: 9px;
  padding: 7px 11px;
  background: #fffbeb;
  border-left: 3px solid #f59e0b;
  border-radius: 0 4px 4px 0;
  font-size: 9.5pt;
  color: #78350f;
}
.pearl .pearl-lbl {
  color: #c2410c;
  font-weight: 800;
  margin-right: 6px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  font-size: 8.5pt;
}

/* Descriptive bolding inside Model Answers + Pearl */
.hl-red    { color: #b91c1c; font-weight: 700; }
.hl-green  { color: #047857; font-weight: 700; }
.hl-purple { color: #6d28d9; font-weight: 700; font-style: italic; }
.hl-orange { color: #c2410c; font-weight: 700; }
.hl-blue   { color: #0284c7; font-weight: 700; }   /* lead clinical term (baby blue) */

/* ---- Per-case primary image figure ---- */
.case-fig { margin: 10px auto 14px; text-align: center; page-break-inside: avoid; }
.case-fig img { max-width: 320px; max-height: 240px; width: auto; height: auto;
                border: 1px solid #cbd5e1; border-radius: 6px;
                box-shadow: 0 2px 6px rgba(15,23,42,.10); }
.case-fig figcaption { margin-top: 5px; font-size: 10.5px; color: #475569;
                       font-style: italic; line-height: 1.35; max-width: 360px;
                       margin-left: auto; margin-right: auto; }
.case-fig-photo img        { border-color: #16a34a; }
.case-fig-imaging img      { border-color: #f59e0b; }
.case-fig-illustration img { border-color: #0284c7; }
.case-fig-other img        { border-color: #94a3b8; }
.case-fig-microscopy img   { border-color: #7c3aed; }
.case-fig-histology img    { border-color: #7c3aed; }

/* Findings bullets shown under microscopy/histology images */
.case-findings {
  list-style: disc inside;
  margin: 6px auto 4px;
  padding: 8px 12px;
  max-width: 360px;
  font-size: 10.5px;
  line-height: 1.4;
  color: #1e293b;
  background: #faf5ff;            /* very pale purple, matches microscopy border */
  border: 1px solid #ddd6fe;
  border-radius: 5px;
  text-align: left;
  page-break-inside: avoid;
}
.case-findings li { margin: 2px 0; }
.case-findings li b { color: #6d28d9; }   /* purple bold for findings keywords */
.case-findings li i { color: #4c1d95; }

/* ---- Comparison table (used by standalone Meningococcal vs Viral) ---- */
.cmp-wrap { margin: 12px 0 18px; border: 1px solid #cbd5e1; border-radius: 6px; overflow: hidden; }
.cmp-head { background: #0f172a; color: #f8fafc; padding: 8px 12px; font-weight: 700; font-size: 13.5px; }
.cmp-table { width: 100%; border-collapse: collapse; font-size: 11.5px; line-height: 1.45; }
.cmp-table th, .cmp-table td { padding: 7px 10px; border-bottom: 1px solid #e2e8f0; vertical-align: top; text-align: left; }
.cmp-table thead th { background: #f1f5f9; font-size: 11px; text-transform: uppercase; letter-spacing: .04em; color: #475569; }
.cmp-table thead th.hdr-m { color: #7f1d1d; }
.cmp-table thead th.hdr-v { color: #075985; }
.cmp-table tbody th { background: #f8fafc; font-weight: 600; color: #0f172a; width: 95px; }
.cmp-table td.m { background: #fef2f2; }
.cmp-table td.v { background: #f0f9ff; }
.cmp-table b.r { color: #b91c1c; }
.cmp-table b.g { color: #047857; }
.cmp-table b.o { color: #c2410c; }
.cmp-table b.b { color: #0284c7; }
.cmp-pearl { padding: 8px 12px; background: #fef3c7; border-top: 1px solid #fbbf24; color: #78350f; font-size: 12px; }
"""

# ----------------------------------------------------------------------
# HTML render
# ----------------------------------------------------------------------

def _strip_tags(html):
    return re.sub(r"<[^>]+>", "", html)


def _memorability_score(item_html):
    """Lower = easier to memorize. Prefer short, low-comma, low-paren items."""
    plain = _strip_tags(item_html)
    words = len(plain.split())
    commas = plain.count(",")
    parens = plain.count("(")
    arrows = plain.count("→") + plain.count("->")
    # Penalize length, punctuation, and explanatory arrows
    return words + 2 * commas + 3 * parens + 4 * arrows


def _pick_easy_backups(extras, n=2):
    """From the leftover items, return up to N of the shortest / easiest.
    Returns (easies_in_original_order, remaining_extras_in_original_order)."""
    if not extras or n <= 0:
        return [], extras
    # Index + score, pick the N lowest-score, then re-sort by original index
    scored = sorted(enumerate(extras), key=lambda t: (_memorability_score(t[1]), t[0]))
    picked_idx = set(i for i, _ in scored[:n])
    easies = [item for i, item in enumerate(extras) if i in picked_idx]
    rest    = [item for i, item in enumerate(extras) if i not in picked_idx]
    return easies, rest


def render_answer_card(label, sec, n_pick=None):
    """sec = (label, lead_html, ordered_bool, [items_html]) OR None.
    n_pick: if int, show the first N items as 'main picks' (★) plus up to 2
    short/easy 'safety net' items (☆) inside the same main list; anything
    further goes into a muted backup section below.
    If n_pick is None, show all items normally."""
    accent, tint, tag = classify(label)
    if sec is None:
        return (f'<div class="a" style="--accent:{accent};--tint:{tint};">'
                f'<div class="sec-head"><span class="tag">{tag}</span>{label}</div>'
                f'<div class="a-missing">[answer not in study guide — add to STUDY_GUIDE.md under this case as <code>**{label}:**</code>]</div>'
                f'</div>')
    src_label, lead, ordered, items = sec
    out = [f'<div class="a" style="--accent:{accent};--tint:{tint};">']
    out.append(f'<div class="sec-head"><span class="tag">{tag}</span>{src_label}</div>')
    if lead:
        out.append(f'<div class="lead">{lead}</div>')

    if items:
        if n_pick is not None and len(items) > n_pick:
            main_picks = items[:n_pick]
            leftover = items[n_pick:]
            easies, extras = _pick_easy_backups(leftover, n=2)
        else:
            main_picks = items
            easies = []
            extras = []

        if main_picks or easies:
            list_tag = "ol" if ordered else "ul"
            out.append(f'<{list_tag} class="picks">')
            for it in main_picks:
                out.append(f'<li class="main-pick"><span class="star">&#9733;</span> {it}</li>')
            for it in easies:
                out.append(f'<li class="easy-pick"><span class="star easy">&#9734;</span> {it}</li>')
            out.append(f"</{list_tag}>")
        if extras:
            out.append('<div class="extras-head">+ further backup options:</div>')
            out.append('<ul class="extras">')
            for it in extras:
                out.append(f"<li>{it}</li>")
            out.append("</ul>")
    out.append("</div>")
    return "\n".join(out)


def render_qa(qtext, label_spec, sections, qnum):
    """Render one Q-block plus its answer card(s).
    label_spec: string  -> single answer
                list    -> multi-card (compound 'X and Y' question)
    """
    if isinstance(label_spec, str):
        labels = [label_spec]
    else:
        labels = list(label_spec)

    counts = parse_counts(qtext)
    # Align counts to labels: if more labels than counts, pad with the last count
    # (e.g., '2 complications and preventive measures' -> [2] -> pad to [2, 2])
    while len(counts) < len(labels):
        counts.append(counts[-1] if counts else None)
    # If only one label but multiple counts, sum them as max for that single card
    if len(labels) == 1 and len(counts) > 1:
        cnt = sum(c for c in counts if c is not None) or None
        counts = [cnt]

    out = ['<div class="qa">']
    out.append(f'<div class="q"><span class="qnum">Q{qnum}</span>{qtext}</div>')

    if len(labels) > 1:
        out.append('<div class="multi-a">')
        for lbl, cnt in zip(labels, counts):
            ans = find_answer(sections, lbl)
            out.append('<div class="multi-a-col">')
            out.append(render_answer_card(lbl, ans, n_pick=cnt))
            out.append('</div>')
        out.append('</div>')
    else:
        ans = find_answer(sections, labels[0])
        out.append(render_answer_card(labels[0], ans, n_pick=counts[0]))

    out.append('</div>')
    return "\n".join(out)


# ----------------------------------------------------------------------
# Descriptive auto-bolding for Model Answers.
# Categories (highest priority first; each token only highlighted once per
# sentence to avoid noise):
#   RED   = diagnoses, red-flag warnings, "do not", "#1 cause of death"
#   GREEN = drugs, vaccines, procedures, definitive treatments
#   PURPLE= organisms (Latin binomials, common pathogens)
#   ORANGE= key numbers, timings, thresholds, doses
# ----------------------------------------------------------------------

# Each tuple: (compiled regex, css class). Order matters — earlier matches win.
HIGHLIGHT_RULES = [
    # RED — red flags / emergencies / mortality / "do not"
    (re.compile(r"\bDO NOT\b[^.;\n]*", re.IGNORECASE), "hl-red"),
    (re.compile(r"\bmedical emergency\b", re.IGNORECASE), "hl-red"),
    (re.compile(r"#\s*1 cause of (?:death|mortality)", re.IGNORECASE), "hl-red"),
    (re.compile(r"\bleading cause of death\b", re.IGNORECASE), "hl-red"),
    (re.compile(r"\bcommonest cause of death\b", re.IGNORECASE), "hl-red"),
    (re.compile(r"\bcan be fatal\b[^.;\n]*", re.IGNORECASE), "hl-red"),
    (re.compile(r"\bnever\b", re.IGNORECASE), "hl-red"),

    # GREEN — drugs (generic + brand), vaccines, procedures, definitive treatments
    (re.compile(r"\b(?:ceftriaxone|cefotaxime|amoxicillin|co-amoxiclav|"
                r"benzylpenicillin|penicillin\s*V|vancomycin|clarithromycin|"
                r"erythromycin|azithromycin|aciclovir|acyclovir|"
                r"ciprofloxacin|rifampicin|tobramycin|dexamethasone|"
                r"prednisolone|prednisone|hydroxyurea|hydroxycarbamide|"
                r"morphine|propranolol|paracetamol|ibuprofen|aspirin|"
                r"IVIG|intravenous immunoglobulin|surfactant|poractant alfa|"
                r"dornase alfa|baclofen|botulinum toxin|salbutamol|"
                r"deferasirox|deferoxamine|cholecalciferol|vitamin\s*[ADK](?:[3-9])?|"
                r"vit\.?\s*[ADK](?:[3-9])?|folic acid|losartan|rasburicase|allopurinol|"
                r"ivacaftor|elexacaftor|tezacaftor|lumacaftor|CFTR modulators?|"
                r"CREON|pancreatic enzyme replacement|"
                r"oestrogen|estrogen|growth hormone)\b", re.IGNORECASE), "hl-green"),

    # Procedures / definitive operations
    (re.compile(r"\b(?:Kasai(?:\s+hepatoportoenterostomy)?|"
                r"duodenoduodenostomy|VP\s+shunt|ventriculoperitoneal\s+shunt|"
                r"endoscopic third ventriculostomy|ETV|"
                r"exchange transfusion|phototherapy|rigid bronchoscopy|"
                r"lumbar puncture|LP|bone marrow (?:aspirate|biopsy)|"
                r"chest physiotherapy|stem[- ]cell transplant|lung transplant|"
                r"sweat chloride test|HIDA scan|echocardiogram|2D echocardiogram|"
                r"DMSA scan|MCUG|karyotype|FISH|NIPT|amniocentesis|CVS|"
                r"hemoglobin electrophoresis|HPLC|genetic testing)\b", re.IGNORECASE), "hl-green"),

    # Vaccines
    (re.compile(r"\b(?:MMR|MenB|MenACWY|PCV13|PPV23|Hib|Bexsero|BCG|HPV|"
                r"varicella vaccine|pneumococcal vaccine|meningococcal vaccine|"
                r"VZIG)\b"), "hl-green"),

    # Regimens / management mnemonics
    (re.compile(r"\bRIPE\b"), "hl-green"),
    (re.compile(r"\bABCDE\b"), "hl-green"),
    (re.compile(r"\bsepsis 6\b", re.IGNORECASE), "hl-green"),

    # PURPLE — organisms (Latin and common names)
    (re.compile(r"\b(?:Neisseria meningitidis|Streptococcus pneumoniae|"
                r"Streptococcus pyogenes|Staphylococcus aureus|Staph\s+aureus|"
                r"Strep\s+pneumoniae|S\.\s*pneumoniae|S\.\s*pyogenes|"
                r"S\.\s*aureus|Haemophilus influenzae(?:\s+type\s*b)?|"
                r"Escherichia coli|E\.\s*coli|Mycoplasma pneumoniae|"
                r"Listeria(?:\s+monocytogenes)?|Pseudomonas aeruginosa|"
                r"Klebsiella|Proteus|Enterococcus|Group [AB] (?:beta-haemolytic\s+)?"
                r"strep(?:tococcus)?|"
                r"Coxsackievirus(?:\s+A?\d+)?|enterovirus(?:\s*\d+)?|"
                r"varicella[- ]zoster virus|VZV|measles virus|"
                r"human herpesvirus[- ]?6|HHV[- ]?6|HHV[- ]?7|"
                r"parvovirus B19|paramyxovirus)\b"), "hl-purple"),

    # ORANGE — numbers / timings / thresholds / doses
    # Time intervals / thresholds
    (re.compile(r"\b(?:within|in)\s+\d+\s*(?:hours?|h|hrs?|days?|weeks?|wks?|months?|years?|yrs?)\b", re.IGNORECASE), "hl-orange"),
    (re.compile(r"\b(?:before|after)\s+(?:age\s+)?\d+\s*(?:hours?|h|hrs?|days?|weeks?|wks?|months?|years?|yrs?)\b", re.IGNORECASE), "hl-orange"),
    (re.compile(r"\bfor\s+\d+(?:[-–]\d+)?\s*(?:hours?|h|hrs?|days?|weeks?|wks?|months?|years?|yrs?)\b", re.IGNORECASE), "hl-orange"),
    (re.compile(r"\bage[ds]?\s+\d+(?:[-–]\d+)?\s*(?:years?|yrs?|months?)\b", re.IGNORECASE), "hl-orange"),
    (re.compile(r"\b\d+(?:[-–]\d+)?\s*mg/kg(?:/(?:day|dose))?\b"), "hl-orange"),
    (re.compile(r"\b\d+(?:[-–]\d+)?\s*g/kg\b"), "hl-orange"),
    (re.compile(r"\b\d+(?:[-–]\d+)?\s*mL/kg\b"), "hl-orange"),
    (re.compile(r"\b\d+(?:,\d{3})?(?:[-–]\d+(?:,\d{3})?)?\s*IU(?:/(?:day|kg))?\b"), "hl-orange"),
    (re.compile(r"\b\d+(?:\.\d+)?\s*g/dL\b"), "hl-orange"),
    (re.compile(r"\b\d+(?:\.\d+)?\s*g/L\b"), "hl-orange"),
    (re.compile(r"\bSpO[₂2]\s*[<>≥≤]\s*\d+%?\b"), "hl-orange"),
    (re.compile(r"\b\d+(?:\.\d+)?\s*mmol/L\b"), "hl-orange"),
    (re.compile(r"\b\d+(?:\.\d+)?\s*[µu]mol/L\b"), "hl-orange"),
    (re.compile(r"\b(?:>|<|≥|≤)\s?\d+\s*(?:days?|weeks?|months?|years?|hours?|h)\b"), "hl-orange"),
    (re.compile(r"\b\d+(?:[-–]\d+)?\s*(?:days?|weeks?|months?|years?)\b(?!\s*(?:old|of\s+age))",
                re.IGNORECASE), "hl-orange"),
]


# Match the first natural break in an answer. The lead term ends just
# BEFORE this delimiter so the bolded headline stays clean.
#   - " — ", " – ", " - "  (em/en/hyphen with surrounding spaces)
#   - ":" / ";" / "," at end of clause
#   - " (" preceded by a space (parenthetical qualifier — keep the space outside the bold)
#   - "." followed by space-or-end (sentence terminator)
_LEAD_DELIM_RE = re.compile(r"\s+[—–-]\s+|\s+\(|[:;,]|\.(?:\s|$)")


def bold_lead_term(html):
    """Bold the leading clinical term of a model answer (the diagnosis /
    drug / action that comes BEFORE the first delimiter). Wraps it in
    <strong class="hl-green"> so the answer's headline reads as the
    primary takeaway.

    Skips if the answer already starts with a tag (e.g. <strong>) so we
    never double-wrap. Skips numbered/bulleted leads."""
    if not html:
        return html
    # Case A: answer starts with an existing hl-* span (e.g. drug name was
    # already colored by HIGHLIGHT_RULES). Just wrap that opening span in
    # <strong> so it bolds without losing color.
    m_lead_span = re.match(r'^(<span class="hl-(?:green|red|orange|purple)">[^<]+</span>)', html)
    if m_lead_span:
        span = m_lead_span.group(1)
        return f"<strong>{span}</strong>" + html[m_lead_span.end():]
    if html[0] == "<":
        return html
    stripped = html.lstrip()
    if not stripped or stripped[0] in "0123456789-•*":
        return html
    # Find first delimiter OR first embedded tag, whichever comes earlier.
    m_delim = _LEAD_DELIM_RE.search(html)
    m_tag   = re.search(r"<", html)
    candidates = [(m.start(), kind) for kind, m in (("delim", m_delim), ("tag", m_tag)) if m]
    if candidates:
        cut, _ = min(candidates)
        lead = html[:cut].rstrip()
        rest = html[cut:]
    else:
        # No delimiter / tag — whole string is the lead (short single phrase).
        lead = html.rstrip()
        rest = ""
        cut = len(html)
    if not lead or len(lead) > 80:  # guard against runaway matches
        return html
    spacer = html[len(lead):cut]
    return f'<strong class="hl-blue">{lead}</strong>{spacer}{rest}'


def descriptive_bold(html):
    """Apply category-colored highlight spans to the rendered HTML of one
    model-answer sentence. Skips text already inside <strong> tags so we
    don't double-wrap, and skips text already inside <span class='hl-*'>."""
    # Tokenize into segments where each segment is either tag or text.
    # Apply rules only to text outside <strong> / <em> / <code> / <span>.
    out_parts = []
    pos = 0
    # Walk tag-by-tag
    tag_re = re.compile(r"<[^>]+>")
    for m in tag_re.finditer(html):
        if m.start() > pos:
            text_segment = html[pos:m.start()]
            out_parts.append(_apply_rules(text_segment))
        out_parts.append(m.group(0))
        pos = m.end()
    if pos < len(html):
        out_parts.append(_apply_rules(html[pos:]))
    return "".join(out_parts)


def _apply_rules(text):
    if not text.strip():
        return text
    # Track ranges already highlighted so the second rule won't overlap
    spans = []  # list of (start, end, css_class)
    for pat, css in HIGHLIGHT_RULES:
        for m in pat.finditer(text):
            s, e = m.start(), m.end()
            if any(not (e <= ss or s >= ee) for ss, ee, _ in spans):
                continue  # overlaps an earlier highlight, skip
            spans.append((s, e, css))
    if not spans:
        return text
    spans.sort()
    out = []
    cursor = 0
    for s, e, css in spans:
        out.append(text[cursor:s])
        out.append(f'<span class="{css}">{text[s:e]}</span>')
        cursor = e
    out.append(text[cursor:])
    return "".join(out)


def render_model_answers(key, questions=None):
    """Render the Model Answers + Pearl block for a case key (int or str).
    questions: the list of (qtext, label) tuples from CASES — used to label
    each model answer with its question number AND prompt."""
    ma = MODEL_ANSWERS.get(key)
    if not ma:
        return ""
    answers = ma.get("answers", [])
    pearl = ma.get("pearl", "")
    out = ['<div class="model-answers">']
    out.append('<div class="model-head">Model Answers <span class="ma-sub">(one-shot, exam-ready — written like you would on the paper)</span></div>')
    out.append('<ul class="model-list">')
    for idx, a in enumerate(answers, 1):
        qtext = ""
        if questions and idx - 1 < len(questions):
            qtext = questions[idx - 1][0]
        html = bold_lead_term(descriptive_bold(inline_md(a)))
        qtext_html = inline_md(qtext) if qtext else ""
        out.append(
            '<li class="ma-item">'
            f'<div class="ma-qline"><span class="ma-qnum">Q{idx}</span>'
            f'<span class="ma-qtext">{qtext_html}</span></div>'
            f'<div class="ma-aline">{html}</div>'
            '</li>'
        )
    out.append('</ul>')
    if pearl:
        pearl_html = descriptive_bold(inline_md(pearl))
        out.append(f'<div class="pearl"><span class="pearl-lbl">Pearl</span>{pearl_html}</div>')
    out.append('</div>')
    return "\n".join(out)


import json as _json
REPO_IMG_PEDS = r"C:\Users\erick\AppData\Local\Temp\opencode\im-osce-quiz\img\peds"


def _all_images_for(case_num):
    """Return list of dicts for all images of case_num, merged from
    manifest_v2.json + manifest.json (v2 first). Each dict carries:
    {url, label, type, findings (list or None), filename}.
    Dedup by filename (v2 wins).
    """
    case_dir = os.path.join(REPO_IMG_PEDS, f"ped{case_num}")
    if not os.path.isdir(case_dir):
        return []
    seen = set()
    out = []
    for mf_name in ("manifest_v2.json", "manifest.json"):
        mp = os.path.join(case_dir, mf_name)
        if not os.path.isfile(mp):
            continue
        try:
            with open(mp, "r", encoding="utf-8") as f:
                m = _json.load(f)
        except Exception:
            continue
        for img in m.get("images") or []:
            fname = img.get("filename")
            if not fname or fname in seen:
                continue
            abs_path = os.path.join(case_dir, fname)
            if not os.path.isfile(abs_path):
                continue
            seen.add(fname)
            out.append({
                "url": "file:///" + abs_path.replace("\\", "/"),
                "label": (img.get("label") or "").strip(),
                "type": (img.get("type") or "OTHER").upper(),
                "findings": img.get("findings"),
                "filename": fname,
                "pdf_primary": bool(img.get("pdf_primary")),
                "primary": bool(img.get("primary")),
            })
    return out


def _is_microscopy(img):
    """True if image is a histology/microscopy/smear image worth annotating."""
    label_u = (img.get("label") or "").upper()
    typ = (img.get("type") or "").upper()
    if typ in ("MICROSCOPY", "HISTOLOGY"):
        return True
    return any(k in label_u for k in ("MICROSCOPY", "HISTOLOGY", "SMEAR", "BIOPSY", "GRAM"))


def _primary_image_for(case_num):
    """Return (file:///abs_url, label, type) for the primary image of case_num,
    or None if no manifest / no primary / file missing.

    Read order: manifest_v2.json first (so v2 supplements can override v1's
    primary), then manifest.json. Within a manifest, prefer entry with
    primary=True; fall back to first PHOTO; fall back to first image.
    """
    case_dir = os.path.join(REPO_IMG_PEDS, f"ped{case_num}")
    if not os.path.isdir(case_dir):
        return None
    for mf_name in ("manifest_v2.json", "manifest.json"):
        mf_path = os.path.join(case_dir, mf_name)
        if not os.path.isfile(mf_path):
            continue
        try:
            with open(mf_path, "r", encoding="utf-8") as f:
                m = _json.load(f)
        except Exception:
            continue
        images = m.get("images") or []
        if not images:
            continue
        # Priority order:
        #  1. pdf_primary: true                — hand-curated PDF override (wins everything)
        #  2. PHOTO type                        — real clinical photo
        #  3. primary: true                     — site-gallery primary
        #  4. IMAGING type                      — X-ray / US / CT / MRI / microscopy
        #  5. first image
        chosen = next((i for i in images if i.get("pdf_primary")), None)
        if chosen is None:
            chosen = next((i for i in images if (i.get("type") or "").upper() == "PHOTO"), None)
        if chosen is None:
            chosen = next((i for i in images if i.get("primary")), None)
        if chosen is None:
            chosen = next((i for i in images if (i.get("type") or "").upper() == "IMAGING"), None)
        if chosen is None:
            chosen = images[0]
        fname = chosen.get("filename")
        if not fname:
            continue
        abs_path = os.path.join(case_dir, fname)
        if not os.path.isfile(abs_path):
            continue
        url = "file:///" + abs_path.replace("\\", "/")
        label = (chosen.get("label") or "").strip()
        itype = (chosen.get("type") or "OTHER").upper()
        return (url, label, itype)
    return None


_TAG_PREFIX_RE = re.compile(
    r"^(ILLUSTRATION|FACT SHEET|X-RAY|XRAY|CT|MRI|ULTRASOUND|US|PHOTO|MICROSCOPY|HISTOLOGY|DIAGRAM|OTHER|IMAGING)\s*\n+",
    re.IGNORECASE,
)
_MD_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_MD_ITAL_RE = re.compile(r"(?<![\w*])\*([^*]+)\*(?![\w*])")


def _clean_caption(label, case_num, itype):
    cap_raw = label if label else f"Case {case_num} \u2014 {itype.lower()}"
    cap_raw = _TAG_PREFIX_RE.sub("", cap_raw).strip()
    return re.sub(r"\s+", " ", cap_raw)


def _md_inline_to_html(s):
    """Minimal: **bold** -> <b>, *italic* -> <i>. HTML-escape first."""
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = _MD_BOLD_RE.sub(r"<b>\1</b>", s)
    s = _MD_ITAL_RE.sub(r"<i>\1</i>", s)
    return s


def _render_findings_block(findings):
    """Render findings list as a compact bullet panel under image."""
    if not findings:
        return ""
    items = "".join(f"<li>{_md_inline_to_html(f)}</li>" for f in findings)
    return f'<ul class="case-findings">{items}</ul>'


def _render_figure(case_num, img):
    """Render a single image as <figure> with caption + optional findings."""
    cap = _clean_caption(img["label"], case_num, img["type"])
    cap_html = _md_inline_to_html(cap)
    findings_html = _render_findings_block(img.get("findings"))
    type_cls = img["type"].lower()
    return (f'<figure class="case-fig case-fig-{type_cls}">'
            f'<img src="{img["url"]}" alt="Case {case_num} {type_cls}">'
            f'<figcaption>{cap_html}</figcaption>'
            f'{findings_html}'
            f'</figure>')


def _render_primary_image_block(case_num):
    """HTML for the case's primary image figure plus (if the primary itself
    is NOT a microscopy/histology image but the case HAS one with findings)
    a SECOND figure showing the histology with its findings annotated."""
    images = _all_images_for(case_num)
    if not images:
        return ""

    # Primary pick (mirror _primary_image_for logic): pdf_primary -> PHOTO ->
    # primary -> IMAGING -> first
    primary = next((i for i in images if i.get("pdf_primary")), None)
    if primary is None:
        primary = next((i for i in images if i["type"] == "PHOTO"), None)
    if primary is None:
        primary = next((i for i in images if i.get("primary")), None)
    if primary is None:
        primary = next((i for i in images if i["type"] == "IMAGING"), None)
    if primary is None:
        primary = images[0]

    out = [_render_figure(case_num, primary)]

    # If primary isn't microscopy, look for a microscopy image with findings
    # and add it as a secondary figure.
    if not _is_microscopy(primary):
        secondary = next(
            (i for i in images
             if i["filename"] != primary["filename"]
             and _is_microscopy(i)
             and i.get("findings")),
            None,
        )
        if secondary is not None:
            out.append(_render_figure(case_num, secondary))

    return "".join(out)


def render_case(case_num, title, stem, questions, md_cases):
    sections = md_cases.get(case_num, [])
    out = ['<section class="case">']
    out.append(f'<div class="case-header"><span class="case-num">Case {case_num}</span>{title}</div>')
    out.append(f'<div class="stem"><span class="lbl">Stem</span>{stem}</div>')
    img_html = _render_primary_image_block(case_num)
    if img_html:
        out.append(img_html)
    for idx, (qtext, label) in enumerate(questions, 1):
        out.append(render_qa(qtext, label, sections, idx))
    out.append(render_model_answers(case_num, questions=questions))
    out.append('</section>')
    return "\n".join(out)


CMP_TABLE_HTML = """
<div class="cmp-wrap">
  <div class="cmp-head">Meningococcal vs Viral Exanthem &mdash; Side-by-Side</div>
  <table class="cmp-table">
    <thead><tr><th></th><th class="hdr-m">Meningococcal (sepsis)</th><th class="hdr-v">Viral exanthem</th></tr></thead>
    <tbody>
      <tr><th>Appearance</th>
        <td class="m"><b class="r">Petechial &rarr; purpuric / hemorrhagic</b>, dark purple-red, irregular; may coalesce into ecchymoses (<b class="r">purpura fulminans</b>); may start blanching maculopapular early.</td>
        <td class="v">Maculopapular, erythematous, pink/red; may be vesicular (varicella, HFMD); typically discrete.</td></tr>
      <tr><th>Blanching</th>
        <td class="m"><b class="r">NON-blanching</b> (key feature &mdash; glass / tumbler test).</td>
        <td class="v">Blanches on pressure.</td></tr>
      <tr><th>Systemic</th>
        <td class="m">Fever, lethargy, <b class="r">SHOCK</b> (tachycardia, prolonged CRT, hypotension), neck stiffness, photophobia, vomiting, <b class="r">&darr; GCS</b>, leg pain, cold peripheries &mdash; child looks <b class="r">toxic</b>.</td>
        <td class="v">Fever, malaise; child often well between febrile peaks; specific clues (cough/coryza/Koplik in measles; conjunctivitis; oral lesions in HFMD).</td></tr>
      <tr><th>Mechanism</th>
        <td class="m"><i><b class="b">Neisseria meningitidis</b></i> endotoxin &rarr; <b class="r">DIC</b> &rarr; microthrombi + intravascular hemorrhage (vasculitic).</td>
        <td class="v">Viral cytopathic / immune-complex / direct viral effect on skin.</td></tr>
      <tr><th>Investigations</th>
        <td class="m"><b class="o">Do NOT delay antibiotics</b>. Blood culture, PCR (meningococcal), CBC, coag/<b class="o">DIC screen</b>, lactate, ABG, U&amp;E, CRP, LP (only if no contraindication and after Abx).</td>
        <td class="v">Usually clinical. Targeted serology / PCR if needed (measles IgM, VZV PCR, EBV/CMV).</td></tr>
      <tr><th>Management</th>
        <td class="m"><b class="g">IMMEDIATE IV/IM benzylpenicillin or ceftriaxone</b>, IV fluids, ABCDE, PICU, notify public health, <b class="g">chemoprophylaxis</b> for close contacts.</td>
        <td class="v">Supportive &mdash; antipyretics, hydration; specific antivirals only in select cases (e.g., <b class="g">acyclovir</b> for severe varicella / immunocompromised).</td></tr>
      <tr><th>Prognosis</th>
        <td class="m">Time-critical &mdash; mortality <b class="o">10&ndash;15%</b>; higher with purpura fulminans / shock; survivors may need digit/limb amputation.</td>
        <td class="v">Self-limiting in most; complications uncommon in immunocompetent children.</td></tr>
    </tbody>
  </table>
  <div class="cmp-pearl"><b>Pearl:</b> Any <b class="r">non-blanching rash + fever</b> in a child = assume meningococcal sepsis until proven otherwise &rarr; <b class="g">IV/IM antibiotics IMMEDIATELY</b>, do not wait for investigations.</div>
</div>
"""


def render_standalone(md_cases):
    """Standalone topic — no source case in MD; rely on model answers for
    the study content. Renders a comparison table at the top before the
    individual Q/A drill blocks."""
    tag, title, stem, questions = STANDALONE
    out = ['<section class="case">']
    out.append(f'<div class="case-header"><span class="case-num">{tag}</span>{title}</div>')
    out.append(f'<div class="stem"><span class="lbl">Stem</span>{stem}</div>')
    out.append(CMP_TABLE_HTML)
    for idx, (qtext, label) in enumerate(questions, 1):
        out.append(render_qa(qtext, label, [], idx))
    out.append(render_model_answers("standalone", questions=questions))
    out.append('</section>')
    return "\n".join(out)


def render_title():
    return """
<div class="title-page">
  <h1>Pediatrics OSCE Study Guide</h1>
  <div class="sub">38 cases &middot; question-ordered Q&amp;A</div>
  <div class="note">Each case page lists the original exam questions in their
    exact order, with a styled answer card under each. Use the colored answer
    cards as both a cheat sheet and a self-test (cover the card, answer, then
    uncover).</div>
  <div class="meta">Generated for OSCE preparation</div>
</div>
"""


def render_toc():
    out = ['<div class="toc-page"><h2>Contents</h2><div class="toc-grid">']
    for num, title, *_ in CASES:
        out.append(f'<div class="toc-item"><span class="num">{num}.</span> {title}</div>')
    out.append(f'<div class="toc-item"><span class="num">+</span> {STANDALONE[1]}</div>')
    out.append('</div></div>')
    return "\n".join(out)


def main():
    with open(MD_SRC, "r", encoding="utf-8") as f:
        md = f.read()
    md_cases = parse_md_answers(md)
    print(f"Parsed answers for {len(md_cases)} cases from STUDY_GUIDE.md")

    parts = [render_title(), render_toc()]
    missing = []
    for num, title, stem, questions in CASES:
        parts.append(render_case(num, title, stem, questions, md_cases))
        for qtext, label in questions:
            labels = [label] if isinstance(label, str) else list(label)
            for lbl in labels:
                if find_answer(md_cases.get(num, []), lbl) is None:
                    missing.append((num, lbl))
    parts.append(render_standalone(md_cases))

    if missing:
        print(f"WARN: {len(missing)} questions had no matching answer in STUDY_GUIDE.md:")
        for n, lbl in missing[:25]:
            print(f"  - Case {n}: '{lbl}'")
        if len(missing) > 25:
            print(f"  ... and {len(missing)-25} more")

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>Pediatrics OSCE Study Guide</title>
<style>{CSS}</style>
</head><body>
{"".join(parts)}
</body></html>"""

    tmp_dir = os.path.join(tempfile.gettempdir(), "opencode_pdf")
    os.makedirs(tmp_dir, exist_ok=True)
    tmp_html = os.path.join(tmp_dir, "study_guide_v3.html")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML: {tmp_html} ({os.path.getsize(tmp_html):,} bytes)")

    url = "file:///" + tmp_html.replace("\\", "/")
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
           "--allow-file-access-from-files",
           f"--print-to-pdf={OUT_PDF}", "--no-pdf-header-footer",
           "--virtual-time-budget=20000", url]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0 or not os.path.exists(OUT_PDF):
        print("STDERR:", r.stderr)
        print("STDOUT:", r.stdout)
        sys.exit(1)
    print(f"PDF: {OUT_PDF} ({os.path.getsize(OUT_PDF):,} bytes)")


if __name__ == "__main__":
    main()
