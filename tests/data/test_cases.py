TEST_CASES = [
    {
        "question": "If my child that is 4 years old needs glasses how much do i have to pay?",
        "expected_response": "No charge, deductible does not apply",
        "should_match": True,
    },
    {
        "question": "Can I visit the chiropractor?",
        "expected_response": "Yes, 20 Visits per year are allowed but for spinal manipulation only.",
        "should_match": True,
    },
    {
        "question": "How much is the max deductible?",
        "expected_response": "$35,000",
        "should_match": False,
    },
]

TEST_CASES_100 = [
  {
    "question": "What is the monthly premium and does this plan offer a Part B premium reduction?",
    "expected_response": "Monthly plan premium $0\nYou must keep paying your Medicare Part B premium.\nPart B premium reduction Your plan will reduce your Monthly Part B premium by up to $150 but by no more than Original Medicare's Part B Premium for 2025.",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "Does this plan have a medical deductible?",
    "expected_response": "Medical deductible This plan does not have a deductible.",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "What is the maximum out-of-pocket limit for this plan?",
    "expected_response": "Maximum out-of-pocket responsibility\n$3,200 in-network\nThe most you pay for copays, coinsurance and other costs for covered medical services for the year.",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "How much will I pay per day for an inpatient hospital stay under this plan?",
    "expected_response": "INPATIENT HOSPITAL COVERAGE\nThis plan covers an unlimited number of days for an inpatient stay.\n$150 copay per day for days 1-5\n$0 copay per day for days 6-90",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "What is the copay for outpatient surgery at a hospital?",
    "expected_response": "OUTPATIENT HOSPITAL COVERAGE\nDiagnostic colonoscopy $0 copay\nDiagnostic mammography $0 copay\nSurgery services $175 copay",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "How much is a primary care visit on this plan?",
    "expected_response": "Primary Care Provider (PCP)\n• PCP's office: $0 copay\n• Telehealth: $0 copay",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "What is the specialist office visit copay?",
    "expected_response": "Specialist\n• Specialist's office: $10 copay\n• Telehealth: $10 copay",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "What do I pay for emergency room services and are there any conditions?",
    "expected_response": "Emergency services at emergency room\nIf you are admitted to the same hospital within 24 hours, you do not have to pay your share of the cost for the emergency care. When placed in observation, member pays observation cost-share instead of emergency room cost-share.\n$140 copay\nPhysician and professional services at emergency room\n$0 copay",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "How much is the copay for urgently needed care or urgent care center visits?",
    "expected_response": "URGENTLY NEEDED SERVICES\nUrgently needed services are provided to treat a non-emergency, unforeseen medical illness, injury or condition that requires immediate medical attention.\n• Telehealth: $15 copay\n• Urgent care center: $15 copay",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "Are preventive services covered at no cost?",
    "expected_response": "Any additional preventive services approved by Medicare during the contract year will be covered.\n$0 copay",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "What is the cost for ground ambulance transportation under this plan?",
    "expected_response": "AMBULANCE\nAir 20% of the cost\nGround $260 copay per date of service",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "Is air ambulance service covered and if so, what is the cost?",
    "expected_response": "AMBULANCE\nAir 20% of the cost\nGround $260 copay per date of service",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "What will I pay for skilled nursing facility care after the first 20 days?",
    "expected_response": "SKILLED NURSING FACILITY (SNF)\nThis plan covers up to 100 days in a SNF\n$0 copay per day for days 1-20\n$160 copay per day for days 21-100",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "Does this plan cover routine vision exams and eyeglasses?",
    "expected_response": "$0 copay for routine exam up to 1 per year.\n$400 maximum benefit coverage amount per year for contact lenses or eyeglasses-lenses and frames plus fitting; or 3 pairs of select eyeglasses per year at no cost.",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "What dental services are covered and is there an annual maximum benefit?",
    "expected_response": "• $0 copay for periodic oral exam, prophylaxis (cleaning) up to 2 per year.\n• $0 copay for amalgam and/or composite filling, necessary anesthesia with covered service, simple or surgical extraction up to unlimited per year.\n• 30% of the cost for complete dentures, partial dentures up to 1 every 5 years.\n• $1,000 maximum benefit coverage amount per year for all diagnostic/preventive and comprehensive benefits.",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "Are hearing aids covered by this plan and what would I pay?",
    "expected_response": "• $0 copay for fitting/evaluation, routine hearing exams up to 1 per year.\n• $199 copay for each Value Technology hearing aid up to 1 per ear per year.\n• $699 copay for each Advanced Technology hearing aid up to 1 per ear per year.\n• $1,299 copay for each Premium Technology hearing aid up to 1 per ear per year.\n• Note: Includes 1 year warranty and 1 month battery supply.",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "Does the plan include routine acupuncture treatments?",
    "expected_response": "Routine Acupuncture\n$0 copay for acupuncture visits up to 25 visit(s) per year. Authorization rules may apply.",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "Are routine podiatry (foot care) visits covered?",
    "expected_response": "Routine foot care\n$10 copay for routine podiatry visits up to unlimited visit(s) per year.",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "Does this plan offer any in-home support after a hospital or SNF discharge?",
    "expected_response": "Post Discharge Personal Home Care\n$0 copay for a minimum of 4 hours per day, up to a maximum of 44 hours per year for certain in-home support services following a discharge from a skilled nursing facility or from an inpatient hospitalization.",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "Is a fitness program like SilverSneakers included with this plan?",
    "expected_response": "SilverSneakers® fitness program\nLive a healthier, more active life through fitness and social connection at participating locations and online.",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "Do I need referrals from my primary doctor to see specialists on this plan?",
    "expected_response": "Your primary care provider (PCP) will work with you to coordinate the care you need with specialists or certain other providers in the network. This is called a \"referral.\"",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "Is there a cap on insulin costs under this plan?",
    "expected_response": "You won't pay more than $35 for a one-month (up to 30-day) supply of each insulin product covered by this plan.",
    "should_match": True,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "Does this plan provide an allowance for over-the-counter items?",
    "expected_response": "No",
    "should_match": False,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "Are routine chiropractic services covered by this plan?",
    "expected_response": "No",
    "should_match": False,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "Will this plan cover cosmetic surgery procedures?",
    "expected_response": "No",
    "should_match": False,
    "source": "H1036269000SB25.pdf"
  },
  {
    "question": "What is the monthly premium for this plan and who pays the Part B premium?",
    "expected_response": "Monthly plan premium $0\nYou must keep paying your Medicare Part B premium. Your Part A and/or Part B premium may be paid on your behalf by Florida Medicaid Program.",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Is there a deductible for medical or Part D drug coverage on this plan?",
    "expected_response": "Medical deductible  This plan does not have a deductible.\nPharmacy (Part D) deductible $0 deductible if you receive \"Extra Help.\"",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "What is the maximum out-of-pocket I would be responsible for, and what if I have Medicaid?",
    "expected_response": "Maximum out-of-pocket responsibility\n$3,400 in-network\nIf you are eligible for Medicare cost-sharing assistance under Florida Medicaid you are not responsible for paying any out-of-pocket costs toward the maximum out-of-pocket amount for covered Part A and Part B services.",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "How much do I pay for an inpatient hospital stay under this plan?",
    "expected_response": "INPATIENT HOSPITAL COVERAGE\nThis plan covers an unlimited number of days for an inpatient stay.\n$0 copay",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "What is the copay to see a primary care physician (PCP)?",
    "expected_response": "Primary care provider (PCP)\n• PCP's office $0 copay\n• Telehealth $0 copay",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "How much will I pay to see a specialist on this plan?",
    "expected_response": "Specialist's office $0 copay",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "What do covered prescription drugs cost with this plan?",
    "expected_response": "$0 Rx Copay Benefit If you receive \"Extra Help,\" you will pay $0 for all Medicare Part D plan-covered prescription drugs for the entire calendar year.",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Are routine vision services like eye exams and glasses covered?",
    "expected_response": "$0 copay for routine exam up to 1 per year.\n$400 maximum benefit coverage amount per year for contact lenses or eyeglasses-lenses and frames plus fitting; or 3 pairs of select eyeglasses per year at no cost.",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Does this plan cover routine hearing exams and hearing aids?",
    "expected_response": "$0 copay for fitting/evaluation, routine hearing exams up to 1 per year.\n$1,000 maximum benefit coverage amount for each prescription hearing aids (all types) up to 1 per ear per year.",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "What kind of dental coverage does this plan provide?",
    "expected_response": "Plan covers up to $5000 allowance every year for non-Medicare covered preventive and comprehensive dental services.",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Is transportation to medical appointments included in this plan?",
    "expected_response": "TRANSPORTATION\nThe member must contact transportation vendor to arrange transportation and should contact Customer Care to be directed to their plan's specific transportation provider.\n$0 copay for plan approved location up to 4 one-way trip(s) per year.\nThis benefit offers unlimited miles per trip.",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Does this plan offer any monthly allowance for groceries or over-the-counter items?",
    "expected_response": "$100 monthly allowance on a prepaid card to use for essentials you need to support your health.\nThis allowance can be used to buy approved products from participating retail locations (like groceries, over-the-counter health and wellness items, personal care items, home supplies, etc.) or pay for approved services (monthly living expenses like rent, non-medical transportation costs like a taxi, Uber, Lyft, etc.).",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Are routine chiropractic services covered under this plan?",
    "expected_response": "Routine Chiropractic services\n$0 copay for routine chiropractic visits up to 12 visit(s) per year.",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Does the plan provide a meal benefit after a hospital or nursing facility stay?",
    "expected_response": "$0 copayment for Humana Well Dine\u00ae meal program.\nAfter your inpatient stay in either a hospital or a nursing facility, you may be eligible to receive 2 home delivered meals per day for 7 days (up to 14 meals).\nLimited to 4 times per year.",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Are wigs covered for members undergoing chemotherapy?",
    "expected_response": "Wigs (related to chemotherapy treatment)\nUp to an unlimited maximum benefit per year.",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Does this plan cover routine acupuncture visits?",
    "expected_response": "Routine Acupuncture\n$0 copay for acupuncture visits up to 25 visit(s) per year.",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Do I need referrals to see specialists with this plan?",
    "expected_response": "Your primary care provider (PCP) will work with you to coordinate the care you need with specialists or certain other providers in the network. This is called a \"referral.\"",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Is durable medical equipment (DME) provided at no cost?",
    "expected_response": "Durable medical equipment (DME) $0 copay\nDurable medical equipment (DME) \u2013 Oxygen $0 copay\nMedical supplies at medical supplier $0 copay\nProsthetic devices and related supplies $0 copay",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "What do I pay for skilled nursing facility (SNF) care on this plan?",
    "expected_response": "SKILLED NURSING FACILITY\nThis plan covers up to 100 days in a SNF $0 copay",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "How much do mental health therapy visits cost under this plan?",
    "expected_response": "Mental health therapy visits\n\u2022 Outpatient hospital $0 copay\n\u2022 Partial hospitalization $0 copay\n\u2022 Specialist's office $0 copay",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Are adult immunizations and vaccines covered without cost?",
    "expected_response": "$0 vaccines $0 copay for adult Part D covered vaccines recommended by the Advisory Committee on Immunization Practices (ACIP)",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Do Part B chemotherapy drugs have any copay under this plan?",
    "expected_response": "Chemotherapy drugs\n\u2022 Outpatient hospital $0 copay\n\u2022 Specialist's office $0 copay",
    "should_match": True,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Does this plan offer a Part B premium giveback or reduction?",
    "expected_response": "No",
    "should_match": False,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Can I receive care from out-of-network providers on this HMO plan?",
    "expected_response": "No",
    "should_match": False,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "Are infertility treatments or IVF covered by this plan?",
    "expected_response": "No",
    "should_match": False,
    "source": "H1036280000SB25.pdf"
  },
  {
    "question": "What is the monthly premium and Part B premium rebate for this plan?",
    "expected_response": "Monthly plan premium $0\nPart B premium reduction Your plan will reduce your Monthly Part B premium by up to $174.70",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "Is there a deductible for medical services, and what services are excluded from it?",
    "expected_response": "Medical deductible $275 combined\nThe following services listed are excluded from the combined in-network and out-of-network deductible:\n\u2022 Primary Care Physician's Office\n\u2022 Specialist's Office\n\u2022 Emergency Room Services\n\u2022 Medicare Covered Preventive Services (including Immunizations (Flu & Pneumonia))\n\u2022 Urgently Needed Services at Urgent Care Centers",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "What is the Part D pharmacy deductible on this plan?",
    "expected_response": "Pharmacy (Part D) deductible $0 deductible.",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "What is the maximum out-of-pocket for this PPO plan?",
    "expected_response": "Maximum out-of-pocket responsibility\n$6,700 in-network\n$6,700 combined in- and out-of-network\nThe most you pay for copays, coinsurance and other costs for covered medical services for the year.",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "Do I need referrals to see specialists on this plan?",
    "expected_response": "You do not need a referral to receive covered services from plan providers.",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "What are the inpatient hospital costs for this plan?",
    "expected_response": "INPATIENT HOSPITAL COVERAGE\nThis plan covers an unlimited number of days for an inpatient stay.\n$350 copay per day for days 1-7\n$0 copay per day for days 8-90",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "How much is the copay for outpatient surgery in a hospital setting?",
    "expected_response": "OUTPATIENT HOSPITAL COVERAGE\nSurgery services $295 copay $295 copay",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "What is the copay for surgery at an ambulatory surgery center?",
    "expected_response": "AMBULATORY SURGERY CENTER\nSurgery services $175 copay $175 copay",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "How much do I pay for a primary care doctor visit, both in-network and out-of-network?",
    "expected_response": "Primary care provider (PCP)\n\u2022 PCP's office $0 copay\n\u2022 Telehealth $0 copay\n$0 copay (out-of-network PCP's office)",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "What is the specialist visit copay in-network versus out-of-network?",
    "expected_response": "Specialist\n\u2022 Specialist's office $45 copay\n\u2022 Telehealth $45 copay\n$45 copay (out-of-network specialist's office)",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "Are preventive services covered at no charge, even out-of-network?",
    "expected_response": "PREVENTIVE CARE\n$0 copay $0 copay",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "What is the emergency room copay for this plan?",
    "expected_response": "EMERGENCY CARE\nEmergency services at emergency room\n$125 copay $125 copay\nPhysician and professional services at emergency room\n$0 copay $0 copay",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "How much will I pay for urgently needed care or urgent care center visits?",
    "expected_response": "URGENTLY NEEDED SERVICES\n\u2022 Telehealth $15 copay\n\u2022 Urgent care center $15 copay\nNot Covered (telehealth out-of-network); $15 copay (out-of-network urgent care)",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "What are the costs for ambulance services on this plan?",
    "expected_response": "AMBULANCE\nAir 20% of the cost 20% of the cost\nGround $240  copay per date of service $240  copay per date of service",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "How much do I pay for skilled nursing facility care with this plan?",
    "expected_response": "SKILLED NURSING FACILITY (SNF)\nThis plan covers up to 100 days in a SNF\n$0 copay per day for days 1-20\n$160 copay per day for days 21-100",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "Does this plan include any dental coverage for cleanings or fillings?",
    "expected_response": "0% of the cost for periodic oral exam, prophylaxis (cleaning) up to 2 per year.\n$25 copay per tooth for amalgam and/or composite filling up to unlimited per year.\n$1,000 combined maximum benefit coverage amount per year for all diagnostic/preventive and comprehensive benefits.",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "Are routine vision exams and eyewear covered, and if so, what is the benefit?",
    "expected_response": "$0 copay for routine exam up to 1 per year.\n$75 combined maximum benefit coverage amount per year for routine exam.\n$50 maximum benefit coverage amount per year for contact lenses or eyeglasses-lenses and frames, fitting for eyeglasses-lenses and frames.",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "How much do outpatient mental health therapy visits cost on this plan?",
    "expected_response": "Mental health therapy visits\n\u2022 Outpatient hospital $60 copay\n\u2022 Partial hospitalization  $45 copay\n\u2022 Specialist's office $30 copay",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "What coinsurance do I pay for Part B chemotherapy drugs?",
    "expected_response": "Chemotherapy drugs\n\u2022 Outpatient hospital 20% of the cost\n\u2022 Specialist's office 20% of the cost",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "Does this plan limit insulin costs to $35 per month?",
    "expected_response": "You won't pay more than  $35 for a one-month (up to 30-day) supply of each plan-covered insulin product regardless of cost-sharing tier.",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "Are routine hearing exams and hearing aids covered under this plan?",
    "expected_response": "$0 copay for fitting/evaluation, routine hearing exams up to 1 per year.\n$500 combined maximum benefit coverage amount for the choice of each OTC hearing aids or each prescription hearing aids (all types) up to 1 per ear per year.",
    "should_match": True,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "Does this plan cover routine acupuncture visits beyond Medicare's coverage?",
    "expected_response": "No",
    "should_match": False,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "Is there any monthly allowance card for groceries or OTC items on this plan?",
    "expected_response": "No",
    "should_match": False,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "Does this plan include a post-discharge home meal delivery benefit?",
    "expected_response": "No",
    "should_match": False,
    "source": "H5216393000SB25.pdf"
  },
  {
    "question": "What is the individual deductible for in-network and out-of-network services on this plan?",
    "expected_response": "In-Network: $3,500 Individual / $7,000 Family;\nOut-of-Network Provider: $7,000 Individual / $14,000 Family",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "What is the out-of-pocket limit for this plan, in-network vs out-of-network?",
    "expected_response": "In-Network Provider: $7,000 Individual / $14,000 Family;\nOut-of-Network Provider: $14,000 Individual / $28,000 Family",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "Are any services covered before the deductible is met?",
    "expected_response": "Yes. Preventive care and services indicated in chart starting on page 2.",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "Will I pay less if I use a Kaiser network provider?",
    "expected_response": "This plan uses a provider network. You will pay less if you use a provider in the plan\u2019s network. You will pay the most if you use an out-of-network provider, and you might receive a bill from a provider for the difference between the provider\u2019s charge and what your plan pays (balance billing).",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "Do I need a referral to see a specialist?",
    "expected_response": "Yes, but you may self-refer to certain specialists.\nThis plan will pay some or all of the costs to see a specialist for covered services but only if you have a referral before you see the specialist.",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "What is the cost-sharing for a primary care visit under this plan?",
    "expected_response": "Primary care visit to treat an injury or illness\nKP: 20% coinsurance / visit.\nNetwork: 30% coinsurance / visit.\n40% coinsurance",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "What coinsurance applies for a specialist visit?",
    "expected_response": "Specialist visit\nKP: 20% coinsurance / visit.\nNetwork: 30% coinsurance / visit.\n40% coinsurance",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "How much do I pay for preventive care services?",
    "expected_response": "Preventive care/ screening/ immunization\nNo charge, deductible does not apply\n30% coinsurance",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "What is the cost for diagnostic tests like x-rays or blood work?",
    "expected_response": "Diagnostic test (x-ray, blood work)\n20% coinsurance regardless of setting\n40% coinsurance\nNone",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "How much will an MRI or CT scan cost me under this plan?",
    "expected_response": "Imaging (CT/PET scans, MRI's)\n20% coinsurance / scan regardless of setting\n40% coinsurance\nPreauthorization required, or not covered.",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "What do generic prescription drugs cost on this plan?",
    "expected_response": "Generic drugs\nKP: 20% coinsurance / prescription (retail & mail order).\nNetwork: 30% coinsurance / prescription.\n40% coinsurance",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "How are preferred brand drugs covered?",
    "expected_response": "Preferred brand drugs\nKP: 20% coinsurance / prescription (retail & mail order).\nNetwork: 30% coinsurance / prescription.\n40% coinsurance",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "What is the cost for non-preferred brand drugs?",
    "expected_response": "Non-preferred brand drugs\nKP: 20% coinsurance / prescription (retail & mail order).\nNetwork: 30% coinsurance / prescription.\n40% coinsurance",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "How are specialty drugs covered under this plan?",
    "expected_response": "Specialty drugs\nKP: 20% coinsurance / prescription (retail).\nNetwork: 30% coinsurance / prescription.\n40% coinsurance",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "What is the cost-sharing for an outpatient surgery facility fee?",
    "expected_response": "Facility fee (e.g., ambulatory surgery center)\n20% coinsurance\n40% coinsurance\nPreauthorization required, or not covered.",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "How much will I pay for the surgeon or physician fees for surgery?",
    "expected_response": "Physician/surgeon fees\n20% coinsurance\n40% coinsurance\nPreauthorization required, or not covered.",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "What is the emergency room cost under this plan?",
    "expected_response": "Emergency room care\n20% coinsurance\n20% coinsurance\nNone",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "How much do I pay for emergency medical transportation (ambulance)?",
    "expected_response": "Emergency medical transportation\n20% coinsurance\n20% coinsurance\nNone",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "What is the cost for an urgent care visit on this plan?",
    "expected_response": "Urgent care\nKP: 20% coinsurance / visit.\nNetwork: 30% coinsurance / visit.\n40% coinsurance",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "Does this plan provide Minimum Essential Coverage?",
    "expected_response": "Does this plan provide Minimum Essential Coverage? Yes.",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "What expenses do not count toward the out-of-pocket limit?",
    "expected_response": "Premiums, precertification penalties, balance-billing charges, health care this plan doesn't cover, and services indicated in chart starting on page 2.",
    "should_match": True,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "Does this plan cover adult dental or vision care for routine needs?",
    "expected_response": "Yes",
    "should_match": False,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "Are hearing aids or hearing exams covered by this plan?",
    "expected_response": "Yes",
    "should_match": False,
    "source": "KaiserPPO.pdf"
  },
  {
    "question": "Does the plan cover bariatric surgery for weight loss?",
    "expected_response": "No",
    "should_match": False,
    "source": "KaiserPPO.pdf"
  }
]
