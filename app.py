import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================================
# 1. CẤU HÌNH TRANG CHÍNH & BRAND PALETTE
# ==============================================================================
st.set_page_config(
    page_title="Nền tảng Chiến lược Chuyển đổi AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Brand Color Palette
C_DARK_BLUE  = "#293681"
C_MAIN_BLUE  = "#4274D9"
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
    .challenge-grid {{ display: flex; gap: 20px; margin-bottom: 40px; flex-wrap: wrap; }}
    .c-card {{ flex: 1; min-width: 250px; background: {C_WHITE}; border-top: 4px solid; border-radius: 12px; padding: 25px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); transition: transform 0.3s; }}
    .c-card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 25px rgba(41, 54, 129, 0.1); }}
    .c-badge {{ display: inline-block; font-weight: 800; font-size: 12px; padding: 6px 12px; border-radius: 20px; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }}
    .c-title {{ font-size: 18px; font-weight: 800; color: {C_TEXT_DARK}; margin-bottom: 12px; }}
    .c-q {{ font-size: 14px; color: {C_TEXT_DARK}; opacity: 0.85; margin-bottom: 20px; line-height: 1.5; min-height: 60px; }}
    .c-out {{ font-size: 13px; font-weight: 700; color: {C_MAIN_BLUE}; background: {C_GRAY}; padding: 10px; border-radius: 6px; }}

    /* 3. Executive Decision Framework */
    .fw-container {{ display: flex; background: {C_WHITE}; border-radius: 16px; box-shadow: 0 6px 20px rgba(41, 54, 129, 0.06); margin-bottom: 50px; overflow: hidden; border: 1px solid {C_LIGHT_BLUE}; flex-wrap: wrap; }}
    .fw-left {{ flex: 1; min-width: 300px; padding: 40px; border-right: 1px solid {C_LIGHT_BLUE}; display: flex; flex-direction: column; align-items: center; background: {C_GRAY}; }}
    .fw-right {{ flex: 1; min-width: 300px; padding: 40px; display: flex; flex-direction: column; align-items: center; }}
    
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
# 3. TẢI DỮ LIỆU THỰC TẾ TỪ FILE CSV
# ==============================================================================
@st.cache_data
def load_real_data():
    try:
        # Đọc dữ liệu từ file csv thực tế
        df = pd.read_csv("data/final_consolidated_output (1).csv")
        
        df_display = df[[
            "Occupation (O*NET-SOC Title)", 
            "Industry Group", 
            "Cap_norm", 
            "Read_norm", 
            "Quadrant", 
            "Transformation_Strategy"
        ]].copy()
        
        df_display = df_display.rename(columns={
            "Occupation (O*NET-SOC Title)": "Nghề nghiệp",
            "Industry Group": "Ngành nghề",
            "Quadrant": "Phân khúc Chiến lược (Quadrant)",
            "Transformation_Strategy": "Hành động Quản trị"
        })
        
        # GIỮ NGUYÊN ĐỊNH DẠNG SỐ (FLOAT) ĐỂ LÀM GRADIENT MÀU
        df_display["Năng lực AI chuẩn hóa (Norm)"] = df_display["Cap_norm"].astype(float)
        df_display["Sẵn sàng Nhân sự (Norm)"] = df_display["Read_norm"].astype(float)
        
        df_display = df_display[[
            "Nghề nghiệp", "Ngành nghề", "Năng lực AI chuẩn hóa (Norm)", "Sẵn sàng Nhân sự (Norm)", "Phân khúc Chiến lược (Quadrant)", "Hành động Quản trị"
        ]]
        
        return df_display
    except Exception as e:
        st.error(f"Không thể tải dữ liệu từ file. Lỗi: {e}")
        return pd.DataFrame(columns=["Nghề nghiệp", "Ngành nghề", "Năng lực AI chuẩn hóa (Norm)", "Sẵn sàng Nhân sự (Norm)", "Phân khúc Chiến lược (Quadrant)", "Hành động Quản trị"])

df_lookup = load_real_data()

# ==============================================================================
# 4. NAVIGATION SIDEBAR
# ==============================================================================
try:
    st.sidebar.image("data/images.png", use_container_width=True)
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
st.sidebar.caption("© 2026 Khung Chuyển đổi AI (AI Transformation Framework)")

# ==============================================================================
# PAGE 1: NỀN TẢNG HỖ TRỢ QUYẾT ĐỊNH QUẢN TRỊ (TRANG TỔNG)
# ==============================================================================

# --- 1. HERO HEADER ---
st.markdown(f"""<div class="hero-banner"><h1>Nền tảng Chiến lược Chuyển đổi AI</h1><h3>Khung Khuyến nghị Quyết định nhằm Xác định Ưu tiên Đầu tư AI, Rủi ro Chuyển đổi Nhân lực và Lộ trình Thích ứng tại Việt Nam</h3><p>Khung hỗ trợ ra quyết định giúp doanh nghiệp xác định nơi nên đầu tư AI, đánh giá rủi ro chuyển đổi nhân sự và xây dựng lộ trình thích ứng.</p></div>""", unsafe_allow_html=True)

# --- 2. STRATEGIC CHALLENGE ---
st.markdown(f"""<div class="sec-title">🎯 Thách thức Chiến lược</div><div class="sec-subtitle">Làm thế nào để xây dựng một Khung Hỗ trợ Quyết định giúp doanh nghiệp Việt Nam xác định thứ tự ưu tiên đầu tư AI và lựa chọn chiến lược chuyển đổi lực lượng lao động phù hợp cho từng nhóm nghề?</div><div class="challenge-grid"><div class="c-card" style="border-top-color: {C_ACCENT};"><div class="c-badge" style="background: {C_ACCENT_BG}; color: {C_ACCENT};">Câu hỏi 1 — ĐẦU TƯ VÀO ĐÂU?</div><div class="c-title">Ưu tiên Đầu tư AI</div><div class="c-q">Những ngành nghề và lĩnh vực kinh doanh nào nên được ưu tiên đầu tư AI để tối đa hóa giá trị kinh tế?</div><div class="c-out">Đầu ra: → Dashboard 2<br>Chiến lược Đầu tư AI & Nhân sự</div></div><div class="c-card" style="border-top-color: {C_MAIN_BLUE};"><div class="c-badge" style="background: rgba(66,116,217,0.1); color: {C_MAIN_BLUE};">Câu hỏi 2 — ĐỐI TƯỢNG BỊ TÁC ĐỘNG?</div><div class="c-title">Đánh giá Tác động Nhân lực</div><div class="c-q">Những ngành nghề và lĩnh vực nào chịu rủi ro cao nhất từ quá trình chuyển đổi AI?</div><div class="c-out" style="color: {C_MAIN_BLUE};">Đầu ra: → Dashboard 1<br>Phân tích Rủi ro Thị trường (Market Exposure)</div></div><div class="c-card" style="border-top-color: {C_DARK_BLUE};"><div class="c-badge" style="background: rgba(41,54,129,0.1); color: {C_DARK_BLUE};">Câu hỏi 3 — CHUYỂN ĐỔI NHƯ THẾ NÀO?</div><div class="c-title">Lộ trình Chuyển đổi</div><div class="c-q">Tổ chức nên chuẩn bị nguồn nhân lực, hạ tầng và chính sách như thế nào để ứng dụng AI?</div><div class="c-out" style="color: {C_DARK_BLUE};">Đầu ra: → Dashboard 3<br>Mô phỏng Chuyển đổi AI tại Việt Nam</div></div></div>""", unsafe_allow_html=True)

# --- 3. EXECUTIVE DECISION FRAMEWORK ---
st.markdown("""<div class="sec-title">🧭 Khung Quyết định Quản trị (Executive Framework)</div><div class="sec-subtitle">Cấu trúc logic chuyển hóa dữ liệu nhân lực thành các đề xuất chiến lược.</div><div class="fw-container"><div class="fw-left"><div class="fw-block-title">ĐẦU VÀO (INPUT)</div><div class="fw-input-box"><div class="fw-item">Năng lực AI</div><div class="fw-plus">+</div><div class="fw-item">Rủi ro Kinh tế</div><div class="fw-plus">+</div><div class="fw-item">Độ sẵn sàng Nhân sự</div></div><div class="fw-arrow">↓</div><div class="fw-engine">⚙️ Cỗ máy Quyết định Chuyển đổi AI</div><div class="fw-arrow">↓</div><div class="fw-block-title">HÀNH ĐỘNG CHIẾN LƯỢC</div><div class="fw-action-grid"><div class="act-tag a1">Triển khai AI</div><div class="act-tag a2">Đào tạo lại (Reskill)</div><div class="act-tag a3">Cộng tác Người-AI</div><div class="act-tag a4">Con người Dẫn dắt</div></div></div><div class="fw-right"><div class="fw-block-title">CÂU HỎI NGHIỆP VỤ</div><div class="fw-arrow" style="margin-top:0;">↓</div><div class="fw-step"><div class="fw-step-title">1. ĐÁNH GIÁ TÁC ĐỘNG</div><div class="fw-step-q">AI đang thay đổi ở đâu?</div></div><div class="fw-arrow">↓</div><div class="fw-step"><div class="fw-step-title">2. XÁC ĐỊNH ƯU TIÊN</div><div class="fw-step-q">Nên đầu tư vào đâu?</div></div><div class="fw-arrow">↓</div><div class="fw-step"><div class="fw-step-title">3. LỘ TRÌNH CHUYỂN ĐỔI</div><div class="fw-step-q">Cần thích ứng thế nào?</div></div></div></div>""", unsafe_allow_html=True)

# --- 4. EXECUTIVE DECISION JOURNEY ---
st.markdown("""<div class="sec-title">🚀 Hành trình Ra quyết định Quản trị</div><div class="sec-subtitle">Ba tầng phân tích chuyển hóa dữ liệu nhân lực thành hành động chiến lược AI.</div>""", unsafe_allow_html=True)
    
col1, col2, col3 = st.columns(3)
    
with col1:
    st.markdown(f"""<div class="journey-card"><div class="j-step" style="color: {C_MAIN_BLUE};">BƯỚC 1</div><div class="j-title">Chẩn đoán Mức độ Phơi nhiễm AI Hiện tại</div><div class="j-q-box" style="border-left-color: {C_MAIN_BLUE};"><div class="j-q-label">Câu hỏi</div><div class="j-q-text">AI sẽ tạo ra sự gián đoạn lớn nhất ở đâu?</div></div><div class="j-out-label">Đầu ra Cốt lõi</div><ul class="j-out-list"><li>Điểm Phơi nhiễm AI (AI Exposure Score)</li><li>Bản đồ Rủi ro Nhân sự (Vulnerability Map)</li><li>Bức tranh Tác động Ngành</li></ul></div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="journey-card"><div class="j-step" style="color: {C_DARK_BLUE};">BƯỚC 2</div><div class="j-title">Ưu tiên Đầu tư AI</div><div class="j-q-box" style="border-left-color: {C_DARK_BLUE};"><div class="j-q-label">Câu hỏi</div><div class="j-q-text">Tổ chức nên phân bổ nguồn lực AI vào đâu đầu tiên?</div></div><div class="j-out-label">Đầu ra Cốt lõi</div><ul class="j-out-list"><li>Điểm Ưu tiên AI (AIPS)</li><li>Xếp hạng Cơ hội Kinh tế</li><li>Ma trận Chiến lược Nhân sự</li></ul></div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="journey-card"><div class="j-step" style="color: {C_ACCENT};">BƯỚC 3</div><div class="j-title">Mô phỏng Chuyển đổi Tương lai</div><div class="j-q-box" style="border-left-color: {C_ACCENT};"><div class="j-q-label">Câu hỏi</div><div class="j-q-text">Lực lượng lao động Việt Nam sẽ tiến hóa thế nào dưới các kịch bản AI khác nhau?</div></div><div class="j-out-label">Đầu ra Cốt lõi</div><ul class="j-out-list"><li>Kịch bản Ứng dụng Công nghệ</li><li>Lộ trình Dịch chuyển Nhân sự</li><li>Lộ trình Chuyển đổi 2026–2030</li></ul></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. EXECUTIVE QUICK LOOKUP ENGINE ---
st.markdown("""<div class="sec-title">🔎 Công cụ Tra cứu Nhanh cho Quản lý</div><div class="sec-subtitle">Lớp khuyến nghị liên thông giúp các nhà quản lý nhanh chóng xác định chiến lược AI phù hợp theo từng nhóm ngành nghề.</div>""", unsafe_allow_html=True)
    
search_col1, search_col2 = st.columns([3, 7])
with search_col1:
    # Lấy danh sách ngành nghề độc nhất, xử lý các giá trị rỗng/NaN nếu có
    unique_industries = sorted([str(x) for x in df_lookup["Ngành nghề"].unique() if pd.notna(x)])
    selected_ind = st.selectbox("Chọn bộ lọc Ngành nghề:", ["Tất cả các ngành"] + unique_industries)
    
filtered_lookup = df_lookup if selected_ind == "Tất cả các ngành" else df_lookup[df_lookup["Ngành nghề"].astype(str) == selected_ind]

# Hàm tô màu riêng cho cột Phân khúc Chiến lược (Quadrant)
def color_quadrants(val):
    if pd.isna(val): return ''
    val_str = str(val).upper()
    if 'Q1' in val_str: 
        return 'background-color: #e0f2fe; color: #0284c7; font-weight: 700;' # Xanh nhạt
    elif 'Q2' in val_str: 
        return 'background-color: #fee2e2; color: #b91c1c; font-weight: 700;' # Đỏ nhạt
    elif 'Q3' in val_str: 
        return 'background-color: #fef9c3; color: #a16207; font-weight: 700;' # Vàng nhạt
    elif 'Q4' in val_str: 
        return 'background-color: #f3f4f6; color: #374151; font-weight: 700;' # Xám nhạt
    return ''

# Dùng .map() (hoặc .applymap() với pandas cũ) để tô màu
styled_df = (
    filtered_lookup.style
    .map(color_quadrants, subset=["Phân khúc Chiến lược (Quadrant)"])
    .background_gradient(cmap="Blues", subset=["Năng lực AI chuẩn hóa (Norm)"]) # Màu gradient xanh
    .background_gradient(cmap="Purples", subset=["Sẵn sàng Nhân sự (Norm)"]) # Màu gradient tím
    .format({
        "Năng lực AI chuẩn hóa (Norm)": "{:.2f}", 
        "Sẵn sàng Nhân sự (Norm)": "{:.2f}"
    })
)

st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True,
    height=400
)

# --- 6. STRATEGIC IMPLICATIONS ---
st.markdown("""<div class="impl-box"><div class="impl-title">💡 Ý nghĩa Chiến lược</div><div class="impl-text">Chuyển đổi AI không chỉ là bài toán ứng dụng công nghệ. Thách thức lớn nhất nằm ở việc tinh chỉnh đồng bộ:<ul><li>Năng lực AI (AI Capability)</li><li>Tạo ra giá trị kinh tế (Economic Value Creation)</li><li>Mức độ sẵn sàng của lực lượng lao động (Workforce Readiness)</li></ul><span class="impl-highlight">Các tổ chức thành công cần ưu tiên đầu tư AI vào những nơi mang lại tác động kinh tế cao, đồng thời chủ động chuẩn bị cho nhân viên lộ trình thích nghi và chuyển đổi.</span></div></div>""", unsafe_allow_html=True)
