import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. CẤU HÌNH TRANG & MA TRẬN MÀU THIẾT KẾ (BRAND PALETTE)
# ==============================================================================
st.set_page_config(
    page_title="CÔNG CỤ ĐÁNH GIÁ ƯU TIÊN KINH TẾ (ECONOMIC PRIORITIZATION ENGINE)",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Palette màu nhận diện thương hiệu
C_DARK_BLUE = "#293681"   # Primary Dark Blue
C_MAIN_BLUE = "#4274D9"   # Primary Accent Blue
C_LIGHT_BLUE = "#95CCDD"  # Soft Blue Accent
C_TEAL_BG    = "#D0E7E6"  # Soft Background Tint
C_WHITE      = "#FFFFFF"
C_TEXT_DARK  = "#1E2342"
C_DANGER     = "#E63946"  # Cảnh báo rủi ro cao WTRS
C_WARNING    = "#F57F17"

# ==============================================================================
# 2. STYLESHEET (KHUNG DSS NỔI & CÂU CHUYỆN QUẢN TRỊ)
# ==============================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: #F4F7FB;
        color: {C_TEXT_DARK};
    }}

    /* Header Container Gradient */
    .header-container {{
        background: linear-gradient(135deg, {C_DARK_BLUE} 0%, {C_MAIN_BLUE} 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        box-shadow: 0 10px 25px rgba(41, 54, 129, 0.25);
        margin-bottom: 20px;
    }}
    .header-container h1 {{
        color: white !important;
        font-weight: 800;
        margin: 0;
        font-size: 28px;
        letter-spacing: -0.5px;
        text-transform: uppercase;
    }}
    .header-container p {{
        color: {C_TEAL_BG};
        margin-top: 6px;
        margin-bottom: 0;
        font-size: 15px;
        line-height: 1.5;
    }}

    /* Business Question Box */
    .bq-box {{
        background-color: #FFF3CD;
        border-left: 6px solid #FFC107;
        padding: 16px 24px;
        border-radius: 8px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }}
    .bq-title {{
        font-weight: 800;
        font-size: 14px;
        color: #856404;
        margin-bottom: 6px;
        text-transform: uppercase;
    }}
    .bq-content {{
        font-size: 16px;
        font-weight: 600;
        color: #383D41;
        line-height: 1.4;
    }}

    /* Decision Storyline Flow Banner */
    .story-banner {{
        background: {C_WHITE};
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 25px;
        border: 1px solid rgba(149, 204, 221, 0.4);
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }}
    .story-title {{
        font-weight: 700;
        font-size: 13px;
        color: {C_DARK_BLUE};
        text-transform: uppercase;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }}

    /* Section Cards */
    .section-header {{
        border-left: 5px solid {C_MAIN_BLUE};
        padding-left: 12px;
        margin: 30px 0 15px 0;
    }}
    .section-header h3 {{
        color: {C_DARK_BLUE};
        font-weight: 800;
        font-size: 20px;
        margin: 0;
    }}
    .section-header p {{
        color: #6C757D;
        font-size: 14px;
        margin: 4px 0 0 0;
        font-weight: 500;
    }}

    /* KPI Card 3D Nổi */
    .card-3d {{
        background: {C_WHITE};
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 6px 6px 18px rgba(41, 54, 129, 0.06);
        border: 1px solid rgba(149, 204, 221, 0.3);
        height: 100%;
    }}
    
    .kpi-label {{
        font-size: 12px;
        font-weight: 700;
        color: #6C757D;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .kpi-value {{
        font-size: 32px;
        font-weight: 800;
        color: {C_DARK_BLUE};
        margin: 6px 0;
    }}
    .kpi-insight {{
        font-size: 13px;
        color: #555;
        background-color: #F8F9FA;
        padding: 8px 10px;
        border-radius: 6px;
        border-left: 3px solid {C_MAIN_BLUE};
        margin-top: 10px;
    }}

    /* Executive Insight Box */
    .insight-box {{
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        border: 1px solid #90CAF9;
        border-radius: 12px;
        padding: 24px;
        margin-top: 40px;
        box-shadow: 0 8px 20px rgba(25, 118, 210, 0.1);
    }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. TẢI VÀ CHUẨN HÓA DỮ LIỆU
# ==============================================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/final_consolidated_output (1).csv")
        
        # Đổi tên các cột cốt lõi một cách an toàn (tránh trùng lặp tên cột)
        rename_dict = {}
        if "Occupation (O*NET-SOC Title)" in df.columns:
            rename_dict["Occupation (O*NET-SOC Title)"] = "Occupation"
        if "Industry Group" in df.columns:
            rename_dict["Industry Group"] = "Industry"
        if "EE" in df.columns:
            rename_dict["EE"] = "EconomicExposure"
        if "wfi" in df.columns:
            rename_dict["wfi"] = "WFI"
            
        df = df.rename(columns=rename_dict)
        
        # Sử dụng trực tiếp Cap_norm và Read_norm làm Cap và Read để tránh trùng cột
        if "Cap_norm" in df.columns:
            df["Cap"] = df["Cap_norm"]
        if "Read_norm" in df.columns:
            df["Read"] = df["Read_norm"]

        # Kiểm tra và bổ sung các cột còn thiếu
        if "WTRS" not in df.columns:
            df["WTRS"] = df["Cap"] * (1 - df["Read"]) * df["EconomicExposure"]
            
        if "Risk_Level" not in df.columns:
            df["Risk_Level"] = pd.qcut(df["WTRS"].rank(method='first'), q=3, labels=["Low", "Medium", "High"])

        if "Workforce_Strategy" not in df.columns:
            def map_strategy(row):
                q = str(row.get("Quadrant", ""))
                if "Q1" in q: return "Deploy AI"
                elif "Q2" in q: return "Reskill Workforce"
                elif "Q3" in q: return "Human-AI Collaboration"
                else: return "Human-led"
            df["Workforce_Strategy"] = df.apply(map_strategy, axis=1)

        if "Recommended_Action" not in df.columns:
            action_map = {
                "Deploy AI": "AI Agent hỗ trợ 24/7 / Tự động hóa",
                "Reskill Workforce": "Đào tạo lại trước khi tự động hóa",
                "Human-AI Collaboration": "Tăng tốc bằng AI Copilot",
                "Human-led": "Duy trì định hướng con người"
            }
            df["Recommended_Action"] = df["Workforce_Strategy"].map(action_map).fillna("Cần rà soát thủ công")

        return df
    except Exception as e:
        st.error(f"Không thể đọc file dữ liệu. Lỗi: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# ==============================================================================
# HEADER, BUSINESS QUESTION & FRAMEWORK FLOW
# ==============================================================================
st.markdown(f"""
<div class="header-container">
    <h1>CÔNG CỤ ĐÁNH GIÁ ƯU TIÊN KINH TẾ (ECONOMIC PRIORITIZATION ENGINE)</h1>
    <p>Chiến Lược Đầu Tư AI & Chuyển Đổi Lực Lượng Lao Động<br>
    <i>Khung ra quyết định giúp doanh nghiệp xác định ưu tiên phân bổ ngân sách AI và hoạch định lộ trình nhân sự theo từng nhóm nghề.</i></p>
</div>
""", unsafe_allow_html=True)

# Business Question
st.markdown("""
<div class="bq-box">
    <div class="bq-title">🎯 BÀI TOÁN KINH DOANH (BUSINESS QUESTION)</div>
    <div class="bq-content">
        Trong bối cảnh nguồn lực đầu tư AI có giới hạn, doanh nghiệp nên ưu tiên tự động hóa nhóm nghề nào để tối đa hóa giá trị kinh tế nhưng vẫn kiểm soát tốt rủi ro biến động nhân sự?
    </div>
</div>
""", unsafe_allow_html=True)

# Decision Framework Flow
st.markdown(f"""
<div class="story-banner">
    <div class="story-title">Khung Ra Quyết Định (Decision Framework): Từ Dữ Liệu Đến Hành Động Chiến Lược</div>
    <div style="display: flex; justify-content: space-between; align-items: center; text-align: center; font-size: 13px; font-weight: 700; color: {C_DARK_BLUE}; flex-wrap: wrap; gap: 10px;">
        <div style="background: #F0F4FA; padding: 10px 16px; border-radius: 8px; flex: 1;">
            <div style="color:{C_MAIN_BLUE}; font-size: 16px; margin-bottom:4px;">⚙️</div>
            Năng Lực AI (AI Capability) + Độ Sẵn Sàng (Readiness)<br>+ Quy Mô Kinh Tế (Economic Exposure)
        </div>
        <div style="color:{C_MAIN_BLUE}; font-size: 18px;">➔</div>
        <div style="background: #F0F4FA; padding: 10px 16px; border-radius: 8px; flex: 1;">
            <div style="color:{C_WARNING}; font-size: 16px; margin-bottom:4px;">📊</div>
            Điểm Ưu Tiên AI (AIPS)<br>+ Rủi Ro Chuyển Đổi (WTRS)
        </div>
        <div style="color:{C_MAIN_BLUE}; font-size: 18px;">➔</div>
        <div style="background: {C_DARK_BLUE}; color: white; padding: 10px 16px; border-radius: 8px; flex: 1;">
            <div style="font-size: 16px; margin-bottom:4px;">🚀</div>
            Chiến Lược Khuyến Nghị<br>(Workforce Strategy)
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. STRATEGIC OVERVIEW (KPI CARDS)
# ==============================================================================
st.markdown("""
<div class="section-header">
    <h3>Tổng Quan Chiến Lược (Strategic Overview)</h3>
</div>
""", unsafe_allow_html=True)

k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"""
    <div class="card-3d">
        <div class="kpi-label">Tổng Cơ Hội Kinh Tế (Economic Opportunity)</div>
        <div class="kpi-value">{df["EconomicExposure"].sum():.2f}</div>
        <div class="kpi-insight"><b>Phân tích:</b> Tổng mức giá trị kinh tế cốt lõi có tiềm năng được tối ưu hóa thông qua AI.</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="card-3d">
        <div class="kpi-label">Độ Sẵn Sàng Đầu Tư AI (Trung bình AIPS)</div>
        <div class="kpi-value" style="color:{C_MAIN_BLUE};">{df["AIPS"].mean():.3f}</div>
        <div class="kpi-insight"><b>Phân tích:</b> Điểm đánh giá trung bình về tiềm năng giá trị thu lại so với chi phí và nguồn lực triển khai.</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    high_risk_count = len(df[df["Risk_Level"] == 'High']) if "Risk_Level" in df.columns else 0
    st.markdown(f"""
    <div class="card-3d">
        <div class="kpi-label">Rủi Ro Chuyển Đổi (Transition Risk)</div>
        <div class="kpi-value" style="color:{C_DANGER};">{high_risk_count} <span style="font-size:16px;">Vị trí</span></div>
        <div class="kpi-insight"><b>Phân tích:</b> Số nhóm nghề (công việc) yêu cầu chính sách quản trị rủi ro chặt chẽ trước khi áp dụng AI.</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 5. ECONOMIC OPPORTUNITY MAP
# ==============================================================================
st.markdown("""
<div class="section-header">
    <h3>Bản Đồ Cơ Hội Kinh Tế (Economic Opportunity Map)</h3>
</div>
<div style="background: white; padding: 16px; border-radius: 8px; border-left: 4px solid #4274D9; margin-bottom: 20px; font-size: 14px;">
    <b>Mục tiêu:</b> Xác định các nhóm nghề có quy mô lao động lớn, giá trị kinh tế cao và sở hữu tiềm năng ứng dụng AI mạnh mẽ.<br>
    <ul>
        <li><b>Trục ngang (X):</b> Giá Trị Kinh Tế Cốt Lõi (Economic Value - PEI)</li>
        <li><b>Trục dọc (Y):</b> Độ Phơi Nhiễm Công Việc (Employment Exposure - WEI)</li>
        <li><b>Kích thước bong bóng:</b> Tổng Tác Động Kinh Tế (Economic Exposure)</li>
        <li><b>Màu sắc:</b> Định Hướng Chuyển Đổi (Workforce Strategy)</li>
    </ul>
</div>
""", unsafe_allow_html=True)

fig_landscape = px.scatter(
    df, x="PEI", y="WEI", size="EconomicExposure", color="Workforce_Strategy",
    hover_name="Occupation", hover_data={"AIPS": ":.3f", "WTRS": ":.3f"},
    color_discrete_map={"Deploy AI": C_MAIN_BLUE, "Reskill Workforce": C_DANGER, "Human-AI Collaboration": C_WARNING, "Human-led": "#8D99AE"},
    labels={
        "PEI": "Giá Trị Kinh Tế (Economic Value - PEI)", 
        "WEI": "Mức Phơi Nhiễm Công Việc (Employment Exposure - WEI)",
        "Workforce_Strategy": "Chiến Lược Nhân Sự"
    },
    size_max=45
)
fig_landscape.update_layout(height=450, template="plotly_white")
st.plotly_chart(fig_landscape, use_container_width=True)

# ==============================================================================
# 6 & 7. RANKING & TRANSFORMATION MATRIX
# ==============================================================================
col_left, col_right = st.columns([4, 6])

with col_left:
    st.markdown("""
    <div class="section-header" style="margin-top:0;">
        <h3>Bảng Xếp Hạng Ưu Tiên AI (Priority Ranking)</h3>
        <p>Danh sách các nhóm nghề tiềm năng nhất để triển khai thí điểm AI Agent hoặc Tự động hóa ngay lập tức.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hiển thị bảng xếp hạng
    top_jobs = df.sort_values(by="AIPS", ascending=False).head(8)
    # Đổi tên hiển thị cho dataframe 
    display_top_jobs = top_jobs[["Occupation", "AIPS"]].rename(columns={"Occupation": "Nghề Nghiệp"})
    st.dataframe(
        display_top_jobs.style.background_gradient(cmap="Blues", subset=["AIPS"]),
        use_container_width=True, height=350, hide_index=True
    )

with col_right:
    st.markdown("""
    <div class="section-header" style="margin-top:0;">
        <h3>Ma Trận Chiến Lược Chuyển Đổi Nguồn Nhân Lực (Transformation Matrix)</h3>
        <p>Phân loại chiến lược dựa vào Năng lực AI (Capability), Độ Sẵn Sàng (Readiness) và Tác Động Kinh Tế.</p>
    </div>
    <div style="font-size: 13px; margin-bottom: 15px; display: flex; gap: 15px; flex-wrap: wrap;">
        <div>🟢 <b>Triển khai AI (Deploy AI):</b> Tối đa hóa tự động hóa</div>
        <div>🟠 <b>Đào tạo lại (Reskill Workforce):</b> Bắt buộc tái đào tạo trước khi chuyển đổi</div>
        <div>🔵 <b>Hợp tác Người-AI (Human-AI Collab):</b> Sử dụng AI như trợ lý (Copilot)</div>
        <div>⚪ <b>Con người dẫn dắt (Human-led):</b> Bảo lưu vai trò cốt lõi của con người</div>
    </div>
    """, unsafe_allow_html=True)

    fig_matrix = px.scatter(
        df, x="Read", y="Cap", size="EconomicExposure", color="Workforce_Strategy",
        hover_name="Occupation",
        color_discrete_map={"Deploy AI": C_MAIN_BLUE, "Reskill Workforce": C_DANGER, "Human-AI Collaboration": C_WARNING, "Human-led": "#8D99AE"},
        labels={
            "Read": "Độ Sẵn Sàng Của Nhân Sự (Worker Readiness)", 
            "Cap": "Năng Lực Tự Động Hóa (AI Capability)"
        }
    )
    fig_matrix.add_vline(x=0.5, line_dash="dash", line_color="gray", opacity=0.5)
    fig_matrix.add_hline(y=0.65, line_dash="dash", line_color="gray", opacity=0.5)
    fig_matrix.update_layout(height=350, template="plotly_white", showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_matrix, use_container_width=True)

# ==============================================================================
# 8. EXECUTIVE QUICK LOOKUP (RECOMMENDATION TABLE)
# ==============================================================================
st.markdown("""
<div class="section-header">
    <h3>Tra Cứu Nhanh Cho Cấp Quản Lý (Executive Quick Lookup)</h3>
    <p>Bảng tổng hợp giúp Ban lãnh đạo nhanh chóng tra cứu định hướng hành động và đánh giá rủi ro cho từng nhóm nghề mà không cần rà soát qua biểu đồ trực quan.</p>
</div>
""", unsafe_allow_html=True)

# Bảng tổng hợp hành động
lookup_df = df[["Occupation", "Industry", "Workforce_Strategy", "Risk_Level", "Recommended_Action"]].copy()
lookup_df.rename(columns={
    "Occupation": "Nhóm Nghề (Occupation)", 
    "Industry": "Ngành (Industry)", 
    "Workforce_Strategy": "Chiến Lược Nhân Sự", 
    "Risk_Level": "Cấp Độ Rủi Ro (Risk)",
    "Recommended_Action": "Hành Động Khuyến Nghị"
}, inplace=True)

def style_strategy(val):
    colors = {"Deploy AI": "#E8F5E9", "Reskill Workforce": "#FFEBEE", "Human-AI Collaboration": "#FFF8E1", "Human-led": "#ECEFF1"}
    return f'background-color: {colors.get(val, "")}'

st.dataframe(
    lookup_df.style.map(style_strategy, subset=['Chiến Lược Nhân Sự']),
    use_container_width=True, hide_index=True, height=250
)

# ==============================================================================
# 9. EXECUTIVE DECISION INSIGHT
# ==============================================================================
st.markdown("""
<div class="insight-box">
    <h3 style="color: #0D47A1; margin-top: 0; margin-bottom: 12px; font-weight: 800; font-size: 18px;">
        💡 Thông Tin Chỉ Đạo (Executive Decision Insight)
    </h3>
    <p style="font-size: 15px; color: #1E3A8A; line-height: 1.6; margin: 0;">
        Kết quả phân tích cho thấy chiến lược áp dụng AI hiệu quả không chỉ phụ thuộc vào năng lực của công nghệ mà còn phụ thuộc mạnh mẽ vào <b>Mức độ sẵn sàng tiếp nhận (Readiness)</b> của lực lượng lao động. Để tối ưu hóa ROI, doanh nghiệp nên tập trung vào các nhóm nghề có <b>Quy mô kinh tế (Economic Exposure) cao và Rủi ro chuyển đổi (WTRS) thấp</b> nhằm tạo ra các "Thắng lợi nhanh" (Quick Wins). Đồng thời, đối với các nhóm có rủi ro thay thế cao, cần sớm kích hoạt các <b>Chương trình Tái đào tạo (Reskill Program)</b> nhằm đảm bảo quá trình chuyển đổi số diễn ra suôn sẻ và bền vững.
    </p>
</div>
""", unsafe_allow_html=True)
