import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. CẤU HÌNH TRANG & BẢNG MÀU THIẾT KẾ (BRAND PALETTE)
# ==============================================================================
st.set_page_config(
    page_title="Vietnam AI Transformation Simulator",
    page_icon="🇻🇳",
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

# ==============================================================================
# 2. STYLESHEET (KHUNG 3D NỔI & GIAO DIỆN HIỆN ĐẠI)
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
        margin-bottom: 25px;
    }}
    .header-container h1 {{
        color: white !important;
        font-weight: 800;
        margin: 0;
        font-size: 28px;
        letter-spacing: -0.5px;
    }}
    .header-container p {{
        color: {C_TEAL_BG};
        margin-top: 6px;
        margin-bottom: 0;
        font-size: 14px;
    }}

    /* Card 3D Nổi (Neumorphic 3D Effect) */
    .card-3d {{
        background: {C_WHITE};
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 8px 8px 20px rgba(41, 54, 129, 0.08), 
                    -6px -6px 15px rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(149, 204, 221, 0.3);
        transition: all 0.3s ease;
        height: 100%;
    }}
    .card-3d:hover {{
        transform: translateY(-3px);
        box-shadow: 12px 12px 28px rgba(41, 54, 129, 0.15), 
                    -6px -6px 15px rgba(255, 255, 255, 1);
        border-color: {C_MAIN_BLUE};
    }}
    
    .kpi-label {{
        font-size: 12px;
        font-weight: 700;
        color: #6C757D;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}
    .kpi-value {{
        font-size: 30px;
        font-weight: 800;
        color: {C_DARK_BLUE};
        margin: 6px 0;
    }}

    .badge-3d {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
    }}
    .badge-high {{ background-color: #E8F5E9; color: #2E7D32; border: 1px solid #A5D6A7; }}
    .badge-medium {{ background-color: #FFF8E1; color: #F57F17; border: 1px solid #FFE082; }}
    .badge-low {{ background-color: #FFE5E5; color: #D32F2F; border: 1px solid #FFCDD2; }}
    .badge-info {{ background-color: {C_TEAL_BG}; color: {C_DARK_BLUE}; border: 1px solid {C_LIGHT_BLUE}; }}

    /* Insight Banner 3D */
    .insight-box-3d {{
        background: linear-gradient(135deg, {C_WHITE} 0%, {C_TEAL_BG} 100%);
        border-left: 6px solid {C_MAIN_BLUE};
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 4px 6px 15px rgba(0,0,0,0.04);
        margin: 15px 0 25px 0;
    }}
    .insight-box-3d h4 {{
        color: {C_DARK_BLUE};
        margin: 0 0 6px 0;
        font-size: 15px;
        font-weight: 700;
    }}
    .insight-box-3d p {{
        margin: 0;
        font-size: 13px;
        color: {C_TEXT_DARK};
        line-height: 1.6;
    }}

    /* Sidebar Customization */
    .css-1d38150, [data-testid="stSidebar"] {{
        background-color: #FFFFFF !important;
        border-right: 1px solid {C_TEAL_BG};
    }}
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. TẢI DỮ LIỆU ĐÃ XỬ LÝ (SINGLE CONSOLIDATED FILE)
# ==============================================================================
@st.cache_data
def load_base_data():
    # Đọc file dữ liệu đã hợp nhất của bạn
    df = pd.read_csv("data/final_consolidated_output (1).csv")
    
    # Đổi tên các cột tương ứng với logic Simulation Engine bên dưới
    df = df.rename(columns={
        "Occupation (O*NET-SOC Title)": "Occupation",
        "Cap_norm": "Cap_base",
        "Read_norm": "Read_base",
        "EE": "EcoExp_base",
        "WEI_normalized": "WEI_base",
        "PEI_normalized": "PEI_base",
        "CI_normalized": "CI_base"
    })
    
    # Trích xuất ngược (reverse-engineer) các thông số employment_norm, wage_norm, importance_o_norm 
    # từ dữ liệu đã chuẩn hóa để tiếp tục dùng được cho các biến số thay đổi (Sliders).
    # Công thức gốc: WEI_base = Employment_norm * Cap_base -> Employment_norm = WEI_base / Cap_base
    df["Employment_norm"] = np.where(df["Cap_base"] > 0, df["WEI_base"] / df["Cap_base"], 0)
    df["Wage_norm"] = np.where(df["Cap_base"] > 0, df["PEI_base"] / df["Cap_base"], 0)
    df["Importance_o_norm"] = np.where(df["Cap_base"] > 0, df["CI_base"] / df["Cap_base"], 0)

    # Đảm bảo EcoExp_base không bị NA
    df["EcoExp_base"] = df["EcoExp_base"].fillna(0)
    df["AIPS_base"] = (df["Cap_base"] * df["Read_base"] * df["EcoExp_base"]).fillna(0)

    return df

df_raw = load_base_data()

# Hàm phân loại chiến lược dựa trên tọa độ Cap & Read
def get_quadrant_strategy(cap, read, cap_med=0.5, read_med=0.5):
    if cap >= cap_med and read >= read_med:
        return "Deploy AI"
    elif cap >= cap_med and read < read_med:
        return "Reskill Workforce"
    elif cap < cap_med and read >= read_med:
        return "Improve AI Tech"
    else:
        return "Human Role (Keep)"

# ==============================================================================
# HEADER BANNER
# ==============================================================================
st.markdown(f"""
<div class="header-container">
    <h1> Vietnam AI Transformation Simulation</h1>
    <p><i>"Nếu năng lực công nghệ, con người và thể chế của Việt Nam thay đổi trong tương lai, chiến lược AI của doanh nghiệp sẽ thay đổi như thế nào?"</i></p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR: SCENARIO PARAMETERS CONTROL (FIX TRỢ TỈNH TRẠNG KÉO/BẤM)
# ==============================================================================
st.sidebar.markdown(f"<h2 style='color:{C_DARK_BLUE}; font-size:18px;'>🎛️ Bảng Điều Chỉnh Kịch Bản</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# 1. Khởi tạo giá trị mặc định cho kịch bản nếu chưa có
if "preset_choice" not in st.session_state:
    st.session_state.preset_choice = "Tùy Chỉnh (Custom)"
if "tr_val" not in st.session_state:
    st.session_state.tr_val = 0.70
if "pr_val" not in st.session_state:
    st.session_state.pr_val = 0.60
if "ir_val" not in st.session_state:
    st.session_state.ir_val = 0.65

# 2. Radio chọn kịch bản mẫu
preset = st.sidebar.radio(
    "📌 Chọn Kịch Bản Mẫu:",
    ["Tùy Chỉnh (Custom)", "Conservative (Thận trọng)", "Expected (Kỳ vọng 2028)", "Optimistic (Bứt phá 2030)"],
    key="preset_choice"
)

# 3. Khi người dùng click chọn kịch bản mẫu, ta cập nhật lại giá trị và QUAN TRỌNG LÀ XÓA KEY CỦA SLIDER 
# để Streamlit bắt buộc phải vẽ lại slider với giá trị mới.
if preset != "Tùy Chỉnh (Custom)":
    if preset == "Conservative (Thận trọng)":
        new_tr, new_pr, new_ir = 0.50, 0.45, 0.50
    elif preset == "Expected (Kỳ vọng 2028)":
        new_tr, new_pr, new_ir = 0.75, 0.70, 0.65
    elif preset == "Optimistic (Bứt phá 2030)":
        new_tr, new_pr, new_ir = 0.95, 0.90, 0.85
    
    # Chỉ cập nhật nếu giá trị thay đổi để tránh lặp vô tận
    if st.session_state.tr_val != new_tr:
        st.session_state.tr_val = new_tr
        st.session_state.pr_val = new_pr
        st.session_state.ir_val = new_ir
        
        # Xóa các key của slider đi để Streamlit không bị khóa cứng trạng thái cũ
        for k in ["tr_slider", "pr_slider", "ir_slider"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

st.sidebar.markdown("### 1. Technology Readiness (TR)")
st.sidebar.caption("Cloud, Data Infrastructure & AI Platform tại VN")
tr_val = st.sidebar.slider("Chỉ số TR", 0.0, 1.0, value=st.session_state.tr_val, step=0.05, key="tr_slider")

st.sidebar.markdown("### 2. People Readiness (PR)")
st.sidebar.caption("Digital Skill, AI Literacy & Độ chấp nhận của lao động")
pr_val = st.sidebar.slider("Chỉ số PR", 0.0, 1.0, value=st.session_state.pr_val, step=0.05, key="pr_slider")

st.sidebar.markdown("### 3. Institutional Readiness (IR)")
st.sidebar.caption("Khung pháp lý, Quản trị dữ liệu & Bảo mật thông tin")
ir_val = st.sidebar.slider("Chỉ số IR", 0.0, 1.0, value=st.session_state.ir_val, step=0.05, key="ir_slider")

# Cập nhật ngược lại vào session_state để các phần khác trong app đọc được giá trị mới nhất
st.session_state.tr_val = tr_val
st.session_state.pr_val = pr_val
st.session_state.ir_val = ir_val


# ==============================================================================
# SCENARIO SIMULATION ENGINE V2
# AI Workforce Transformation Decision Support Model
# ==============================================================================

def simulate_ai_capability(base_cap, technology, institution):
    readiness_factor = 0.5 + 0.5 * technology * institution
    return (base_cap * readiness_factor).clip(0, 1)

def simulate_worker_readiness(base_read, people):
    readiness_factor = 0.6 + 0.4 * people
    return (base_read * readiness_factor).clip(0, 1)

def calculate_ai_investment_priority(row):
    return (
        0.4 * row["Cap_VN"] +
        0.3 * row["Read_VN"] +
        0.3 * row["EcoExp_VN"]
    )

def recommend_strategy(row):
    cap = row["Cap_VN"]
    read = row["Read_VN"]
    priority = row["AIPS_VN"]

    if cap >= 0.65 and read >= 0.60:
        return "Deploy AI"
    elif cap >= 0.65 and read < 0.60:
        return "Reskill Workforce"
    elif cap < 0.65 and priority >= 0.45:
        return "Improve AI Capability"
    else:
        return "Human-Centric Role"

def workforce_transition(row):
    before = row["Strategy_Before"]
    after = row["Strategy_After"]

    if before == after:
        return "Stable"
    elif after == "Deploy AI":
        return "AI Adoption Opportunity"
    elif after == "Reskill Workforce":
        return "Skill Transformation Required"
    elif after == "Human-Centric Role":
        return "Human Expertise Preserved"
    else:
        return "Technology Investment Needed"

# ==============================================================================
# APPLY SCENARIO MODEL
# ==============================================================================
df_scenario = df_raw.copy()

# 1. AI Capability Simulation
df_scenario["Cap_VN"] = simulate_ai_capability(df_scenario["Cap_base"], tr_val, ir_val)

# 2. Workforce Readiness Simulation
df_scenario["Read_VN"] = simulate_worker_readiness(df_scenario["Read_base"], pr_val)

# 3. Economic Impact
df_scenario["WEI_VN"] = df_scenario["Employment_norm"] * df_scenario["Cap_VN"]
df_scenario["PEI_VN"] = df_scenario["Wage_norm"] * df_scenario["Cap_VN"]
df_scenario["CI_VN"] = df_scenario["Importance_o_norm"] * df_scenario["Cap_VN"]
df_scenario["EcoExp_VN"] = df_scenario[["WEI_VN", "PEI_VN", "CI_VN"]].mean(axis=1)

# 4. AI Investment Priority Score
df_scenario["AIPS_VN"] = df_scenario.apply(calculate_ai_investment_priority, axis=1)

# 5. Strategy Classification
df_scenario["Strategy_Before"] = df_scenario.apply(lambda r: get_quadrant_strategy(r["Cap_base"], r["Read_base"]), axis=1)
df_scenario["Strategy_After"] = df_scenario.apply(recommend_strategy, axis=1)

# 6. Workforce Transition
df_scenario["Transformation_Status"] = df_scenario.apply(workforce_transition, axis=1)

# 7. Visualization Helper
df_scenario["EcoExp_VN_plot"] = df_scenario["EcoExp_VN"].clip(lower=0.01)
df_scenario["EcoExp_base_plot"] = df_scenario["EcoExp_base"].clip(lower=0.01)

# Ranking
df_rank = df_scenario.sort_values("AIPS_VN", ascending=False).reset_index(drop=True)
top_ai_jobs = df_rank.head(5)[["Occupation", "Industry Group", "AIPS_VN", "Strategy_After"]]

# ==============================================================================
# OVERVIEW CARDS (KPI DASHBOARD)
# ==============================================================================
c1, c2, c3, c4 = st.columns(4)

deploy_before = (df_scenario["Strategy_Before"] == "Deploy AI").sum()
deploy_after = (df_scenario["Strategy_After"] == "Deploy AI").sum()

with c1:
    st.markdown(f"""
    <div class="card-3d">
        <div class="kpi-label">Technology Readiness</div>
        <div class="kpi-value">{tr_val*100:.0f}%</div>
        <span class="badge-3d badge-info">Hạ Tầng Công Nghệ</span>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card-3d">
        <div class="kpi-label">People Readiness</div>
        <div class="kpi-value">{pr_val*100:.0f}%</div>
        <span class="badge-3d badge-high">Sẵn Sàng Sức Lao Động</span>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card-3d">
        <div class="kpi-label">Institutional Readiness</div>
        <div class="kpi-value">{ir_val*100:.0f}%</div>
        <span class="badge-3d badge-medium">Khung Pháp Lý & Thể Chế</span>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="card-3d">
        <div class="kpi-label">Số Nghề 'Deploy AI'</div>
        <div class="kpi-value">{deploy_before} ➔ <span style="color:{C_MAIN_BLUE};">{deploy_after}</span></div>
        <span class="badge-3d badge-high">Chuyển Dịch Chiến Lược</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# VISUALIZATION 1: BEFORE - AFTER TRANSFORMATION MATRIX
# ==============================================================================
st.subheader("1. Transformation Map: Before vs After Scenario Simulation")

col_fig1, col_fig2 = st.columns(2)

with col_fig1:
    fig_before = px.scatter(
        df_scenario,
        x="Read_base",
        y="Cap_base",
        color="Strategy_Before",
        hover_name="Occupation",
        size="EcoExp_base_plot",
        size_max=30,
        title="<b>BASELINE (Toàn Cầu / Hiện Tại)</b>",
        labels={"Read_base": "Worker Readiness", "Cap_base": "AI Capability"},
        color_discrete_map={
            "Deploy AI": C_MAIN_BLUE,
            "Reskill Workforce": "#E63946",
            "Improve AI Tech": C_LIGHT_BLUE,
            "Human Role (Keep)": "#8D99AE"
        }
    )
    fig_before.add_hline(y=0.5, line_dash="dash", line_color="gray")
    fig_before.add_vline(x=0.5, line_dash="dash", line_color="gray")
    fig_before.update_layout(height=420, template="plotly_white", showlegend=False)
    st.plotly_chart(fig_before, use_container_width=True)

with col_fig2:
    fig_after = px.scatter(
        df_scenario,
        x="Read_VN",
        y="Cap_VN",
        color="Strategy_After",
        hover_name="Occupation",
        size="EcoExp_VN_plot",
        size_max=30,
        title=f"<b>VIETNAM SIMULATION (TR={tr_val}, PR={pr_val}, IR={ir_val})</b>",
        labels={"Read_VN": "Readiness (VN)", "Cap_VN": "Capability (VN)"},
        color_discrete_map={
            "Deploy AI": C_MAIN_BLUE,
            "Reskill Workforce": "#E63946",
            "Improve AI Tech": C_LIGHT_BLUE,
            "Human Role (Keep)": "#8D99AE"
        }
    )
    fig_after.add_hline(y=0.5*tr_val*ir_val, line_dash="dash", line_color="gray")
    fig_after.add_vline(x=0.5*pr_val, line_dash="dash", line_color="gray")
    fig_after.update_layout(height=420, template="plotly_white")
    st.plotly_chart(fig_after, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# VISUALIZATION 2 & 3: STRATEGY SHIFT & 3 SCENARIO COMPARISON
# ==============================================================================
col_v2, col_v3 = st.columns([5, 5])

with col_v2:
    st.subheader("2. Dịch Chuyển Phân Bổ Chiến Lược (Strategy Shift)")
    
    df_shift_b = df_scenario["Strategy_Before"].value_counts().reset_index()
    df_shift_b.columns = ["Strategy", "Count"]
    df_shift_b["Stage"] = "1. Baseline (Trước)"

    df_shift_a = df_scenario["Strategy_After"].value_counts().reset_index()
    df_shift_a.columns = ["Strategy", "Count"]
    df_shift_a["Stage"] = "2. Vietnam Scenario (Sau)"

    df_shift_all = pd.concat([df_shift_b, df_shift_a])

    fig_shift = px.bar(
        df_shift_all,
        x="Strategy",
        y="Count",
        color="Stage",
        barmode="group",
        color_discrete_sequence=[C_LIGHT_BLUE, C_DARK_BLUE],
        labels={"Count": "Số Lượng Nghề Nghiệp", "Strategy": "Chiến Lược Chi Tiết"},
        title="So Sánh Số Lượng Nghề Nghiệp Theo Chiến Lược"
    )
    fig_shift.update_layout(height=400, template="plotly_white", legend=dict(orientation="h", y=1.15))
    st.plotly_chart(fig_shift, use_container_width=True)

with col_v3:
    st.subheader("3. So Sánh 3 Kịch Bản Lớn (Scenario Comparison)")
    
    scenarios_summary = [
        {"Kịch Bản": "Conservative", "Deploy AI": len(df_raw[(df_raw["Cap_base"]*0.5*0.5 >= 0.125) & (df_raw["Read_base"]*0.45 >= 0.1125)])},
        {"Kịch Bản": "Expected", "Deploy AI": len(df_raw[(df_raw["Cap_base"]*0.75*0.65 >= 0.125) & (df_raw["Read_base"]*0.70 >= 0.1125)])},
        {"Kịch Bản": "Optimistic", "Deploy AI": len(df_raw[(df_raw["Cap_base"]*0.95*0.85 >= 0.125) & (df_raw["Read_base"]*0.90 >= 0.1125)])},
    ]
    df_scen_comp = pd.DataFrame(scenarios_summary)
    
    fig_scen = px.bar(
        df_scen_comp,
        x="Kịch Bản",
        y="Deploy AI",
        text="Deploy AI",
        color="Kịch Bản",
        color_discrete_sequence=["#8D99AE", C_MAIN_BLUE, C_DARK_BLUE],
        title="Số Lượng Nghề Đạt Ngưỡng Triển Khai AI (Deploy AI)"
    )
    fig_scen.update_traces(textposition='outside')
    fig_scen.update_layout(height=400, template="plotly_white", showlegend=False)
    st.plotly_chart(fig_scen, use_container_width=True)

# ==============================================================================
# RECOMMENDATION ENGINE & BANG DỊCH CHUYỂN
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("🔍 Bảng Chi Tiết Dịch Chuyển Chiến Lược Nghề Nghiệp")

df_shift_detail = df_scenario[[
    "Occupation", "Industry Group", "Strategy_Before", "Strategy_After", 
    "Cap_base", "Cap_VN", "Read_base", "Read_VN", "AIPS_VN"
]].copy()

df_shift_detail["Trạng Thái Dịch Chuyển"] = np.where(
    df_shift_detail["Strategy_Before"] != df_shift_detail["Strategy_After"],
    "🔄 Có Dịch Chuyển", "➡️ Giữ Nguyên"
)

changed_jobs = df_shift_detail[df_shift_detail["Trạng Thái Dịch Chuyển"] == "🔄 Có Dịch Chuyển"]

styler = df_shift_detail.style.format({
    "Cap_base": "{:.2f}",
    "Cap_VN": "{:.2f}",
    "Read_base": "{:.2f}",
    "Read_VN": "{:.2f}",
    "AIPS_VN": "{:.3f}"
})

if hasattr(styler, "map"):
    styler = styler.map(
        lambda v: 'background-color: #E8F5E9; font-weight: bold;' if v == '🔄 Có Dịch Chuyển' else '', 
        subset=['Trạng Thái Dịch Chuyển']
    )
else:
    styler = styler.applymap(
        lambda v: 'background-color: #E8F5E9; font-weight: bold;' if v == '🔄 Có Dịch Chuyển' else '', 
        subset=['Trạng Thái Dịch Chuyển']
    )

st.dataframe(
    styler,
    use_container_width=True,
    height=360
)

# Executive Recommendation Output
st.markdown(f"""
<div class="insight-box-3d">
    <h4>💡 Khuyến Nghị Quản Trị Cuối Cùng (Executive Scenario Recommendation)</h4>
    <p>• <b>Insight Dịch Chuyển:</b> Khi môi trường Việt Nam thay đổi theo kịch bản hiện tại (TR={tr_val}, PR={pr_val}, IR={ir_val}), 
    có <b>{len(changed_jobs)}</b> nhóm nghề chuyển đổi trạng thái chiến lược trực tiếp.</p>
    <p>• <b>Ví dụ thực tế:</b> Nghề <i>'Accountants and Auditors'</i> hoặc <i>'Human Resources Specialists'</i> chuyển dịch từ 
    <b>'Reskill Workforce' (Đào tạo lại)</b> sang <b>'Deploy AI / AI-assisted' (Sẵn sàng triển khai AI)</b>.</p>
    <p>• <b>Thông điệp cốt lõi cho Lãnh Đạo:</b> Chiến lược AI của doanh nghiệp <b>không cố định</b> mà phụ thuộc hoàn toàn vào tốc độ trưởng thành hệ sinh thái (Công nghệ - Con người - Thể chế). Việc đẩy mạnh đầu tư hạ tầng dữ liệu và đào tạo AI literacy nội bộ sẽ giúp thu hẹp khoảng cách dịch chuyển này nhanh hơn 2–3 năm.</p>
</div>
""", unsafe_allow_html=True)
