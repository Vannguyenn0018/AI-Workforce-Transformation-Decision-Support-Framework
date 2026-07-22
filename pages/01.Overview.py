import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. CẤU HÌNH TRANG STREAMLIT & PALETTE MÀU THIẾT KẾ
# ==============================================================================
st.set_page_config(
    page_title="AI Workforce Transformation Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Brand Color Palette Definition
C_DARK_BLUE = "#293681"   # Primary Dark
C_MAIN_BLUE = "#4274D9"   # Primary Accent / Highlight
C_LIGHT_BLUE = "#95CCDD"  # Secondary Soft Accent
C_TEAL_BG    = "#D0E7E6"  # Light Tint / Subtle Fill
C_WHITE      = "#FFFFFF"
C_TEXT_DARK  = "#1E2342"

# ==============================================================================
# 2. CUSTOM CSS - THIẾT KẾ KHUNG 3D NỔI & BRANDING
# ==============================================================================
st.markdown(f"""
<style>
    /* Google Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: #F4F7FB;
        color: {C_TEXT_DARK};
    }}

    /* Title Styling */
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
        margin-top: 5px;
        margin-bottom: 0;
        font-size: 14px;
    }}

    /* CSS Khung Metric 3D Nổi (Neumorphic 3D Effect) */
    .card-3d {{
        background: {C_WHITE};
        border-radius: 16px;
        padding: 20px 22px;
        position: relative;
        /* Đổ bóng 3D nổi */
        box-shadow: 8px 8px 20px rgba(41, 54, 129, 0.08), 
                    -6px -6px 15px rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(149, 204, 221, 0.3);
        transition: all 0.3s ease;
        height: 100%;
    }}
    .card-3d:hover {{
        transform: translateY(-5px);
        box-shadow: 12px 12px 28px rgba(41, 54, 129, 0.15), 
                    -6px -6px 15px rgba(255, 255, 255, 1);
        border-color: {C_MAIN_BLUE};
    }}
    
    .kpi-label {{
        font-size: 13px;
        font-weight: 700;
        color: #6C757D;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}
    .kpi-value {{
        font-size: 32px;
        font-weight: 800;
        color: {C_DARK_BLUE};
        margin: 8px 0;
    }}
    .badge-3d {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
    }}
    .badge-danger {{ background-color: #FFE5E5; color: #D32F2F; border: 1px solid #FFCDD2; }}
    .badge-warning {{ background-color: #FFF8E1; color: #F57F17; border: 1px solid #FFE082; }}
    .badge-success {{ background-color: #E8F5E9; color: #2E7D32; border: 1px solid #A5D6A7; }}
    .badge-info {{ background-color: {C_TEAL_BG}; color: {C_DARK_BLUE}; border: 1px solid {C_LIGHT_BLUE}; }}

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
        padding: 16px 20px;
        box-shadow: 4px 6px 15px rgba(0,0,0,0.04);
        margin: 15px 0;
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
        line-height: 1.5;
    }}

    /* Custom Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 12px;
        background-color: transparent;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {C_WHITE};
        border-radius: 10px 10px 0 0;
        padding: 12px 20px;
        font-weight: 600;
        color: {C_DARK_BLUE};
        border: 1px solid rgba(149, 204, 221, 0.4);
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {C_DARK_BLUE} !important;
        color: {C_WHITE} !important;
        border-color: {C_DARK_BLUE} !important;
        box-shadow: 0 6px 12px rgba(41, 54, 129, 0.2) !important;
    }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. TẢI VÀ TÍNH TOÁN DỮ LIỆU
# ==============================================================================
def min_max_normalize(series):
    s_min, s_max = series.min(skipna=True), series.max(skipna=True)
    if pd.isna(s_min) or pd.isna(s_max) or s_max == s_min:
        return series * 0
    return (series - s_min) / (s_max - s_min)

@st.cache_data
def load_data():
    try:
        task_meta = pd.read_csv(r"C:\Users\HP\Downloads\master_data_task_level.csv")
        expert_cap = pd.read_csv(r"C:\Users\HP\Downloads\master_data_expert_ratings.csv")
        worker_desire = pd.read_csv(r"C:\Users\HP\Downloads\master_data_worker_desire.csv")
    except Exception:
        # Tạo dữ liệu giả định nếu không thấy file (để app luôn hiển thị thử nghiệm được)
        np.random.seed(42)
        occs = [
            ("13-2011.00", "Accountants and Auditors", "Finance & Accounting", 0.82, 0.78),
            ("13-2051.00", "Financial Analysts", "Finance & Accounting", 0.88, 0.82),
            ("15-1252.00", "Software Developers", "Information Technology", 0.92, 0.89),
            ("11-1021.00", "General Managers", "Management", 0.58, 0.91),
            ("41-2031.00", "Retail Salespersons", "Sales & Retail", 0.42, 0.35),
            ("29-1141.00", "Registered Nurses", "Healthcare", 0.31, 0.94),
            ("43-3031.00", "Bookkeeping & Auditing Clerks", "Finance & Accounting", 0.89, 0.45),
            ("15-1211.00", "Computer Systems Analysts", "Information Technology", 0.81, 0.72),
            ("13-1111.00", "Management Analysts", "Management", 0.73, 0.76),
            ("11-3031.00", "Financial Managers", "Finance & Accounting", 0.77, 0.83)
        ]
        task_rows, expert_rows, worker_rows = [], [], []
        tid = 1
        for soc, title, ind, emp, wage in occs:
            for _ in range(6):
                t_str = f"TASK-{tid}"
                tid += 1
                task_rows.append({"O*NET-SOC Code": soc, "Occupation (O*NET-SOC Title)": title, "Industry Group": ind, "Employment_norm": emp, "Wage_norm": wage, "Task ID": t_str, "Importance": np.random.uniform(2,5), "Importance_norm": np.random.uniform(0.3, 0.9)})
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
            "Importance_o_norm": Imp_o,
            "Task_Count": len(df_occ)
        })

    occ_df = task_summary.groupby([
        "O*NET-SOC Code", "Occupation (O*NET-SOC Title)",
        "Employment_norm", "Wage_norm", "Industry Group"
    ]).apply(aggregate_occ, include_groups=False).reset_index()

    occ_df.rename(columns={"Occupation (O*NET-SOC Title)": "Occupation"}, inplace=True)

    # Chuẩn hóa
    occ_df["Cap_norm"] = min_max_normalize(occ_df["Cap_o"])
    occ_df["Read_norm"] = min_max_normalize(occ_df["Read_o"])
    
    # Chỉ số Gap & Exposure
    occ_df["WFI"] = occ_df["Cap_norm"] - occ_df["Read_norm"]
    occ_df["WEI"] = occ_df["Employment_norm"] * occ_df["Cap_norm"]
    occ_df["PEI"] = occ_df["Wage_norm"] * occ_df["Cap_norm"]
    occ_df["CI"] = occ_df["Importance_o_norm"] * occ_df["Cap_norm"]

    occ_df['EconomicExposure'] = (occ_df['WEI'].fillna(0) + occ_df['PEI'].fillna(0) + occ_df['CI'].fillna(0)) / 3
    occ_df['AIPS'] = occ_df['Cap_norm'] * occ_df['Read_norm'] * occ_df['EconomicExposure']

    # Phân loại 4 Quadrants
    cap_med, read_med = occ_df["Cap_norm"].median(), occ_df["Read_norm"].median()
    def classify(r):
        if r["Cap_norm"] >= cap_med and r["Read_norm"] >= read_med:
            return "AI Adoption (Deploy AI)"
        elif r["Cap_norm"] >= cap_med and r["Read_norm"] < read_med:
            return "Workforce Transition (Reskill)"
        elif r["Cap_norm"] < cap_med and r["Read_norm"] >= read_med:
            return "Prepare & Wait"
        else:
            return "Human-led (Human-Centric)"

    occ_df["Quadrant"] = occ_df.apply(classify, axis=1)
    return occ_df

df = load_data()

# ==============================================================================
# HEADER BANNERS & BRANDING
# ==============================================================================
st.markdown(f"""
<div class="header-container">
    <h1>🤖 AI Workforce Transformation Executive Dashboard</h1>
    <p>Hệ thống Phân tích Chiến lược Năng lực AI, Mức độ Sẵn sàng Nhân sự & Mức độ Tác động Kinh tế</p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# BỘ TAB GIAO DIỆN HIỆN ĐẠI
# ==============================================================================
tab_overview, tab_matrix, tab_friction, tab_economic, tab_action = st.tabs([
    "📌 Executive Overview",
    "🎯 Transformation Matrix",
    "⚡ Friction & Gap Analysis",
    "💼 Economic Exposure",
    "🚀 Strategic Action Plan"
])

# Plotly Theme Settings
plotly_template = "plotly_white"
color_discrete_map = {
    "AI Adoption (Deploy AI)": C_MAIN_BLUE,
    "Workforce Transition (Reskill)": "#E63946", # Red
    "Prepare & Wait": C_LIGHT_BLUE,
    "Human-led (Human-Centric)": "#8D99AE"
}

# ------------------------------------------------------------------------------
# TAB 1: EXECUTIVE OVERVIEW
# ------------------------------------------------------------------------------
with tab_overview:
    st.markdown("### 📊 Tổng quan Chỉ số Cốt lõi (Executive KPIs)")
    
    avg_cap = df["Cap_norm"].mean()
    avg_read = df["Read_norm"].mean()
    avg_wfi = df["WFI"].mean()
    high_risk_count = len(df[(df["Cap_norm"] > 0.6) & (df["Read_norm"] < 0.4)])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="card-3d">
            <div class="kpi-label">AI Capacity (Cap)</div>
            <div class="kpi-value">{avg_cap:.2f}</div>
            <span class="badge-3d badge-info">Khả năng AI Cao</span>
            <div class="kpi-footer-insight">Mức độ tự động hóa công việc bằng AI đạt mức cao đáng kể.</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card-3d">
            <div class="kpi-label">Worker Readiness (Read)</div>
            <div class="kpi-value">{avg_read:.2f}</div>
            <span class="badge-3d badge-warning">Sẵn sàng Trung bình</span>
            <div class="kpi-footer-insight">Tốc độ tiếp nhận công nghệ của nhân sự đang tụt hậu hơn AI.</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card-3d">
            <div class="kpi-label">Avg Friction Index (WFI)</div>
            <div class="kpi-value">{avg_wfi:+.2f}</div>
            <span class="badge-3d badge-danger">Lệch pha (Gap)</span>
            <div class="kpi-footer-insight">Khoảng cách năng lực vs sẵn sàng tạo ra điểm nghẽn tổ chức.</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="card-3d">
            <div class="kpi-label">High Risk Transition</div>
            <div class="kpi-value">{high_risk_count} <span style="font-size:16px;">Nghề</span></div>
            <span class="badge-3d badge-danger">Rủi ro Phản kháng</span>
            <div class="kpi-footer-insight">Cần ưu tiên tái đào tạo (Reskill) trước khi áp dụng AI.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        st.markdown("#### 📈 Phân bổ Ngành theo Chỉ số Chuyển đổi AIPS")
        fig_aips = px.bar(
            df.groupby("Industry Group")["AIPS"].mean().reset_index().sort_values(by="AIPS", ascending=True),
            x="AIPS", y="Industry Group",
            orientation="h",
            color="AIPS",
            color_continuous_scale=[C_TEAL_BG, C_MAIN_BLUE, C_DARK_BLUE],
            title="Chỉ số Tác động Tổng hợp AIPS theo Ngành"
        )
        fig_aips.update_layout(height=380, template=plotly_template, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_aips, use_container_width=True)

    with col_right:
        st.markdown("#### 🧩 Cơ cấu Phân vùng Nhóm Nghề")
        quad_counts = df["Quadrant"].value_counts().reset_index()
        fig_pie = px.pie(
            quad_counts, values="count", names="Quadrant",
            color="Quadrant", color_discrete_map=color_discrete_map,
            hole=0.45
        )
        fig_pie.update_layout(height=380, template=plotly_template, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("""
    <div class="insight-box-3d">
        <h4>💡 Insight Lãnh đạo Executive Summary</h4>
        <p>• Dữ liệu cho thấy <b>Tài chính & CNTT</b> là hai khu vực chịu áp lực chuyển đổi lớn nhất. Rào cản chuyển đổi lớn nhất hiện nay không phải ở khía cạnh công nghệ (Cap score cao), mà nằm ở mức độ sẵn sàng và tâm lý lo ngại của lao động (WFI cao).</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 2: TRANSFORMATION MATRIX
# ------------------------------------------------------------------------------
with tab_matrix:
    st.markdown("### 🎯 Ma trận Tương quan Khả năng AI vs Mức độ Sẵn sàng (Quadrant Matrix)")
    
    cap_med = df["Cap_norm"].median()
    read_med = df["Read_norm"].median()

    fig_matrix = px.scatter(
        df,
        x="Cap_norm", y="Read_norm",
        color="Quadrant",
        size="EconomicExposure",
        hover_name="Occupation",
        hover_data=["Industry Group", "WFI"],
        color_discrete_map=color_discrete_map,
        labels={"Cap_norm": "Khả năng Tự động hóa AI (Cap_norm)", "Read_norm": "Sẵn sàng của Nhân sự (Read_norm)"}
    )

    # Thêm đường cắt Phân vùng Median
    fig_matrix.add_vline(x=cap_med, line_dash="dash", line_color=C_LIGHT_BLUE)
    fig_matrix.add_hline(y=read_med, line_dash="dash", line_color=C_LIGHT_BLUE)

    fig_matrix.update_layout(height=520, template=plotly_template)
    st.plotly_chart(fig_matrix, use_container_width=True)

    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""
        <div class="insight-box-3d">
            <h4>🟢 AI Adoption Zone (Cap Cao, Read Cao)</h4>
            <p>Các vị trí triển khai AI ngay lập tức. Nhân sự hào hứng tiếp nhận và công nghệ đã sẵn sàng. Tập trung tự động hóa mở rộng quy mô.</p>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="insight-box-3d" style="border-left-color: #E63946;">
            <h4>🔴 Workforce Transition Zone (Cap Cao, Read Thấp)</h4>
            <p><b>Vùng rủi ro cao:</b> AI có khả năng làm tốt nhưng nhân sự có tâm lý đề phòng/thiếu kỹ năng. Cần tập trung truyền thông Quản trị Thay đổi (Change Management) & Reskill.</p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 3: FRICTION & GAP ANALYSIS
# ------------------------------------------------------------------------------
with tab_friction:
    st.markdown("### ⚡ Phân tích Khoảng cách Ma sát Lao động (Worker Friction Index)")

    col_f1, col_f2 = st.columns([6, 4])
    
    with col_f1:
        top_wfi = df.sort_values(by="WFI", ascending=False).head(10)
        fig_wfi = px.bar(
            top_wfi,
            x="WFI", y="Occupation",
            orientation="h",
            color="WFI",
            color_continuous_scale=["#FFCDD2", "#D32F2F"],
            title="Top 10 Nghề có Khoảng cách Ma sát (WFI) Lớn Nhất"
        )
        fig_wfi.update_layout(yaxis=dict(autorange="reversed"), height=450, template=plotly_template)
        st.plotly_chart(fig_wfi, use_container_width=True)

    with col_f2:
        st.markdown("#### 🔍 Chi tiết Khoảng cách theo Nhóm Nghề")
        selected_occ = st.selectbox("Chọn nghề nghiệp để kiểm tra chi tiết:", df["Occupation"].unique())
        occ_detail = df[df["Occupation"] == selected_occ].iloc[0]

        fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=0.65,  # Thay bằng biến giá trị của bạn
    gauge={
        'axis': {'range': [0, 1]},  # Khoảng từ 0 đến 1 (hoặc 0 đến 100)
        'bar': {'color': "#293681"}, # Màu của thanh chỉ số
        'steps': [
            {'range': [0, 0.35], 'color': "#D0E7E6"},   # Thấp: [bắt đầu, kết thúc]
            {'range': [0.35, 0.70], 'color': "#95CCDD"}, # Trung bình
            {'range': [0.70, 1.0], 'color': "#4274D9"}   # Cao
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 0.8
        }
    }
))
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

        st.write(f"• **AI Capacity:** `{occ_detail['Cap_norm']:.2f}`")
        st.write(f"• **Worker Readiness:** `{occ_detail['Read_norm']:.2f}`")

    st.markdown(f"""
    <div class="insight-box-3d">
        <h4>📌 Nguyên nhân cốt lõi của WFI (Gap Analysis)</h4>
        <p>Chỉ số WFI dương cao thể hiện sự mất cân bằng giữa kỳ vọng tự động hóa của doanh nghiệp và sự chuẩn bị năng lực/tâm lý của người lao động, tạo ra nguy cơ suy giảm năng suất nếu ép buộc triển khai AI quá nhanh.</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 4: ECONOMIC EXPOSURE
# ------------------------------------------------------------------------------
with tab_economic:
    st.markdown("### 💼 Phân tích Tác động Kinh tế (Economic Exposure & Value at Stake)")

    ec1, ec2 = st.columns(2)
    with ec1:
        fig_e1 = px.scatter(
            df, x="Employment_norm", y="Cap_norm",
            size="Wage_norm", color="Industry Group",
            hover_name="Occupation",
            title="Quy mô Nhân sự (Employment) vs Năng lực AI (Cap)",
            color_discrete_sequence=[C_DARK_BLUE, C_MAIN_BLUE, C_LIGHT_BLUE, "#E63946", "#8D99AE"]
        )
        fig_e1.update_layout(height=420, template=plotly_template)
        st.plotly_chart(fig_e1, use_container_width=True)

    with ec2:
        fig_e2 = px.scatter(
            df, x="Wage_norm", y="Cap_norm",
            size="Employment_norm", color="Industry Group",
            hover_name="Occupation",
            title="Mức Lương (Wage Level) vs Năng lực AI (Cap)",
            color_discrete_sequence=[C_DARK_BLUE, C_MAIN_BLUE, C_LIGHT_BLUE, "#E63946", "#8D99AE"]
        )
        fig_e2.update_layout(height=420, template=plotly_template)
        st.plotly_chart(fig_e2, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box-3d">
        <h4>💰 Insight Giá trị Kinh tế</h4>
        <p>Các nhóm nghề có <b>Lương cao (Wage_norm)</b> và <b>Năng lực AI cao</b> đại diện cho cơ hội tối ưu hóa chi phí và nâng cao năng suất lớn nhất cho tổ chức. Trong khi đó, các nhóm nghề có quy mô nhân sự lớn đòi hỏi lộ trình chuyển đổi cẩn trọng để tránh xáo trộn quy mô lao động.</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 5: STRATEGIC ACTION PLAN
# ------------------------------------------------------------------------------
with tab_action:
    st.markdown("### 🚀 Khuyến nghị Lộ trình Chuyển đổi Khai phá AI")

    st.markdown("""
    | Nhóm Quadrant | Định hướng Chiến lược | Hành động Cụ thể (Action Items) | Đơn vị Phụ trách |
    | :--- | :--- | :--- | :--- |
    | **🟢 AI Adoption** | **Scale Fast (Tăng tốc)** | • Triển khai công cụ AI vào quy trình làm việc chuẩn hàng ngày.<br>• Tối ưu hóa năng suất và đo lường ROI. | Phòng Công nghệ / Operation |
    | **🔴 Workforce Transition** | **Reskill & Change Mgmt** | • Tổ chức các khóa đào tạo lại kỹ năng AI Copilot.<br>• Xây dựng chính sách an tâm tâm lý và giải tỏa lo ngại thay thế công việc. | Phòng Nhân sự (HR) / L&D |
    | **🔵 Prepare & Wait** | **Pilot & Monitor** | • Thử nghiệm các dự án AI nhỏ (Proof of Concept).<br>• Theo dõi sự trưởng thành của mô hình AI mới. | Bộ phận R&D / Innovation |
    | **⚪ Human-Led** | **Human First** | • Tập trung nâng cao các kỹ năng mềm, cảm xúc và tư duy chiến lược.<br>• Giữ con người làm trung tâm quyết định. | Ban Giám đốc / Leadership |
    """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📋 Lọc Danh sách Nghề nghiệp Ưu tiên Hành động")
    
    selected_quad = st.multiselect(
        "Lọc theo nhóm Quadrant:",
        options=df["Quadrant"].unique(),
        default=df["Quadrant"].unique()
    )
    
    filtered_df = df[df["Quadrant"].isin(selected_quad)][[
        "Occupation", "Industry Group", "Cap_norm", "Read_norm", "WFI", "AIPS", "Quadrant"
    ]].sort_values(by="WFI", ascending=False)

    st.dataframe(
        filtered_df.style.background_gradient(cmap="Blues", subset=["Cap_norm", "AIPS"])
                         .background_gradient(cmap="Reds", subset=["WFI"]),
        use_container_width=True,
        height=350
    )
