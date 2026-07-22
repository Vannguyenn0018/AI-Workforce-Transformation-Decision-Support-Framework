import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. CẤU HÌNH TRANG & MA TRẬN MÀU THIẾT KẾ (BRAND PALETTE)
# ==============================================================================
st.set_page_config(
    page_title="Dashboard 2 — AI Investment & Workforce Transformation Strategy",
    page_icon="💰",
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

# ==============================================================================
# 2. STYLESHEET (KHUNG 3D NỔI & KHUNG LUỒNG DECISION FRAMEWORK)
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
        font-size: 25px;
        letter-spacing: -0.5px;
    }}
    .header-container p {{
        color: {C_TEAL_BG};
        margin-top: 6px;
        margin-bottom: 0;
        font-size: 14px;
    }}

    /* Framework Diagram Box */
    .framework-box {{
        background: {C_WHITE};
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 25px;
        border: 1px solid rgba(149, 204, 221, 0.4);
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }}
    .framework-title {{
        font-weight: 700;
        font-size: 13px;
        color: {C_DARK_BLUE};
        text-transform: uppercase;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }}

    /* Card 3D Nổi */
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
        transform: translateY(-4px);
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
        font-size: 32px;
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
    .badge-info {{ background-color: {C_TEAL_BG}; color: {C_DARK_BLUE}; border: 1px solid {C_LIGHT_BLUE}; }}
    .badge-danger {{ background-color: #FFEBEE; color: {C_DANGER}; border: 1px solid #FFCDD2; }}

    .kpi-footer-insight {{
        font-size: 12px;
        color: #555555;
        margin-top: 10px;
        border-top: 1px dashed {C_TEAL_BG};
        padding-top: 8px;
        font-style: italic;
    }}

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
        margin: 0 0 6px 0;
        font-size: 13px;
        color: {C_TEXT_DARK};
        line-height: 1.6;
    }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. TẢI VÀ XỬ LÝ DỮ LIỆU TỰ ĐỘNG (XỬ LÝ DỮ LIỆU MASTER_DATASET)
# ==============================================================================
def min_max_normalize(series):
    s_min, s_max = series.min(skipna=True), series.max(skipna=True)
    if pd.isna(s_min) or pd.isna(s_max) or s_max == s_min:
        return series * 0
    return (series - s_min) / (s_max - s_min)

@st.cache_data
def load_data():
    try:
        # Tải từ master_dataset.csv theo mô tả dataset
        df_raw = pd.read_csv("master_dataset.csv")
    except Exception:
        # Tạo Mock Dataset chuẩn hóa nếu chưa sẵn file master_dataset.csv local
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
            ("43-3031.00", "Bookkeeping & Payroll Clerks", "Finance & Accounting", 0.89, 0.45),
            ("15-1211.00", "Computer Systems Analysts", "Information Technology", 0.81, 0.72),
            ("43-9061.00", "Data Entry Clerks", "Administrative Support", 0.90, 0.80)
        ]
        task_rows, expert_rows, worker_rows = [], [], []
        tid = 1
        for soc, title, ind, emp, wage in occs:
            for _ in range(6):
                t_str = f"TASK-{tid}"
                tid += 1
                if title in ["Data Entry Clerks", "Customer Service Representatives"]:
                    cap_val, read_val = np.random.uniform(4.0, 5.0), np.random.uniform(4.0, 5.0)
                elif title in ["Accountants and Auditors", "Bookkeeping & Payroll Clerks"]:
                    cap_val, read_val = np.random.uniform(3.8, 4.8), np.random.uniform(1.0, 2.2)
                else:
                    cap_val, read_val = np.random.uniform(1.5, 4.8), np.random.uniform(1.2, 4.5)
                
                task_rows.append({"O*NET-SOC Code": soc, "Occupation": title, "Industry Group": ind, "Employment_norm": emp, "Wage_norm": wage, "Task ID": t_str, "Importance": np.random.uniform(2, 5), "Importance_norm": np.random.uniform(0.3, 0.9)})
                expert_rows.append({"Task ID": t_str, "Cap": cap_val})
                worker_rows.append({"Task ID": t_str, "Read": read_val})
        
        task_meta, expert_cap, worker_desire = pd.DataFrame(task_rows), pd.DataFrame(expert_rows), pd.DataFrame(worker_rows)
        task_cap = expert_cap.groupby("Task ID")["Cap"].mean().reset_index()
        task_read = worker_desire.groupby("Task ID")["Read"].mean().reset_index()
        task_summary = task_meta.merge(task_cap, on="Task ID").merge(task_read, on="Task ID")

        def aggregate_occ(df_occ):
            return pd.Series({
                "Cap_o": np.average(df_occ["Cap"], weights=df_occ["Importance"]),
                "Read_o": np.average(df_occ["Read"], weights=df_occ["Importance"]),
                "Importance_norm": df_occ["Importance_norm"].mean()
            })

        df_raw = task_summary.groupby(["O*NET-SOC Code", "Occupation", "Employment_norm", "Wage_norm", "Industry Group"]).apply(aggregate_occ, include_groups=False).reset_index()

    # Chuẩn hóa biến (Cap, Read) về scale (0 - 1)
    if "Cap_norm" not in df_raw.columns:
        df_raw["Cap"] = min_max_normalize(df_raw["Cap_o"] if "Cap_o" in df_raw.columns else df_raw["Cap"])
        df_raw["Read"] = min_max_normalize(df_raw["Read_o"] if "Read_o" in df_raw.columns else df_raw["Read"])
    else:
        df_raw["Cap"] = df_raw["Cap_norm"]
        df_raw["Read"] = df_raw["Read_norm"]

    # 1. Tính toán Derived Metrics: WEI, PEI, CI
    df_raw["WEI"] = df_raw["Employment_norm"] * df_raw["Cap"]
    df_raw["PEI"] = df_raw["Wage_norm"] * df_raw["Cap"]
    df_raw["CI"]  = df_raw["Importance_norm"] * df_raw["Cap"]

    # 2. Economic Exposure = (WEI + PEI + CI) / 3
    df_raw["EconomicExposure"] = (df_raw["WEI"] + df_raw["PEI"] + df_raw["CI"]) / 3

    # 3. AI Prioritization Score (AIPS) = Cap * Read * EconomicExposure
    df_raw["AIPS"] = df_raw["Cap"] * df_raw["Read"] * df_raw["EconomicExposure"]

    # 4. Workforce Transition Risk Score (WTRS) = Cap * (1 - Read) * EconomicExposure
    df_raw["WTRS"] = df_raw["Cap"] * (1 - df_raw["Read"]) * df_raw["EconomicExposure"]

    # Phân loại AIPS Category (High, Medium, Low Priority)
    p70, p35 = df_raw["AIPS"].quantile(0.7), df_raw["AIPS"].quantile(0.35)
    def cat_aips(val):
        if val >= p70: return "High Priority"
        elif val >= p35: return "Medium Priority"
        else: return "Low Priority"
    df_raw["AIPS_Category"] = df_raw["AIPS"].apply(cat_aips)

    # 5. Workforce Transformation Decision Engine Rules
    def decision_engine(r):
        # 1. Deploy AI: Cap cao, Read cao, WTRS thấp
        if r["Cap"] >= 0.65 and r["Read"] >= 0.55 and r["WTRS"] < 0.3:
            return "Deploy AI"
        # 2. Reskill Workforce: Cap cao, Read thấp, WTRS cao
        elif r["Cap"] >= 0.65 and (r["Read"] < 0.55 or r["WTRS"] >= 0.3):
            return "Reskill Workforce"
        # 3. Human-AI Collaboration: Cap trung bình, CI cao
        elif 0.35 <= r["Cap"] < 0.65 and r["CI"] >= 0.3:
            return "Human-AI Collaboration"
        # 4. Human-led: Cap thấp
        else:
            return "Human-led"

    df_raw["Workforce_Strategy"] = df_raw.apply(decision_engine, axis=1)

    return df_raw

df = load_data()

# ==============================================================================
# HEADER BANNER & FRAMEWORK SUMMARY
# ==============================================================================
st.markdown(f"""
<div class="header-container">
    <h1>DASHBOARD 2 — ECONOMY</h1>
    <h3 style="color: {C_TEAL_BG}; margin-top:4px; font-weight:600; font-size:18px;">AI Investment & Workforce Transformation Strategy</h3>
    <p style="margin-top:8px;"><i>"Trong hàng trăm nhóm nghề khác nhau, doanh nghiệp nên ưu tiên triển khai AI Agent vào đâu để tạo ra giá trị kinh tế lớn nhất — và sau đó cần điều chỉnh lực lượng lao động như thế nào?"</i></p>
</div>
""", unsafe_allow_html=True)

# Hiển thị sơ đồ luồng Framework Decision Layer
st.markdown(f"""
<div class="framework-box">
    <div class="framework-title">⚙️ Sơ đồ Luồng Decision Layer trong Framework</div>
    <div style="display: flex; justify-content: space-between; align-items: center; text-align: center; font-size: 12px; font-weight: 600; color: {C_DARK_BLUE}; flex-wrap: wrap; gap: 8px;">
        <div style="background: #F0F4FA; padding: 8px 12px; border-radius: 8px;">1. AI Capability (Cap)</div>
        <div>+</div>
        <div style="background: #F0F4FA; padding: 8px 12px; border-radius: 8px;">2. Worker Readiness (Read)</div>
        <div>+</div>
        <div style="background: #F0F4FA; padding: 8px 12px; border-radius: 8px;">3. Economic Exposure</div>
        <div>➔</div>
        <div style="background: {C_TEAL_BG}; padding: 8px 12px; border-radius: 8px; font-weight: 800;">AI Prioritization Score (AIPS)</div>
        <div>➔</div>
        <div style="background: #FFCDD2; color: {C_DANGER}; padding: 8px 12px; border-radius: 8px; font-weight: 800;">Workforce Risk (WTRS)</div>
        <div>➔</div>
        <div style="background: {C_DARK_BLUE}; color: white; padding: 8px 14px; border-radius: 8px; font-weight: 800;">Workforce Strategy</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# SECTION 1: LAYOUT TỔNG THỂ - KPI CARDS (3 CHỈ SỐ MỤC TIÊU)
# ==============================================================================
total_exposure = df["EconomicExposure"].sum()
avg_aips = df["AIPS"].mean()
high_risk_count = len(df[df["WTRS"] >= 0.3])

k1, k2, k3 = st.columns(3)

with k1:
    st.markdown(f"""
    <div class="card-3d">
        <div class="kpi-label">Total Economic Exposure</div>
        <div class="kpi-value">{total_exposure:.2f}</div>
        <span class="badge-3d badge-info">Tổng Tác Động Kinh Tế</span>
        <div class="kpi-footer-insight">Tác động giá trị kinh tế tổng hợp từ WEI, PEI và CI.</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="card-3d">
        <div class="kpi-label">Average AIPS</div>
        <div class="kpi-value">{avg_aips:.3f}</div>
        <span class="badge-3d badge-high">Điểm Ưu Tiên Đầu Tư TB</span>
        <div class="kpi-footer-insight">Mức độ sẵn sàng đầu tư AI trung bình toàn bộ nhóm nghề.</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="card-3d">
        <div class="kpi-label">High Risk Jobs (WTRS ≥ 0.3)</div>
        <div class="kpi-value">{high_risk_count} <span style="font-size:16px;">Occupations</span></div>
        <span class="badge-3d badge-danger">Rủi Ro Chuyển Đổi Cao</span>
        <div class="kpi-footer-insight">Số nhóm nghề gặp rủi ro kháng cự nhân sự cao khi triển khai AI.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# VISUALIZATION 1: ECONOMIC OPPORTUNITY BUBBLE CHART
# ==============================================================================
st.subheader("1. Economic Opportunity Map (Employment vs Wage)")

fig_bubble = px.scatter(
    df,
    x="Wage_norm",
    y="Employment_norm",
    size="EconomicExposure",
    color="AIPS_Category",
    hover_name="Occupation",
    hover_data={
        "Industry Group": True,
        "AIPS": ":.3f",
        "WTRS": ":.3f",
        "EconomicExposure": ":.3f",
        "Workforce_Strategy": True
    },
    color_discrete_map={
        "High Priority": C_MAIN_BLUE,
        "Medium Priority": C_LIGHT_BLUE,
        "Low Priority": "#8D99AE"
    },
    labels={
        "Employment_norm": "Quy Mô Lao Động (Employment Size)",
        "Wage_norm": "Mức Lương / Giá Trị (Annual Wage)",
        "EconomicExposure": "Economic Exposure",
        "AIPS_Category": "Mức Độ Ưu Tiên"
    },
    size_max=45,
    title="Phân Bố Giá Trị Kinh Tế Theo Quy Mô Lao Động & Mức Lương"
)

fig_bubble.update_layout(
    height=460,
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_bubble, use_container_width=True)

# Insight Mẫu Visualization 1
st.markdown("""
<div class="insight-box-3d">
    <h4>💡 Key Insight — Economic Opportunity Map</h4>
    <p>Một số nhóm nghề có <b>AI Capability cao</b> nhưng <b>quy mô lao động thấp</b> nên chưa tạo ra tác động kinh tế tổng thể quá lớn. Ngược lại, nhóm nghề có lực lượng lao động lớn và mức tự động hóa cao (như <i>Customer Service</i> hay <i>Accounting</i>) cần được ưu tiên đánh giá hàng đầu để tối ưu hóa ROI.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# VISUALIZATION 2 & 3: RANKING & WORKFORCE TRANSFORMATION MATRIX
# ==============================================================================
col_v2, col_v3 = st.columns([5, 5])

with col_v2:
    # Visualization 2: AI Investment Ranking
    st.subheader("2. Top AI Investment Ranking (AIPS)")
    
    top10_aips = df.sort_values(by="AIPS", ascending=False).head(10)
    
    fig_rank = px.bar(
        top10_aips,
        x="AIPS",
        y="Occupation",
        orientation="h",
        color="AIPS",
        color_continuous_scale=[C_TEAL_BG, C_MAIN_BLUE, C_DARK_BLUE],
        labels={"AIPS": "Chỉ số AIPS", "Occupation": "Nghề Nghiệp"},
        title="Top 10 Nhóm Nghề Nên Thử Nghiệm Ngân Sách AI Trước"
    )
    
    fig_rank.update_layout(
        yaxis=dict(autorange="reversed"),
        height=450,
        template="plotly_white",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_rank, use_container_width=True)

with col_v3:
    # Visualization 3: Workforce Transformation Matrix
    st.subheader("3. Workforce Transformation Matrix")
    
    fig_matrix = px.scatter(
        df,
        x="Read",
        y="Cap",
        size="EconomicExposure",
        color="Workforce_Strategy",
        hover_name="Occupation",
        hover_data={"WTRS": ":.3f", "AIPS": ":.3f"},
        color_discrete_map={
            "Deploy AI": C_MAIN_BLUE,
            "Reskill Workforce": C_DANGER,
            "Human-AI Collaboration": "#F57F17",
            "Human-led": "#8D99AE"
        },
        labels={
            "Read": "Sẵn Sàng Nhân Sự (Worker Readiness)",
            "Cap": "Năng Lực AI (AI Capability)",
            "Workforce_Strategy": "Chiến Lược Nhân Sự"
        },
        title="Ma Trận Định Hướng Xử Lý Lực Lượng Lao Động"
    )

    # Đường phân vùng ma trận
    fig_matrix.add_vline(x=0.55, line_dash="dash", line_color="gray")
    fig_matrix.add_hline(y=0.65, line_dash="dash", line_color="gray")

    fig_matrix.update_layout(
        height=450,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3)
    )
    st.plotly_chart(fig_matrix, use_container_width=True)

# ==============================================================================
# SECTION 7: RECOMMENDATION TABLE & FINAL OUTPUT
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📋 Recommendation Table & Workforce Strategy Roadmap")

# Chuẩn bị Bảng kết quả tổng hợp
display_df = df.sort_values(by="AIPS", ascending=False).copy()

display_table = display_df[[
    "Occupation", "Industry Group", "AIPS", "WTRS", "Cap", "Read", 
    "EconomicExposure", "Workforce_Strategy"
]].rename(columns={
    "Occupation": "Occupation",
    "Industry Group": "Industry",
    "AIPS": "AIPS",
    "WTRS": "WTRS",
    "Cap": "AI Cap",
    "Read": "Worker Read",
    "EconomicExposure": "Eco Exposure",
    "Workforce_Strategy": "Strategy"
})

# Filter theo ngành
industries = ["Tất cả"] + list(df["Industry Group"].unique())
selected_ind = st.selectbox("🎯 Lọc theo Ngành:", industries)

if selected_ind != "Tất cả":
    display_table = display_table[display_table["Industry"] == selected_ind]

# Format hiển thị bảng
st.dataframe(
    display_table.style.format({
        "AIPS": "{:.3f}",
        "WTRS": "{:.3f}",
        "AI Cap": "{:.2f}",
        "Worker Read": "{:.2f}",
        "Eco Exposure": "{:.2f}"
    }).background_gradient(cmap="Blues", subset=["AIPS"])
      .background_gradient(cmap="Reds", subset=["WTRS"]),
    use_container_width=True,
    height=360
)

# Output Khuyến nghị Executive dành cho Nhà Quản trị
st.markdown("---")
st.subheader("🚀 Output Khuyến Nghị Dành Cho Lãnh Đạo (Executive Conclusion)")

# Tìm ví dụ tiêu biểu đại diện (Accountant hoặc Vị trí Top 1)
acc_row = df[df["Occupation"].str.contains("Accountant", case=False, na=False)]
if not acc_row.empty:
    sample = acc_row.iloc[0]
else:
    sample = display_df.iloc[0]

st.markdown(f"""
<div class="insight-box-3d">
    <h4>📌 Ví Dụ Phân Tích Thực Tế: Case Study [{sample['Occupation']}]</h4>
    <p>• <b>Chỉ số AIPS:</b> <span style="color:{C_DARK_BLUE}; font-weight:700;">{sample['AIPS']:.2f}</span> (Mức độ ưu tiên triển khai cao).</p>
    <p>• <b>Chỉ số Rủi Ro WTRS:</b> <span style="color:{C_DANGER}; font-weight:700;">{sample['WTRS']:.2f}</span> (Đạt ngưỡng rủi ro kháng cự chuyển đổi lớn).</p>
    <p>• <b>Kết luận & Hành động:</b> <i>"Nhóm nghề <b>{sample['Occupation']}</b> có tiềm năng triển khai AI rất cao nhờ giá trị kinh tế lớn (Exposure = {sample['EconomicExposure']:.2f}), tuy nhiên tồn tại rủi ro chuyển đổi nhân lực lớn do tâm lý sẵn sàng của nhân sự còn thấp (Read = {sample['Read']:.2f}). Doanh nghiệp nên áp dụng mô hình <b>Human-AI Collaboration ({sample['Workforce_Strategy']})</b> kết hợp chương trình <b>Reskill đào tạo lại nhân lực</b> trước khi tự động hóa toàn phần."</i></p>
</div>
""", unsafe_allow_html=True)