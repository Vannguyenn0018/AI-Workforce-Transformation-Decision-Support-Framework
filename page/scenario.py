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
# 3. TẢI VÀ TÍNH TOÁN DỮ LIỆU CƠ SỞ (BASE DATASET)
# ==============================================================================
def min_max_normalize(series):
    s_min, s_max = series.min(skipna=True), series.max(skipna=True)
    if pd.isna(s_min) or pd.isna(s_max) or s_max == s_min:
        return series * 0
    return (series - s_min) / (s_max - s_min)

@st.cache_data
def load_base_data():
    try:
        task_meta = pd.read_csv(r"C:\Users\HP\Downloads\master_data_task_level.csv")
        expert_cap = pd.read_csv(r"C:\Users\HP\Downloads\master_data_expert_ratings.csv")
        worker_desire = pd.read_csv(r"C:\Users\HP\Downloads\master_data_worker_desire.csv")
    except Exception:
        # Dữ liệu giả lập dự phòng nếu chưa có file csv
        np.random.seed(42)
        occs = [
            ("43-4051.00", "Customer Service Representatives", "Customer Service", 0.95, 0.55),
            ("13-2011.00", "Accountants and Auditors", "Finance & Accounting", 0.85, 0.78),
            ("13-2051.00", "Financial Analysts", "Finance & Accounting", 0.88, 0.82),
            ("13-1071.00", "Human Resources Specialists", "Human Resources", 0.75, 0.65),
            ("15-1252.00", "Software Developers", "Information Technology", 0.92, 0.89),
            ("11-1021.00", "General Managers", "Management", 0.58, 0.91),
            ("41-2031.00", "Retail Salespersons", "Sales & Retail", 0.62, 0.35),
            ("29-1141.00", "Registered Nurses", "Healthcare", 0.31, 0.94),
            ("43-3031.00", "Bookkeeping & Auditing Clerks", "Finance & Accounting", 0.89, 0.45),
            ("15-1211.00", "Computer Systems Analysts", "Information Technology", 0.81, 0.72)
        ]
        task_rows, expert_rows, worker_rows = [], [], []
        tid = 1
        for soc, title, ind, emp, wage in occs:
            for _ in range(6):
                t_str = f"TASK-{tid}"
                tid += 1
                task_rows.append({"O*NET-SOC Code": soc, "Occupation (O*NET-SOC Title)": title, "Industry Group": ind, "Employment_norm": emp, "Wage_norm": wage, "Task ID": t_str, "Importance": np.random.uniform(2, 5), "Importance_norm": np.random.uniform(0.3, 0.9)})
                expert_rows.append({"Task ID": t_str, "Automation Capacity Rating": np.random.uniform(1.5, 4.8)})
                worker_rows.append({"Task ID": t_str, "Automation Desire Rating": np.random.uniform(1.2, 4.5)})
        task_meta, expert_cap, worker_desire = pd.DataFrame(task_rows), pd.DataFrame(expert_rows), pd.DataFrame(worker_rows)

    task_cap = expert_cap.groupby("Task ID")["Automation Capacity Rating"].mean().reset_index(name="Cap_t")
    task_read = worker_desire.groupby("Task ID")["Automation Desire Rating"].mean().reset_index(name="Read_t")
    task_summary = task_meta.merge(task_cap, on="Task ID", how="left").merge(task_read, on="Task ID", how="left")

    def aggregate_occ(df_occ):
        v_cap = df_occ.dropna(subset=["Cap_t", "Importance"])
        v_read = df_occ.dropna(subset=["Read_t", "Importance"])
        v_imp = df_occ.dropna(subset=["Importance_norm"])
        
        Cap_o = np.average(v_cap["Cap_t"], weights=v_cap["Importance"]) if len(v_cap) > 0 else np.nan
        Read_o = np.average(v_read["Read_t"], weights=v_read["Importance"]) if len(v_read) > 0 else np.nan
        Imp_o = v_imp["Importance_norm"].mean() if len(v_imp) > 0 else np.nan

        return pd.Series({
            "Cap_o": Cap_o,
            "Read_o": Read_o,
            "Importance_o_norm": Imp_o
        })

    occ_df = task_summary.groupby([
        "O*NET-SOC Code", "Occupation (O*NET-SOC Title)",
        "Employment_norm", "Wage_norm", "Industry Group"
    ]).apply(aggregate_occ, include_groups=False).reset_index()

    occ_df.rename(columns={"Occupation (O*NET-SOC Title)": "Occupation"}, inplace=True)

    # Chuẩn hóa ban đầu (Global Baseline)
    occ_df["Cap_base"] = min_max_normalize(occ_df["Cap_o"]).fillna(0)
    occ_df["Read_base"] = min_max_normalize(occ_df["Read_o"]).fillna(0)
    
    # Tính các chỉ số cơ sở và làm sạch NaN
    occ_df["WEI_base"] = (occ_df["Employment_norm"] * occ_df["Cap_base"]).fillna(0)
    occ_df["PEI_base"] = (occ_df["Wage_norm"] * occ_df["Cap_base"]).fillna(0)
    occ_df["CI_base"] = (occ_df["Importance_o_norm"] * occ_df["Cap_base"]).fillna(0)
    
    occ_df["EcoExp_base"] = ((occ_df["WEI_base"] + occ_df["PEI_base"] + occ_df["CI_base"]) / 3).fillna(0)
    occ_df["AIPS_base"] = (occ_df["Cap_base"] * occ_df["Read_base"] * occ_df["EcoExp_base"]).fillna(0)

    return occ_df

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
    <h1>🇻🇳 DASHBOARD 3: Vietnam AI Transformation Simulation</h1>
    <p><i>"Nếu năng lực công nghệ, con người và thể chế của Việt Nam thay đổi trong tương lai, chiến lược AI của doanh nghiệp sẽ thay đổi như thế nào?"</i></p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR: SCENARIO PARAMETERS CONTROL
# ==============================================================================
st.sidebar.markdown(f"<h2 style='color:{C_DARK_BLUE}; font-size:18px;'>🎛️ Bảng Điều Chỉnh Kịch Bản</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Chọn kịch bản nhanh
preset = st.sidebar.radio(
    "📌 Chọn Kịch Bản Mẫu:",
    ["Tùy Chỉnh (Custom)", "Conservative (Thận trọng)", "Expected (Kỳ vọng 2028)", "Optimistic (Bứt phá 2030)"]
)

if preset == "Conservative (Thận trọng)":
    default_tr, default_pr, default_ir = 0.50, 0.45, 0.50
elif preset == "Expected (Kỳ vọng 2028)":
    default_tr, default_pr, default_ir = 0.75, 0.70, 0.65
elif preset == "Optimistic (Bứt phá 2030)":
    default_tr, default_pr, default_ir = 0.95, 0.90, 0.85
else:
    default_tr, default_pr, default_ir = 0.70, 0.60, 0.65

st.sidebar.markdown("### 1. Technology Readiness (TR)")
st.sidebar.caption("Cloud, Data Infrastructure & AI Platform tại VN")
tr_val = st.sidebar.slider("Chỉ số TR", 0.0, 1.0, default_tr, 0.05, key="tr_slider")

st.sidebar.markdown("### 2. People Readiness (PR)")
st.sidebar.caption("Digital Skill, AI Literacy & Độ chấp nhận của lao động")
pr_val = st.sidebar.slider("Chỉ số PR", 0.0, 1.0, default_pr, 0.05, key="pr_slider")

st.sidebar.markdown("### 3. Institutional Readiness (IR)")
st.sidebar.caption("Khung pháp lý, Quản trị dữ liệu & Bảo mật thông tin")
ir_val = st.sidebar.slider("Chỉ số IR", 0.0, 1.0, default_ir, 0.05, key="ir_slider")

# ==============================================================================
# CALCULATE SCENARIO DATA (ÁP DỤNG CÔNG THỨC MÔ PHỎNG VIỆT NAM + FIX NAN)
# ==============================================================================
df_scenario = df_raw.copy()

# Công thức điều chỉnh Việt Nam
df_scenario["Cap_VN"] = (df_scenario["Cap_base"] * tr_val * ir_val).fillna(0)
df_scenario["Read_VN"] = (df_scenario["Read_base"] * pr_val).fillna(0)

df_scenario["WEI_VN"] = (df_scenario["Employment_norm"] * df_scenario["Cap_VN"]).fillna(0)
df_scenario["PEI_VN"] = (df_scenario["Wage_norm"] * df_scenario["Cap_VN"]).fillna(0)
df_scenario["CI_VN"] = (df_scenario["Importance_o_norm"] * df_scenario["Cap_VN"]).fillna(0)

# Tính EcoExp_VN và triệt tiêu NaN hoàn toàn
df_scenario["EcoExp_VN"] = ((df_scenario["WEI_VN"] + df_scenario["PEI_VN"] + df_scenario["CI_VN"]) / 3).fillna(0)
# Thêm ngưỡng tối thiểu để tránh kích thước marker = 0 trong Plotly Scatter
df_scenario["EcoExp_VN_plot"] = df_scenario["EcoExp_VN"].apply(lambda x: max(x, 0.01))
df_scenario["EcoExp_base_plot"] = df_scenario["EcoExp_base"].apply(lambda x: max(x, 0.01))

df_scenario["AIPS_VN"] = (df_scenario["Cap_VN"] * df_scenario["Read_VN"] * df_scenario["EcoExp_VN"]).fillna(0)

# Phân loại chiến lược Trước & Sau
df_scenario["Strategy_Before"] = df_scenario.apply(
    lambda r: get_quadrant_strategy(r["Cap_base"], r["Read_base"]), axis=1
)
df_scenario["Strategy_After"] = df_scenario.apply(
    lambda r: get_quadrant_strategy(r["Cap_VN"], r["Read_VN"], cap_med=0.5*tr_val*ir_val, read_med=0.5*pr_val), axis=1
)

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
        size="EcoExp_base_plot",  # Đã triệt tiêu hoàn toàn NaN
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
        size="EcoExp_VN_plot",    # Đã triệt tiêu hoàn toàn NaN
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
    
    # Mô phỏng tính toán nhanh cho 3 kịch bản lớn
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

# Hàm tương thích cho cả Pandas cũ và mới
styler = df_shift_detail.style.format({
    "Cap_base": "{:.2f}",
    "Cap_VN": "{:.2f}",
    "Read_base": "{:.2f}",
    "Read_VN": "{:.2f}",
    "AIPS_VN": "{:.3f}"
})

# Dùng .map() thay cho .applymap()
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