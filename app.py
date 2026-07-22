import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================================
# 1. CẤU HÌNH TRANG CHÍNH & BRAND PALETTE
# ==============================================================================
st.set_page_config(
    page_title="AI Transformation Strategy Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Brand Color Palette
C_DARK_BLUE = "#293681"
C_MAIN_BLUE = "#4274D9"
C_LIGHT_BLUE = "#95CCDD"
C_TEAL_BG    = "#D0E7E6"
C_WHITE      = "#FFFFFF"
C_TEXT_DARK  = "#1E2342"
C_GRAY       = "#F4F7FB"
C_ACCENT     = "#FF6B6B"
C_ACCENT_BG  = "rgba(255,107,107,0.1)"

# ==============================================================================
# 2. STYLESHEET TỔNG HỢP (STRICT BRANDING UI)
# ==============================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; background-color: {C_GRAY}; color: {C_TEXT_DARK}; }}
    
    /* 1. Hero Header */
    .hero-banner {{ background: linear-gradient(135deg, {C_DARK_BLUE} 0%, {C_MAIN_BLUE} 100%); padding: 45px 30px; border-radius: 20px; color: {C_WHITE}; box-shadow: 0 12px 30px rgba(41, 54, 129, 0.22); margin-bottom: 40px; text-align: center; }}
    .hero-banner h1 {{ color: {C_WHITE} !important; font-weight: 800; font-size: 34px; margin-bottom: 15px; letter-spacing: -0.5px; text-transform: uppercase; }}
    .hero-banner h3 {{ color: {C_TEAL_BG} !important; font-weight: 600; font-size: 18px; margin-bottom: 10px; line-height: 1.4; max-width: 900px; margin-left: auto; margin-right: auto; }}
    .hero-banner p {{ color: {C_WHITE}; opacity: 0.8; font-size: 15px; font-style: italic; max-width: 850px; margin: 0 auto; }}

    /* Section Titles */
    .sec-title {{ color: {C_DARK_BLUE}; font-size: 24px; font-weight: 800; margin-bottom: 5px; text-transform: uppercase; display: flex; align-items: center; gap: 10px; }}
    .sec-subtitle {{ font-size: 16px; color: {C_TEXT_DARK}; opacity: 0.7; font-weight: 500; margin-bottom: 25px; }}

    /* 2. Strategic Challenge */
    .challenge-grid {{ display: flex; gap: 20px; margin-bottom: 40px; }}
    .c-card {{ flex: 1; background: {C_WHITE}; border-top: 4px solid; border-radius: 12px; padding: 25px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); transition: transform 0.3s; }}
    .c-card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 25px rgba(41, 54, 129, 0.1); }}
    .c-badge {{ display: inline-block; font-weight: 800; font-size: 12px; padding: 6px 12px; border-radius: 20px; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }}
    .c-title {{ font-size: 18px; font-weight: 800; color: {C_TEXT_DARK}; margin-bottom: 12px; }}
    .c-q {{ font-size: 14px; color: {C_TEXT_DARK}; opacity: 0.85; margin-bottom: 20px; line-height: 1.5; min-height: 60px; }}
    .c-out {{ font-size: 13px; font-weight: 700; color: {C_MAIN_BLUE}; background: {C_GRAY}; padding: 10px; border-radius: 6px; }}

    /* 3. Executive Decision Framework */
    .fw-container {{ display: flex; background: {C_WHITE}; border-radius: 16px; box-shadow: 0 6px 20px rgba(41, 54, 129, 0.06); margin-bottom: 50px; overflow: hidden; border: 1px solid {C_LIGHT_BLUE}; }}
    .fw-left {{ flex: 1; padding: 40px; border-right: 1px solid {C_LIGHT_BLUE}; display: flex; flex-direction: column; align-items: center; background: {C_GRAY}; }}
    .fw-right {{ flex: 1; padding: 40px; display: flex; flex-direction: column; align-items: center; }}
    
    .fw-block-title {{ font-size: 12px; font-weight: 800; color: {C_TEXT_DARK}; opacity: 0.5; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 15px; }}
    .fw-input-box {{ display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }}
    .fw-item {{ background: {C_WHITE}; border: 1px solid {C_LIGHT_BLUE}; color: {C_DARK_BLUE}; font-weight: 600; font-size: 13px; padding: 10px 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }}
    .fw-plus {{ font-weight: bold; color: {C_LIGHT_BLUE}; font-size: 18px; margin-top: 8px; }}
    .fw-arrow {{ font-weight: bold; color: {C_MAIN_BLUE}; font-size: 24px; margin: 15px 0; }}
    .fw-engine {{ background: linear-gradient(135deg, {C_DARK_BLUE}, {C_MAIN_BLUE}); color: {C_WHITE}; font-weight: 800; font-size: 16px; padding: 15px 30px; border-radius: 30px; box-shadow: 0 8px 15px rgba(66, 116, 217, 0.2); width: 100%; text-align: center; }}
    
    .fw-action-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; width: 100%; }}
    .act-tag {{ padding: 10px; border-radius: 6px; font-size: 12px; font-weight: 700; text-align: center; }}
    .act-tag.a1 {{ background: {C_MAIN_BLUE}; color: {C_WHITE}; }} 
    .act-tag.a2 {{ background: {C_ACCENT}; color: {C_WHITE}; }} 
    .act-tag.a3 {{ background: {C_LIGHT_BLUE}; color: {C_TEXT_DARK}; }} 
    .act-tag.a4 {{ background: {C_DARK_BLUE}; color: {C_WHITE}; }}

    .fw-step {{ background: {C_WHITE}; border-left: 4px solid {C_MAIN_BLUE}; padding: 15px 20px; border-radius: 8px; width: 100%; box-shadow: 0 3px 10px rgba(0,0,0,0.04); text-align: center; border: 1px solid {C_LIGHT_BLUE}; border-left-width: 4px; }}
    .fw-step-title {{ font-size: 15px; font-weight: 800; color: {C_DARK_BLUE}; margin-bottom: 5px; }}
    .fw-step-q {{ font-size: 13px; color: {C_TEXT_DARK}; opacity: 0.7; font-style: italic; }}

    /* 4. Executive Decision Journey (Cards) */
    .journey-card {{ background: {C_WHITE}; border: 1px solid {C_LIGHT_BLUE}; border-radius: 12px; padding: 25px; box-shadow: 0 4px 12px rgba(41, 54, 129, 0.05); height: 100%; }}
    .j-step {{ font-size: 13px; font-weight: 800; margin-bottom: 10px; text-transform: uppercase; }}
    .j-title {{ font-size: 18px; font-weight: 800; color: {C_TEXT_DARK}; margin-bottom: 15px; }}
    .j-q-box {{ background: {C_GRAY}; padding: 12px; border-radius: 6px; border-left: 3px solid; margin-bottom: 15px; }}
    .j-q-label {{ font-size: 11px; font-weight: 700; color: {C_TEXT_DARK}; opacity: 0.6; text-transform: uppercase; margin-bottom: 3px; }}
    .j-q-text {{ font-size: 13px; font-weight: 600; color: {C_DARK_BLUE}; }}
    .j-out-label {{ font-size: 12px; font-weight: 700; color: {C_TEXT_DARK}; opacity: 0.5; text-transform: uppercase; margin-bottom: 8px; }}
    .j-out-list {{ font-size: 13px; color: {C_TEXT_DARK}; opacity: 0.85; line-height: 1.6; padding-left: 15px; margin-bottom: 20px; }}

    /* 5. Strategic Implications */
    .impl-box {{ background: linear-gradient(135deg, {C_TEXT_DARK}, {C_DARK_BLUE}); border-left: 6px solid {C_ACCENT}; border-radius: 12px; padding: 30px 40px; color: {C_WHITE}; margin-top: 40px; box-shadow: 0 10px 25px rgba(41, 54, 129, 0.2); }}
    .impl-title {{ font-size: 20px; font-weight: 800; color: {C_TEAL_BG}; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }}
    .impl-text {{ font-size: 15px; color: {C_WHITE}; opacity: 0.95; line-height: 1.7; }}
    .impl-text ul {{ margin-top: 10px; margin-bottom: 15px; padding-left: 20px; }}
    .impl-text li {{ margin-bottom: 5px; }}
    .impl-highlight {{ color: {C_ACCENT}; font-weight: 800; }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. TẢI DỮ LIỆU TẬP TRUNG CHO TRA CỨU NHANH
# ==============================================================================
@st.cache_data
def load_quick_lookup_data():
    occs = [
        ("Accountants", "Finance & Accounting", "High", "High", "Reskill Workforce", "Train employees before automation"),
        ("Customer Service", "Customer Service", "High", "Medium", "Deploy AI Agent", "Implement AI support system"),
        ("Financial Analysts", "Finance & Accounting", "High", "Low", "AI Copilot", "Augment analytical capability"),
        ("Software Developers", "IT", "Medium", "Low", "Human-AI Collaboration", "Improve productivity with coding assistant"),
        ("General Managers", "Management", "Low", "Low", "Human-led", "Duy trì vai trò cốt lõi của con người"),
        ("Retail Salespersons", "Sales & Retail", "Medium", "High", "Reskill Workforce", "Lộ trình chuyển đổi kỹ năng giao tiếp"),
        ("Registered Nurses", "Healthcare", "Low", "Low", "Human-led", "Hỗ trợ tác vụ phụ, giữ nhân sự y tế")
    ]
    return pd.DataFrame(occs, columns=["Occupation", "Industry", "AI Priority", "Transformation Risk", "Recommended Strategy", "Executive Action"])

df_lookup = load_quick_lookup_data()

# ==============================================================================
# 4. NAVIGATION SIDEBAR
# ==============================================================================
try:
    st.sidebar.image(r"C:\Users\HP\Downloads\images.png", use_container_width=True)
except:
    st.sidebar.markdown(f"<h2 style='color:{C_MAIN_BLUE}; text-align:center;'>HUB LOGO</h2>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.header("🎓 Thông tin nhóm thực hiện")
st.sidebar.markdown("**Nhóm trưởng:** Nguyễn Thái Thanh Vân")
st.sidebar.markdown("• Nguyễn Thị Phương Uyên")
st.sidebar.markdown("• Phạm Thanh Tuyền")
st.sidebar.markdown("• Nguyễn Huy Gia Toàn")
st.sidebar.markdown("---")

st.sidebar.markdown(f"<h2 style='color:{C_DARK_BLUE}; font-size:18px;'>📍 Điều Hướng Hệ Thống</h2>", unsafe_allow_html=True)
st.sidebar.info("Hãy chọn các trang **`overview`**, **`scenario`**, **`economy`** ở menu bên trên góc trái thanh Sidebar để bắt đầu điều khiển Dashboard!")

st.sidebar.markdown("---")
st.sidebar.caption("Đồ án cuối kỳ - Môn Trực Quan Hoá Dữ Liệu")
st.sidebar.caption("Trường Đại học Ngân hàng TP. Hồ Chí Minh (HUB)")
st.sidebar.caption("© 2026 AI Transformation Framework")

# ==============================================================================
# PAGE 1: EXECUTIVE DECISION SUPPORT PLATFORM (TRANG TỔNG)
# ==============================================================================

# --- 1. HERO HEADER ---
st.markdown(f"""<div class="hero-banner"><h1>AI Transformation Strategy Platform</h1><h3>Decision Intelligence Framework for Identifying AI Investment Priorities, Workforce Transition Risks, and Transformation Roadmaps in Vietnam</h3><p>Khung hỗ trợ ra quyết định giúp doanh nghiệp xác định nơi nên đầu tư AI, đánh giá rủi ro chuyển đổi nhân sự và xây dựng lộ trình thích ứng.</p></div>""", unsafe_allow_html=True)

# --- 2. STRATEGIC CHALLENGE ---
st.markdown(f"""<div class="sec-title">🎯 Strategic Challenge</div><div class="sec-subtitle">Làm thế nào để xây dựng một Decision Support Framework giúp doanh nghiệp Việt Nam xác định thứ tự ưu tiên đầu tư AI và lựa chọn chiến lược chuyển đổi lực lượng lao động phù hợp cho từng nhóm nghề?</div><div class="challenge-grid"><div class="c-card" style="border-top-color: {C_ACCENT};"><div class="c-badge" style="background: {C_ACCENT_BG}; color: {C_ACCENT};">Q1 — WHERE TO INVEST?</div><div class="c-title">AI Investment Prioritization</div><div class="c-q">Which occupations and business areas should receive AI investment first to maximize economic value?</div><div class="c-out">Output: → Dashboard 2<br>AI Investment & Workforce Strategy</div></div><div class="c-card" style="border-top-color: {C_MAIN_BLUE};"><div class="c-badge" style="background: rgba(66,116,217,0.1); color: {C_MAIN_BLUE};">Q2 — WHAT WILL BE IMPACTED?</div><div class="c-title">Workforce Impact Assessment</div><div class="c-q">Which industries and occupations are most exposed to AI-driven transformation?</div><div class="c-out" style="color: {C_MAIN_BLUE};">Output: → Dashboard 1<br>Market Exposure Analysis</div></div><div class="c-card" style="border-top-color: {C_DARK_BLUE};"><div class="c-badge" style="background: rgba(41,54,129,0.1); color: {C_DARK_BLUE};">Q3 — HOW TO TRANSFORM?</div><div class="c-title">Transformation Roadmap</div><div class="c-q">How should organizations prepare workforce, infrastructure, and policies for AI adoption?</div><div class="c-out" style="color: {C_DARK_BLUE};">Output: → Dashboard 3<br>Vietnam AI Transformation Simulator</div></div></div>""", unsafe_allow_html=True)

# --- 3. EXECUTIVE DECISION FRAMEWORK ---
st.markdown("""<div class="sec-title">🧭 Executive Decision Framework</div><div class="sec-subtitle">The logical architecture translating workforce data into strategic recommendations.</div><div class="fw-container"><div class="fw-left"><div class="fw-block-title">INPUT</div><div class="fw-input-box"><div class="fw-item">AI Capability</div><div class="fw-plus">+</div><div class="fw-item">Economic Exposure</div><div class="fw-plus">+</div><div class="fw-item">Worker Readiness</div></div><div class="fw-arrow">↓</div><div class="fw-engine">⚙️ AI Transformation Decision Engine</div><div class="fw-arrow">↓</div><div class="fw-block-title">STRATEGIC ACTION</div><div class="fw-action-grid"><div class="act-tag a1">Deploy AI</div><div class="act-tag a2">Reskill Workforce</div><div class="act-tag a3">Human-AI Collaboration</div><div class="act-tag a4">Human-led</div></div></div><div class="fw-right"><div class="fw-block-title">BUSINESS QUESTION</div><div class="fw-arrow" style="margin-top:0;">↓</div><div class="fw-step"><div class="fw-step-title">1. IMPACT ASSESSMENT</div><div class="fw-step-q">Where is AI changing?</div></div><div class="fw-arrow">↓</div><div class="fw-step"><div class="fw-step-title">2. PRIORITIZATION</div><div class="fw-step-q">Where should invest?</div></div><div class="fw-arrow">↓</div><div class="fw-step"><div class="fw-step-title">3. TRANSFORMATION</div><div class="fw-step-q">How should adapt?</div></div></div></div>""", unsafe_allow_html=True)

# --- 4. EXECUTIVE DECISION JOURNEY ---
st.markdown("""<div class="sec-title">🚀 Executive Decision Journey</div><div class="sec-subtitle">Three analytical layers converting workforce data into strategic AI actions.</div>""", unsafe_allow_html=True)
    
col1, col2, col3 = st.columns(3)
    
with col1:
    st.markdown(f"""<div class="journey-card"><div class="j-step" style="color: {C_MAIN_BLUE};">STEP 1</div><div class="j-title">Diagnose Current AI Exposure</div><div class="j-q-box" style="border-left-color: {C_MAIN_BLUE};"><div class="j-q-label">Question</div><div class="j-q-text">Where will AI create the greatest disruption?</div></div><div class="j-out-label">Core Outputs</div><ul class="j-out-list"><li>AI Exposure Score</li><li>Workforce Vulnerability Map</li><li>Industry Impact Landscape</li></ul></div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="journey-card"><div class="j-step" style="color: {C_DARK_BLUE};">STEP 2</div><div class="j-title">Prioritize AI Investment</div><div class="j-q-box" style="border-left-color: {C_DARK_BLUE};"><div class="j-q-label">Question</div><div class="j-q-text">Where should organizations allocate AI resources first?</div></div><div class="j-out-label">Core Outputs</div><ul class="j-out-list"><li>AI Prioritization Score (AIPS)</li><li>Economic Opportunity Ranking</li><li>Workforce Strategy Matrix</li></ul></div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="journey-card"><div class="j-step" style="color: {C_ACCENT};">STEP 3</div><div class="j-title">Simulate Future Transformation</div><div class="j-q-box" style="border-left-color: {C_ACCENT};"><div class="j-q-label">Question</div><div class="j-q-text">How will Vietnam's workforce evolve under different AI scenarios?</div></div><div class="j-out-label">Core Outputs</div><ul class="j-out-list"><li>Technology Adoption Scenario</li><li>Workforce Transition Path</li><li>2026–2030 Transformation Roadmap</li></ul></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. EXECUTIVE QUICK LOOKUP ENGINE ---
st.markdown("""<div class="sec-title">🔎 Executive Quick Lookup Engine</div><div class="sec-subtitle">A cross-dashboard recommendation layer allowing executives to quickly identify recommended AI strategies by occupation.</div>""", unsafe_allow_html=True)
    
search_col1, search_col2 = st.columns([3, 7])
with search_col1:
    selected_ind = st.selectbox("Select Industry Filter:", ["All Industries"] + list(df_lookup["Industry"].unique()))
    
filtered_lookup = df_lookup if selected_ind == "All Industries" else df_lookup[df_lookup["Industry"] == selected_ind]

st.dataframe(
    filtered_lookup.style.set_properties(**{'background-color': C_WHITE, 'color': C_TEXT_DARK}),
    use_container_width=True,
    hide_index=True
)

# --- 6. STRATEGIC IMPLICATIONS ---
st.markdown("""<div class="impl-box"><div class="impl-title">💡 Strategic Implications</div><div class="impl-text">AI transformation is not only a technology adoption problem. The major challenge is aligning:<ul><li>AI capability</li><li>Economic value creation</li><li>Workforce readiness</li></ul><span class="impl-highlight">Successful organizations should prioritize AI investment where economic impact is high while simultaneously preparing employees for workforce transition.</span></div></div>""", unsafe_allow_html=True)
