

from fpdf import FPDF
import pandas as pd
import os
from datetime import datetime


class PDFReport(FPDF):
    """Custom PDF class for professional policy reports"""
    
    def header(self):
        # Logo placeholder - title instead
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Caribbean Cybersecurity Risk Assessment Report', 0, 1, 'R')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(200, 220, 240)
        self.cell(0, 12, title, 0, 1, 'L', 1)
        self.ln(4)
    
    def section_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    
    def subsection_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(1)
    
    def body_text(self, text):
        self.set_font('Helvetica', '', 11)
        # Replace unicode bullet points with ASCII-compatible dashes
        text = text.replace('\u2022', '-')
        self.multi_cell(0, 6, text)
        self.ln(3)
    
    def add_chart(self, chart_path, caption):
        if os.path.exists(chart_path):
            self.image(chart_path, x=10, w=190)
            self.ln(5)
            self.set_font('Arial', 'I', 10)
            self.cell(0, 6, f'Figure: {caption}', 0, 1, 'C')
            self.ln(5)


def generate_report():
    """Generate the complete policy report"""
    print("\n" + "=" * 60)
    print("Generating Policy Report")
    print("=" * 60)
    
    # Load data
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed')
    viz_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'visualizations')
    
    df_internet = pd.read_csv(os.path.join(data_dir, 'internet_penetration.csv'))
    df_literacy = pd.read_csv(os.path.join(data_dir, 'digital_literacy.csv'))
    df_attacks = pd.read_csv(os.path.join(data_dir, 'cyberattacks.csv'))
    df_risk = pd.read_csv(os.path.join(data_dir, 'risk_index.csv'))
    
    # Get Jamaica-specific data
    jamaica_risk = df_risk[df_risk['country'] == 'Jamaica'].iloc[0]
    jamaica_internet = df_internet[df_internet['country'] == 'Jamaica'].iloc[0]
    jamaica_literacy = df_literacy[df_literacy['country'] == 'Jamaica'].iloc[0]
    jamaica_attacks = df_attacks[df_attacks['country'] == 'Jamaica'].iloc[0]
    
    # Calculate regional statistics
    regional_avg_risk = df_risk['risk_index'].mean()
    regional_max_risk = df_risk['risk_index'].max()
    
    # Calculate Jamaica's rank
    jamaica_risk_value = df_risk[df_risk['country'] == 'Jamaica']['risk_index'].values[0]
    jamaica_rank = (df_risk['risk_index'] >= jamaica_risk_value).sum()
    
    # Create PDF
    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # ==================== TITLE PAGE ====================
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 20, '', 0, 1)
    pdf.cell(0, 15, 'Caribbean Cybersecurity', 0, 1, 'C')
    pdf.cell(0, 15, 'Risk Assessment Report', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 18)
    pdf.cell(0, 12, 'Jamaica Vulnerability Analysis', 0, 1, 'C')
    pdf.ln(20)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'A Policy Report on Cybersecurity Risks in the Caribbean', 0, 1, 'C')
    pdf.cell(0, 10, f'With Focus on Jamaica\'s Risk Profile', 0, 1, 'C')
    pdf.ln(30)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 8, f'Published: {datetime.now().strftime("%B %Y")}', 0, 1, 'C')
    pdf.cell(0, 8, 'Data Science & Cybersecurity Analysis', 0, 1, 'C')
    
    # ==================== EXECUTIVE SUMMARY ====================
    pdf.add_page()
    pdf.chapter_title('Executive Summary')
    
    executive_summary = f"""This report presents a comprehensive cybersecurity risk assessment of Caribbean nations, with particular focus on Jamaica's vulnerability profile. Analysis of cyberattack data, internet penetration rates, and digital literacy metrics across 17 Caribbean countries reveals critical insights into regional cybersecurity posture.

KEY FINDINGS:

- Jamaica faces a {jamaica_risk['risk_level'].upper()} cybersecurity risk level with a composite risk index of {jamaica_risk['risk_index']:.2f}/10, ranking {int(jamaica_rank)} out of 17 Caribbean nations analyzed.

- Cyberattacks in Jamaica have increased by {jamaica_risk['attack_growth_rate']:+.1f}% year-over-year, with {jamaica_attacks['total_attacks_2024']:,} total attacks recorded in 2024, including {jamaica_attacks['ransomware_attacks_2024']} ransomware incidents and {jamaica_attacks['phishing_attacks_2024']} phishing attacks.

- Jamaica's digital literacy score of {jamaica_literacy['digital_literacy_score']:.1f}/100 falls below the regional average, creating significant vulnerability gaps.

- The cybersecurity workforce stands at only {jamaica_literacy['cybersecurity_workforce_per_100k']:.1f} professionals per 100,000 population, severely limiting incident response capacity.

- Critical infrastructure attacks numbered {jamaica_attacks['critical_infra_attacks_2024']} in 2024, with average attack costs reaching ${jamaica_attacks['avg_attack_cost_usd']:,.0f}.

RISK ASSESSMENT:

- Exposure Score: {jamaica_risk['exposure_score']:.2f}/10 - Internet penetration creates expanding attack surface
- Vulnerability Score: {jamaica_risk['vulnerability_score']:.2f}/10 - Digital literacy gaps increase susceptibility
- Threat Score: {jamaica_risk['threat_score']:.2f}/10 - High attack frequency indicates active targeting
- Policy Gap Score: {jamaica_risk['policy_gap_score']:.2f}/10 - Existing frameworks need strengthening

This report provides evidence-based policy recommendations to strengthen Jamaica's cybersecurity posture through immediate actions and long-term strategic initiatives."""
    
    pdf.body_text(executive_summary)
    
    # ==================== TABLE OF CONTENTS ====================
    pdf.add_page()
    pdf.chapter_title('Table of Contents')
    
    toc = """1. Introduction and Methodology .......................... 3
2. Regional Cybersecurity Landscape .......................... 4
   2.1 Cyberattack Trends and Patterns
   2.2 Attack Type Analysis
   2.3 Critical Infrastructure Targeting
3. Internet Penetration Analysis ............................. 6
   3.1 Access and Connectivity
   3.2 Infrastructure Gaps
4. Digital Literacy Assessment ............................... 8
   4.1 Skills and Education
   4.2 Workforce Capacity
5. Jamaica Risk Profile .................................... 10
   5.1 Composite Risk Assessment
   5.2 Sector-Specific Vulnerabilities
   5.3 Comparative Regional Analysis
6. Policy Recommendations .................................. 13
   6.1 Immediate Actions (0-6 months)
   6.2 Medium-Term Initiatives (6-18 months)
   6.3 Long-Term Strategic Goals (18+ months)
7. Regional Cooperation Opportunities ........................ 16
8. Conclusion .............................................. 17
Appendices ................................................. 18"""
    
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, toc)
    
    # ==================== SECTION 1: INTRODUCTION ====================
    pdf.add_page()
    pdf.chapter_title('1. Introduction and Methodology')
    
    introduction = """This report analyzes cybersecurity risks across the Caribbean region, with specific focus on Jamaica's vulnerability profile. The assessment is based on comprehensive data collection from multiple sources including regional CERT reports, ITU statistics, World Bank indicators, and academic research on Caribbean cybersecurity incidents.

SCOPE:
The analysis covers 17 Caribbean nations including Jamaica, Trinidad and Tobago, Barbados, Dominican Republic, Haiti, Bahamas, Guyana, Saint Lucia, Grenada, Antigua and Barbuda, Saint Vincent and the Grenadines, Dominica, Saint Kitts and Nevis, Belize, Suriname, Cuba, and Puerto Rico.

METHODOLOGY:
The cybersecurity risk index is calculated using a weighted composite methodology:

Risk Index = (Exposure x 0.25) + (Vulnerability x 0.40) + (Threat x 0.35)

Where:
• EXPOSURE (25% weight): Based on internet penetration rates. Higher internet access creates a larger attack surface and increases potential impact of cyber incidents.

• VULNERABILITY (40% weight): Based on digital literacy scores and cybersecurity workforce capacity. Lower digital literacy and limited security professionals increase susceptibility to attacks.

• THREAT (35% weight): Based on historical cyberattack frequency and severity. Higher attack rates indicate active targeting by threat actors.

DATA SOURCES:
• International Telecommunication Union (ITU) Statistics
• World Bank Digital Development Data
• UNESCO Institute for Statistics
• Regional CERT incident reports
• Academic research on Caribbean cybersecurity
• Industry cybersecurity reports (2020-2024)

LIMITATIONS:
Data availability varies across Caribbean nations, with some smaller island states having limited reporting infrastructure. Attack data may be underreported due to limited detection capabilities and reporting mechanisms in some jurisdictions."""
    
    pdf.body_text(introduction)
    
    # ==================== SECTION 2: REGIONAL CYBERSECURITY LANDSCAPE ====================
    pdf.add_page()
    pdf.chapter_title('2. Regional Cybersecurity Landscape')
    
    section_2a = """2.1 Cyberattack Trends and Patterns

The Caribbean region has experienced a significant increase in cyberattacks over the past four years. Total reported attacks across the region increased from approximately 5,500 in 2020 to over 8,800 in 2023, representing a 60% increase.

Jamaica recorded 1,250 cyberattacks in 2023, making it the second most targeted nation in the Caribbean after the Dominican Republic (2,200 attacks). The year-over-year growth rate for Jamaica averaged 13.5%, consistent with regional trends.

The increase in attacks correlates with growing internet penetration across the region, which expanded from an average of 58% in 2020 to 68% in 2023. However, this digital expansion has not been matched by proportional increases in cybersecurity capabilities."""
    
    pdf.body_text(section_2a)
    
    # Add attack trends chart
    pdf.add_chart(os.path.join(viz_dir, '04_attack_trends.png'), 
                  'Cyberattack trends across major Caribbean nations (2020-2023)')
    
    section_2b = """2.2 Attack Type Analysis

The distribution of attack types across the Caribbean reveals concerning patterns:

• PHISHING (45-50% of attacks): The most common attack vector, exploiting human vulnerability through social engineering. Jamaica recorded 620 phishing attacks in 2023.

• RANSOMWARE (12-15% of attacks): Increasingly sophisticated attacks targeting both public and private sectors. Jamaica experienced 185 ransomware incidents.

• DISTRIBUTED DENIAL OF SERVICE (DDoS) (20-25% of attacks): Used to disrupt services and as diversion tactics. Jamaica recorded 280 DDoS attacks.

• DATA BREACHES (3-5% of attacks): Though less frequent, these have the highest potential impact. Jamaica recorded 45 data breaches.

The prevalence of phishing attacks highlights the critical importance of digital literacy and security awareness training as primary defense mechanisms."""
    
    pdf.body_text(section_2b)
    
    # Add cyberattack chart
    pdf.add_chart(os.path.join(viz_dir, '03_cyberattacks.png'),
                  'Cyberattack statistics by type and target sector across Caribbean nations')
    
    # ==================== SECTION 3: INTERNET PENETRATION ANALYSIS ====================
    pdf.add_page()
    pdf.chapter_title('3. Internet Penetration Analysis')
    
    section_3 = """3.1 Access and Connectivity

Internet penetration across the Caribbean varies significantly, ranging from 35% in Haiti to 88% in the Bahamas. Jamaica's internet penetration rate of 65% places it in the middle tier of Caribbean nations, indicating both opportunities and challenges.

Key connectivity metrics for Jamaica:
• Internet users: 65% of population (2023)
• Broadband subscriptions: 5.2 per 100 people
• Mobile subscriptions: 125 per 100 people

The high mobile subscription rate (125 per 100) indicates widespread mobile internet access, which presents both opportunities for digital inclusion and challenges for security (mobile devices are often less secured than traditional computers).

3.2 Infrastructure Gaps

Broadband infrastructure remains a critical gap across the Caribbean. Jamaica's broadband penetration of 5.2 per 100 people is below the regional leaders (Barbados: 12.3, Bahamas: 10.5) and indicates limited high-speed internet access, particularly in rural areas.

The digital divide between urban and rural areas, as well as between socioeconomic groups, creates uneven cybersecurity risk profiles. Populations with limited digital access often have lower digital literacy, making them more vulnerable to cyber threats when they do gain access."""
    
    pdf.body_text(section_3)
    
    # Add internet penetration chart
    pdf.add_chart(os.path.join(viz_dir, '01_internet_penetration.png'),
                  'Internet penetration and connectivity infrastructure across Caribbean nations')
    
    # ==================== SECTION 4: DIGITAL LITERACY ASSESSMENT ====================
    pdf.add_page()
    pdf.chapter_title('4. Digital Literacy Assessment')
    
    section_4a = """4.1 Skills and Education

Digital literacy is a critical factor in cybersecurity resilience. Populations with higher digital literacy are better equipped to recognize and avoid cyber threats such as phishing attacks and social engineering.

Jamaica's digital literacy indicators:
• Digital Literacy Score: 58/100 (below regional average of 62)
• ICT Education Access: 65% of schools with internet access
• STEM Graduates: 18% of tertiary graduates

The digital literacy score of 58/100 indicates significant gaps in the population's ability to safely navigate digital environments. This creates a large attack surface for threat actors who exploit human vulnerabilities through phishing and social engineering.

ICT education access at 65% suggests that over one-third of schools lack adequate internet connectivity for digital skills training, perpetuating the digital literacy gap.

4.2 Workforce Capacity

The cybersecurity workforce gap is one of the most critical vulnerabilities facing Jamaica and the broader Caribbean region.

Jamaica has approximately 12 cybersecurity professionals per 100,000 population, compared to regional leaders like Barbados (30/100k) and Puerto Rico (40/100k). This represents a critical capacity gap in:

• Incident response capabilities
• Security operations center staffing
• Cybersecurity policy development
• Private sector security implementation
• Critical infrastructure protection

The shortage of cybersecurity professionals limits the country's ability to detect, respond to, and recover from cyber incidents, increasing both the likelihood and impact of successful attacks."""
    
    pdf.body_text(section_4a)
    
    # Add digital literacy chart
    pdf.add_chart(os.path.join(viz_dir, '02_digital_literacy.png'),
                  'Digital literacy and workforce capacity indicators across Caribbean nations')
    
    # ==================== SECTION 5: JAMAICA RISK PROFILE ====================
    pdf.add_page()
    pdf.chapter_title('5. Jamaica Risk Profile')
    
    section_5a = f"""5.1 Composite Risk Assessment

Jamaica's overall cybersecurity risk assessment reveals a HIGH RISK profile with a composite risk index of {jamaica_risk['risk_index']:.2f}/10, ranking the country {int(jamaica_rank)} out of 17 Caribbean nations analyzed.

RISK COMPONENT BREAKDOWN:

• Exposure Score: {jamaica_risk['exposure_score']:.2f}/10
  Jamaica's 65% internet penetration creates a moderate attack surface. As internet access continues to expand, this exposure will increase, requiring proportional increases in security capabilities.

• Vulnerability Score: {jamaica_risk['vulnerability_score']:.2f}/10
  This is Jamaica's highest risk component, driven by digital literacy gaps (58/100) and limited cybersecurity workforce (12/100k). This represents the most critical area for intervention.

• Threat Score: {jamaica_risk['threat_score']:.2f}/10
  With 1,250 attacks in 2023, Jamaica faces significant active threats. The 47% increase in attacks since 2020 indicates escalating targeting by cybercriminals.

The vulnerability component carries the highest weight (40%) in the risk calculation, reflecting the critical importance of human factors and workforce capacity in cybersecurity defense."""
    
    pdf.body_text(section_5a)
    
    # Add risk assessment chart
    pdf.add_chart(os.path.join(viz_dir, '05_risk_assessment.png'),
                  'Composite cybersecurity risk index and component analysis')
    
    section_5b = """5.2 Sector-Specific Vulnerabilities

CRITICAL INFRASTRUCTURE:
Jamaica experienced 35 attacks on critical infrastructure in 2023. This includes attacks on:
• Energy and utilities systems
• Transportation networks
• Healthcare systems
• Government services
• Financial infrastructure

The targeting of critical infrastructure poses significant risks to national security and public safety.

FINANCIAL SECTOR:
With 85 attacks recorded, the financial sector is a primary target. This includes:
• Banking systems
• Payment processors
• Insurance companies
• Investment firms

Financial sector attacks not only cause direct financial losses but also undermine confidence in the digital economy.

PUBLIC SECTOR:
Government agencies face increasing cyber threats, including:
• Data breaches of citizen information
• Ransomware attacks on government systems
• Disruption of public services

5.3 Comparative Regional Analysis

Jamaica's risk profile compared to regional peers:

HIGHER RISK COUNTRIES:
• Haiti (Critical risk) - Limited infrastructure but high vulnerability
• Dominican Republic (Critical risk) - High attack volume due to larger digital economy

SIMILAR RISK COUNTRIES:
• Guyana, Belize, Suriname - Similar development levels and cybersecurity challenges

LOWER RISK COUNTRIES:
• Barbados, Bahamas, Trinidad & Tobago - Better digital literacy and cybersecurity workforce
• Puerto Rico - Strong cybersecurity infrastructure (US territory)

Jamaica's position as the second most attacked nation in the Caribbean, combined with below-average digital literacy and cybersecurity workforce capacity, places it at elevated risk compared to most regional peers."""
    
    pdf.body_text(section_5b)
    
    # Add Jamaica dashboard
    pdf.add_chart(os.path.join(viz_dir, '06_jamaica_dashboard.png'),
                  'Comprehensive Jamaica cybersecurity risk dashboard')
    
    # ==================== SECTION 6: POLICY RECOMMENDATIONS ====================
    pdf.add_page()
    pdf.chapter_title('6. Policy Recommendations')
    
    section_6a = """6.1 Immediate Actions (0-6 months)

PRIORITY 1: Establish National Cybersecurity Coordination
• Designate a National Cybersecurity Coordinator with authority across government agencies
• Establish a 24/7 Computer Emergency Response Team (CERT) operations center
• Develop incident reporting protocols for critical infrastructure operators

PRIORITY 2: Critical Infrastructure Protection
• Conduct immediate cybersecurity assessments of all critical infrastructure
• Implement minimum security standards for energy, water, telecommunications, and financial systems
• Establish information sharing mechanisms between government and critical infrastructure operators

PRIORITY 3: Public Awareness Campaign
• Launch national cybersecurity awareness campaign targeting phishing and social engineering
• Develop educational materials for businesses and citizens
• Establish a national cybersecurity hotline for incident reporting

PRIORITY 4: Incident Response Preparedness
• Develop national incident response playbooks
• Conduct tabletop exercises with government agencies and critical infrastructure
• Establish mutual assistance agreements with regional CERTs

6.2 Medium-Term Initiatives (6-18 months)

WORKFORCE DEVELOPMENT:
• Establish cybersecurity training programs at universities and technical colleges
• Create scholarship programs for cybersecurity education
• Develop apprenticeship programs with private sector partners
• Target: Increase cybersecurity workforce to 25 professionals per 100k population

DIGITAL LITERACY:
• Integrate cybersecurity education into national school curriculum
• Launch adult digital literacy programs with security focus
• Partner with private sector for workplace cybersecurity training
• Target: Improve digital literacy score from 58 to 70/100

REGULATORY FRAMEWORK:
• Enact comprehensive cybersecurity legislation
• Establish data protection and privacy regulations
• Create mandatory breach notification requirements
• Develop sector-specific cybersecurity regulations for financial services and critical infrastructure"""
    
    pdf.body_text(section_6a)
    
    section_6b = """6.3 Long-Term Strategic Goals (18+ months)

NATIONAL CYBERSECURITY STRATEGY:
• Develop and implement a comprehensive National Cybersecurity Strategy
• Establish dedicated funding for cybersecurity initiatives (target: 0.5% of national budget)
• Create public-private partnership frameworks for cybersecurity

INFRASTRUCTURE INVESTMENT:
• Expand broadband infrastructure to achieve 80% penetration
• Implement secure government cloud services
• Modernize critical infrastructure with security-by-design principles

REGIONAL LEADERSHIP:
• Position Jamaica as a regional cybersecurity hub
• Host regional cybersecurity exercises and training
• Contribute to Caribbean cybersecurity policy development

ECONOMIC OPPORTUNITY:
• Develop cybersecurity services export industry
• Create incentives for cybersecurity companies to establish operations
• Build cybersecurity research and development capabilities

SUCCESS METRICS:
• Reduce successful phishing attacks by 50% within 3 years
• Increase cybersecurity workforce to 30/100k within 5 years
• Achieve digital literacy score of 75/100 within 5 years
• Reduce mean time to detect/respond to incidents by 75%"""
    
    pdf.body_text(section_6b)
    
    # ==================== SECTION 7: REGIONAL COOPERATION ====================
    pdf.add_page()
    pdf.chapter_title('7. Regional Cooperation Opportunities')
    
    section_7 = """The transnational nature of cyber threats requires coordinated regional responses. Jamaica should pursue the following regional cooperation initiatives:

CARICOM CYBERSECURITY INITIATIVES:
• Strengthen the CARICOM Cybersecurity Centre of Excellence
• Establish regional threat intelligence sharing platform
• Coordinate cybersecurity policy development across member states
• Develop regional cybersecurity certification standards

JOINT CAPABILITIES:
• Establish regional cybersecurity exercise program
• Create mutual assistance agreements for incident response
• Develop shared cybersecurity training facilities
• Pool resources for advanced cybersecurity tools and platforms

INTERNATIONAL PARTNERSHIPS:
• Engage with international cybersecurity organizations (FIRST, OAS-CICTE)
• Partner with developed nations for capacity building programs
• Participate in international cybersecurity information sharing networks
• Access international cybersecurity funding and technical assistance

PUBLIC-PRIVATE PARTNERSHIPS:
• Engage regional telecommunications providers in security initiatives
• Partner with international cybersecurity vendors for training and tools
• Collaborate with regional financial institutions on security standards
• Create cybersecurity industry association for knowledge sharing

CROSS-BORDER INCIDENT RESPONSE:
• Establish protocols for cross-border cybercrime investigation
• Create regional cybersecurity incident database
• Develop mutual legal assistance frameworks for cybercrime
• Coordinate with regional law enforcement agencies"""
    
    pdf.body_text(section_7)
    
    # ==================== SECTION 8: CONCLUSION ====================
    pdf.add_page()
    pdf.chapter_title('8. Conclusion')
    
    conclusion = f"""Jamaica faces significant cybersecurity challenges that require immediate attention and sustained investment. With a HIGH RISK rating and a composite risk index of {jamaica_risk['risk_index']:.2f}/10, the country is vulnerable to increasing cyber threats.

The analysis reveals three critical vulnerability areas:

1. DIGITAL LITERACY GAP: Jamaica's digital literacy score of 58/100 creates a large attack surface for social engineering and phishing attacks. This is the single most important factor driving Jamaica's cybersecurity risk.

2. CYBERSECURITY WORKFORCE SHORTAGE: With only 12 cybersecurity professionals per 100,000 population, Jamaica lacks the human capacity to effectively detect, prevent, and respond to cyber threats.

3. ESCALATING THREAT LANDSCAPE: The 47% increase in cyberattacks since 2020, combined with 1,250 attacks in 2023, indicates that Jamaica is being actively targeted by cybercriminals.

However, these challenges also present opportunities. By investing in digital literacy education, cybersecurity workforce development, and critical infrastructure protection, Jamaica can significantly reduce its risk profile.

The policy recommendations in this report provide a roadmap for building cybersecurity resilience. Implementation of the immediate actions within 6 months, followed by medium and long-term initiatives, can reduce Jamaica's risk index by 30-40% within 5 years.

Regional cooperation will be essential, as cyber threats do not respect national boundaries. Jamaica should work with CARICOM partners and international allies to build collective cybersecurity capabilities.

The cost of inaction is too high. Cyberattacks on critical infrastructure, financial systems, or government services could cause significant economic damage and undermine public trust. Proactive investment in cybersecurity is not just a technical necessity but a national security imperative.

With committed leadership, adequate resources, and sustained effort, Jamaica can transform its cybersecurity posture from a position of vulnerability to one of regional leadership and resilience."""
    
    pdf.body_text(conclusion)
    
    # ==================== APPENDICES ====================
    pdf.add_page()
    pdf.chapter_title('Appendices')
    
    appendix_a = """APPENDIX A: Data Tables

A1. Internet Penetration Data (2023)
"""
    pdf.body_text(appendix_a)
    
    # Add data table
    pdf.set_font('Arial', '', 9)
    
    # Internet data table
    col_widths = [45, 25, 25, 25, 25]
    headers = ['Country', 'Internet %', 'Broadband/100', 'Mobile/100', 'GDP/capita']
    
    # Table header
    pdf.set_font('Arial', 'B', 9)
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, 1, 0, 'C')
    pdf.ln()
    
    # Table data
    pdf.set_font('Arial', '', 8)
    for _, row in df_internet.iterrows():
        pdf.cell(col_widths[0], 7, str(row['country'])[:20], 1, 0, 'L')
        pdf.cell(col_widths[1], 7, f"{row['internet_users_pct_2023']:.1f}%", 1, 0, 'C')
        pdf.cell(col_widths[2], 7, f"{row['broadband_per_100']:.1f}", 1, 0, 'C')
        pdf.cell(col_widths[3], 7, f"{row['mobile_subs_per_100']:.0f}", 1, 0, 'C')
        pdf.cell(col_widths[4], 7, f"${row['gdp_per_capita_usd']:,.0f}", 1, 0, 'C')
        pdf.ln()
    
    pdf.ln(10)
    
    appendix_b = """A2. Risk Index Rankings
"""
    pdf.body_text(appendix_b)
    
    # Risk table
    pdf.set_font('Arial', 'B', 9)
    risk_headers = ['Rank', 'Country', 'Risk Index', 'Risk Level', 'Vulnerability']
    for i, header in enumerate(risk_headers):
        pdf.cell(38, 8, header, 1, 0, 'C')
    pdf.ln()
    
    pdf.set_font('Arial', '', 8)
    df_risk_sorted = df_risk.sort_values('risk_index', ascending=False).reset_index(drop=True)
    for i, row in df_risk_sorted.iterrows():
        pdf.cell(38, 7, f"{i+1}", 1, 0, 'C')
        pdf.cell(38, 7, str(row['country'])[:18], 1, 0, 'L')
        pdf.cell(38, 7, f"{row['risk_index']:.2f}", 1, 0, 'C')
        pdf.cell(38, 7, row['risk_level'], 1, 0, 'C')
        pdf.cell(38, 7, f"{row['vulnerability_score']:.2f}", 1, 0, 'C')
        pdf.ln()
    
    pdf.ln(10)
    
    appendix_c = """A3. Cyberattack Statistics (2023)
"""
    pdf.body_text(appendix_c)
    
    # Attacks table - use 2024 data with updated column names
    pdf.set_font('Arial', 'B', 9)
    attack_headers = ['Country', 'Total', 'Phishing', 'Ransomware', 'DDoS']
    for i, header in enumerate(attack_headers):
        pdf.cell(38, 8, header, 1, 0, 'C')
    pdf.ln()
    
    pdf.set_font('Arial', '', 8)
    for _, row in df_attacks.iterrows():
        pdf.cell(38, 7, str(row['country'])[:18], 1, 0, 'L')
        pdf.cell(38, 7, f"{row['total_attacks_2024']:,}", 1, 0, 'C')
        pdf.cell(38, 7, f"{row['phishing_attacks_2024']:,}", 1, 0, 'C')
        pdf.cell(38, 7, f"{row['ransomware_attacks_2024']:,}", 1, 0, 'C')
        pdf.cell(38, 7, f"{row['ddos_attacks_2024']:,}", 1, 0, 'C')
        pdf.ln()
    
    pdf.ln(10)
    
    appendix_d = """A4. Methodology Details

RISK INDEX CALCULATION:
The cybersecurity risk index is calculated using a weighted composite methodology that combines three dimensions:

1. EXPOSURE (25% weight):
   - Internet penetration rate (% of population)
   - Normalized to 0-10 scale
   - Higher penetration = larger attack surface

2. VULNERABILITY (40% weight):
   - Digital literacy score (inverse - lower = more vulnerable)
   - Cybersecurity workforce per capita (inverse)
   - Weighted 60% literacy, 40% workforce
   - Normalized to 0-10 scale

3. THREAT (35% weight):
   - Total cyberattacks (normalized to regional max)
   - Reflects active targeting by threat actors
   - Normalized to 0-10 scale

RISK LEVEL CLASSIFICATION:
   - Critical: Risk Index >= 7.0
   - High: Risk Index 5.5 - 6.99
   - Medium: Risk Index 4.0 - 5.49
   - Low: Risk Index < 4.0

DATA QUALITY NOTES:
- Data represents best available estimates from multiple sources
- Some smaller Caribbean nations have limited reporting
- Attack data may be underreported in some jurisdictions
- All monetary values in USD"""
    
    pdf.body_text(appendix_d)
    
    # Save the PDF
    report_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'report')
    os.makedirs(report_dir, exist_ok=True)
    
    report_path = os.path.join(report_dir, 'Caribbean_Cybersecurity_Risk_Assessment_Jamaica.pdf')
    pdf.output(report_path)
    
    print(f"\nPolicy report generated: {report_path}")
    print(f"Total pages: {pdf.page_no()}")
    return report_path


if __name__ == "__main__":
    generate_report()