

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# Set style for professional reports
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")

# Custom colors for consistency
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'tertiary': '#F18F01',
    'quaternary': '#C73E1D',
    'jamaica': '#009B3A',
    'high_risk': '#D32F2F',
    'medium_risk': '#F57C00',
    'low_risk': '#388E3C',
    'critical_risk': '#B71C1C'
}


def create_internet_penetration_chart(df_internet, output_dir):
    """Create internet penetration comparison chart"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Internet Penetration Across Caribbean Nations (2024)', fontsize=18, fontweight='bold')
    
    df_sorted = df_internet.sort_values('internet_users_pct_2024', ascending=True)
    
    # Chart 1: Internet Users % (Horizontal Bar)
    ax1 = axes[0, 0]
    colors = [COLORS['jamaica'] if c == 'Jamaica' else COLORS['primary'] for c in df_sorted['country']]
    bars = ax1.barh(df_sorted['country'], df_sorted['internet_users_pct_2024'], color=colors)
    ax1.set_xlabel('Internet Users (% of Population)')
    ax1.set_title('Internet Penetration by Country (2024)', fontweight='bold')
    ax1.axvline(x=df_sorted[df_sorted['country'] == 'Jamaica']['internet_users_pct_2024'].values[0], 
                color='red', linestyle='--', alpha=0.7, label='Jamaica (68.5%)')
    ax1.legend()
    
    # Chart 2: Broadband vs Mobile Subscriptions
    ax2 = axes[0, 1]
    x = np.arange(len(df_sorted['country']))
    width = 0.35
    ax2.bar(x - width/2, df_sorted['broadband_per_100'], width, label='Broadband (per 100)', color=COLORS['primary'])
    ax2.bar(x + width/2, df_sorted['mobile_subs_per_100'], width, label='Mobile (per 100)', color=COLORS['secondary'])
    ax2.set_ylabel('Subscriptions per 100 People')
    ax2.set_title('Connectivity Infrastructure', fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_sorted['country'], rotation=45, ha='right', fontsize=8)
    ax2.legend()
    
    # Chart 3: Internet Growth (2020 vs 2024)
    ax3 = axes[1, 0]
    growth = df_sorted['internet_users_pct_2024'] - df_sorted['internet_users_pct_2020']
    colors_growth = [COLORS['jamaica'] if c == 'Jamaica' else COLORS['tertiary'] if g > 0 else COLORS['quaternary'] 
                     for c, g in zip(df_sorted['country'], growth)]
    bars = ax3.bar(df_sorted['country'], growth, color=colors_growth)
    ax3.set_ylabel('Percentage Point Change')
    ax3.set_title('Internet Penetration Growth (2020-2024)', fontweight='bold')
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Chart 4: GDP vs Internet Penetration Scatter
    ax4 = axes[1, 1]
    for _, row in df_sorted.iterrows():
        color = COLORS['jamaica'] if row['country'] == 'Jamaica' else COLORS['primary']
        ax4.scatter(row['gdp_per_capita_usd'], row['internet_users_pct_2024'], 
                   color=color, s=100, alpha=0.7, edgecolors='black')
        ax4.annotate(row['country'][:3], (row['gdp_per_capita_usd'], row['internet_users_pct_2024']), 
                    fontsize=7, ha='left')
    ax4.set_xlabel('GDP per Capita (USD)')
    ax4.set_ylabel('Internet Users (%)')
    ax4.set_title('Economic Development vs Internet Access', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '01_internet_penetration.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 01_internet_penetration.png")


def create_digital_literacy_chart(df_literacy, output_dir):
    """Create digital literacy comparison charts"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Digital Literacy & Workforce Readiness (2024)', fontsize=18, fontweight='bold')
    
    df_sorted = df_literacy.sort_values('digital_literacy_score', ascending=True)
    
    # Chart 1: Digital Literacy Score
    ax1 = axes[0, 0]
    colors = [COLORS['jamaica'] if c == 'Jamaica' else COLORS['primary'] for c in df_sorted['country']]
    bars = ax1.barh(df_sorted['country'], df_sorted['digital_literacy_score'], color=colors)
    ax1.set_xlabel('Digital Literacy Score (0-100)')
    ax1.set_title('Digital Literacy Index', fontweight='bold')
    ax1.axvline(x=df_sorted[df_sorted['country'] == 'Jamaica']['digital_literacy_score'].values[0], 
                color='red', linestyle='--', alpha=0.7, label='Jamaica')
    ax1.legend()
    
    # Chart 2: ICT Education Access
    ax2 = axes[0, 1]
    colors = [COLORS['jamaica'] if c == 'Jamaica' else COLORS['secondary'] for c in df_sorted['country']]
    bars = ax2.barh(df_sorted['country'], df_sorted['ict_education_access'], color=colors)
    ax2.set_xlabel('% of Schools with Internet Access')
    ax2.set_title('ICT Education Infrastructure', fontweight='bold')
    ax2.axvline(x=df_sorted[df_sorted['country'] == 'Jamaica']['ict_education_access'].values[0], 
                color='red', linestyle='--', alpha=0.7, label='Jamaica')
    ax2.legend()
    
    # Chart 3: Cybersecurity Workforce
    ax3 = axes[1, 0]
    colors = [COLORS['jamaica'] if c == 'Jamaica' else COLORS['quaternary'] for c in df_sorted['country']]
    bars = ax3.barh(df_sorted['country'], df_sorted['cybersecurity_workforce_per_100k'], color=colors)
    ax3.set_xlabel('Cybersecurity Professionals per 100k')
    ax3.set_title('Cybersecurity Workforce Capacity', fontweight='bold')
    ax3.axvline(x=df_sorted[df_sorted['country'] == 'Jamaica']['cybersecurity_workforce_per_100k'].values[0], 
                color='red', linestyle='--', alpha=0.7, label='Jamaica (15.2/100k)')
    ax3.legend()
    
    # Chart 4: Cyber Hygiene & Online Safety
    ax4 = axes[1, 1]
    x = np.arange(len(df_sorted['country']))
    width = 0.35
    ax4.bar(x - width/2, df_sorted['cyber_hygiene_score'], width, label='Cyber Hygiene', color=COLORS['primary'])
    ax4.bar(x + width/2, df_sorted['online_safety_awareness'], width, label='Online Safety', color=COLORS['secondary'])
    ax4.set_ylabel('Score (0-100)')
    ax4.set_title('Security Awareness Metrics', fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(df_sorted['country'], rotation=45, ha='right', fontsize=8)
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '02_digital_literacy.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 02_digital_literacy.png")


def create_cyberattack_chart(df_attacks, output_dir):
    """Create cyberattack statistics charts"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Cyberattack Landscape in the Caribbean (2024)', fontsize=18, fontweight='bold')
    
    df_sorted = df_attacks.sort_values('total_attacks_2024', ascending=True)
    
    # Chart 1: Total Attacks
    ax1 = axes[0, 0]
    colors = [COLORS['jamaica'] if c == 'Jamaica' else COLORS['high_risk'] for c in df_sorted['country']]
    bars = ax1.barh(df_sorted['country'], df_sorted['total_attacks_2024'], color=colors)
    ax1.set_xlabel('Total Cyberattacks')
    ax1.set_title('Total Cyberattacks by Country (2024)', fontweight='bold')
    ax1.axvline(x=df_sorted[df_sorted['country'] == 'Jamaica']['total_attacks_2024'].values[0], 
                color='red', linestyle='--', alpha=0.7, label='Jamaica (1,425)')
    ax1.legend()
    
    # Chart 2: Attack Types Breakdown (Stacked Bar)
    ax2 = axes[0, 1]
    attack_types = ['phishing_attacks_2024', 'ransomware_attacks_2024', 'ddos_attacks_2024', 'data_breaches_2024']
    attack_labels = ['Phishing', 'Ransomware', 'DDoS', 'Data Breaches']
    attack_colors = [COLORS['primary'], COLORS['secondary'], COLORS['tertiary'], COLORS['quaternary']]
    
    bottom = np.zeros(len(df_sorted))
    for i, (attack_type, color) in enumerate(zip(attack_types, attack_colors)):
        ax2.barh(df_sorted['country'], df_sorted[attack_type], left=bottom, label=attack_labels[i], color=color)
        bottom += df_sorted[attack_type].values
    
    ax2.set_xlabel('Number of Attacks')
    ax2.set_title('Attack Type Distribution (2024)', fontweight='bold')
    ax2.legend(loc='lower right')
    
    # Chart 3: Critical Infrastructure Attacks
    ax3 = axes[1, 0]
    colors = [COLORS['jamaica'] if c == 'Jamaica' else COLORS['critical_risk'] for c in df_sorted['country']]
    bars = ax3.barh(df_sorted['country'], df_sorted['critical_infra_attacks_2024'], color=colors)
    ax3.set_xlabel('Attacks on Critical Infrastructure')
    ax3.set_title('Critical Infrastructure Targeting (2024)', fontweight='bold')
    ax3.axvline(x=df_sorted[df_sorted['country'] == 'Jamaica']['critical_infra_attacks_2024'].values[0], 
                color='red', linestyle='--', alpha=0.7, label='Jamaica (42)')
    ax3.legend()
    
    # Chart 4: Attack Cost & Data Exposed
    ax4 = axes[1, 1]
    x = np.arange(len(df_sorted['country']))
    width = 0.35
    ax4.bar(x - width/2, df_sorted['avg_attack_cost_usd'] / 1000, width, label='Avg Cost ($K)', color=COLORS['high_risk'])
    ax4.bar(x + width/2, df_sorted['data_exposed_records'] / 1000, width, label='Data Exposed (K records)', color=COLORS['medium_risk'])
    ax4.set_ylabel('Value (thousands)')
    ax4.set_title('Economic Impact of Attacks', fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(df_sorted['country'], rotation=45, ha='right', fontsize=8)
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '03_cyberattacks.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 03_cyberattacks.png")


def create_attack_trends_chart(df_trends, output_dir):
    """Create attack trends over time"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    countries = [col for col in df_trends.columns if col != 'year']
    colors_list = [COLORS['jamaica'], COLORS['primary'], COLORS['secondary'], 
                   COLORS['tertiary'], COLORS['quaternary'], COLORS['high_risk'], COLORS['medium_risk']]
    
    for i, country in enumerate(countries):
        color = colors_list[i % len(colors_list)]
        linewidth = 3 if country == 'Jamaica' else 2
        ax.plot(df_trends['year'], df_trends[country], marker='o', label=country.replace('_', ' '), 
               color=color, linewidth=linewidth)
    
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Cyberattacks', fontsize=12)
    ax.set_title('Cyberattack Trends (2020-2024)', fontsize=16, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_attack_trends.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 04_attack_trends.png")


def create_risk_index_chart(df_risk, output_dir):
    """Create risk index visualization"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Caribbean Cybersecurity Risk Assessment (2024)', fontsize=18, fontweight='bold')
    
    df_sorted = df_risk.sort_values('risk_index', ascending=True)
    
    # Chart 1: Overall Risk Index
    ax1 = axes[0, 0]
    risk_colors = []
    for _, row in df_sorted.iterrows():
        if row['risk_level'] == 'Critical':
            risk_colors.append(COLORS['critical_risk'])
        elif row['risk_level'] == 'High':
            risk_colors.append(COLORS['high_risk'])
        elif row['risk_level'] == 'Medium':
            risk_colors.append(COLORS['medium_risk'])
        else:
            risk_colors.append(COLORS['low_risk'])
    
    risk_colors = [COLORS['jamaica'] if c == 'Jamaica' else rc for c, rc in zip(df_sorted['country'], risk_colors)]
    
    bars = ax1.barh(df_sorted['country'], df_sorted['risk_index'], color=risk_colors)
    ax1.set_xlabel('Risk Index (0-10)')
    ax1.set_title('Composite Cybersecurity Risk Index', fontweight='bold')
    ax1.axvline(x=df_sorted[df_sorted['country'] == 'Jamaica']['risk_index'].values[0], 
                color='red', linestyle='--', alpha=0.7, label=f'Jamaica ({df_sorted[df_sorted["country"]=="Jamaica"]["risk_index"].values[0]:.2f})')
    ax1.legend()
    
    # Add risk level text
    for i, (country, level) in enumerate(zip(df_sorted['country'], df_sorted['risk_level'])):
        ax1.text(df_sorted[df_sorted['country'] == country]['risk_index'].values[0] + 0.1, 
                i, f' ({level})', va='center', fontsize=8, fontstyle='italic')
    
    # Chart 2: Risk Components
    ax2 = axes[0, 1]
    components = ['exposure_score', 'vulnerability_score', 'threat_score', 'policy_gap_score']
    component_labels = ['Exposure\n(Internet)', 'Vulnerability\n(Literacy)', 'Threat\n(Attacks)', 'Policy\nGap']
    
    jamaica_data = df_risk[df_risk['country'] == 'Jamaica'].iloc[0]
    regional_avg = df_risk[components].mean()
    
    x = np.arange(len(components))
    width = 0.35
    ax2.bar(x - width/2, [jamaica_data[c] for c in components], width, label='Jamaica', color=COLORS['jamaica'], alpha=0.8)
    ax2.bar(x + width/2, regional_avg.values, width, label='Regional Average', color=COLORS['primary'], alpha=0.8)
    ax2.set_ylabel('Score (0-10)')
    ax2.set_title('Risk Component Comparison', fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(component_labels, fontsize=9)
    ax2.legend()
    
    # Chart 3: Attack Growth Rate
    ax3 = axes[1, 0]
    colors = [COLORS['jamaica'] if c == 'Jamaica' else COLORS['critical_risk'] if g > 10 else COLORS['high_risk'] 
              for c, g in zip(df_sorted['country'], df_sorted['attack_growth_rate'])]
    bars = ax3.barh(df_sorted['country'], df_sorted['attack_growth_rate'], color=colors)
    ax3.set_xlabel('Attack Growth Rate (%)')
    ax3.set_title('Year-over-Year Attack Growth (2023-2024)', fontweight='bold')
    ax3.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
    
    # Chart 4: Ransomware Risk
    ax4 = axes[1, 1]
    colors = [COLORS['jamaica'] if c == 'Jamaica' else COLORS['critical_risk'] for c in df_sorted['country']]
    bars = ax4.barh(df_sorted['country'], df_sorted['ransomware_risk'], color=colors)
    ax4.set_xlabel('Ransomware Risk Score (0-10)')
    ax4.set_title('Ransomware Attack Risk', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '05_risk_assessment.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 05_risk_assessment.png")


def create_jamaica_dashboard(df_internet, df_literacy, df_attacks, df_risk, output_dir):
    """Create a focused dashboard on Jamaica's risk profile"""
    fig = plt.figure(figsize=(20, 14))
    fig.suptitle('JAMAICA CYBERSECURITY RISK DASHBOARD (2024)', fontsize=20, fontweight='bold', y=0.98)
    
    # Get Jamaica data
    jamaica_internet = df_internet[df_internet['country'] == 'Jamaica'].iloc[0]
    jamaica_literacy = df_literacy[df_literacy['country'] == 'Jamaica'].iloc[0]
    jamaica_attacks = df_attacks[df_attacks['country'] == 'Jamaica'].iloc[0]
    jamaica_risk = df_risk[df_risk['country'] == 'Jamaica'].iloc[0]
    
    # Get regional averages for comparison
    regional_avg_attacks = df_attacks['total_attacks_2024'].mean()
    regional_avg_literacy = df_literacy['digital_literacy_score'].mean()
    regional_avg_internet = df_internet['internet_users_pct_2024'].mean()
    
    # Subplot 1: Key Metrics Summary
    ax1 = plt.subplot2grid((4, 4), (0, 0), colspan=2, rowspan=2)
    ax1.axis('off')
    
    metrics_text = f"""
    JAMAICA CYBERSECURITY PROFILE (2024)
    
    Risk Level: {jamaica_risk['risk_level'].upper()}
    Risk Index: {jamaica_risk['risk_index']:.2f} / 10
    Regional Rank: 2 of 17 countries
    
    KEY INDICATORS:
    - Internet Penetration:    {jamaica_internet['internet_users_pct_2024']:.1f}%  (Reg. avg: {regional_avg_internet:.0f}%)
    - Digital Literacy Score:  {jamaica_literacy['digital_literacy_score']:.1f}/100 (Reg. avg: {regional_avg_literacy:.0f}/100)
    - Cybersecurity Workforce: {jamaica_literacy['cybersecurity_workforce_per_100k']:.1f}/100k (Reg. max: {df_literacy['cybersecurity_workforce_per_100k'].max():.1f}/100k)
    
    THREAT METRICS:
    - Total Cyberattacks:      {jamaica_attacks['total_attacks_2024']:,}  (Reg. avg: {regional_avg_attacks:.0f})
    - Ransomware Attacks:      {jamaica_attacks['ransomware_attacks_2024']}
    - Phishing Attacks:        {jamaica_attacks['phishing_attacks_2024']}
    - Critical Infrastructure: {jamaica_attacks['critical_infra_attacks_2024']}
    - Avg Attack Cost:         ${jamaica_attacks['avg_attack_cost_usd']:,.0f}
    - YoY Attack Growth:       {jamaica_risk['attack_growth_rate']:+.1f}%
    """
    ax1.text(0.02, 0.98, metrics_text, transform=ax1.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # Subplot 2: Attack Type Distribution (Pie Chart)
    ax2 = plt.subplot2grid((4, 4), (0, 2), colspan=2, rowspan=1)
    attack_types = ['Phishing', 'DDoS', 'Ransomware', 'Data Breaches', 'Other']
    attack_values = [
        jamaica_attacks['phishing_attacks_2024'],
        jamaica_attacks['ddos_attacks_2024'],
        jamaica_attacks['ransomware_attacks_2024'],
        jamaica_attacks['data_breaches_2024'],
        jamaica_attacks['total_attacks_2024'] - jamaica_attacks['phishing_attacks_2024'] - 
        jamaica_attacks['ddos_attacks_2024'] - jamaica_attacks['ransomware_attacks_2024'] - jamaica_attacks['data_breaches_2024']
    ]
    colors_pie = [COLORS['primary'], COLORS['secondary'], COLORS['critical_risk'], COLORS['quaternary'], COLORS['tertiary']]
    ax2.pie(attack_values, labels=attack_types, autopct='%1.1f%%', colors=colors_pie, startangle=90)
    ax2.set_title('Attack Type Distribution (2024)', fontweight='bold')
    
    # Subplot 3: Risk Component Breakdown
    ax3 = plt.subplot2grid((4, 4), (1, 2), colspan=2, rowspan=1)
    components = ['Exposure', 'Vulnerability', 'Threat', 'Policy Gap']
    scores = [jamaica_risk['exposure_score'], jamaica_risk['vulnerability_score'], 
              jamaica_risk['threat_score'], jamaica_risk['policy_gap_score']]
    weights = [0.20, 0.35, 0.30, 0.15]
    
    bars = ax3.bar(components, scores, color=[COLORS['primary'], COLORS['high_risk'], COLORS['secondary'], COLORS['medium_risk']])
    ax3.set_ylabel('Score (0-10)')
    ax3.set_title('Risk Component Analysis', fontweight='bold')
    for bar, weight in zip(bars, weights):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'Weight: {weight:.0%}', ha='center', va='bottom', fontsize=9)
    
    # Subplot 4: Regional Comparison
    ax4 = plt.subplot2grid((4, 4), (2, 0), colspan=2, rowspan=1)
    categories = ['Internet\nPenetration', 'Digital\nLiteracy', 'ICT Education', 'Cyber\nWorkforce', 'Cyber\nHygiene']
    jamaica_scores = [
        jamaica_internet['internet_users_pct_2024'] / 100 * 10,
        jamaica_literacy['digital_literacy_score'] / 10,
        jamaica_literacy['ict_education_access'] / 10,
        jamaica_literacy['cybersecurity_workforce_per_100k'] / 4,
        jamaica_literacy['cyber_hygiene_score'] / 10
    ]
    regional_scores = [
        regional_avg_internet / 100 * 10,
        regional_avg_literacy / 10,
        df_literacy['ict_education_access'].mean() / 10,
        df_literacy['cybersecurity_workforce_per_100k'].mean() / 4,
        df_literacy['cyber_hygiene_score'].mean() / 10
    ]
    
    x = np.arange(len(categories))
    width = 0.35
    ax4.bar(x - width/2, jamaica_scores, width, label='Jamaica', color=COLORS['jamaica'], alpha=0.8)
    ax4.bar(x + width/2, regional_scores, width, label='Regional Avg', color=COLORS['primary'], alpha=0.8)
    ax4.set_ylabel('Normalized Score (0-10)')
    ax4.set_title('Jamaica vs Regional Average', fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(categories, fontsize=8)
    ax4.legend()
    ax4.set_ylim(0, 11)
    
    # Subplot 5: Attack Trend for Jamaica
    ax5 = plt.subplot2grid((4, 4), (2, 2), colspan=2, rowspan=1)
    years = [2020, 2021, 2022, 2023, 2024]
    jamaica_trend = [850, 1050, 1180, 1250, 1425]
    ax5.plot(years, jamaica_trend, marker='o', color=COLORS['jamaica'], linewidth=3, markersize=8)
    ax5.fill_between(years, jamaica_trend, alpha=0.2, color=COLORS['jamaica'])
    ax5.set_xlabel('Year')
    ax5.set_ylabel('Number of Attacks')
    ax5.set_title('Jamaica Attack Trend', fontweight='bold')
    ax5.grid(True, alpha=0.3)
    
    growth_rate = ((jamaica_trend[-1] - jamaica_trend[0]) / jamaica_trend[0]) * 100
    ax5.text(2023, jamaica_trend[-1] + 30, f'+{growth_rate:.0f}% (2020-2024)', 
            fontsize=10, fontweight='bold', color=COLORS['critical_risk'])
    
    # Subplot 6: Risk Level Comparison
    ax6 = plt.subplot2grid((4, 4), (3, 0), colspan=4, rowspan=1)
    ax6.axis('off')
    
    risk_comparison = df_risk[['country', 'risk_index', 'risk_level', 'attack_growth_rate']].sort_values('risk_index', ascending=False)
    
    table_text = "REGIONAL RISK COMPARISON (2024):\n"
    table_text += "=" * 85 + "\n"
    table_text += f"{'Rank':<6}{'Country':<28}{'Risk Index':<14}{'Risk Level':<12}{'Growth':<12}\n"
    table_text += "-" * 85 + "\n"
    
    for i, (_, row) in enumerate(risk_comparison.iterrows(), 1):
        jamaica_highlight = ">>>" if row['country'] == 'Jamaica' else "   "
        table_text += f"{jamaica_highlight} {i:<5}{row['country']:<28}{row['risk_index']:<14.2f}{row['risk_level']:<12}{row['attack_growth_rate']:+.1f}%\n"
    
    table_text += "=" * 85 + "\n"
    table_text += f"\nJAMAICA RANKING: {list(risk_comparison['country']).index('Jamaica') + 1} out of {len(risk_comparison)} countries"
    table_text += f"\nJamaica's risk index ({jamaica_risk['risk_index']:.2f}) is {'ABOVE' if jamaica_risk['risk_index'] > df_risk['risk_index'].mean() else 'BELOW'} regional average ({df_risk['risk_index'].mean():.2f})"
    
    ax6.text(0.02, 0.95, table_text, transform=ax6.transAxes, fontsize=9,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '06_jamaica_dashboard.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  Created: 06_jamaica_dashboard.png")


def create_all_visualizations(data_dir=None):
    """Main function to create all visualizations"""
    print("\n" + "=" * 70)
    print("  GENERATING VISUALIZATIONS")
    print("=" * 70)
    
    # Load data
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed')
    
    df_internet = pd.read_csv(os.path.join(data_dir, 'internet_penetration.csv'))
    df_literacy = pd.read_csv(os.path.join(data_dir, 'digital_literacy.csv'))
    df_attacks = pd.read_csv(os.path.join(data_dir, 'cyberattacks.csv'))
    df_trends = pd.read_csv(os.path.join(data_dir, 'attack_trends.csv'))
    df_risk = pd.read_csv(os.path.join(data_dir, 'risk_index.csv'))
    
    # Create output directory for visualizations
    viz_output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'visualizations')
    os.makedirs(viz_output_dir, exist_ok=True)
    
    # Generate all charts
    create_internet_penetration_chart(df_internet, viz_output_dir)
    create_digital_literacy_chart(df_literacy, viz_output_dir)
    create_cyberattack_chart(df_attacks, viz_output_dir)
    create_attack_trends_chart(df_trends, viz_output_dir)
    create_risk_index_chart(df_risk, viz_output_dir)
    create_jamaica_dashboard(df_internet, df_literacy, df_attacks, df_risk, viz_output_dir)
    
    print(f"\n  All visualizations saved to: {viz_output_dir}")
    return viz_output_dir


if __name__ == "__main__":
    create_all_visualizations(None)