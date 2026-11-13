"""
Financial knowledge base loader.
Provides curated, structured content on UPI, online scams, interest rates,
budgeting, and personal finance — sourced from government portals and banking guidelines.
Documents are returned as LangChain Document objects ready for vector indexing.
"""

from langchain_core.documents import Document

# ---------------------------------------------------------------------------
# Topic: UPI (Unified Payments Interface)
# ---------------------------------------------------------------------------

UPI_CONTENT = [
    Document(
        page_content="""
UPI (Unified Payments Interface) is a real-time payment system developed by the National Payments 
Corporation of India (NPCI). It allows instant money transfer between bank accounts using a 
Virtual Payment Address (VPA), also called a UPI ID (e.g., yourname@okaxis).

HOW TO SEND MONEY VIA UPI:
1. Open any UPI-enabled app: Google Pay, PhonePe, Paytm, BHIM, or your bank's app.
2. Tap "Send Money" or "Pay".
3. Enter the recipient's UPI ID, mobile number, or scan their QR code.
4. Enter the amount and add a note (optional).
5. Enter your 4- or 6-digit UPI PIN to confirm.
6. You receive a transaction confirmation immediately.

IMPORTANT: Your UPI PIN is ONLY used to SEND money or verify yourself — never to RECEIVE money.
If someone asks for your UPI PIN to send you money, it is a SCAM.

TRANSACTION LIMITS: Most banks allow up to ₹1,00,000 per transaction. Some banks allow up to ₹2,00,000.
UPI transactions are FREE of charge for users.
""",
        metadata={"source": "NPCI UPI Guidelines", "topic": "UPI Payments"},
    ),
    Document(
        page_content="""
UPI SAFETY TIPS:
- Never share your UPI PIN, OTP, or bank password with anyone, including people claiming to be bank officials.
- Verify the recipient's UPI ID before transferring money. Once sent, UPI payments cannot be reversed.
- Do NOT click on "Collect Money" requests from unknown people — these are designed to trick you into paying.
- Use only official apps from Google Play Store or Apple App Store.
- Enable transaction notifications so you are alerted instantly.
- If you receive a suspicious collect request, REJECT it immediately.
- Report fraud at: https://cybercrime.gov.in or call 1930 (Cybercrime Helpline).

COMMON UPI SCAMS:
1. QR Code Scam: Scammer sends a QR code saying "scan to receive ₹500". Scanning actually DEBITS your account.
2. Screen Mirroring: Scammer asks you to install AnyDesk or TeamViewer to "help" and then steals your PIN.
3. Fake Customer Care: Fake bank numbers found on Google ask for your UPI PIN over call.
""",
        metadata={"source": "RBI Digital Payment Safety", "topic": "UPI Safety"},
    ),
]

# ---------------------------------------------------------------------------
# Topic: Online Scams & Fraud Prevention
# ---------------------------------------------------------------------------

SCAM_CONTENT = [
    Document(
        page_content="""
TYPES OF ONLINE FINANCIAL SCAMS IN INDIA:

1. PHISHING SCAMS: Fake emails or SMS that look like they are from your bank, asking you to click a link 
   and enter your credentials. Always verify the sender's email domain.

2. KYC FRAUD: Calls claiming your bank/wallet account will be blocked unless you complete KYC immediately 
   by sharing OTP or account details. Banks NEVER ask for OTP over phone.

3. LOTTERY/PRIZE SCAMS: Messages saying you've won a prize. You are asked to pay "processing fees" to claim 
   it. Legitimate lotteries do not ask for advance payment.

4. INVESTMENT SCAMS: Promises of 30–100% returns in short time. Legitimate investments regulated by SEBI 
   do not guarantee such returns.

5. PART-TIME JOB SCAMS: Asked to invest money to "unlock tasks" or earn commissions — this is a Ponzi scheme.

6. LOAN SCAMS: Instant loan apps that charge hidden fees upfront and then harass borrowers. 
   Only use RBI-registered lenders.

HOW TO STAY SAFE:
- Verify any financial platform at: https://www.rbi.org.in/Scripts/EntitySearch.aspx
- Never pay any upfront fee to receive a loan or prize.
- File complaints at: https://cybercrime.gov.in
- Cybercrime Helpline: 1930
""",
        metadata={"source": "RBI Financial Fraud Awareness", "topic": "Online Scams"},
    ),
    Document(
        page_content="""
RED FLAGS OF A FINANCIAL SCAM:
- Urgency: "Act NOW or your account will be blocked in 2 hours."
- Secrecy: "Don't tell your family about this investment."
- Guaranteed high returns: "Earn ₹10,000 daily with zero risk."
- Request for OTP, PIN, or password via phone/SMS/WhatsApp.
- Advance fees for a loan or prize.
- Requests to install remote-access apps (AnyDesk, TeamViewer, QuickSupport).

WHAT TO DO IF SCAMMED:
1. Call 1930 (National Cybercrime Helpline) immediately.
2. Report online at https://cybercrime.gov.in
3. Contact your bank to block the account or card.
4. File an FIR at the nearest police station.
5. Preserve all evidence: screenshots, transaction IDs, phone numbers.

REMEMBER: Banks, NPCI, and government agencies will NEVER ask for your PIN or OTP.
""",
        metadata={"source": "Ministry of Home Affairs Cybercrime Portal", "topic": "Fraud Prevention"},
    ),
]

# ---------------------------------------------------------------------------
# Topic: Interest Rates
# ---------------------------------------------------------------------------

INTEREST_CONTENT = [
    Document(
        page_content="""
UNDERSTANDING INTEREST RATES:

SIMPLE INTEREST: Interest calculated only on the principal amount.
Formula: SI = (Principal × Rate × Time) / 100
Example: ₹10,000 at 8% for 2 years → SI = ₹1,600. Total repayment = ₹11,600.

COMPOUND INTEREST: Interest calculated on principal + previously earned interest.
Formula: A = P × (1 + r/n)^(n×t)   where n = compounding frequency per year.
Compound interest grows faster — works IN YOUR FAVOUR for savings/FDs, but AGAINST YOU for loans.

TYPICAL INTEREST RATES IN INDIA (2024):
- Home Loan: 8.5% – 10.5% per annum (floating/fixed, RBI-regulated banks)
- Personal Loan: 10% – 24% per annum (bank) | up to 36% from NBFCs — compare carefully
- Credit Card: 36% – 42% per annum — ALWAYS pay full bill to avoid this
- Fixed Deposit (FD): 6.5% – 7.5% per annum (bank FDs, up to ₹5 lakh insured by DICGC)
- Savings Account: 2.5% – 7% per annum
- Pradhan Mantri Jan Dhan Account: 4% per annum

SAFE INTEREST RATE FOR A LOAN:
- For personal loans from RBI-regulated banks: up to 18% per annum is considered reasonable.
- Avoid any lender charging more than 36% per annum — this is very high.
- Always check the Annual Percentage Rate (APR) which includes processing fees.
- Microfinance Institutions (MFI): RBI caps interest at ~24% for small borrowers.
""",
        metadata={"source": "RBI Interest Rate Guidelines & Banking Awareness", "topic": "Interest Rates"},
    ),
    Document(
        page_content="""
EMI (Equated Monthly Instalment):
EMI = [P × r × (1+r)^n] / [(1+r)^n – 1]
Where P = Principal, r = monthly interest rate, n = number of months.

Example: ₹5,00,000 home loan at 9% for 20 years → Monthly EMI ≈ ₹4,496.

TIPS TO SAVE INTEREST:
1. Make prepayments when possible — reduces principal and total interest paid.
2. Choose shorter tenure if you can afford higher EMI.
3. Maintain a good CIBIL credit score (above 750) to get lower interest rates.
4. Compare loans on https://www.bankbazaar.com or https://www.paisabazaar.com
5. Read all loan documents carefully before signing — check for hidden charges.

CREDIT SCORE BASICS:
- CIBIL Score range: 300–900. Above 750 is excellent.
- Affects your loan eligibility and interest rate.
- Check your free credit report at: https://www.cibil.com (once per year free)
- Build score by: paying EMIs on time, keeping credit utilisation below 30%.
""",
        metadata={"source": "RBI Consumer Education", "topic": "Loans and EMI"},
    ),
]

# ---------------------------------------------------------------------------
# Topic: Budgeting
# ---------------------------------------------------------------------------

BUDGET_CONTENT = [
    Document(
        page_content="""
PERSONAL BUDGETING BASICS:

The 50-30-20 Rule is a simple and popular budgeting framework:
- 50% of income → Needs (rent, groceries, utilities, EMIs, medicine)
- 30% of income → Wants (eating out, entertainment, shopping, travel)
- 20% of income → Savings & Investments (emergency fund, FD, SIP, PPF)

HOW TO CREATE A MONTHLY BUDGET:
1. Calculate your total monthly take-home income.
2. List all fixed expenses (rent, loan EMI, insurance premium).
3. Estimate variable expenses (groceries, transport, bills).
4. Subtract total expenses from income → this is your savings potential.
5. Set saving goals (emergency fund = 3–6 months of expenses).
6. Track spending using apps: ET Money, Money View, Walnut, or a simple notebook.

EMERGENCY FUND: Aim to save at least 3 months of living expenses in a liquid savings account or 
liquid mutual fund before making any other investments.

FREE BUDGETING TOOLS:
- https://www.etmoney.com (Indian personal finance app)
- https://moneyview.in
- RBI's financial literacy material: https://www.rbi.org.in/financialeducation
""",
        metadata={"source": "RBI Financial Education Portal", "topic": "Budgeting"},
    ),
    Document(
        page_content="""
SAVINGS INSTRUMENTS FOR BEGINNERS IN INDIA:

1. SAVINGS ACCOUNT: Instant liquidity, 2.5–7% interest. Best for emergency fund.
2. FIXED DEPOSIT (FD): 6.5–7.5% interest, locked for a period. Up to ₹5 lakh insured by DICGC.
3. PUBLIC PROVIDENT FUND (PPF): 7.1% interest (tax-free), 15-year lock-in. Excellent for long-term saving.
4. NATIONAL SAVINGS CERTIFICATE (NSC): 7.7%, 5-year lock-in. Good for conservative investors.
5. RECURRING DEPOSIT (RD): Save a fixed amount every month. Good discipline tool.
6. SIP (Systematic Investment Plan): Invest in mutual funds monthly starting from ₹100. 
   Higher returns potential but subject to market risk.
7. PRADHAN MANTRI JAN DHAN YOJANA: Zero-balance account with ₹2 lakh accident insurance and ₹30,000 life cover.
8. SUKANYA SAMRIDDHI YOJANA: For girl child. 8.2% interest, tax-free — excellent scheme.
9. ATAL PENSION YOJANA: Government-backed pension scheme for unorganized sector workers.

RULE: Never invest in something you don't understand. Start simple with FD or RD before mutual funds.
""",
        metadata={"source": "India Post / RBI Savings Schemes", "topic": "Savings Instruments"},
    ),
]

# ---------------------------------------------------------------------------
# Topic: Personal Finance Management
# ---------------------------------------------------------------------------

PERSONAL_FINANCE_CONTENT = [
    Document(
        page_content="""
PERSONAL FINANCE MANAGEMENT — GETTING STARTED:

STEP 1 — KNOW YOUR NET WORTH:
Net Worth = Total Assets − Total Liabilities
Assets: cash, savings, property, gold, investments.
Liabilities: loans, credit card dues, any money owed.
A positive and growing net worth means you're on the right track.

STEP 2 — MANAGE DEBT WISELY:
- Pay off high-interest debt first (credit cards, personal loans).
- Avoid taking new debt to pay old debt.
- Debt-to-Income Ratio should stay below 40%: (monthly debt payments / monthly income) × 100.

STEP 3 — PROTECT YOURSELF WITH INSURANCE:
- Health Insurance: Minimum ₹5 lakh cover. Protects savings from medical emergencies.
- Term Life Insurance: Pure protection plan. ₹1 crore cover available from ~₹700/month.
- Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY): ₹2 lakh life cover at ₹436/year.
- Pradhan Mantri Suraksha Bima Yojana (PMSBY): ₹2 lakh accident cover at ₹20/year.

STEP 4 — START INVESTING EARLY:
- Power of compounding: ₹1,000/month at 12% for 30 years → ₹35 lakh+.
- Start a SIP in an index fund (Nifty 50 / Sensex) for long-term wealth creation.
- Register at SEBI-registered platforms only: Zerodha, Groww, ET Money, etc.
""",
        metadata={"source": "SEBI Investor Education / RBI Personal Finance", "topic": "Personal Finance"},
    ),
    Document(
        page_content="""
DIGITAL BANKING SAFETY — BEST PRACTICES:

1. Use strong, unique passwords for banking apps and internet banking.
2. Enable two-factor authentication (2FA) on all financial accounts.
3. Never use public Wi-Fi for banking transactions.
4. Regularly check your bank statements for unauthorised transactions.
5. Register for SMS and email alerts for all account transactions.
6. Log out of banking apps after every session.
7. Keep your registered mobile number updated with your bank.
8. Download banking apps only from official bank websites or Play Store/App Store.

GOVERNMENT FINANCIAL SCHEMES (Quick Reference):
- PM Kisan: ₹6,000/year for farmers
- PM Awas Yojana: Home loan subsidy for EWS/LIG
- Mudra Loan (PMMY): Up to ₹10 lakh for small businesses, no collateral
- Stand-Up India: Loans for SC/ST/women entrepreneurs
- Digital payment cashbacks: Many UPI apps offer cashback promotions

USEFUL HELPLINES & PORTALS:
- RBI Ombudsman (bank complaints): https://cms.rbi.org.in | 14448
- Cybercrime: https://cybercrime.gov.in | 1930
- SEBI investor complaints: https://scores.gov.in | 1800-266-7575 (toll-free)
- IRDAI insurance complaints: 155255
""",
        metadata={"source": "RBI / Government of India Financial Portals", "topic": "Digital Banking Safety"},
    ),
]


# ---------------------------------------------------------------------------
# Public loader
# ---------------------------------------------------------------------------

def get_all_documents() -> list:
    """Return all curated financial literacy documents."""
    return (
        UPI_CONTENT
        + SCAM_CONTENT
        + INTEREST_CONTENT
        + BUDGET_CONTENT
        + PERSONAL_FINANCE_CONTENT
    )
