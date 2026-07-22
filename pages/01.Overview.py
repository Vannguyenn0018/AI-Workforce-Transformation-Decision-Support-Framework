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

# Brand Color Palette
C_DARK_BLUE = "#293681"
C_MAIN_BLUE = "#4274D9"
C_LIGHT_BLUE = "#95CCDD"
C_TEAL_BG    = "#D0E7E6"
C_WHITE      = "#FFFFFF"
C_TEXT_DARK  = "#1E2342"

# ==============================================================================
# 2. CUSTOM CSS - THIẾT KẾ KHUNG 3D NỔI & BRANDING
# ==============================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: #F4F7FB;
        color: {C_TEXT_DARK};
    }}
    .header-container {{
        background: linear-gradient(135deg, {C_DARK_BLUE} 0%, {C_MAIN_BLUE} 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        box-shadow: 0 10px 25px rgba(41, 54, 129, 0.25);
        margin-bottom: 25px;
    }}
    .header-container h1 {{
        color: white !important; font-weight: 800; margin: 0; font-size: 28px;
    }}
    .header-container p {{
        color: {C_TEAL_BG}; margin-top: 5px; margin-bottom: 0; font-size: 14px;
    }}
    .card-3d {{
        background: {C_WHITE}; border-radius: 16px; padding: 20px 22px;
        box-shadow: 8px 8px 20px rgba(41, 54, 129, 0.08), -6px -6px 15px rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(149, 204, 221, 0.3); transition: all 0.3s ease; height: 100%;
    }}
    .card-3d:hover {{
        transform: translateY(-5px);
        box-shadow: 12px 12px 28px rgba(41, 54, 129, 0.15), -6px -6px 15px rgba(255, 255, 255, 1);
        border-color: {C_MAIN_BLUE};
    }}
    .kpi-label {{ font-size: 13px; font-weight: 700; color: #6C757D; text-transform: uppercase; }}
    .kpi-value {{ font-size: 32px; font-weight: 800; color: {C_DARK_BLUE}; margin: 8px 0; }}
    .badge-3d {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; }}
    .badge-danger {{ background-color: #FFE5E5; color: #D32F2F; border: 1px solid #FFCDD2; }}
    .badge-warning {{ background-color: #FFF8E1; color: #F57F17; border: 1px solid #FFE082; }}
    .badge-success {{ background-color: #E8F5E9; color: #2E7D32; border: 1px solid #A5D6A7; }}
    .badge-info {{ background-color: {C_TEAL_BG}; color: {C_DARK_BLUE}; border: 1px solid {C_LIGHT_BLUE}; }}
    .kpi-footer-insight {{ font-size: 12px; color: #555555; margin-top: 10px; border-top: 1px dashed {C_TEAL_BG}; padding-top: 8px; font-style: italic; }}
    .insight-box-3d {{
        background: linear-gradient(135deg, {C_WHITE} 0%, {C_TEAL_BG} 100%);
        border-left: 6px solid {C_MAIN_BLUE}; border-radius: 12px; padding: 16px 20px;
        box-shadow: 4px 6px 15px rgba(0,0,0,0.04); margin: 15px 0;
    }}
    .insight-box-3d h4 {{ color: {C_DARK_BLUE}; margin: 0 0 6px 0; font-size: 15px; font-weight: 700; }}
    .insight-box-3d p {{ margin: 0; font-size: 13px; line-height: 1.5; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 12px; background-color: transparent; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {C_WHITE}; border-radius: 10px 10px 0 0; padding: 12px 20px; font-weight: 600;
        color: {C_DARK_BLUE}; border: 1px solid rgba(149, 204, 221, 0.4); box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {C_DARK_BLUE} !important; color: {C_WHITE} !important;
        border-color: {C_DARK_BLUE} !important; box-shadow: 0 6px 12px rgba(41, 54, 129, 0.2) !important;
    }}
    /* Bổ sung CSS cho Playbook cards ở Tab 5 */
    .playbook-card {{ background: white; border-radius: 10px; padding: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); height: 100%; border-top: 4px solid transparent; }}
    .playbook-card.deploy {{ border-top-color: #1E88E5; }}
    .playbook-card.reskill {{ border-top-color: #E63946; }}
    .playbook-card.collab {{ border-top-color: #43A047; }}
    .playbook-card.monitor {{ border-top-color: #757575; }}
    .playbook-card h4 {{ margin-top: 0; font-size: 16px; color: {C_TEXT_DARK}; }}
    .playbook-tag {{ font-size: 12px; font-weight: 600; color: #666; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #eee; }}
    .playbook-card ul {{ padding-left: 20px; font-size: 13px; margin-bottom: 0; }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. TẢI VÀ XỬ LÝ DỮ LIỆU TỪ FILE CSV
# ==============================================================================
@st.cache_data
def load_data():
    try:
        # Đọc dữ liệu trực tiếp từ file (vui lòng đảm bảo file chung thư mục với script)
        df = pd.read_csv(r"C:\Users\HP\Downloads\final_consolidated_output (1).csv", encoding="utf-8")
        
        # 1. Mapping tên cột từ file sang format của source code
        rename_columns = {
            "Occupation (O*NET-SOC Title)": "Occupation",
            "EE": "EconomicExposure", 
            "WEI_normalized": "WEI_norm",
            "PEI_normalized": "PEI_norm",
            "wfi": "WFI" # Sử dụng luôn wfi đã có trong file
        }
        df = df.rename(columns=rename_columns)
        
        # 2. Sử dụng Quadrant có sẵn và map lại nhãn để đồng bộ với UI
        quadrant_map = {
            'Q1: Deploy AI Now': 'AI Adoption (Deploy AI)',
            'Q2: Reskill Workforce': 'Workforce Transition (Reskill)',
            'Q3: Prepare & Wait': 'Prepare & Wait',
            'Q4: Human-Centric': 'Human-led (Human-Centric)'
        }
        if "Quadrant" in df.columns:
            df["Quadrant"] = df["Quadrant"].map(quadrant_map).fillna(df["Quadrant"])

        # 3. Xác định Decision_Strategy cho TAB 5 dựa vào AIPS và WTRS (các chỉ số này đã tồn tại sẵn trong file)
        aips_med = df["AIPS"].median()
        wtrs_med = df["WTRS"].median()
        
        def classify_decision(r):
            if r["AIPS"] >= aips_med and r["WTRS"] >= wtrs_med:
                return "Strategic Priority" # High AIPS, High WTRS -> Reskill first
            elif r["AIPS"] >= aips_med and r["WTRS"] < wtrs_med:
                return "AI Opportunity" # High AIPS, Low WTRS -> Quick deploy
            elif r["AIPS"] < aips_med and r["WTRS"] >= wtrs_med:
                return "Workforce Transition" # Low AIPS, High WTRS -> Collab/Transition
            else:
                return "Monitor" # Low AIPS, Low WTRS
        
        df["Decision_Strategy"] = df.apply(classify_decision, axis=1)
        
        return df
    except Exception as e:
        st.error(f"Lỗi tải file: {e}. Vui lòng đảm bảo file 'final_consolidated_output (1).csv' nằm cùng thư mục.")
        return pd.DataFrame()

df = load_data()

# Dừng render nếu không có dữ liệu
if df.empty:
    st.stop()

# ==============================================================================
# GIAO DIỆN CHÍNH
# ==============================================================================
st.markdown(f"""
<div class="header-container">
    <h1>AI Workforce Transformation Executive Dashboard</h1>
    <p>Hệ thống Phân tích Năng lực AI, Mức độ Sẵn sàng Nhân sự & Khoảng cách Chuyển đổi</p>
</div>
""", unsafe_allow_html=True)

tab_overview, tab_matrix, tab_friction, tab_economic, tab_action = st.tabs([
    "📌 Executive Overview",
    "🎯 Transformation Matrix",
    "⚡ Friction & Gap Analysis",
    "💼 Economic Exposure",
    "🚀 Strategic Action Plan"
])

plotly_template = "plotly_white"
color_discrete_map = {
    "AI Adoption (Deploy AI)": C_MAIN_BLUE,
    "Workforce Transition (Reskill)": "#E63946", 
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
    high_risk_count = len(df[(df["Cap_norm"] > df["Cap_norm"].median()) & (df["Read_norm"] < df["Read_norm"].median())])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="card-3d">
            <div class="kpi-label">Avg AI Capacity (Norm)</div>
            <div class="kpi-value">{avg_cap:.2f}</div>
            <span class="badge-3d badge-info">Khả năng AI</span>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="card-3d">
            <div class="kpi-label">Avg Readiness (Norm)</div>
            <div class="kpi-value">{avg_read:.2f}</div>
            <span class="badge-3d badge-warning">Sẵn sàng Nhân sự</span>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="card-3d">
            <div class="kpi-label">Avg Friction Index (WFI)</div>
            <div class="kpi-value">{avg_wfi:+.2f}</div>
            <span class="badge-3d badge-danger">Lệch pha (Gap)</span>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="card-3d">
            <div class="kpi-label">High Risk Occupations</div>
            <div class="kpi-value">{high_risk_count} <span style="font-size:16px;">Nghề</span></div>
            <span class="badge-3d badge-danger">Cần Reskill Khẩn cấp</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([6, 4])
    with col_left:
        st.markdown("#### 📈 Top 10 Nghề nghiệp theo Chỉ số AIPS")
        top_aips = df.sort_values(by="AIPS", ascending=False).head(10)
        fig_aips = px.bar(
            top_aips, x="AIPS", y="Occupation", orientation="h",
            color="AIPS", color_continuous_scale=[C_TEAL_BG, C_MAIN_BLUE, C_DARK_BLUE],
        )
        fig_aips.update_layout(yaxis=dict(autorange="reversed"), height=380, template=plotly_template)
        st.plotly_chart(fig_aips, use_container_width=True)

    with col_right:
        st.markdown("#### 🧩 Cơ cấu Phân vùng Nhóm Nghề")
        quad_counts = df["Quadrant"].value_counts().reset_index()
        fig_pie = px.pie(
            quad_counts, values="count", names="Quadrant",
            color="Quadrant", color_discrete_map=color_discrete_map, hole=0.45
        )
        fig_pie.update_layout(height=380, template=plotly_template)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("""
    <div class="insight-box-3d">
        <h4>💡Executive Recommendation</h4>
        <p>Đầu tư AI nên bắt đầu từ những ngành nghề có tác động lớn và khả năng tự động hóa cao, nhưng chuẩn bị lực lượng lao động phải được thực hiện song song. Phân tích xác định các ngành nghề tài chính và hành chính là ưu tiên hàng đầu cho đầu tư AI do tiềm năng tự động hóa mạnh và mức độ ảnh hưởng kinh tế cao. Tuy nhiên, khoảng cách tích cực giữa năng lực AI và sự sẵn sàng (+0.04) cùng 8 ngành nghề có nguy cơ cao cho thấy các tổ chức cần kết hợp triển khai AI với chiến lược đào tạo lại để đảm bảo chuyển đổi lực lượng lao động bền vững.</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 2: TRANSFORMATION MATRIX
# ------------------------------------------------------------------------------
with tab_matrix:
    st.markdown("### 🎯 Ma trận Tương quan Khả năng AI vs Mức độ Sẵn sàng (Quadrant Matrix)")
    
    cap_med = df["Cap_norm"].median()
    read_med = df["Read_norm"].median()

    fig_matrix_quad = px.scatter(
        df, x="Cap_norm", y="Read_norm", color="Quadrant",
        size="EconomicExposure", hover_name="Occupation",
        hover_data=["WFI", "AIPS"],
        color_discrete_map=color_discrete_map,
        labels={"Cap_norm": "Khả năng AI (Cap_norm)", "Read_norm": "Sẵn sàng (Read_norm)"}
    )
    fig_matrix_quad.add_vline(x=cap_med, line_dash="dash", line_color=C_LIGHT_BLUE)
    fig_matrix_quad.add_hline(y=read_med, line_dash="dash", line_color=C_LIGHT_BLUE)
    fig_matrix_quad.update_layout(height=520, template=plotly_template)
    st.plotly_chart(fig_matrix_quad, use_container_width=True)

    st.markdown("""
        <div class="insight-box-3d">
            <h4>💡Key Finding</h4>
            <p> Tiềm năng triển khai AI không chỉ phụ thuộc vào khả năng tự động hóa. Rào cản chính là sự sẵn sàng của lực lượng lao động. Các tổ chức nên ưu tiên triển khai AI cho các ngành nghề có mức sẵn sàng cao trong khi đầu tư vào chương trình đào tạo lại cho các vị trí có năng lực cao nhưng chưa sẵn sàng.</p>
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
            top_wfi, x="WFI", y="Occupation", orientation="h",
            color="WFI", color_continuous_scale=["#FFCDD2", "#D32F2F"],
            title="Top 10 Nghề có Lệch Pha (WFI) Lớn Nhất"
        )
        fig_wfi.update_layout(yaxis=dict(autorange="reversed"), height=450, template=plotly_template)
        st.plotly_chart(fig_wfi, use_container_width=True)

    with col_f2:
        st.markdown("#### 🔍 Chi tiết Khoảng cách theo Nhóm Nghề")
        selected_occ = st.selectbox("Chọn nghề nghiệp để kiểm tra chi tiết:", df["Occupation"].unique())
        occ_detail = df[df["Occupation"] == selected_occ].iloc[0]

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=occ_detail['Cap_norm'],
            title={'text': "AI Capacity", 'font': {'size': 14}},
            gauge={
                'axis': {'range': [0, 1]},
                'bar': {'color': "#293681"},
                'steps': [
                    {'range': [0, cap_med], 'color': "#D0E7E6"},
                    {'range': [cap_med, 1.0], 'color': "#95CCDD"}
                ],
            }
        ))
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.write(f"• **AI Capacity Norm:** `{occ_detail['Cap_norm']:.2f}`")
        st.write(f"• **Worker Readiness Norm:** `{occ_detail['Read_norm']:.2f}`")
        st.write(f"• **Friction (WFI):** `{occ_detail['WFI']:.2f}`")

# ------------------------------------------------------------------------------
# TAB 4: ECONOMIC VALUE AT STAKE
# ------------------------------------------------------------------------------
with tab_economic:
    st.markdown("### 💼 Economic Value at Stake")
    st.markdown("<p style='font-size: 15px; color: #6C757D;'><em>\"Where can AI create the largest business impact?\"</em></p>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box-3d">
        <h4>💡 Executive Insight — AI Value Is Concentrated in High-Impact Knowledge Work</h4>
        <p>Phân tích Economic Exposure cho thấy tác động tiềm năng của AI không chỉ phụ thuộc vào khả năng tự động hóa, mà còn phụ thuộc vào <b>quy mô lực lượng lao động bị ảnh hưởng (WEI)</b> và <b>giá trị kinh tế của từng nhóm nghề (PEI)</b>. Đây là những khu vực mà doanh nghiệp có thể tạo ra tác động lớn nhất khi triển khai AI.</p>
        <p style="margin-top: 6px;">Tuy nhiên, kết quả cho thấy một số nghề có AI capability cao nhưng rủi ro chuyển đổi nhân sự (Transition Risk) cũng rất lớn. Điều này hàm ý rằng giá trị kinh tế từ AI chỉ có thể đạt được khi đi kèm với <b>chiến lược chuyển đổi nhân lực phù hợp, thay vì chỉ tập trung vào tự động hóa</b>.</p>
    </div>
    """, unsafe_allow_html=True)

    total_exposure = df["EconomicExposure"].sum()
    high_impact_jobs = len(df[df["EconomicExposure"] > df["EconomicExposure"].quantile(0.75)])
    high_risk_jobs = len(df[df["Quadrant"] == "Workforce Transition (Reskill)"])

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="card-3d">
            <div class="kpi-label">Total Economic Exposure</div>
            <div class="kpi-value">{total_exposure:.1f}</div>
            <div class="kpi-footer-insight">Tổng giá trị quy đổi chịu tác động bởi AI.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="card-3d">
            <div class="kpi-label">🚀 High Impact Occupations</div>
            <div class="kpi-value">{high_impact_jobs} <span style="font-size:16px;">Jobs</span></div>
            <div class="kpi-footer-insight">Nhóm nghề mang lại cơ hội đột phá kinh tế lớn nhất.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="card-3d">
            <div class="kpi-label">⚠️ High Transition Risk</div>
            <div class="kpi-value">{high_risk_jobs} <span style="font-size:16px;">Jobs</span></div>
            <div class="kpi-footer-insight">Khu vực cần ưu tiên chiến lược Reskill khẩn cấp.</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)

    ec1, ec2 = st.columns(2)
    with ec1:
        top_wei_thresh = df["WEI_norm"].nlargest(5).min()
        df["Label_WEI"] = df.apply(lambda x: x["Occupation"] if x["WEI_norm"] >= top_wei_thresh else "", axis=1)

        fig_e1 = px.scatter(
            df, x="WEI_norm", y="Cap_norm", size="PEI_norm", color="Quadrant",
            text="Label_WEI", hover_name="Occupation", color_discrete_map=color_discrete_map,
            title="Employment Impact: Quy mô Lao động vs Khả năng AI",
            labels={"WEI_norm": "Employment Exposure (WEI)", "Cap_norm": "AI Capability (Cap_norm)"}
        )
        fig_e1.update_traces(textposition='top center', textfont_size=10, textfont_color="#333333")
        fig_e1.update_layout(height=450, template=plotly_template)
        st.plotly_chart(fig_e1, use_container_width=True)

    with ec2:
        fig_e2 = px.scatter(
            df, x="EconomicExposure", y="WFI", size="WEI_norm", color="Quadrant",
            hover_name="Occupation", color_discrete_map=color_discrete_map,
            title="Value vs Risk: Giá trị Kinh tế vs Rủi ro Chuyển đổi",
            labels={"EconomicExposure": "Economic Value at Stake", "WFI": "Workforce Transition Risk (WFI)"}
        )
        fig_e2.add_vline(x=df["EconomicExposure"].median(), line_dash="dot", line_color="gray", opacity=0.6)
        fig_e2.add_hline(y=df["WFI"].median(), line_dash="dot", line_color="gray", opacity=0.6)
        
        fig_e2.add_annotation(x=df["EconomicExposure"].max()*0.9, y=df["WFI"].max()*0.9, text="High Value - High Risk<br>(Reskill Priority)", showarrow=False, font=dict(color="#E63946", size=10))
        fig_e2.add_annotation(x=df["EconomicExposure"].max()*0.9, y=df["WFI"].min()*1.1, text="High Value - Low Risk<br>(AI Quick Wins)", showarrow=False, font=dict(color=C_MAIN_BLUE, size=10))

        fig_e2.update_layout(height=450, template=plotly_template)
        st.plotly_chart(fig_e2, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box-3d" style="border-left-color: #8D99AE; background: linear-gradient(135deg, {C_WHITE} 0%, #E9ECEF 100%);">
        <h4>📌 Key Finding</h4>
        <p>Tác động kinh tế của AI được thúc đẩy bởi sự kết hợp giữa quy mô lực lượng lao động và tiềm năng tự động hóa. Các ngành nghề có mức độ tiếp xúc cao với việc làm đại diện cho cơ hội chuyển đổi lớn nhất, trong khi các vị trí giá trị cao đòi hỏi chiến lược triển khai AI và chuyển đổi lực lượng lao động cân bằng.</p>
        <p style="margin-top: 8px; font-weight: 600; color: {C_DARK_BLUE};"><i>"Chuyển đổi AI tạo ra một quỹ cơ hội kinh tế, nhưng để nắm bắt giá trị này cần cân bằng giữa ưu tiên đầu tư và sự sẵn sàng chuyển đổi lực lượng lao động."</i></p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 5: STRATEGIC ACTION PLAN 
# ------------------------------------------------------------------------------
with tab_action:
    st.markdown("### 🚀 Strategic Action Plan")
    st.markdown("<p style='font-size: 16px; color: #6C757D; margin-top: -10px;'><em>From AI Assessment to Workforce Transformation Decision</em></p>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-box-3d">
        <h4>💡 Hướng dẫn Triển khai Chiến lược Dựa trên Dữ liệu</h4>
        <p>Chiến lược dưới đây phân loại các nhóm nghề theo mức độ cấp thiết và cách tiếp cận AI dựa trên hai chỉ số: <b>AIPS (Điểm Ưu tiên Triển khai AI)</b> và <b>WTRS (Điểm Rủi ro Chuyển đổi Nhân sự)</b>. Hệ thống này giúp lãnh đạo phân bổ ngân sách, thời gian, và nguồn lực một cách tối ưu, tránh rủi ro "chuyển đổi số thất bại do thiếu đồng bộ với nhân sự".</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="playbook-card deploy">
            <span class="badge-3d badge-info playbook-tag">Quick Wins</span>
            <h4>AI Opportunity</h4>
            <p style="font-size: 13px; color: #555; margin-bottom: 15px; font-style: italic;">
                Lợi ích cao, Rủi ro nhân sự thấp.
            </p>
            <ul>
                <li>Triển khai ngay giải pháp AI (Copilots, RPA)</li>
                <li>Hỗ trợ tự động hóa các tác vụ lặp lại</li>
                <li>Tạo ROI nhanh chóng</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="playbook-card reskill">
            <span class="badge-3d badge-danger playbook-tag">Urgent Action</span>
            <h4>Strategic Priority</h4>
            <p style="font-size: 13px; color: #555; margin-bottom: 15px; font-style: italic;">
                Lợi ích cao nhưng nguy cơ đào thải lớn.
            </p>
            <ul>
                <li>Chiến dịch Reskilling trên diện rộng</li>
                <li>Thiết kế lại công việc (Job Redesign)</li>
                <li>Tránh gián đoạn lực lượng lao động</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div class="playbook-card collab">
            <span class="badge-3d badge-success playbook-tag">Long-term</span>
            <h4>Workforce Transition</h4>
            <p style="font-size: 13px; color: #555; margin-bottom: 15px; font-style: italic;">
                Tác động AI chậm, tập trung vào con người.
            </p>
            <ul>
                <li>Đào tạo chéo (Cross-skilling)</li>
                <li>Chuẩn bị văn hóa sử dụng AI</li>
                <li>Phát triển kỹ năng mềm (Human-centric)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with c4:
        st.markdown(f"""
        <div class="playbook-card monitor">
            <span class="badge-3d badge-warning playbook-tag" style="background-color: #EEEEEE; border-color: #BDBDBD; color: #616161;">Watchlist</span>
            <h4>Monitor</h4>
            <p style="font-size: 13px; color: #555; margin-bottom: 15px; font-style: italic;">
                Tác động AI và rủi ro nhân sự đều thấp.
            </p>
            <ul>
                <li>Theo dõi xu hướng công nghệ</li>
                <li>Duy trì hoạt động hiện tại</li>
                <li>Chưa cần đầu tư nguồn lực lớn</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border: 1px dashed #D0E7E6; margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown("#### 📋 Action Filter theo Nhóm Nghề nghiệp")

    # Layout Dropdown & KPI bên cạnh
    filter_col1, filter_col2 = st.columns([1, 2])
    with filter_col1:
        strategy_options = ["Tất cả"] + list(df["Decision_Strategy"].unique())
        selected_strategy = st.selectbox("Chọn Chiến lược Hành động:", strategy_options)

    filtered_df = df if selected_strategy == "Tất cả" else df[df["Decision_Strategy"] == selected_strategy]
    
    with filter_col2:
         st.markdown(f"<div style='padding-top: 30px; font-weight: 600; color: {C_DARK_BLUE};'>Đang hiển thị {len(filtered_df)} ngành nghề thuộc chiến lược này.</div>", unsafe_allow_html=True)

    # DataFrame Tùy chỉnh (Đẹp hơn, ẩn index)
    display_cols = ["Occupation", "Decision_Strategy", "Quadrant", "AIPS", "WTRS", "WFI"]
    st.dataframe(
        filtered_df[display_cols].sort_values(by="AIPS", ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Occupation": st.column_config.TextColumn("Nhóm Nghề nghiệp", width="medium"),
            "Decision_Strategy": st.column_config.TextColumn("Chiến lược (Action)", width="small"),
            "Quadrant": st.column_config.TextColumn("Trạng thái Matrix", width="small"),
            "AIPS": st.column_config.NumberColumn("AIPS (Độ ưu tiên AI)", format="%.2f"),
            "WTRS": st.column_config.NumberColumn("WTRS (Rủi ro Chuyển đổi)", format="%.2f"),
            "WFI": st.column_config.NumberColumn("WFI (Lệch pha)", format="%.2f")
        }
    )
