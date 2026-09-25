"""
MindCare Mental Health Bot - Lightweight Streamlit Version
Optimized for Streamlit Cloud FREE tier
Uses rule-based responses for faster performance
"""

import streamlit as st
import re
from collections import defaultdict
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="MindCare - Mental Health Support",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for calming UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #E3F2FD 0%, #F0F4F8 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #6B9BD1 0%, #5A8AC6 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stChatMessage {
        background-color: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .crisis-box {
        background: linear-gradient(135deg, #FFE0B2 0%, #FFB74D 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #FF9800;
    }
</style>
""", unsafe_allow_html=True)

# Mental health patterns
MENTAL_HEALTH_PATTERNS = {
    'depression': [
        r'\b(sad|depressed|hopeless|worthless|empty|numb|down|blue)\b',
        r'\b(no energy|tired|exhausted|fatigue|drained)\b',
        r'\b(can\'t sleep|insomnia|sleeping too much|sleep)\b',
        r'\b(no interest|don\'t care|nothing matters|meaningless)\b',
    ],
    'anxiety': [
        r'\b(anxious|worried|nervous|panic|fear|scared|afraid|terrified)\b',
        r'\b(can\'t breathe|heart racing|sweating|trembling|shaking)\b',
        r'\b(overthinking|can\'t stop thinking|racing thoughts|racing mind)\b',
        r'\b(restless|on edge|tense|wound up)\b',
    ],
    'stress': [
        r'\b(overwhelmed|stressed|pressure|burden|weight)\b',
        r'\b(can\'t cope|too much|breaking down|breaking point)\b',
        r'\b(burnout|exhausted mentally)\b',
    ],
    'trauma': [
        r'\b(flashback|nightmare|reliving|haunted|ptsd)\b',
        r'\b(abuse|trauma|attacked|violated)\b',
    ],
    'self_harm': [
        r'\b(hurt myself|cut myself|harm myself|self harm|self-harm|cutting)\b',
        r'\b(burning myself|punish myself)\b',
    ],
    'suicidal': [
        r'\b(suicide|suicidal|kill myself|end my life|want to die|want to be dead)\b',
        r'\b(better off dead|no reason to live|end it all|take my life)\b',
    ]
}

SEVERITY_WEIGHTS = {
    'suicidal': 10,
    'self_harm': 9,
    'trauma': 7,
    'depression': 6,
    'anxiety': 5,
    'stress': 4
}

# Empathetic response templates
RESPONSE_TEMPLATES = {
    'suicidal': [
        "I'm deeply concerned about what you're sharing with me. Your life has incredible value, and you deserve support and care. Please know that you're not alone in this darkness, even when it feels that way.\n\n**Please reach out for immediate help:**\n- 📞 Call **988** (Suicide & Crisis Lifeline) - Available 24/7\n- 💬 Text **HOME to 741741** (Crisis Text Line)\n- 🚨 Call **911** if you're in immediate danger\n\nWould you like to talk about what's been making you feel this way? I'm here to listen.",
        
        "What you're sharing is really serious, and I'm glad you're talking about it. These feelings can be overwhelming, but there are people who can help you through this right now.\n\n**Immediate resources:**\n- **988** - Suicide & Crisis Lifeline (call or text)\n- **741741** - Text HOME for Crisis Text Line\n- **911** - For emergencies\n\nYou don't have to go through this alone. Can you tell me what's been happening?",
    ],
    
    'self_harm': [
        "I hear that you're struggling with urges to hurt yourself, and that must be incredibly difficult to deal with. Your safety and wellbeing are so important.\n\nHave you been able to talk to anyone about these feelings? A counselor or therapist could provide you with strategies to cope with these urges. The Crisis Text Line (text HOME to 741741) is also available 24/7.\n\nWhat do you usually feel right before these urges come up?",
        
        "Thank you for trusting me enough to share this. Self-harm urges can be really intense and scary. You deserve compassionate support, not judgment.\n\nSome people find it helps to:\n- Hold ice cubes\n- Snap a rubber band on your wrist\n- Draw on yourself with red marker\n- Talk to someone immediately\n\nWould you like to talk about what triggers these feelings for you?",
    ],
    
    'depression': [
        "I hear that you're going through a really tough time right now. Depression can make everything feel so heavy and exhausting, and I want you to know that your feelings are completely valid.\n\nYou don't have to face this alone. Many people have walked this path and found their way through with support.\n\nWhat's been the hardest part for you lately?",
        
        "It sounds like you're carrying a lot of weight right now. Depression can make even simple things feel impossible, and that's not your fault.\n\nRemember:\n- These feelings, however intense, are temporary\n- You deserve compassion, especially from yourself\n- Small steps count as progress\n- Professional help can make a real difference\n\nWhat does your day-to-day look like right now?",
        
        "I'm really glad you're sharing this with me. Depression can be so isolating, and talking about it takes courage.\n\nHave you been able to talk to a doctor or therapist about how you're feeling? They can help create a plan to support you, whether that's therapy, medication, lifestyle changes, or a combination.\n\nHow long have you been feeling this way?",
    ],
    
    'anxiety': [
        "It sounds like you're experiencing a lot of anxiety right now. That racing, overwhelmed feeling can be so exhausting and uncomfortable.\n\nLet's take a moment together - can you try breathing in slowly for 4 counts, holding for 4, then out for 4? You're safe in this moment.\n\nWhat's been triggering these anxious feelings for you?",
        
        "Anxiety can feel so overwhelming, like your mind and body are in overdrive. I want you to know that what you're experiencing is real, and there are ways to manage it.\n\nSome things that might help right now:\n- Deep, slow breathing\n- Grounding yourself (name 5 things you can see, 4 you can touch, 3 you can hear)\n- Moving your body, even just a short walk\n\nWhat usually helps you when you feel this way?",
        
        "I hear you, and anxiety like this can be really frightening. Your mind might be racing with 'what ifs' and worst-case scenarios.\n\nRemember: anxiety lies. It makes everything seem more dangerous than it really is. You've gotten through anxious moments before, and you can get through this one too.\n\nWhat are you most worried about right now?",
    ],
    
    'stress': [
        "You're dealing with a lot of stress, and that's completely understandable. When everything piles up, it can feel like you're drowning in responsibilities and pressure.\n\nIt's okay to feel overwhelmed. That feeling is your mind and body telling you that you need some support and maybe a break.\n\nWhat's been weighing on you the most?",
        
        "Stress can build up until it feels like too much to handle. I'm glad you're talking about it - sometimes just sharing the burden can help lighten the load a little.\n\nHave you been able to take any time for yourself lately? Even small moments of rest matter.\n\nWhat would help you feel a bit lighter right now?",
    ],
    
    'trauma': [
        "Thank you for sharing something so difficult. Trauma can leave deep marks, and healing isn't linear - it's okay if you're still struggling with what happened.\n\nYou deserve professional support from someone trained in trauma therapy. They can help you process these experiences in a safe way.\n\nHow are you coping with these feelings right now?",
        
        "What you experienced was real and difficult, and your reactions to it are completely valid. Trauma can affect us in so many ways - flashbacks, nightmares, anxiety, and more.\n\nHealing is possible, though it takes time and support. A trauma-informed therapist can provide you with tools to process what happened.\n\nDo you have support in your life right now?",
    ],
    
    'general': [
        "Thank you for sharing that with me. I'm here to listen and support you, without any judgment. Your feelings and experiences are valid.\n\nTell me more about what's been on your mind.",
        
        "I appreciate you opening up. It takes courage to talk about what we're going through, especially during difficult times.\n\nHow are you feeling right now in this moment?",
        
        "I hear you, and I want you to know that you're not alone in what you're experiencing. Many people go through similar struggles, even if it doesn't always feel that way.\n\nWhat would be most helpful for you to talk about?",
        
        "That sounds really challenging. I'm glad you're here talking about it rather than keeping it all inside.\n\nWhat's been the hardest part of this for you?",
        
        "Your feelings are completely valid, and I'm here to support you through this. Sometimes just having someone listen can make a difference.\n\nWhat else has been going on?",
    ],
    
    'positive': [
        "I'm glad to hear things are going a bit better! It's important to acknowledge and celebrate the good moments, even small ones.\n\nWhat's been helping you feel better?",
        
        "That's wonderful to hear. Taking care of your mental health is so important, and it sounds like you're making positive steps.\n\nHow can I support you today?",
    ]
}

# Greeting responses
GREETINGS = [
    "Hello! I'm here to listen and support you. This is a safe, judgment-free space. How are you feeling today?",
    "Hi there! I'm glad you're here. This is a safe space where you can share whatever is on your mind. How are you doing?",
    "Welcome! I'm here to provide support and listen without judgment. What's been on your mind lately?",
]

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.symptom_counts = defaultdict(int)
    st.session_state.severity_score = 0
    st.session_state.risk_level = 'low'
    st.session_state.conversation_count = 0

def analyze_message(message):
    """Detect mental health symptoms"""
    detected = []
    message_lower = message.lower()
    
    for symptom, patterns in MENTAL_HEALTH_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, message_lower, re.IGNORECASE):
                detected.append(symptom)
                st.session_state.symptom_counts[symptom] += 1
                break
    
    return detected

def calculate_severity():
    """Calculate risk level"""
    score = 0
    for symptom, count in st.session_state.symptom_counts.items():
        weight = SEVERITY_WEIGHTS.get(symptom, 3)
        score += weight * min(count, 3)
    
    st.session_state.severity_score = score
    
    if score >= 25 or st.session_state.symptom_counts['suicidal'] > 0:
        st.session_state.risk_level = 'critical'
    elif score >= 15:
        st.session_state.risk_level = 'high'
    elif score >= 8:
        st.session_state.risk_level = 'moderate'
    else:
        st.session_state.risk_level = 'low'

def is_greeting(message):
    """Check if message is a greeting"""
    greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
    message_lower = message.lower().strip()
    return any(message_lower.startswith(g) for g in greetings) and len(message.split()) <= 3

def is_positive(message):
    """Check if message is positive"""
    positive_words = ['good', 'better', 'great', 'fine', 'okay', 'ok', 'well', 'happy', 'improving']
    return any(word in message.lower() for word in positive_words)

def get_response(message, symptoms):
    """Generate appropriate response based on symptoms"""
    
    # Check for greetings
    if is_greeting(message):
        return random.choice(GREETINGS)
    
    # Check for positive sentiment
    if is_positive(message) and not symptoms:
        return random.choice(RESPONSE_TEMPLATES['positive'])
    
    # Respond based on most severe symptom
    if 'suicidal' in symptoms:
        return random.choice(RESPONSE_TEMPLATES['suicidal'])
    elif 'self_harm' in symptoms:
        return random.choice(RESPONSE_TEMPLATES['self_harm'])
    elif 'trauma' in symptoms:
        return random.choice(RESPONSE_TEMPLATES['trauma'])
    elif 'depression' in symptoms:
        return random.choice(RESPONSE_TEMPLATES['depression'])
    elif 'anxiety' in symptoms:
        return random.choice(RESPONSE_TEMPLATES['anxiety'])
    elif 'stress' in symptoms:
        return random.choice(RESPONSE_TEMPLATES['stress'])
    else:
        return random.choice(RESPONSE_TEMPLATES['general'])

# Header
st.markdown("""
<div class="main-header">
    <h1>🧠 MindCare - Mental Health Support</h1>
    <p>Your safe, judgment-free space for emotional support</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("💙 Mental Health Overview")
    
    # Risk level indicator
    risk_colors = {
        'low': '🟢',
        'moderate': '🟡',
        'high': '🟠',
        'critical': '🔴'
    }
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>Risk Level: {risk_colors.get(st.session_state.risk_level, '⚪')} {st.session_state.risk_level.upper()}</h3>
        <p>Severity Score: {st.session_state.severity_score}</p>
        <p>Conversations: {st.session_state.conversation_count}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Crisis resources
    st.markdown("""
    <div class="crisis-box">
        <h3>🆘 Crisis Resources</h3>
        <p><strong>Suicide & Crisis Lifeline:</strong><br>988 (US) - 24/7 Support</p>
        <p><strong>Crisis Text Line:</strong><br>Text HOME to 741741</p>
        <p><strong>Emergency:</strong> 911</p>
        <p><strong>International:</strong><br>findahelpline.com</p>
    </div>
    """, unsafe_allow_html=True)
    
    # SOS Button
    if st.button("🔴 EMERGENCY SOS", type="primary", use_container_width=True):
        st.error("⚠️ If you're in immediate danger, please call 911 or go to your nearest emergency room.")
        st.warning("📞 Call 988 for the Suicide & Crisis Lifeline (24/7)")
        st.info("💬 Text HOME to 741741 for Crisis Text Line")
    
    st.markdown("---")
    
    # About section
    with st.expander("ℹ️ About MindCare"):
        st.write("""
        MindCare is a mental health support tool designed to:
        - Provide emotional support
        - Detect concerning patterns
        - Offer resources and guidance
        - Connect you with professional help
        
        **Important:** This is a support tool, not a replacement for professional mental health care.
        """)
    
    # Detected symptoms
    if st.session_state.symptom_counts:
        with st.expander("📊 Detected Patterns"):
            for symptom, count in st.session_state.symptom_counts.items():
                st.write(f"• {symptom.title()}: {count} mentions")

# Main chat area
st.header("💬 Your Safe Space to Talk")

# Display welcome message
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("""
        Hello! I'm here to listen and support you. 💙
        
        This is a safe, judgment-free space where you can share what's on your mind. 
        How are you feeling today?
        """)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything...", key="chat_input"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.conversation_count += 1
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Analyze message
    symptoms = analyze_message(prompt)
    calculate_severity()
    
    # Generate response
    with st.chat_message("assistant"):
        response = get_response(prompt, symptoms)
        st.markdown(response)
    
    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Check for crisis
    if st.session_state.risk_level == 'critical':
        st.error("⚠️ Your responses indicate you may be in crisis. Please reach out for immediate help.")
        st.warning("📞 Call 988 (Suicide & Crisis Lifeline) or 911 for emergencies")

# Footer
st.markdown("---")
st.caption("""
💙 Remember: You're not alone. Professional help is available.  
⚠️ This is a support tool, not a replacement for professional mental health care.  
🆘 For crisis: Call 988 (US) | Text HOME to 741741 | Emergency: 911
""")

# Reset button
if st.button("🔄 Start New Conversation"):
    st.session_state.messages = []
    st.session_state.symptom_counts = defaultdict(int)
    st.session_state.severity_score = 0
    st.session_state.risk_level = 'low'
    st.session_state.conversation_count = 0
    st.rerun()
