import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Tools Comparison - MDAA Team",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern color palette - works in both light and dark mode
COLORS = {
    'ChatGPT': '#74AA9C',  # Sage green
    'Claude': '#E67E50',   # Terracotta
    'Gemini': '#F4B942',   # Warm yellow
    'Perplexity': '#2E7D87' # Deep teal
}

# Tool logos with actual URLs
LOGOS = {
    'ChatGPT': 'https://cdn.oaistatic.com/_next/static/media/apple-touch-icon.82af6fe1.png',
    'Claude':  'https://i.namu.wiki/i/RCyWSYQpcaimM9Mt_bbdnA_6b3DPDME0I_pfdv1Wm-x3JXK3o_l6zLaSFUDhT7ln54bnIIKp2Rg0_6ssPg_eUXMtWJq5Mmp4i1nra2RkpnoBZu8vQd5QmV_eDhDwyY1KQahyrcOYc0P3rZSkgVjv1Q.svg',
    'Gemini': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/480px-Google_%22G%22_logo.svg.png',
    'Perplexity': 'https://i.namu.wiki/i/Ix-v4RWLZiVwkd-LMEdI2KzlrCNm8KKJFV3eQR04uWUx4xrA5DeI-XcimnJ5yvUG_IMkWOdX2RRA69R4J9I6DEfjJTUYASDof2WQM0vXqMqf2sgXMHMPc-zT3K9AXEsS4nXkPosqo0uNI386yKSS6Q.svg'
}

# Custom CSS with dark mode support
st.markdown("""
<style>
    .stMetric {
        background-color: rgba(28, 31, 35, 0.5);
        padding: 15px;
        border-radius: 12px;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .card {
        background: rgba(28, 31, 35, 0.5);
        padding: 20px;
        border-radius: 16px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .tool-header {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 8px;
    }
    .recommendation-box {
        background: rgba(244, 185, 66, 0.1);
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #F4B942;
        margin: 15px 0;
    }
    .nuance-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        margin: 4px;
    }
    .feature-box {
        background: rgba(28, 31, 35, 0.3);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with enhanced data
if 'data' not in st.session_state:
    st.session_state.data = {
        'tools': {
            'ChatGPT': {
                'logo': 'https://cdn.oaistatic.com/_next/static/media/apple-touch-icon.82af6fe1.png',
                'strengths': ['General tasks', 'Coding with Code Interpreter', 'Creative writing', 'Conversational AI', 'Custom GPTs', 'DALL-E integration'],
                'weaknesses': ['Can be verbose', 'Knowledge cutoff issues', 'Sometimes hallucinates', 'No native citations'],
                'nuances': ['Best voice mode', 'Excellent mobile app', 'Strong ecosystem', 'Canvas for editing'],
                'best_for': 'Creative professionals and general users',
                'price': {'free': True, 'paid': 20},
                'scores': {
                    'Writing': 9,
                    'Coding': 9,
                    'Research': 6,
                    'Analysis': 7,
                    'Creative': 10,
                    'Conversation': 10,
                    'Current Info': 5
                }
            },
            'Claude': {
                'logo': 'https://www-cdn.anthropic.com/images/claude-app-icon.png',
                'strengths': ['Long documents (200K tokens)', 'Deep analysis', 'Nuanced writing', 'Code debugging', 'Artifacts feature', 'Projects for context'],
                'weaknesses': ['No image generation', 'No web search', 'Can be overly cautious', 'Limited integrations'],
                'nuances': ['Best for long-form content', 'Superior context retention', 'Excellent at following complex instructions', 'Artifacts for iterative work'],
                'best_for': 'Writers, analysts, and developers working with complex documents',
                'price': {'free': True, 'paid': 20},
                'scores': {
                    'Writing': 10,
                    'Coding': 10,
                    'Research': 5,
                    'Analysis': 10,
                    'Creative': 9,
                    'Conversation': 8,
                    'Current Info': 5
                }
            },
            'Gemini': {
                'logo': 'https://www.gstatic.com/lamda/images/gemini_favicon_f069958c85030456e93de685481c559f160ea06b.png',
                'strengths': ['Google integration', 'Multilingual', 'Multimodal', 'Fast responses', 'Best video calls', 'Screen sharing'],
                'weaknesses': ['Less consistent', 'Smaller community', 'Less refined outputs', 'Limited customization'],
                'nuances': ['BEST video call & screen sharing features', 'Seamless Google Workspace integration', 'Real-time collaboration', 'YouTube analysis'],
                'best_for': 'Google users, video meetings, and visual learners',
                'price': {'free': True, 'paid': 20},
                'scores': {
                    'Writing': 7,
                    'Coding': 7,
                    'Research': 8,
                    'Analysis': 7,
                    'Creative': 6,
                    'Conversation': 7,
                    'Current Info': 8
                }
            },
            'Perplexity': {
                'logo': 'https://www.perplexity.ai/favicon.ico',
                'strengths': ['Real-time research', 'Source citations', 'Current events', 'Academic mode', 'Focus mode', 'Multiple search engines'],
                'weaknesses': ['Not creative', 'Limited conversation memory', 'No code execution', 'Basic UI'],
                'nuances': ['Chats NOT in focus - BEST for pure search', 'Pro searches with multiple models', 'Academic citations', 'Daily news digest'],
                'best_for': 'Researchers, students, and fact-checkers',
                'price': {'free': True, 'paid': 20},
                'scores': {
                    'Writing': 6,
                    'Coding': 5,
                    'Research': 10,
                    'Analysis': 8,
                    'Creative': 3,
                    'Conversation': 5,
                    'Current Info': 10
                }
            }
        },
        'use_cases': {
            'Marketing Teams': ['ChatGPT', 'Claude', 'Perplexity'],
            'Data Analysts': ['Claude', 'Perplexity', 'Gemini'],
            'Content Writers': ['Claude', 'ChatGPT', 'Perplexity'],
            'Developers': ['Claude', 'ChatGPT', 'Gemini'],
            'Researchers': ['Perplexity', 'Claude', 'Gemini'],
            'Project Managers': ['Gemini', 'Claude', 'ChatGPT']
        },
        'recommendations': {
            'quick_answers': 'Perplexity',
            'long_documents': 'Claude',
            'creative_work': 'ChatGPT',
            'video_collaboration': 'Gemini',
            'academic_research': 'Perplexity',
            'code_review': 'Claude',
            'brainstorming': 'ChatGPT',
            'screen_sharing': 'Gemini'
        }
    }

# Sidebar
with st.sidebar:
    st.title("⚙️ Dashboard Controls")
    st.markdown("**MDAA Team** | Marketing Data & Advanced Analytics")
    
    st.markdown("### 🎯 Quick Recommendations")
    
    task = st.selectbox(
        "What do you need to do?",
        ["Select a task...", "Research with citations", "Write long content", "Creative brainstorming", 
         "Video collaboration", "Code debugging", "Current events", "Data analysis"]
    )
    
    if task != "Select a task...":
        task_map = {
            "Research with citations": "Perplexity",
            "Write long content": "Claude",
            "Creative brainstorming": "ChatGPT",
            "Video collaboration": "Gemini",
            "Code debugging": "Claude",
            "Current events": "Perplexity",
            "Data analysis": "Claude"
        }
        recommended = task_map.get(task, "ChatGPT")
        st.success(f"🎯 Recommended: **{recommended}**")
        st.info(st.session_state.data['tools'][recommended]['best_for'])
    
    st.divider()
    
    edit_mode = st.toggle("Edit Mode", value=False)
    
    st.divider()
    
    # Filter options
    st.subheader("Filters")
    selected_tools = st.multiselect(
        "Select Tools to Compare",
        options=list(st.session_state.data['tools'].keys()),
        default=list(st.session_state.data['tools'].keys())
    )
    
    st.divider()
    
    # Export/Import
    if st.button("📥 Export Data"):
        json_data = json.dumps(st.session_state.data, indent=2)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name=f"ai_comparison_mdaa_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

# Main content
st.title("AI Apps Comparison")
st.markdown("### MDAA Team - Marketing Data & Advanced Analytics (INTERNAL)")

# Recommendation banner
st.markdown("""
<div class="recommendation-box">
    <h3>💡 Quick Summary</h3>
    <p><strong>Gemini</strong> has the BEST video call and screen sharing features for team collaboration</p>
    <p><strong>Perplexity</strong> keeps chats out of focus, making it the BEST for pure search and research</p>
    <p><strong>Claude</strong> excels at analyzing long marketing reports and data documentation</p>
</div>
""", unsafe_allow_html=True)

# Key metrics with logos
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏆 Best for Research", "Perplexity", "Real-time + Citations")
with col2:
    st.metric("📝 Best for Analysis", "Claude", "200K token context")
with col3:
    st.metric("🎨 Most Creative", "ChatGPT", "Creative Content")
with col4:
    st.metric("📹 Best Collab", "Gemini", "Video + Screen Share")

st.divider()

# Tabs
tab1, tab2, tab3, tab4, tab6 = st.tabs([
    "🎯 Smart Recommendations", 
    "📊 Capability Analysis", 
    "🔍 Unique Features",
    "📋 Detailed Comparison",
    #"👥 Use Cases",
    "✏️ Edit Data"
])

# TAB 1: Smart Recommendations
with tab1:
    st.subheader("Personalized Tool Recommendations")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎯 Choose Your Priority")
        
        priority = st.radio(
            "What matters most for your task?",
            ["Current Information", "Long Context Analysis", "Creative Output", "Team Collaboration", "Academic Research", "Code Quality"]
        )
        
        priority_map = {
            "Current Information": "Perplexity",
            "Long Context Analysis": "Claude",
            "Creative Output": "ChatGPT",
            "Team Collaboration": "Gemini",
            "Academic Research": "Perplexity",
            "Code Quality": "Claude"
        }
        
        recommended_tool = priority_map[priority]
        tool_data = st.session_state.data['tools'][recommended_tool]
        
        st.markdown(f"""
        <div class="card" style="border: 2px solid {COLORS[recommended_tool]};">
            <h2 style="color: {COLORS[recommended_tool]};"><img src="{LOGOS[recommended_tool]}" style="width: 30px; height: 30px; vertical-align: middle; margin-right: 8px;"> {recommended_tool}</h2>
            <p style="font-size: 18px; margin: 15px 0;"><strong>Perfect for:</strong> {tool_data['best_for']}</p>
            <div style="margin: 20px 0;">
                <h4>Key Advantages:</h4>
                {''.join([f'<div style="margin: 8px 0;">✓ {s}</div>' for s in tool_data['strengths'][:3]])}
            </div>
            <div style="margin: 20px 0;">
                <h4>Unique Features:</h4>
                {''.join([f'<span class="nuance-tag" style="background: {COLORS[recommended_tool]}33; color: {COLORS[recommended_tool]}; padding: 4px 8px; margin: 4px; border-radius: 12px; display: inline-block;">{n}</span>' for n in tool_data['nuances'][:2]])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Tool Comparison Matrix")
        
        # Full radar chart with all metrics
        categories = list(list(st.session_state.data['tools'].values())[0]['scores'].keys())
        
        fig = go.Figure()
        
        for tool_name in selected_tools:
            tool_data = st.session_state.data['tools'][tool_name]
            scores = [tool_data['scores'][cat] for cat in categories]
            
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=categories,
                fill='toself',
                name=tool_name,
                line=dict(color=COLORS[tool_name], width=3),
                fillcolor=COLORS[tool_name],
                opacity=0.25
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10], gridcolor='rgba(255,255,255,0.2)'),
                angularaxis=dict(gridcolor='rgba(255,255,255,0.2)')
            ),
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # # Scenario-based recommendations for MDAA
    # st.markdown("### 🎬 MDAA Team Scenario Recommendations")
    
    # scenarios = {
    #     "📊 Marketing Analytics": ["Claude (analysis)", "Perplexity (research)", "ChatGPT (insights)"],
    #     "📝 Campaign Planning": ["ChatGPT (creative)", "Claude (strategy)", "Perplexity (research)"],
    #     "📈 Data Reporting": ["Claude (analysis)", "Gemini (presentation)", "Perplexity (data)"],
    #     "🎯 Competitor Analysis": ["Perplexity (research)", "Claude (analysis)", "ChatGPT (strategy)"]
    # }
    
    # cols = st.columns(2)
    # for idx, (scenario, tools) in enumerate(scenarios.items()):
    #     with cols[idx % 2]:
    #         tool_name_only = tools[0].split()[0]  # Extract just the tool name
    #         st.markdown(f"""
    #         <div class="card">
    #             <h4>{scenario}</h4>
    #             <div style="margin-top: 10px;">
    #                 {''.join([f'<div style="margin: 8px 0; padding: 8px; background: rgba(255,255,255,0.05); border-left: 3px solid {COLORS[tool.split()[0]]}; border-radius: 4px;"><img src="{LOGOS[tool.split()[0]]}" style="width: 16px; height: 16px; vertical-align: middle; margin-right: 5px;"> {tool}</div>' for tool in tools])}
    #             </div>
    #         </div>
    #         """, unsafe_allow_html=True)

# TAB 2: Capability Analysis  
with tab2:
    st.subheader("Detailed Capability Breakdown")
    
    # Enhanced capability comparison
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create enhanced heatmap
        df_scores = pd.DataFrame({
            tool: st.session_state.data['tools'][tool]['scores']
            for tool in selected_tools
        }).T
        
        fig = px.imshow(
            df_scores,
            labels=dict(x="Capability", y="AI Tool", color="Score"),
            x=df_scores.columns,
            y=df_scores.index,
            color_continuous_scale='Viridis',
            aspect="auto",
            text_auto=True
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            font=dict(color='white', size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏆 Category Leaders")
        
        for category in ['Writing', 'Research', 'Creative', 'Analysis']:
            scores = {tool: st.session_state.data['tools'][tool]['scores'][category] 
                     for tool in selected_tools}
            winner = max(scores, key=scores.get)
            
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid {COLORS[winner]};">
                <div style="font-weight: 600; color: {COLORS[winner]}; font-size: 14px;">
                    {category.upper()}
                </div>
                <div style="font-size: 20px; margin: 5px 0;">
                    <img src="{LOGOS[winner]}" style="width: 20px; height: 20px; vertical-align: middle; margin-right: 5px;"> {winner}
                </div>
                <div style="color: #888; font-size: 14px;">
                    Score: {scores[winner]}/10
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Strength comparison bars
    st.markdown("### 💪 Comparative Strengths")
    
    strength_categories = ['Writing', 'Coding', 'Research', 'Analysis', 'Creative', 'Current Info']
    
    fig = go.Figure()
    
    for tool in selected_tools:
        scores = [st.session_state.data['tools'][tool]['scores'].get(cat, 0) for cat in strength_categories]
        fig.add_trace(go.Bar(
            name=tool,
            x=strength_categories,
            y=scores,
            marker_color=COLORS[tool],
            text=scores,
            textposition='outside'
        ))
    
    fig.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        font=dict(color='white'),
        yaxis=dict(range=[0, 11], gridcolor='rgba(255,255,255,0.1)'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)

# TAB 3: Unique Features
with tab3:
    st.subheader("🌟 Unique Features & Hidden Gems")
    
    # Feature highlights
    st.markdown("""
    <div class="recommendation-box">
        <h3>🔍 Key Differentiators</h3>
        <ul style="margin: 10px 0;">
            <li><strong>Gemini:</strong> Video call quality with screen sharing - your assistant with eyes by your side</li>
            <li><strong>Perplexity:</strong> Minimal chat interface, maximum search efficiency - ideal for quick fact check or research</li>
            <li><strong>Claude:</strong> 200K token context window - great for analysis and coding</li>
            <li><strong>ChatGPT:</strong> Canvas mode enables real-time collaborative content editing and in-app features</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Detailed feature cards - Fixed HTML rendering issue
    cols = st.columns(2)
    
    for idx, tool_name in enumerate(selected_tools):
        with cols[idx % 2]:
            tool = st.session_state.data['tools'][tool_name]
            
            with st.container():
                # Display logo with tool name
                col_logo, col_name = st.columns([1, 4])
                with col_logo:
                    st.image(LOGOS[tool_name], width=40)
                with col_name:
                    st.markdown(f"### {tool_name}")
                
                # Unique Features section
                st.markdown("**🌟 Unique Features**")
                for nuance in tool['nuances']:
                    st.markdown(f"""
                    <span style="background: {COLORS[tool_name]}33; 
                          color: {COLORS[tool_name]}; 
                          padding: 4px 12px; 
                          border-radius: 20px; 
                          display: inline-block;
                          margin: 4px;">
                        {nuance}
                    </span>
                    """, unsafe_allow_html=True)
                
                # Best Use Case section
                st.markdown("**💡 Best Use Case**")
                st.info(tool['best_for'])
                
                # Pricing section
                st.markdown("**💰 Pricing**")
                col_free, col_paid = st.columns(2)
                with col_free:
                    if tool['price']['free']:
                        st.success("Free Tier ✓")
                    else:
                        st.error("No Free Tier")
                with col_paid:
                    st.warning(f"Pro: ${tool['price']['paid']}/mo")
                
                st.markdown("---")

# TAB 4: Detailed Comparison
with tab4:
    st.subheader("📊 Comprehensive Comparison Table")
    
    # Create enhanced comparison dataframe
    comparison_data = []
    
    for tool_name in selected_tools:
        tool = st.session_state.data['tools'][tool_name]
        comparison_data.append({
            'Tool': tool_name,
            'Best For': tool['best_for'],
            'Top Strength': tool['strengths'][0],
            'Unique Feature': tool['nuances'][0],
            'Free': '✅' if tool['price']['free'] else '❌',
            'Pro Price': f"${tool['price']['paid']}/mo",
            'Overall Score': f"{sum(tool['scores'].values()) / len(tool['scores']):.1f}/10"
        })
    
    df = pd.DataFrame(comparison_data)
    
    # Display styled dataframe
    st.dataframe(
        df,
        use_container_width=True,
        height=250,
        hide_index=True,
        column_config={
            "Tool": st.column_config.TextColumn("Tool", width="medium"),
            "Best For": st.column_config.TextColumn("Best For", width="large"),
            "Overall Score": st.column_config.ProgressColumn(
                "Overall Score",
                help="Average score across all categories",
                format="%.1f/10",
                min_value=0,
                max_value=10,
            ),
        }
    )
    
    st.divider()
    
    # Side-by-side comparison
    st.markdown("### 🔄 Side-by-Side Comparison")
    
    if len(selected_tools) >= 2:
        compare_tools = st.multiselect(
            "Select exactly 2 tools to compare",
            selected_tools,
            default=selected_tools[:2] if len(selected_tools) >= 2 else selected_tools,
            max_selections=2
        )
        
        if len(compare_tools) == 2:
            col1, col2 = st.columns(2)
            
            with col1:
                t1 = st.session_state.data['tools'][compare_tools[0]]
                st.markdown(f"""
                <div class="card" style="border: 2px solid {COLORS[compare_tools[0]]};">
                    <h3 style="color: {COLORS[compare_tools[0]]};">
                        <img src="{LOGOS[compare_tools[0]]}" style="width: 25px; height: 25px; vertical-align: middle; margin-right: 8px;"> {compare_tools[0]}
                    </h3>
                    <div style="margin: 15px 0;">
                        <h4>✅ Advantages</h4>
                        {''.join([f'<div>• {s}</div>' for s in t1['strengths'][:4]])}
                    </div>
                    <div style="margin: 15px 0;">
                        <h4>⚠️ Limitations</h4>
                        {''.join([f'<div>• {w}</div>' for w in t1['weaknesses'][:3]])}
                    </div>
                    <div style="margin: 15px 0;">
                        <h4>🌟 Unique Features</h4>
                        {''.join([f'<div>• {n}</div>' for n in t1['nuances'][:2]])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                t2 = st.session_state.data['tools'][compare_tools[1]]
                st.markdown(f"""
                <div class="card" style="border: 2px solid {COLORS[compare_tools[1]]};">
                    <h3 style="color: {COLORS[compare_tools[1]]};">
                        <img src="{LOGOS[compare_tools[1]]}" style="width: 25px; height: 25px; vertical-align: middle; margin-right: 8px;"> {compare_tools[1]}
                    </h3>
                    <div style="margin: 15px 0;">
                        <h4>✅ Advantages</h4>
                        {''.join([f'<div>• {s}</div>' for s in t2['strengths'][:4]])}
                    </div>
                    <div style="margin: 15px 0;">
                        <h4>⚠️ Limitations</h4>
                        {''.join([f'<div>• {w}</div>' for w in t2['weaknesses'][:3]])}
                    </div>
                    <div style="margin: 15px 0;">
                        <h4>🌟 Unique Features</h4>
                        {''.join([f'<div>• {n}</div>' for n in t2['nuances'][:2]])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    # MDAA-specific comparison metrics
    st.markdown("### 📈 MDAA Team Performance Metrics")
    
    mdaa_metrics = {
        'Marketing Content': {'ChatGPT': 10, 'Claude': 8, 'Gemini': 6, 'Perplexity': 4},
        'Data Analysis': {'ChatGPT': 7, 'Claude': 10, 'Gemini': 7, 'Perplexity': 8},
        'Market Research': {'ChatGPT': 6, 'Claude': 7, 'Gemini': 7, 'Perplexity': 10},
        'Report Writing': {'ChatGPT': 8, 'Claude': 10, 'Gemini': 7, 'Perplexity': 6},
        'Team Collaboration': {'ChatGPT': 7, 'Claude': 6, 'Gemini': 10, 'Perplexity': 4}
    }
    
    # Create MDAA-specific comparison chart
    fig = go.Figure()
    
    for tool in selected_tools:
        scores = [mdaa_metrics[metric].get(tool, 5) for metric in mdaa_metrics.keys()]
        fig.add_trace(go.Bar(
            name=tool,
            x=list(mdaa_metrics.keys()),
            y=scores,
            marker_color=COLORS[tool],
            text=scores,
            textposition='outside'
        ))
    
    fig.update_layout(
        title="MDAA Team-Specific Performance Scores",
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        font=dict(color='white'),
        yaxis=dict(range=[0, 11], gridcolor='rgba(255,255,255,0.1)', title="Score"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title="Use Case")
    )
    
    st.plotly_chart(fig, use_container_width=True)

# # TAB 5: Use Cases
# with tab5:
#     st.subheader("👥 Recommended Tools by MDAA Role")
    
#     # Interactive use case selector
#     user_type = st.selectbox(
#         "Select your role in MDAA:",
#         list(st.session_state.data['use_cases'].keys())
#     )
    
#     recommended = st.session_state.data['use_cases'][user_type]
    
#     st.markdown(f"### Recommendations for {user_type}")
    
#     cols = st.columns(3)
#     for idx, tool in enumerate(recommended[:3]):
#         with cols[idx]:
#             priority = ["🥇 Primary", "🥈 Secondary", "🥉 Alternative"][idx]
#             tool_data = st.session_state.data['tools'][tool]
            
#             st.markdown(f"""
#             <div class="card" style="border-top: 4px solid {COLORS[tool]};">
#                 <div style="font-size: 18px; font-weight: 600; color: {COLORS[tool]}; margin-bottom: 10px;">
#                     {priority}
#                 </div>
#                 <h3><img src="{LOGOS[tool]}" style="width: 20px; height: 20px; vertical-align: middle; margin-right: 5px;"> {tool}</h3>
#                 <div style="margin: 10px 0; font-size: 14px; color: #888;">
#                     {tool_data['best_for']}
#                 </div>
#                 <div style="margin-top: 15px;">
#                     <strong>Why this tool?</strong>
#                     <div style="margin-top: 8px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 6px;">
#                         {tool_data['nuances'][0]}
#                     </div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)
    
#     st.divider()
    
#     # MDAA Team workflow recommendations
#     st.markdown("### 🔄 MDAA Team Workflow Recommendations")
    
#     workflows = {
#         "Campaign Launch": {
#             "Research Phase": "Perplexity",
#             "Content Creation": "ChatGPT",
#             "Analysis & Review": "Claude",
#             "Team Presentation": "Gemini"
#         },
#         "Quarterly Reporting": {
#             "Data Collection": "Perplexity",
#             "Report Writing": "Claude",
#             "Visualization Ideas": "ChatGPT",
#             "Team Review": "Gemini"
#         },
#         "Competitor Analysis": {
#             "Market Research": "Perplexity",
#             "Deep Analysis": "Claude",
#             "Strategy Formulation": "ChatGPT",
#             "Team Discussion": "Gemini"
#         }
#     }
    
#     selected_workflow = st.selectbox("Select a workflow:", list(workflows.keys()))
    
#     st.markdown(f"#### {selected_workflow} Workflow")
    
#     workflow_steps = workflows[selected_workflow]
#     cols = st.columns(len(workflow_steps))
    
#     for idx, (step, tool) in enumerate(workflow_steps.items()):
#         with cols[idx]:
#             st.markdown(f"""
#             <div class="feature-box" style="text-align: center; border: 2px solid {COLORS[tool]};">
#                 <div style="font-size: 12px; color: #888; margin-bottom: 5px;">Step {idx + 1}</div>
#                 <div style="font-weight: 600; margin-bottom: 10px;">{step}</div>
#                 <div style="margin: 10px 0;"><img src="{LOGOS[tool]}" style="width: 30px; height: 30px;"></div>
#                 <div style="color: {COLORS[tool]}; font-weight: 600;">{tool}</div>
#             </div>
#             """, unsafe_allow_html=True)
    
#     st.divider()
    
#     # Use case matrix visualization
#     st.markdown("### 📊 Complete Use Case Matrix")
    
#     # Create treemap with modern colors
#     use_case_data = []
#     for use_case, tools in st.session_state.data['use_cases'].items():
#         for idx, tool in enumerate(tools):
#             use_case_data.append({
#                 'Role': use_case,
#                 'Tool': tool,
#                 'Priority': 3 - idx if idx < 3 else 1,
#                 'Value': 3 - idx if idx < 3 else 1
#             })
    
#     df_treemap = pd.DataFrame(use_case_data)
    
#     fig = px.treemap(
#         df_treemap,
#         path=['Role', 'Tool'],
#         values='Value',
#         color='Priority',
#         color_continuous_scale=[[0, '#2E7D87'], [0.5, '#F4B942'], [1, '#74AA9C']],
#         title="Tool Recommendations by MDAA Role"
#     )
    
#     fig.update_layout(
#         paper_bgcolor='rgba(0,0,0,0)',
#         font=dict(color='white'),
#         height=500
#     )
    
#     st.plotly_chart(fig, use_container_width=True)

# TAB 6: Edit Data
with tab6:
    if not edit_mode:
        st.warning("⚠️ Enable Edit Mode in the sidebar to modify data")
    else:
        st.subheader("✏️ Edit Tool Information")
        
        selected_tool = st.selectbox("Select Tool to Edit", list(st.session_state.data['tools'].keys()))
        
        tool_data = st.session_state.data['tools'][selected_tool]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Basic Information")
            
            new_best_for = st.text_input(
                "Best For",
                value=tool_data['best_for']
            )
            
            new_strengths = st.text_area(
                "Strengths (one per line)",
                value='\n'.join(tool_data['strengths']),
                height=150
            )
            
            new_weaknesses = st.text_area(
                "Weaknesses (one per line)",
                value='\n'.join(tool_data['weaknesses']),
                height=150
            )
        
        with col2:
            st.markdown("### Unique Features")
            
            new_nuances = st.text_area(
                "Nuances/Special Features (one per line)",
                value='\n'.join(tool_data['nuances']),
                height=150
            )
            
            st.markdown("### Pricing")
            
            new_free = st.checkbox("Has Free Tier", value=tool_data['price']['free'])
            new_price = st.number_input(
                "Pro Price ($)",
                value=tool_data['price']['paid'],
                min_value=0
            )
        
        with col3:
            st.markdown("### Capability Scores")
            
            new_scores = {}
            for category, score in tool_data['scores'].items():
                new_scores[category] = st.slider(
                    category,
                    min_value=0,
                    max_value=10,
                    value=score,
                    key=f"score_{selected_tool}_{category}"
                )
        
        if st.button("💾 Save Changes", type="primary", use_container_width=True):
            st.session_state.data['tools'][selected_tool] = {
                'logo': tool_data['logo'],
                'best_for': new_best_for,
                'strengths': [s.strip() for s in new_strengths.split('\n') if s.strip()],
                'weaknesses': [w.strip() for w in new_weaknesses.split('\n') if w.strip()],
                'nuances': [n.strip() for n in new_nuances.split('\n') if n.strip()],
                'price': {'free': new_free, 'paid': new_price},
                'scores': new_scores
            }
            st.success(f"✅ {selected_tool} data updated successfully!")
            st.rerun()
        
        st.divider()
        
        st.subheader("Edit Use Cases")
        
        selected_use_case = st.selectbox("Select Use Case", list(st.session_state.data['use_cases'].keys()))
        
        current_tools = st.session_state.data['use_cases'][selected_use_case]
        
        new_tools = st.multiselect(
            f"Tools for {selected_use_case} (in order of preference)",
            options=list(st.session_state.data['tools'].keys()),
            default=current_tools
        )
        
        if st.button("💾 Save Use Case", type="primary"):
            st.session_state.data['use_cases'][selected_use_case] = new_tools
            st.success(f"✅ {selected_use_case} updated successfully!")
            st.rerun()
        
        st.divider()
        
        # Add new use case
        st.subheader("Add New Use Case")
        
        new_use_case_name = st.text_input("Use Case Name")
        new_use_case_tools = st.multiselect(
            "Select tools (in order of preference)",
            options=list(st.session_state.data['tools'].keys())
        )
        
        if st.button("➕ Add Use Case", type="secondary"):
            if new_use_case_name and new_use_case_tools:
                st.session_state.data['use_cases'][new_use_case_name] = new_use_case_tools
                st.success(f"✅ {new_use_case_name} added successfully!")
                st.rerun()
            else:
                st.error("Please provide both name and tools for the new use case")

# Footer
st.divider()
st.markdown(f"""
<div style="text-align: center; color: #888; padding: 20px; background: rgba(28, 31, 35, 0.5); border-radius: 12px; margin-top: 30px;">
    <h4> AI Tools Comparison Dashboard - MDAA Team (INTERNAL)</h4>
    <p>Marketing Data & Advanced Analytics</p>
    <p style="font-size: 12px; margin-top: 10px;">
        Last Updated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")} | Powered by MDSG
    </p>
    <p style="font-size: 11px; margin-top: 5px; color: #666;">
        💡 Tip: Enable Edit Mode in sidebar to customize recommendations for your specific needs
    </p>
</div>
""", unsafe_allow_html=True)
