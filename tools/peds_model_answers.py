"""
Model Answers for the Pediatrics OSCE Study Guide.

For each case number: list of one-sentence exam-ready answers in the SAME
ORDER as the questions defined in peds_pdf_v3.CASES, plus a single 'pearl'
that captures the highest-yield buzzword / clinical reasoning shortcut.

Voice: terse, declarative, single sentence per Q, like an examiner's
official answer key. Use approved abbreviations only after first full form.
"""

MODEL_ANSWERS = {
    1: {  # Cephalohematoma
        "answers": [
            "Cephalohematoma — subperiosteal hemorrhage, firm, well-demarcated, confined to one cranial bone (does not cross suture lines).",
            "Caput succedaneum — diffuse soft pitting scalp edema, present at birth, crosses suture lines, resolves in days.",
            "Instrumental delivery (vacuum > forceps); prolonged or difficult labor (also: macrosomia, primigravida, fetal coagulopathy).",
            "Hyperbilirubinemia/neonatal jaundice (from breakdown of pooled blood), and anemia.",
            "Reassurance — self-resolves over 2 weeks to 3 months; do NOT aspirate (infection risk); monitor bilirubin ± phototherapy and monitor hematocrit if large.",
        ],
        "pearl": "Does NOT cross suture lines = cephalohematoma (subperiosteal). Crosses sutures + soft = caput; crosses sutures + boggy/shocky = subgaleal (dangerous).",
    },

    2: {  # Down syndrome
        "answers": [
            "Down syndrome (Trisomy 21).",
            "Upslanting palpebral fissures, epicanthal folds, flat nasal bridge/flat facial profile (plus protruding tongue, small low-set ears, single transverse palmar crease, Brushfield spots, hypotonia, brachycephaly).",
            "Karyotype (chromosomal analysis) — gold standard; FISH for rapid diagnosis; antenatal NIPT, combined test, amniocentesis/CVS.",
            "Trisomy 21 (95%) due to meiotic nondisjunction (extra copy of chromosome 21); 4% Robertsonian translocation (usually 14;21); 1% mosaicism.",
            "Congenital heart defects (~50%, AVSD most common) and duodenal atresia (also: hypothyroidism, ALL/AML-M7, atlantoaxial instability, hearing loss, intellectual disability).",
        ],
        "pearl": "Newborn + flat facies + single palmar crease + hypotonia = Down. Always echo (AVSD) + abdo film (duodenal atresia, double bubble) + TFTs.",
    },

    3: {  # Preseptal cellulitis
        "answers": [
            "Preseptal (periorbital) cellulitis — infection of soft tissues anterior to the orbital septum.",
            "Staph aureus, Streptococcus species, and Streptococcus pneumoniae (Hib historically; less since vaccine).",
            "Orbital (post-septal) cellulitis — distinguished by proptosis, painful/restricted eye movement, decreased visual acuity, RAPD.",
            "Admit, IV broad-spectrum antibiotics (ceftriaxone ± vancomycin or co-amoxiclav), urgent ophthalmology consult, CT orbits if any concern for orbital involvement.",
        ],
        "pearl": "Eye still moves freely + no proptosis + vision intact = preseptal (treat IV antibiotics). Proptosis/pain on eye movement/diplopia = orbital — CT now, ENT/ophthal in.",
    },

    4: {  # RDS
        "answers": [
            "Diffuse bilateral ground-glass / reticulonodular (\"white-out\") lung fields with air bronchograms and low lung volumes.",
            "Neonatal respiratory distress syndrome (RDS / hyaline membrane disease) due to surfactant deficiency.",
            "Surfactant deficiency in a preterm infant — reduced production by immature type II pneumocytes leads to alveolar collapse and decreased compliance.",
            "Nasal CPAP (or intubation + mechanical ventilation if severe) and intratracheal surfactant replacement (e.g., poractant alfa via INSURE/LISA).",
            "Antenatal corticosteroids (betamethasone/dexamethasone) to mothers at risk of preterm delivery 24–34 weeks, plus avoidance of preterm delivery where possible.",
        ],
        "pearl": "Preterm + grunting + retractions in first hours + ground-glass CXR = RDS. Antenatal steroids are the single biggest win; surfactant + CPAP after birth.",
    },
}

MODEL_ANSWERS[5] = {  # ALL
    "answers": [
        "Anemia (Hb 6.5), thrombocytopenia, leukocytosis with blast cells on peripheral smear (pancytopenia + circulating blasts).",
        "Acute lymphoblastic leukemia (ALL).",
        "Bone marrow aspirate and biopsy (>20% blasts, immunophenotyping by flow cytometry, cytogenetics including BCR-ABL/Philadelphia); lumbar puncture for CNS staging.",
        "Multi-agent chemotherapy in phases (induction, consolidation, CNS prophylaxis with intrathecal methotrexate, maintenance for 2–3 years), with allogeneic stem-cell transplant for high-risk/relapsed disease; supportive care (transfusions, antimicrobials, tumor-lysis prophylaxis).",
    ],
    "pearl": "Child + pancytopenia + blasts on smear = ALL until proven otherwise. Bone marrow + LP at diagnosis (always CNS-stage). Tumor lysis: allopurinol/rasburicase + hydration.",
}

MODEL_ANSWERS[6] = {  # Sickle cell
    "answers": [
        "Sickle cell anemia (homozygous HbSS).",
        "Hemoglobin electrophoresis or HPLC (shows predominant HbS, no HbA); confirm with sickle solubility test and CBC/reticulocytes/blood film (sickle cells, target cells, Howell-Jolly bodies).",
        "Vaso-occlusive (painful) crisis and acute chest syndrome (also: splenic sequestration, aplastic crisis from parvovirus B19, stroke, priapism).",
        "Hydroxyurea (hydroxycarbamide) — increases fetal hemoglobin (HbF) and reduces frequency of vaso-occlusive crises and acute chest syndrome.",
        "Daily oral penicillin V prophylaxis from 3 months until at least age 5, and full vaccination including pneumococcal (PCV13 + PPV23), meningococcal (MenACWY + MenB), Hib and annual influenza.",
    ],
    "pearl": "Functional asplenia from age 1 → penicillin prophylaxis + vaccines = lifesaving. Pain crisis = hydration + analgesia + O2. Hydroxyurea is the disease-modifier.",
}

MODEL_ANSWERS[7] = {  # Acute chest syndrome
    "answers": [
        "Acute chest syndrome — new pulmonary infiltrate on CXR plus fever, chest pain, hypoxia, or respiratory symptoms in a sickle-cell patient (commonest cause of death in SCD).",
        "Oxygen, IV fluids (cautious — avoid overload), IV opioid analgesia (morphine), broad-spectrum antibiotics (ceftriaxone + macrolide), incentive spirometry, and urgent simple or exchange transfusion if severe/hypoxic.",
        "Stroke, splenic sequestration, aplastic crisis (parvovirus B19), priapism, gallstones, avascular necrosis of femoral head, chronic renal failure, retinopathy.",
        "Daily penicillin V prophylaxis 3 months–5 years and full vaccination schedule (pneumococcal, meningococcal, Hib, annual influenza).",
    ],
    "pearl": "Sickle + new fever/chest pain/hypoxia + new infiltrate = ACS. Don't wait — start antibiotics, oxygen, exchange transfusion if hypoxic. #1 cause of SCD death.",
}

MODEL_ANSWERS[8] = {  # Beta-thalassemia major
    "answers": [
        "\"Chipmunk facies\" — frontal bossing, maxillary prominence/overgrowth, depressed nasal bridge from extramedullary hematopoiesis and bone-marrow expansion.",
        "Beta-thalassemia major (Cooley anemia).",
        "Autosomal recessive (HBB gene on chromosome 11).",
        "Hemoglobin electrophoresis / HPLC — markedly increased HbF and HbA2 with little or no HbA; supportive findings include severe microcytic hypochromic anemia with target cells and nucleated RBCs.",
        "Lifelong regular packed-RBC transfusions every 2–4 weeks to keep Hb >9–10 g/dL, iron-chelation therapy (deferasirox/deferoxamine), folic acid supplementation, and allogeneic stem-cell transplant as the only cure.",
        "Iron overload (hemosiderosis) → cardiomyopathy (#1 cause of death), liver cirrhosis, and endocrinopathies — diabetes, hypothyroidism, hypogonadism (also: growth failure, osteoporosis).",
    ],
    "pearl": "Transfusion-dependent from infancy + chipmunk facies + microcytic anemia = β-thal major. Chelation is what kills the patient when missed — iron-overload cardiomyopathy is #1 cause of death.",
}

MODEL_ANSWERS[9] = {  # IDA
    "answers": [
        "Microcytic hypochromic anemia — low Hb, low MCV, low MCH, low MCHC, with high RDW; blood film shows pencil cells and target cells.",
        "Iron deficiency anemia.",
        "Excessive cow's milk intake (>500 mL/day inhibits iron absorption and causes occult GI blood loss), low dietary iron intake, prolonged exclusive breast-feeding beyond 6 months without iron supplementation, and pica.",
        "Serum ferritin (low — most specific), serum iron low, total iron-binding capacity (TIBC) high, transferrin saturation low.",
        "Oral elemental iron 3–6 mg/kg/day for 3 months (continue 2–3 months after Hb normalizes to replenish stores) plus dietary modification — reduce cow's milk to <500 mL/day and add iron-rich foods.",
    ],
    "pearl": "Toddler + pallor + pica + 800 mL milk/day = IDA. Low ferritin + low transferrin sat seals it. Treat with oral iron 3 months past normalization.",
}

MODEL_ANSWERS[10] = {  # Nephrotic syndrome
    "answers": [
        "Nephrotic syndrome.",
        "Minimal change disease (>80% of nephrotic syndrome in children aged 2–6).",
        "Heavy proteinuria (>40 mg/m²/hr or urine protein:creatinine >200 mg/mmol), hypoalbuminemia (<25 g/L), generalized edema, and hyperlipidemia.",
        "Urinalysis + urine protein:creatinine ratio, 24-hour urine protein, serum albumin, U&Es, lipid profile, FBC, complement (C3/C4), ASO titre, hepatitis B/C and HIV serology, renal ultrasound; renal biopsy if atypical features.",
        "Oral prednisolone 60 mg/m²/day for 4–6 weeks then weaning, plus dietary salt restriction, fluid balance, albumin infusion if severely hypovolemic, penicillin V prophylaxis until in remission, pneumococcal vaccination, and treatment of any infection promptly.",
    ],
    "pearl": "Boy 2–6 + facial/scrotal edema + 4+ protein on dipstick = minimal change until proven otherwise. Steroids first, biopsy only if atypical or steroid-resistant.",
}

MODEL_ANSWERS[11] = {  # Meningococcemia
    "answers": [
        "Non-blanching petechial / purpuric rash (purpura fulminans) — does not blanch on glass-tumbler test, indicates intravascular hemorrhage from DIC, and is a medical emergency signaling meningococcal sepsis.",
        "Meningococcal septicemia (meningococcemia) ± meningitis.",
        "Neisseria meningitidis — gram-negative diplococcus (serogroups B and C commonest in UK; also A, W, Y).",
        "High fever, non-blanching purpuric rash, and signs of shock — tachycardia, prolonged capillary refill, cold peripheries, hypotension (late sign in children).",
        "ABC with high-flow oxygen, two large-bore IV/IO access, 20 mL/kg crystalloid fluid bolus (repeat as needed) and immediate empirical IV ceftriaxone (community: IM/IV benzylpenicillin before transfer), plus dexamethasone before/with first antibiotic dose, blood cultures, PICU admission, and notify public health for contact prophylaxis.",
        "Septic shock with DIC, multi-organ failure, and Waterhouse-Friderichsen syndrome (also: limb gangrene/amputation, hearing loss, neurodevelopmental impairment); preventive measures are MenB (Bexsero) and MenACWY conjugate vaccines and chemoprophylaxis (rifampicin or ciprofloxacin) for close contacts.",
    ],
    "pearl": "Non-blanching rash + ill child = meningococcal sepsis until proven otherwise — give antibiotics in the community before transfer. Do NOT delay antibiotics for LP.",
}

MODEL_ANSWERS[12] = {  # HSP
    "answers": [
        "Henoch-Schönlein purpura (IgA vasculitis).",
        "Blood pressure measurement and urine dipstick (proteinuria/hematuria) at every visit to detect renal involvement.",
        "Supportive care with hydration, paracetamol/NSAIDs for joint pain (avoid if renal involvement), oral prednisolone for severe abdominal pain or scrotal involvement, and regular BP/urinalysis monitoring for 6–12 months.",
        "IgA nephropathy / HSP nephritis (most important long-term — can progress to chronic kidney disease), and intussusception (typically ileo-ileal).",
    ],
    "pearl": "Palpable purpura on buttocks/legs + abdo pain + joint pain + normal platelets = HSP. Watch BP and urine for 6–12 months — renal disease is the long-term killer.",
}

MODEL_ANSWERS[13] = {  # Varicella
    "answers": [
        "Varicella (chickenpox).",
        "Varicella-zoster virus (VZV) — a DNA herpesvirus.",
        "Respiratory droplets and direct contact with vesicle fluid (highly contagious from 1–2 days before rash until all lesions crusted).",
        "Generalized pruritic vesicular rash in crops at different stages (\"dew-drops on rose petals\"), centripetal distribution (trunk > limbs, includes scalp and mucous membranes), and prodromal fever and malaise.",
        "Supportive — hydration, paracetamol (NOT aspirin/ibuprofen — risk of Reye syndrome and necrotising fasciitis), calamine lotion/antihistamines for itch, and oral aciclovir only if immunocompromised, neonate, adolescent/adult, or severe disease.",
        "Secondary bacterial skin infection (Strep/Staph cellulitis, necrotising fasciitis) and varicella pneumonia (also: encephalitis, cerebellar ataxia).",
        "Live attenuated varicella vaccine (two doses) and post-exposure varicella-zoster immunoglobulin (VZIG) or aciclovir for high-risk contacts (immunocompromised, neonates, pregnant women).",
    ],
    "pearl": "Vesicles in different stages (papule/vesicle/crust at the same time) = varicella. NEVER NSAIDs/aspirin (necrotising fasciitis, Reye's). Aciclovir only if immunocompromised, neonate, or adult.",
}

MODEL_ANSWERS[14] = {  # Measles
    "answers": [
        "Measles (rubeola).",
        "Measles virus — a single-stranded RNA paramyxovirus.",
        "Otitis media and pneumonia (also: acute encephalitis 1:1000 and subacute sclerosing panencephalitis years later).",
        "Two-dose live attenuated MMR vaccine at 12–15 months and 3–5 years.",
        "Supportive care — hydration, antipyretics, isolation for 4 days after rash onset, vitamin A supplementation (reduces mortality and morbidity), and notify public health.",
    ],
    "pearl": "4 C's: Cough, Coryza, Conjunctivitis, Koplik spots (white spots on buccal mucosa, pathognomonic). Then cephalocaudal maculopapular rash. Vitamin A is a real treatment.",
}

MODEL_ANSWERS[15] = {  # Roseola
    "answers": [
        "Roseola infantum (exanthem subitum / sixth disease).",
        "Human herpesvirus 6 (HHV-6), occasionally HHV-7.",
        "High fever for 3–5 days in an otherwise well-looking infant (often with a febrile convulsion at peak), then defervescence followed by sudden onset of a fine pink maculopapular rash starting on the trunk and spreading outward.",
        "Measles and rubella (also: scarlet fever, drug eruption, parvovirus B19 — erythema infectiosum).",
        "Supportive — antipyretics (paracetamol), maintain hydration, and reassurance (self-limiting in 5–7 days).",
    ],
    "pearl": "High fever in a WELL infant → fever breaks → THEN rash appears = roseola. Most common cause of first febrile convulsion (6 months–2 years).",
}

MODEL_ANSWERS[16] = {  # HFMD
    "answers": [
        "Hand, foot and mouth disease (HFMD).",
        "Coxsackievirus A16 (most common) or enterovirus 71 — enteroviruses of the Picornaviridae family.",
        "Faeco-oral and respiratory droplet, plus direct contact with vesicle fluid (highly contagious in childcare settings).",
        "Excellent — self-limiting illness that resolves spontaneously in 7–10 days without sequelae in immunocompetent children.",
        "Dehydration (from painful oral ulcers limiting oral intake) and rarely viral encephalitis or aseptic meningitis (especially with enterovirus 71).",
        "Supportive — oral hydration (cold fluids, ice lollies), paracetamol/ibuprofen for fever and pain, topical mouth gels (e.g., lidocaine) for ulcers, and hand-hygiene to prevent spread.",
    ],
    "pearl": "Oral ulcers + vesicular rash on palms/soles + low-grade fever in a toddler = HFMD. Watch for dehydration from painful mouth ulcers — that's the main pitfall.",
}

MODEL_ANSWERS[17] = {  # Scarlet fever
    "answers": [
        "Scarlet fever.",
        "Group A beta-hemolytic streptococcus (Streptococcus pyogenes).",
        "Fine erythematous \"sandpaper\" maculopapular rash sparing the perioral area (circumoral pallor), sore throat with exudative tonsillopharyngitis, strawberry tongue (initially white-coated then bright red with prominent papillae), and high fever with cervical lymphadenopathy.",
        "Erythrogenic (pyrogenic) exotoxin (SpeA/B/C) produced by Streptococcus pyogenes.",
        "Throat swab for culture and rapid antigen detection test (Streptococcal antigen/throat culture); anti-streptolysin O (ASO) titre if late presentation.",
        "Oral penicillin V (or amoxicillin) for 10 days — erythromycin/clarithromycin if penicillin-allergic — to eradicate the organism, prevent rheumatic fever, and reduce transmission.",
        "Acute rheumatic fever (1–5 weeks post-infection — pancarditis, polyarthritis, chorea) and post-streptococcal glomerulonephritis (1–3 weeks post-infection — hematuria, edema, hypertension).",
    ],
    "pearl": "Sandpaper rash + circumoral pallor + strawberry tongue + sore throat = scarlet fever. Always give 10 days of penicillin to prevent rheumatic fever (not GN — that's immune-complex driven and not prevented).",
}

MODEL_ANSWERS[18] = {  # Kawasaki disease
    "answers": [
        "Kawasaki disease (mucocutaneous lymph node syndrome).",
        "Fever ≥5 days plus 4 of 5 of CRASH: Conjunctivitis (bilateral, non-purulent), Rash (polymorphous), Adenopathy (unilateral cervical, >1.5 cm), Strawberry tongue/cracked red lips/oral mucosal changes, Hand/foot changes (palmar/plantar erythema and edema, later periungual desquamation).",
        "Coronary artery aneurysms (with risk of thrombosis and myocardial infarction) and myocarditis (also: pericarditis, valvulitis, heart failure).",
        "ECG and 2D echocardiogram (at diagnosis, 2 weeks and 6–8 weeks — looking for coronary artery aneurysms), CBC (leukocytosis, thrombocytosis after week 1), CRP/ESR markedly elevated, LFTs (transaminitis), serum albumin (low), urinalysis (sterile pyuria).",
        "Single dose IV immunoglobulin (IVIG) 2 g/kg within first 10 days of fever, plus high-dose aspirin (30–50 mg/kg/day until afebrile, then low-dose 3–5 mg/kg/day for 6–8 weeks or until aneurysms resolve).",
    ],
    "pearl": "CRASH and Burn: Conjunctivitis, Rash, Adenopathy, Strawberry tongue, Hand/foot changes + ≥5 days fever. IVIG within 10 days saves coronaries. One of the few times we give aspirin to a child.",
}

MODEL_ANSWERS[19] = {  # Mongolian spots
    "answers": [
        "Blue-gray macular pigmented patches on the lower back and buttocks of a well infant — flat, irregular, well-demarcated, non-tender, non-blanching.",
        "Mongolian spots (congenital dermal melanocytosis).",
        "Reassurance and documentation (including photographs in the notes) — no treatment required; important to record at birth so they are not later mistaken for non-accidental injury bruising.",
        "Excellent — spontaneously fade by age 2–6 years; no functional sequelae.",
        "Bruising from non-accidental injury (key differential — bruises change colour over days, are tender, and have a different distribution); also dermal melanocytic hamartoma and nevus of Ito/Ota.",
    ],
    "pearl": "Blue-gray macules over sacrum/buttocks in a brown/Asian baby = Mongolian spots — DOCUMENT them at birth to avoid being misread as NAI bruising later.",
}

MODEL_ANSWERS[20] = {  # Lobar pneumonia
    "answers": [
        "Homogeneous consolidation confined to one lobe (here: right lower/middle lobe) with air bronchograms and preserved lung volume; no significant pleural effusion in uncomplicated cases.",
        "Streptococcus pneumoniae (most common in children >5; also Mycoplasma pneumoniae in school-age, Staph aureus or Group A strep in severe disease).",
        "Lobar pneumonia (community-acquired, bacterial).",
        "Oral amoxicillin first-line for uncomplicated cases; IV ceftriaxone or co-amoxiclav if severe/hospitalised; add a macrolide (clarithromycin) if atypical pneumonia suspected; duration 5–7 days.",
        "Parapneumonic effusion / empyema and respiratory failure (also: lung abscess, sepsis, pneumatocele with Staph).",
        "Consolidation localised to one lobe ± necrotising change ± parapneumonic effusion.",
        "High fever, productive cough, tachypnea, focal crackles/bronchial breath sounds, dullness to percussion over the affected lobe.",
        "Oxygen to maintain SpO₂ ≥92% and IV antibiotics (ceftriaxone) plus fluids and analgesia.",
    ],
    "pearl": "Child + high fever + productive cough + lobar consolidation on CXR = bacterial pneumonia (think pneumococcus). Empyema if fever persists despite antibiotics — drain it.",
}

MODEL_ANSWERS[21] = {  # Foreign body inhalation
    "answers": [
        "Foreign body (FB) aspiration / inhalation — most commonly into the right main bronchus.",
        "Sudden-onset cough and respiratory distress during play/eating, with unilateral wheeze and decreased air entry on the affected side (here: right) and hypoxia (SpO₂ 88%).",
        "Rigid bronchoscopy under general anaesthesia — both diagnostic and therapeutic (removes the FB); CXR (inspiratory and expiratory) may show air-trapping/hyperinflation of the affected lobe or atelectasis.",
        "Post-obstructive pneumonia and bronchiectasis (also: pneumothorax, lung abscess, complete airway obstruction with cardiac arrest if FB shifts).",
    ],
    "pearl": "Sudden choking while playing/eating + unilateral wheeze + hypoxia = inhaled FB until proven otherwise. Rigid bronchoscopy is BOTH diagnosis and treatment — don't wait for the CXR.",
}

MODEL_ANSWERS[22] = {  # Cystic fibrosis
    "answers": [
        "Cystic fibrosis (CF).",
        "Autosomal recessive mutation in the CFTR (Cystic Fibrosis Transmembrane conductance Regulator) gene on chromosome 7 — ΔF508 is the most common mutation (~70%).",
        "Bronchiectasis with recurrent Pseudomonas aeruginosa chest infections, and pancreatic insufficiency with diabetes (CF-related diabetes) (also: distal intestinal obstruction syndrome, infertility in males, osteoporosis, liver disease).",
        "Bronchiectasis with tram-track shadowing, dilated thick-walled bronchi, mucus plugging, and upper-lobe predominant fibrosis.",
        "Sweat chloride test (>60 mmol/L on two occasions — gold standard); also CFTR genetic testing, newborn heel-prick screening (immunoreactive trypsinogen — IRT), and faecal elastase (low) for pancreatic insufficiency.",
        "Multidisciplinary — airway clearance (chest physiotherapy, mucolytics dornase alfa and hypertonic saline), bronchodilators, prophylactic and rescue antibiotics (oral azithromycin, nebulised tobramycin, IV for exacerbations), CFTR modulators (ivacaftor/lumacaftor/elexacaftor combinations), pancreatic enzyme replacement (CREON) with high-calorie diet, fat-soluble vitamins (ADEK), and consideration of lung transplant in end-stage disease.",
    ],
    "pearl": "Failure to thrive + recurrent chest infections + bulky/greasy stools = CF. Sweat chloride is the test. CFTR modulators (elexacaftor/tezacaftor/ivacaftor) are revolutionising prognosis.",
}

MODEL_ANSWERS[23] = {  # Bacterial meningitis
    "answers": [
        "Bacterial meningitis.",
        "Streptococcus pneumoniae and Neisseria meningitidis (most common >3 months); Group B Streptococcus, E. coli, and Listeria in neonates; Haemophilus influenzae type b (now rare due to vaccination).",
        "Lumbar puncture with CSF microscopy/culture/biochemistry (turbid CSF, neutrophil pleocytosis, raised protein, low glucose), blood cultures, FBC + CRP, U&E, glucose, coagulation, and CT head if focal signs/altered consciousness/raised ICP before LP.",
        "Immediate empirical IV ceftriaxone (add IV amoxicillin in <3 months for Listeria), IV dexamethasone before/with first dose of antibiotic (reduces hearing loss and neurological sequelae), supportive care (oxygen, fluids, antiepileptics for seizures), PICU admission if shocked/depressed consciousness, and notification of public health for contact prophylaxis.",
        "Seizures, sensorineural hearing loss, hydrocephalus, neurodevelopmental impairment, and death (also: subdural effusions, cerebral abscess, septic shock with DIC).",
        "Routine childhood immunisations — Hib, MenB and MenACWY, and pneumococcal conjugate (PCV13) vaccines, plus chemoprophylaxis (rifampicin/ciprofloxacin) for close contacts of meningococcal cases.",
    ],
    "pearl": "Fever + neck stiffness + altered mental state + petechial rash = meningococcal meningitis. Antibiotics + dexamethasone BEFORE the LP — never delay treatment.",
}

MODEL_ANSWERS[24] = {  # Tetralogy of Fallot
    "answers": [
        "Digital clubbing — loss of nail-bed angle (>180°) from chronic hypoxia secondary to right-to-left shunting.",
        "Boot-shaped heart (\"coeur en sabot\") due to right ventricular hypertrophy with an uplifted cardiac apex, plus oligemic lung fields from decreased pulmonary blood flow.",
        "Tetralogy of Fallot (TOF).",
        "The four classical lesions: ventricular septal defect (VSD), pulmonary outflow stenosis (subvalvular/valvular), overriding aorta, and right ventricular hypertrophy.",
        "Knee-to-chest positioning (squatting — increases SVR and reduces right-to-left shunt), high-flow oxygen, IV morphine (relieves agitation and infundibular spasm), IV propranolol (relaxes infundibulum), IV fluids, and IV sodium bicarbonate if acidotic; definitive surgical repair before age 1.",
    ],
    "pearl": "Cyanotic spell + child squats to relieve it + boot-shaped heart on CXR = TOF. PROS in tet spells: Position (knee-chest), Reassure, Oxygen, Sedation (morphine) ± beta-blocker.",
}

MODEL_ANSWERS[25] = {  # Neonatal jaundice (ABO)
    "answers": [
        "Pathological neonatal jaundice (jaundice in first 24 hours of life — always pathological).",
        "ABO or Rh haemolytic disease of the newborn, G6PD deficiency / hereditary spherocytosis, sepsis (neonatal infection causing haemolysis), and cephalohematoma / large bruising with breakdown of pooled blood.",
        "ABO incompatibility — maternal anti-A or anti-B IgG antibodies crossing the placenta and haemolysing fetal red cells (mother O, baby A or B).",
        "Phototherapy with blue light (480 nm) to convert unconjugated bilirubin to water-soluble lumirubin, and exchange transfusion if bilirubin exceeds exchange thresholds or features of acute bilirubin encephalopathy.",
        "Acute bilirubin encephalopathy (lethargy, hypotonia, poor feeding, high-pitched cry) progressing to kernicterus (athetoid cerebral palsy, sensorineural deafness, gaze palsy, dental enamel dysplasia).",
        "Pathological neonatal jaundice.",
        "Timing of onset, mother's and baby's blood groups, family history of haemolytic disease, breast vs formula feeding, infection symptoms (fever, lethargy, poor feeding), pale stools/dark urine (cholestasis), and birth trauma/instrumental delivery.",
        "Total and conjugated (split) bilirubin, blood group + Rh + direct Coombs test (DAT) on baby and mother, FBC + reticulocyte count + blood film, G6PD assay, TFTs, septic screen if unwell.",
        "Haemolysis (ABO/Rh, G6PD, spherocytosis), sepsis, and hepatobiliary disease (biliary atresia, neonatal hepatitis).",
    ],
    "pearl": "Jaundice in the first 24 hours of life is ALWAYS pathological — get split bilirubin, blood groups, Coombs. Phototherapy + exchange thresholds drive treatment.",
}

MODEL_ANSWERS[26] = {  # Biliary atresia
    "answers": [
        "Conjugated (cholestatic) hyperbilirubinaemia — conjugated bilirubin >25 µmol/L (or >20% of total) is pathological at any age.",
        "Total and split (conjugated/unconjugated) bilirubin, LFTs (raised GGT, ALP, transaminases), coagulation (PT/INR — may be prolonged from vitamin K malabsorption), TORCH screen, alpha-1 antitrypsin level, sweat test, and TFTs.",
        "Persistent jaundice beyond 2 weeks of life with pale (acholic, putty-coloured) stools and dark urine, and hepatomegaly.",
        "Abdominal ultrasound showing absent or triangular-cord-sign gallbladder, and HIDA scan (hepatobiliary scintigraphy) showing hepatic uptake but no excretion into the bowel; intraoperative cholangiogram and liver biopsy are confirmatory.",
        "Kasai hepatoportoenterostomy ideally before 60 days of age (success rate falls rapidly after this), followed by liver transplantation as definitive long-term treatment when Kasai fails or for end-stage disease.",
    ],
    "pearl": "Jaundice >2 weeks + pale stools + dark urine + raised CONJUGATED bilirubin = biliary atresia. Kasai before 60 days — every day matters. Always check stool colour in prolonged neonatal jaundice.",
}

MODEL_ANSWERS[27] = {  # CDH
    "answers": [
        "Bowel loops (gas-filled) in the left hemithorax with mediastinal shift to the right, absent left hemidiaphragm contour, paucity of bowel gas in the abdomen, and the NG tube tip coiled in the chest.",
        "Congenital diaphragmatic hernia (CDH) — most commonly left-sided Bochdalek-type defect.",
        "Pulmonary hypoplasia — herniation of abdominal contents into the chest during fetal life compresses the developing lung, producing reduced alveoli and pulmonary vessels with associated persistent pulmonary hypertension of the newborn (PPHN).",
        "Immediate NG tube insertion for gastric decompression (DO NOT bag-mask ventilate — distends bowel and worsens lung compression), endotracheal intubation and gentle (\"protective\") ventilation, and management of pulmonary hypertension (inhaled nitric oxide, ECMO if refractory).",
        "Surgical reduction of abdominal contents and repair of the diaphragmatic defect once the infant is haemodynamically stable and pulmonary hypertension has resolved (usually after 24–72 hours of stabilisation).",
    ],
    "pearl": "Antenatal polyhydramnios + respiratory distress + scaphoid abdomen + bowel in chest on CXR = CDH. Intubate and NG decompress — NEVER bag-mask. Stabilise first, repair later.",
}

MODEL_ANSWERS[28] = {  # Duodenal atresia
    "answers": [
        "Duodenal atresia.",
        "\"Double-bubble\" sign — two gas-filled bubbles (stomach and proximal duodenum) with no distal bowel gas.",
        "Trisomy 21 (Down syndrome) — present in ~30% of duodenal atresia cases.",
        "Other Down-syndrome associations (AVSD/VSD/ASD, atlantoaxial instability, hypothyroidism, leukaemia) and surgical complications (anastomotic leak, stricture, short bowel).",
        "NG tube decompression, IV fluids and electrolyte correction, broad-spectrum antibiotics, and surgical duodenoduodenostomy (definitive) once stabilised.",
    ],
    "pearl": "Newborn + bilious vomiting + Down syndrome features + double-bubble on AXR = duodenal atresia. NG decompress + IV fluids first, then duodenoduodenostomy.",
}

MODEL_ANSWERS[29] = {  # Duchenne MD
    "answers": [
        "Duchenne muscular dystrophy (DMD).",
        "Waddling (Trendelenburg) gait, calf pseudohypertrophy, and Gowers sign — child uses hands to \"climb up\" the legs to stand from the floor due to proximal hip-girdle weakness.",
        "Serum creatine kinase (CK) — markedly elevated (often 10–100× normal) — the screening enzyme.",
        "Genetic testing for dystrophin gene (DMD) mutations on Xp21 (deletions, duplications, point mutations) — confirmatory; muscle biopsy with dystrophin immunohistochemistry/Western blot if genetics non-diagnostic.",
        "X-linked recessive — affects boys, transmitted by carrier mothers (one-third are de-novo mutations).",
    ],
    "pearl": "Boy 3–5 + waddling gait + calf pseudohypertrophy + Gowers sign = DMD. CK is screening; dystrophin gene test confirms. Glucocorticoids (prednisolone) + new gene therapies prolong ambulation.",
}

MODEL_ANSWERS[30] = {  # Becker MD
    "answers": [
        "Becker muscular dystrophy (BMD).",
        "X-linked recessive — same DMD gene (Xp21) but in-frame mutations preserve a partially functional dystrophin (vs out-of-frame in Duchenne).",
        "Affected maternal uncle confirms X-linked inheritance — the mother is an obligate carrier and 50% of her sons will be affected, 50% of her daughters will be carriers.",
        "Genetic testing for in-frame DMD gene mutations (confirmatory); markedly elevated serum CK; muscle biopsy with dystrophin immunostaining showing reduced (not absent) dystrophin.",
        "Same gene as Duchenne but in-frame mutation → partial dystrophin function → later onset (typically >5 years, often adolescence), slower progression, ambulation often preserved into adulthood, and longer life expectancy (often >40 years); cardiomyopathy is still the leading cause of death.",
    ],
    "pearl": "Same gene as DMD but milder course = BMD. In-frame mutation = partial dystrophin = walks longer. Still get cardiomyopathy — annual echo + cardio follow-up.",
}

MODEL_ANSWERS[31] = {  # Myelomeningocele
    "answers": [
        "Myelomeningocele (open spina bifida — most severe form of neural tube defect).",
        "Lower-limb motor and sensory loss (flaccid paralysis below the lesion) and neurogenic bladder/bowel (also: hydrocephalus from associated Chiari II malformation).",
        "Arnold-Chiari II malformation (downward herniation of cerebellar tonsils and brainstem) leading to hydrocephalus.",
        "Cover the defect with sterile saline-soaked dressing immediately at birth (prevent infection and drying), nurse prone, broad-spectrum IV antibiotics, neurosurgical closure within 24–72 hours, ventriculoperitoneal (VP) shunt for hydrocephalus, and lifelong MDT input (urology for neurogenic bladder, orthopaedics, physiotherapy, special education).",
        "Periconceptional folic acid 400 µg daily for all women (5 mg daily if previous affected pregnancy, diabetes, or on anti-epileptics) starting at least 1 month before conception and continuing through first trimester.",
    ],
    "pearl": "Open sac on back at birth = myelomeningocele. Cover with saline, prone, antibiotics, close within 72h, watch for hydrocephalus. PREVENT with folic acid pre-conception.",
}

MODEL_ANSWERS[32] = {  # Hydrocephalus
    "answers": [
        "Markedly enlarged head with frontal bossing and \"sunset sign\" (eyes deviated downward); CT brain shows dilated lateral and third ventricles with periventricular lucency from transependymal CSF flow.",
        "Hydrocephalus (likely obstructive / non-communicating).",
        "Ventriculoperitoneal (VP) shunt — diverts CSF from lateral ventricle to peritoneum; endoscopic third ventriculostomy (ETV) is an alternative for obstructive hydrocephalus; treat the underlying cause (e.g., tumour resection).",
        "Achondroplasia (megalencephaly with skeletal dysplasia) and rickets (frontal/parietal bossing from craniotabes); also subdural haematoma, intracranial tumour, and Alexander/Canavan leukodystrophies.",
    ],
    "pearl": "Bulging fontanelle + sunset sign + crossing centiles for head circumference + vomiting = hydrocephalus. VP shunt is workhorse; ETV preferred when obstruction is at the aqueduct.",
}

MODEL_ANSWERS[33] = {  # Cerebral palsy
    "answers": [
        "Spastic diplegia / quadriplegia — hypertonia, brisk reflexes with clonus, scissoring of the lower limbs on suspension, and persistent primitive reflexes; head may show microcephaly.",
        "Cerebral palsy (CP) — most likely spastic type given the clinical picture.",
        "Antenatal infection (TORCH — toxoplasmosis, rubella, CMV, herpes, here hinted by maternal fever in pregnancy); other causes include perinatal hypoxic-ischaemic encephalopathy, prematurity with periventricular leukomalacia, and postnatal kernicterus/meningitis/head injury.",
        "Multidisciplinary supportive care — physiotherapy and occupational therapy for spasticity and contractures, plus oral baclofen / intrathecal baclofen or botulinum toxin injections for severe spasticity (also: orthotics, speech and language therapy, anti-epileptics for seizures, orthopaedic surgery for fixed deformities).",
    ],
    "pearl": "Non-progressive motor disorder + lesion fixed in time + scissoring/spasticity/persistent primitive reflexes = CP. Antenatal/perinatal hypoxia is the leading cause in the developed world.",
}

MODEL_ANSWERS[34] = {  # Sturge-Weber
    "answers": [
        "Port-wine stain (capillary malformation / naevus flammeus) in the V1 (ophthalmic) trigeminal distribution — unilateral, well-demarcated, non-blanching pink-purple patch present from birth.",
        "Leptomeningeal angiomatosis ipsilateral to the facial naevus with characteristic \"tram-track\" gyriform cortical calcification on CT, and underlying cerebral atrophy on MRI.",
        "Sturge-Weber syndrome.",
        "Refractory epilepsy and intellectual disability/developmental delay (also: contralateral hemiparesis, hemianopia, and glaucoma in the affected eye).",
    ],
    "pearl": "V1 port-wine stain + seizures + tram-track calcifications = Sturge-Weber. Always check intraocular pressure — glaucoma is common and preventable blindness.",
}

MODEL_ANSWERS[35] = {  # Rickets
    "answers": [
        "Nutritional rickets (vitamin D deficiency).",
        "Vitamin D deficiency from inadequate sunlight exposure and dietary intake (also: dark skin pigmentation, exclusive breast-feeding without supplementation, malabsorption, anticonvulsant therapy).",
        "Genu varum (bow legs) or genu valgum (knock knees), with widened wrists and rachitic rosary (costochondral junctions).",
        "Oral cholecalciferol (vitamin D3) 2,000–5,000 IU daily for 6–12 weeks, followed by maintenance 400–800 IU/day, plus adequate dietary calcium intake (500–1000 mg/day).",
    ],
    "pearl": "Toddler + bowing legs + widened wrists + delayed walking/teething = rickets. Vit D + calcium for 6–12 weeks fixes it; check ALP and 25-OH vit D to confirm.",
}

MODEL_ANSWERS[36] = {  # Turner syndrome
    "answers": [
        "Turner syndrome (45,XO — complete or partial monosomy of X chromosome).",
        "Short stature, webbed neck, wide-spaced nipples (\"shield chest\"), increased carrying angle (cubitus valgus), low posterior hairline, lymphoedema of hands/feet at birth, and primary amenorrhoea / streak ovaries.",
        "Coarctation of the aorta and bicuspid aortic valve (also: horseshoe kidney, hypothyroidism, recurrent otitis media, osteoporosis, and learning difficulties in non-verbal/visuospatial domains).",
        "Growth hormone therapy from early childhood to maximise final height, oestrogen replacement from age 11–12 for pubertal induction, and lifelong follow-up — annual echocardiogram, TFTs, hearing checks, and fertility counselling (assisted reproduction with donor oocytes).",
    ],
    "pearl": "Short girl + webbed neck + wide-spaced nipples + delayed puberty = Turner syndrome (45,XO). Always echo (coarctation, bicuspid AV) + renal US (horseshoe kidney). GH + oestrogen.",
}

MODEL_ANSWERS[37] = {  # Marfan syndrome
    "answers": [
        "Steinberg thumb sign (thumb adducted across the palm protrudes beyond the ulnar border of the hand) and Walker-Murdoch wrist sign (thumb and fifth finger overlap when encircling the contralateral wrist).",
        "Marfan syndrome.",
        "Mutation in the FBN1 gene on chromosome 15 (encodes fibrillin-1, a glycoprotein essential for elastic fibres in connective tissue); autosomal dominant inheritance with variable expressivity.",
        "Tall stature with disproportionately long limbs (arm-span > height) and arachnodactyly; high-arched palate with dental crowding; aortic root dilatation with risk of aortic dissection and aortic regurgitation; ectopia lentis (superotemporal lens dislocation) and severe myopia (also: pectus excavatum/carinatum, scoliosis, mitral valve prolapse, spontaneous pneumothorax).",
    ],
    "pearl": "Tall + long arms + high palate + thumb/wrist sign + lens dislocation = Marfan. Annual echo for aortic root — death is from aortic dissection. Beta-blocker (or losartan) slows root dilatation.",
}

MODEL_ANSWERS[38] = {  # Pyelonephritis
    "answers": [
        "Nitrites positive (1+), leukocyte esterase strongly positive (3+), and significant bacteriuria (3+) — together highly suggestive of urinary tract infection.",
        "Acute pyelonephritis (upper urinary tract infection).",
        "Midstream urine (or clean-catch/suprapubic aspirate in young children) for microscopy, culture and sensitivity (>10⁵ CFU/mL is diagnostic); blood cultures if systemically unwell, FBC, CRP, U&E, and renal ultrasound to look for hydronephrosis/structural anomalies; DMSA scan at 4–6 months for renal scarring; MCUG for vesicoureteric reflux in selected cases.",
        "Vesicoureteric reflux (most common predisposing factor in children) or urinary stasis from posterior urethral valves, neuropathic bladder, or obstructive uropathy.",
        "Escherichia coli (≈80% of paediatric UTIs; also Klebsiella, Proteus, Enterococcus, and Staph saprophyticus in adolescents).",
    ],
    "pearl": "Child + fever + loin pain + nitrites/leukocytes on dipstick = pyelonephritis. Get culture before antibiotics. After first UTI in child <6 months: US + DMSA + MCUG to rule out reflux.",
}

# Standalone reference topic (no source case in CASES)
MODEL_ANSWERS["standalone"] = {
    "answers": [
        "Meningococcal rash: dark purple/red, NON-blanching (negative tumbler test); viral rash: pink/red, BLANCHES on pressure.",
        "Meningococcal: does NOT blanch (capillary haemorrhage from DIC); viral: blanches and returns (vascular dilatation only).",
        "Meningococcal: starts on extremities/pressure points and spreads centrally, may have any distribution; viral: typically generalised, often starting on trunk/face with centrifugal spread.",
        "Meningococcal: child is acutely unwell — high fever, lethargy, neck stiffness, signs of shock; viral: child usually mild–moderately unwell with coryza, cough, conjunctivitis.",
        "Meningococcal: rapidly progressive over hours, purpura fulminans, can be fatal within hours; viral: gradual onset, evolves over days, self-limiting.",
        "Meningococcal: medical emergency — immediate IM/IV benzylpenicillin or ceftriaxone in the community before transfer, then full sepsis management; viral: supportive care (paracetamol, fluids, antipyretics).",
    ],
    "pearl": "The tumbler (glass) test is your bedside discriminator. Any non-blanching rash in an unwell febrile child = meningococcal sepsis until proven otherwise — antibiotics in the COMMUNITY, before hospital.",
}
