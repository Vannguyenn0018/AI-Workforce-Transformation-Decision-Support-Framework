import streamlit as st
import os

# ==============================================================================
# 1. CẤU HÌNH TRANG CHÍNH & MÀU THIẾT KẾ (BRAND PALETTE)
# ==============================================================================
st.set_page_config(
    page_title="AI Transformation Decision Support Framework - HUB",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Palette màu nhận diện thương hiệu
C_DARK_BLUE = "#293681"   # Primary Dark Blue (Màu chuẩn HUB)
C_MAIN_BLUE = "#4274D9"   # Primary Accent Blue
C_LIGHT_BLUE = "#95CCDD"  # Soft Blue Accent
C_TEAL_BG    = "#D0E7E6"  # Soft Background Tint
C_WHITE      = "#FFFFFF"
C_TEXT_DARK  = "#1E2342"

# ==============================================================================
# 2. STYLESHEET CHUNG (3D NEUMORPHIC STYLE)
# ==============================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: #F4F7FB;
        color: {C_TEXT_DARK};
    }}

    /* Card Tiêu Đề Dự Án */
    .project-header-card {{
        background: {C_WHITE};
        border-radius: 16px;
        padding: 28px 32px;
        box-shadow: 8px 8px 20px rgba(41, 54, 129, 0.08), 
                    -6px -6px 15px rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(149, 204, 221, 0.4);
        margin-top: 15px;
        margin-bottom: 25px;
    }}
    .project-title-en {{
        color: {C_DARK_BLUE};
        font-size: 24px;
        font-weight: 800;
        line-height: 1.35;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: -0.3px;
    }}
    .project-title-vi {{
        color: {C_MAIN_BLUE};
        font-size: 16px;
        font-weight: 600;
        font-style: italic;
        margin-bottom: 0;
        line-height: 1.5;
    }}

    /* Research Question Banner 3D */
    .rq-box-3d {{
        background: linear-gradient(135deg, {C_WHITE} 0%, {C_TEAL_BG} 100%);
        border-left: 6px solid {C_MAIN_BLUE};
        border-radius: 14px;
        padding: 22px 26px;
        box-shadow: 6px 6px 18px rgba(41, 54, 129, 0.06);
        margin-bottom: 30px;
    }}
    .rq-title {{
        color: {C_DARK_BLUE};
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .rq-content {{
        color: {C_TEXT_DARK};
        font-size: 15px;
        font-weight: 500;
        line-height: 1.6;
        margin: 0;
    }}

    /* Banner 3D Hero */
    .hero-banner {{
        background: linear-gradient(135deg, {C_DARK_BLUE} 0%, {C_MAIN_BLUE} 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        box-shadow: 0 12px 30px rgba(41, 54, 129, 0.22);
        margin-bottom: 30px;
        text-align: center;
    }}
    .hero-banner h2 {{
        color: white !important;
        font-weight: 800;
        font-size: 28px;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }}
    .hero-banner p {{
        color: {C_TEAL_BG};
        font-size: 15px;
        max-width: 850px;
        margin: 0 auto;
        line-height: 1.5;
    }}

    /* Card 3D Navigation */
    .card-nav-3d {{
        background: {C_WHITE};
        border-radius: 18px;
        padding: 24px;
        box-shadow: 8px 8px 20px rgba(41, 54, 129, 0.08), 
                    -6px -6px 15px rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(149, 204, 221, 0.3);
        transition: all 0.3s ease;
        height: 100%;
    }}
    .card-nav-3d:hover {{
        transform: translateY(-5px);
        box-shadow: 12px 12px 28px rgba(41, 54, 129, 0.15), 
                    -6px -6px 15px rgba(255, 255, 255, 1);
        border-color: {C_MAIN_BLUE};
    }}
    .card-title {{
        font-size: 18px;
        font-weight: 700;
        color: {C_DARK_BLUE};
        margin-bottom: 6px;
    }}
    .card-desc {{
        font-size: 13px;
        color: #555;
        line-height: 1.5;
    }}

    /* Sidebar Customization */
    .css-1d38150, [data-testid="stSidebar"] {{
        background-color: #FFFFFF !important;
        border-right: 1px solid {C_TEAL_BG};
    }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. HERO BANNER FRAMEWORK
# ==============================================================================
st.markdown(f"""
<div class="hero-banner">
    <h2>🤖 AI TRANSFORMATION FRAMEWORK</h2>
    <p>Hệ thống Quản trị & Mô phỏng Chiến lược Chuyển đổi AI cho Doanh nghiệp: Đánh giá Tác động, Định hình Năng lực & Mô phỏng Kịch bản Mô hình Lao động Việt Nam.</p>
</div>
""", unsafe_allow_html=True)
# Khung Research Question
st.markdown(f"""
<div class="rq-box-3d">
    <div class="rq-title">❓ RESEARCH QUESTION (CÂU HỎI NGHIÊN CỨU CỐT LÕI)</div>
    <p class="rq-content">
        <i>"Làm thế nào để xây dựng một <b>Decision Support Framework</b> giúp doanh nghiệp Việt Nam xác định thứ tự ưu tiên đầu tư AI và lựa chọn chiến lược chuyển đổi lực lượng lao động phù hợp cho từng nhóm nghề?"</i>
    </p>
</div>
""", unsafe_allow_html=True)
# ==============================================================================
# 5. DANH SÁCH DASHBOARDS (3 TRỤ CỘT CHÍNH)
# ==============================================================================
st.markdown(f"<h3 style='color:{C_DARK_BLUE}; font-weight:800; font-size:20px; margin-bottom:15px;'>📌 Khám Phá Các Dashboard Chuyên Sâu</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card-nav-3d">
        <div class="card-title">📊 DASHBOARD 1</div>
        <h4 style="color:{C_MAIN_BLUE}; margin-top:0; font-size:15px;">Global Baseline & Market Exposure</h4>
        <div class="card-desc">
            Đánh giá mức độ tác động của AI tới các nhóm ngành và công việc toàn cầu. Phân tích chỉ số WEI, PEI, CI và AIPS để nhận diện nhóm nghề có rủi ro/cơ hội cao nhất.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card-nav-3d">
        <div class="card-title">📈 DASHBOARD 2</div>
        <h4 style="color:{C_MAIN_BLUE}; margin-top:0; font-size:15px;">Enterprise & Capability Overview</h4>
        <div class="card-desc">
            Phân tích sâu khả năng tự động hóa (AI Capability) vs Mức độ sẵn sàng tiếp nhận của nhân sự (Worker Readiness). Định vị chiến lược: Deploy AI, Reskill hay Keep Human.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card-nav-3d">
        <div class="card-title">🇻🇳 VN DASHBOARD 3</div>
        <h4 style="color:{C_MAIN_BLUE}; margin-top:0; font-size:15px;">Vietnam AI Transformation Simulator</h4>
        <div class="card-desc">
            Mô phỏng kịch bản thích ứng AI tại Việt Nam dựa trên 3 tham số: Technology Readiness (TR), People Readiness (PR), Institutional Readiness (IR) để đưa ra lộ trình quản trị 2028-2030.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 6. SIDEBAR
# ==============================================================================
st.sidebar.image("data/images.png", use_container_width=True) # Placeholder Logo BUH
st.sidebar.markdown("---")
st.sidebar.header("Thông tin nhóm thực hiện")
st.sidebar.markdown("**Nhóm trưởng:** Nguyễn Thái Thanh Vân")
st.sidebar.markdown("Nguyễn Thị Phương Uyên")
st.sidebar.markdown("Phạm Thanh Tuyền")
st.sidebar.markdown("Nguyễn Huy Gia Toàn")
st.sidebar.markdown(f"<h2 style='color:{C_DARK_BLUE}; font-size:18px;'>📍 Điều Hướng Hệ Thống</h2>", unsafe_allow_html=True)
st.sidebar.info("Hãy chọn các trang **`overview`**, **`scenario`**, **`economy`** ở menu bên trên góc trái thanh Sidebar để bắt đầu điều khiển Dashboard!")

st.sidebar.markdown("---")
st.sidebar.caption("Đồ án cuối kỳ - Môn Trực Quan Hoá Dữ Liệu")
st.sidebar.caption("Trường Đại học Ngân hàng TP. Hồ Chí Minh (HUB)")
st.sidebar.caption("© 2026 AI Transformation Framework")
