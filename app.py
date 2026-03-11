import streamlit as st
import config
import finance_analysis
import ai_advisor
import visualization
import utils

# Page configuration
st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS from file
def load_css():
    try:
        with open('styles.css', 'r') as f:
            css = f.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# Initialize Session State
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None
if "generated_advice" not in st.session_state:
    st.session_state.generated_advice = None
if "goal_plan" not in st.session_state:
    st.session_state.goal_plan = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

# HEADER SECTION
st.markdown('<div class="main-header">🌐 AI Financial Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Your Personal AI-Powered Financial Planning Assistant</div>', unsafe_allow_html=True)

st.markdown("""
<div class='hero-section' style='text-align: center;'>
    <h2 style='color: white; font-size: 2.5rem; margin-bottom: 1rem;'>Take Control of Your Financial Future</h2>
    <p style='font-size: 1.2rem; color: #f0f0f0; margin-bottom: 0.5rem;'>
    Get personalized financial advice, investment strategies, and goal planning powered by AI
    </p>
</div>
""", unsafe_allow_html=True)


# SIDEBAR INPUTS
with st.sidebar:
    st.markdown(" ")
    
    with st.expander("ℹ️ About Tool", expanded=False):
        st.markdown("""
        **AI Financial Advisor** uses Google's advanced Gemini 2.0 Flash model to provide personalized financial budgeting, goal-planning, and conversational advice based on your explicit constraints.
        
        *Technologies:*
        - Streamlit (Frontend/UI)
        - Google Generative AI (LLM)
        - Python (Core Data Analysis)
        - Matplotlib & Seaborn (Charts)
        """)
        
    profile = st.selectbox("Profile", ["Student", "Professional", "Other"])
    
    if profile == "Student":
        income = st.number_input("Monthly Income (₹)", min_value=0.0, step=1000.0, value=10000.0)
        part_time = st.selectbox(
            "Do you have part-time income?",
            ["No", "Yes"],
            help="Select if you have additional income from part-time work"
        )
        if part_time == "Yes":
            extra_income = st.number_input("Extra Part-time Income (₹)", min_value=0.0, step=500.0, value=2000.0)
            income += extra_income
    elif profile == "Professional":
        income = st.number_input("Monthly Income (₹)", min_value=0.0, step=1000.0, value=50000.0)
    else:
        income = st.number_input("Monthly Income (₹)", min_value=0.0, step=1000.0, value=30000.0)
        
    expenses = st.number_input("Monthly Expenses (₹)", min_value=0.0, step=1000.0, value=30000.0)
    existing_savings = st.number_input("Existing Savings (₹)", min_value=0.0, step=1000.0, value=100000.0)
    debts = st.number_input("Total Debts (₹)", min_value=0.0, step=1000.0, value=0.0)
    
    goals_input = st.text_area("Financial Goals", value="Build Emergency Fund, Invest for Retirement")
    goals = [goal.strip() for goal in goals_input.split(",") if goal.strip()]
    
    risk_tolerance = st.selectbox("Investment Risk Tolerance", ["Low", "Medium", "High"])
    
    st.session_state.user_data = {
        'profile': profile,
        'income': income,
        'expenses': expenses,
        'existing_savings': existing_savings,
        'debts': debts,
        'risk_tolerance': risk_tolerance,
        'goals': goals
    }
    
    generate_btn = st.button("Financial Analysis & Advice")

# MAIN CONTENT AREA
if st.session_state.user_data and st.session_state.user_data['income'] > 0:
    # Removing old static CSS to rely on external styles.css instead
    
    if generate_btn:
        st.session_state.analysis_data = finance_analysis.analyze_finances(st.session_state.user_data)
        st.session_state.generated_advice = ai_advisor.generate_financial_advice(
            st.session_state.user_data,
            st.session_state.analysis_data
        )

    if st.session_state.analysis_data:
        ad = st.session_state.analysis_data
        
        # Key Metrics (Row 1)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Savings Ratio", f"{ad['savings_ratio']*100:.1f}%")
        with col2:
            st.metric("Debt-to-Income", f"{ad['debt_to_income_ratio']*100:.1f}%", 
                      delta="High Debt!" if ad['high_debt_alert'] else None,
                      delta_color="inverse")
        with col3:
            st.metric("Investment Capacity", f"₹{ad['investment_capacity']:,.0f}")
        with col4:
            st.metric("Total Net Worth", f"₹{ad['total_net_worth']:,.0f}")

        st.markdown(" <br> ", unsafe_allow_html=True)
        
        # Key Metrics (Row 2)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Monthly Savings", f"₹{ad['savings']:,.0f}")
        with col2:
            st.metric("Existing Funds", f"₹{ad['existing_savings']:,.0f}")
        with col3:
            st.metric("Emergency Fund Target", f"₹{ad['emergency_fund']:,.0f}",
                     delta=f"-₹{ad['emergency_fund_shortfall']:,.0f}" if ad['emergency_fund_shortfall'] > 0 else "Fully Funded",
                     delta_color="inverse" if ad['emergency_fund_shortfall'] > 0 else "normal")
            
        # Progress Indicators
        st.markdown(" ")
        st.markdown("#### Financial Health Indicators")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Emergency Fund Progress**")
            current = ad['existing_savings']
            target = ad['emergency_fund']
            progress = min(1.0, current / target if target > 0 else 1.0)
            st.progress(progress)
            st.caption(f"₹{current:,.0f} / ₹{target:,.0f} ({progress*100:.1f}%)")
            
        with col2:
            st.markdown("**Income Utilization (Expenses vs Savings)**")
            savings_pct = ad['savings_ratio']
            expense_pct = ad['expense_ratio']
            
            # Simple custom HTML progress bar for stacking
            st.markdown(f"""
            <div style="width: 100%; background-color: #f0f2f6; border-radius: 5px; height: 16px; display: flex; overflow: hidden; margin-bottom: 8px;">
                <div style="width: {expense_pct*100}%; background-color: #ff6b6b;" title="Expenses: {expense_pct*100:.1f}%"></div>
                <div style="width: {savings_pct*100}%; background-color: #2ecc71;" title="Savings/Investments: {savings_pct*100:.1f}%"></div>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"<span style='color:#ff6b6b'>Expenses ({expense_pct*100:.1f}%)</span> / <span style='color:#2ecc71'>Savings ({savings_pct*100:.1f}%)</span>", unsafe_allow_html=True)

        st.divider()
        
    st.subheader("📊 Visual Analysis")
    # ensure we have local copies
    user_data = st.session_state.user_data
    analysis_data = st.session_state.analysis_data
    if analysis_data:
        fig = visualization.plot_advised_financial_overview(user_data, analysis_data)
        st.pyplot(fig)
    else:
        st.info("Click 'Financial Analysis & Advice' to generate your financial overview and charts.")
        
    
    st.divider()
    
    st.subheader("💡 AI Financial Guidance")
    if st.session_state.generated_advice:
        with st.spinner("Generating personalized insights..."):
            advice = st.session_state.generated_advice
            sections = utils.split_advice_sections(advice)
            
            for title, content_html in sections:
                with st.expander(title, expanded=True):
                    st.markdown(content_html, unsafe_allow_html=True)
        
    # Advanced Planning Input
    st.divider()
    st.markdown("### 🎯 Advanced Goal Oriented Planning")
    
    user_instructions = st.text_area(
        "Your Specific Instructions:",
        placeholder="e.g., I want to save 30% of income directly, Pay debt as fast as possible, Reach goal in 2 years, Invest only in stocks, etc.",
        height=80,
        help="Enter your specific financial instructions that will be prioritized above all else"
    )
    
    advanced_plan_btn = st.button("🎲 Generate Advanced Goal Plan", use_container_width=True)
    
    if advanced_plan_btn:
        if not user_instructions.strip():
            st.warning("Please enter your specific instructions for advanced planning")
        elif not st.session_state.analysis_data:
            st.error("Please click 'Financial Analysis & Advice' in the sidebar first to generate your base analysis.")
        else:
            with st.spinner("Creating advanced plan with your specific instructions..."):
                st.session_state.goal_plan = ai_advisor.generate_goal_plan(
                    st.session_state.user_data,
                    st.session_state.analysis_data,
                    user_instructions
                )
                
    if st.session_state.goal_plan:
        st.markdown("---")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
                    padding: 1.5rem;
                    border-radius: 15px;
                    text-align: center;
                    margin-bottom: 2rem;
                    box-shadow: 0 6px 20px rgba(78, 205, 196, 0.3);'>
            <h1 style='font-size: 2rem; font-weight: 700; color: white; margin-bottom: 0.3rem;'>
            🎯 Goal-Oriented Planning
            </h1>
        </div>
        """, unsafe_allow_html=True)
        
        sections = utils.split_goal_sections(st.session_state.goal_plan)
        
        col1, col2 = st.columns(2)
        
        for i, (title, content_html) in enumerate(sections):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"""
                <div class='glass-card' style='border-top: 4px solid #4ECDC4;'>
                    {f"<h4 style='color: #4ECDC4; margin-bottom: 10px; font-weight: 600;'>{title}</h4>" if title else ""}
                    <div style='color: var(--text-color);'>{content_html}</div>
                </div>
                """, unsafe_allow_html=True)
        
    # Store data in session state for chatbot
    st.session_state['user_data'] = user_data
    st.session_state['analysis_data'] = analysis_data

# CHATBOT SECTION
st.divider()
st.markdown("""
<div class='section-header' style='text-align: center; margin-bottom: 20px;'>
    <h3 style='color: var(--text-color); font-size: 1.8rem; font-weight: 700;'>💬 AI Financial Assistant</h3>
    <p style='color: var(--text-color); opacity: 0.8;'>Ask any questions about your finances, investments, or general budgeting strategies.</p>
</div>
""", unsafe_allow_html=True)

chat_col1, chat_col2 = st.columns([2, 1])

with chat_col1:
    # Display chat messages from history on app rerun
    for msg in st.session_state.chat_history:
        if msg['user']:
            with st.chat_message("user"):
                st.markdown(msg["user"])
        if msg['bot']:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg["bot"])

    # React to user input
    if prompt := st.chat_input("Ask your financial question here..."):
        if not st.session_state.user_data or st.session_state.user_data.get("income", 0) == 0:
            st.error("Please enter your financial details in the sidebar before using the chatbot.")
        elif not st.session_state.analysis_data:
            st.error("Please generate your financial analysis first.")
        else:
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("Analyzing your question..."):
                    try:
                        response = ai_advisor.finance_chatbot_response(
                            st.session_state.user_data,
                            st.session_state.analysis_data,
                            prompt
                        )
                        st.markdown(response)
                        
                        # Add user message to chat history
                        st.session_state.chat_history.append({
                            "user": prompt,
                            "bot": response
                        })
                    except Exception as e:
                        st.error(f"Chatbot Error: {e}")

with chat_col2:
    st.markdown("""
    <div class='glass-card'>
        <h4 style='color: var(--text-color); margin-bottom: 15px; font-weight: 600;'>💡 Chat Tips</h4>
        <ul style='font-size: 0.95rem; color: var(--text-color); opacity: 0.9; padding-left: 20px; line-height: 1.6;'>
            <li>Ask about investments</li>
            <li>Get budgeting advice</li>
            <li>Discuss debt management</li>
            <li>Plan for specific goals</li>
            <li>Understand financial terms</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
