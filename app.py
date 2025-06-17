import streamlit as st
import json
import random
import time
from datetime import datetime, timedelta
import base64
from pathlib import Path
import asyncio
import threading

# Configure Streamlit page
st.set_page_config(
    page_title="🍵 Teabuddy - Your Personal Chai Assistant",
    page_icon="🍵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced tea-themed CSS
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #d4a373 0%, #8c5523 100%);
        font-family: 'Poppins', sans-serif;
        color: #3c2f2f;
    }
    
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(255, 245, 224, 0.95);
        backdrop-filter: blur(12px);
        border-radius: 25px;
        margin: 2rem auto;
        box-shadow: 0 20px 40px rgba(60, 47, 47, 0.2);
        border: 2px solid #f4d35e;
        max-width: 800px;
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #8c5523 0%, #d4a373 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(60, 47, 47, 0.2);
    }
    
    .main-header p {
        font-size: 1.3rem;
        color: #5c4033;
        font-weight: 400;
        margin-bottom: 0;
    }
    
    .language-btn {
        background: linear-gradient(135deg, #d4a373 0%, #8c5523 100%);
        color: #fff5e1;
        border: 2px solid #f4d35e;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(140, 85, 35, 0.3);
        cursor: pointer;
    }
    
    .language-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(140, 85, 35, 0.4);
        background: linear-gradient(135deg, #e8b923 0%, #a86e33 100%);
    }
    
    .recipe-card {
        background: rgba(255, 245, 224, 0.95);
        backdrop-filter: blur(12px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(60, 47, 47, 0.2);
        margin: 1rem 0;
        border: 2px solid #f4d35e;
        transition: all 0.3s ease;
    }
    
    .recipe-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 45px rgba(60, 47, 47, 0.25);
    }
    
    .step-card {
        background: rgba(255, 245, 224, 0.9);
        backdrop-filter: blur(12px);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #d4a373;
        box-shadow: 0 8px 25px rgba(60, 47, 47, 0.1);
        transition: all 0.3s ease;
        border: 2px solid #f4d35e;
    }
    
    .step-card.active {
        background: linear-gradient(135deg, #fefae0 0%, #f4d35e 100%);
        border-left-color: #8c5523;
        box-shadow: 0 12px 35px rgba(140, 85, 35, 0.3);
        transform: scale(1.02);
    }
    
    .step-card.completed {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        border-left-color: #4caf50;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.2);
    }
    
    .timer-container {
        background: linear-gradient(135deg, #d4a373 0%, #8c5523 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(140, 85, 35, 0.3);
        color: #fff5e1;
        border: 2px solid #f4d35e;
    }
    
    .timer-display {
        font-size: 4rem;
        font-weight: 700;
        font-family: 'Courier New', monospace;
        text-shadow: 0 2px 4px rgba(60, 47, 47, 0.3);
        margin-bottom: 1rem;
    }
    
    .timer-label {
        font-size: 1.2rem;
        font-weight: 500;
        opacity: 0.9;
        margin-bottom: 1.5rem;
    }
    
    .progress-container {
        background: rgba(255, 245, 224, 0.3);
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
        margin: 1rem 0;
        border: 2px solid #f4d35e;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #fff5e1, #f4d35e);
        border-radius: 10px;
        transition: width 1s ease;
        box-shadow: 0 2px 8px rgba(255, 245, 224, 0. sobre);
    }
    
    .heat-indicator {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem;
        box-shadow: 0 4px 15px rgba(60, 47, 47, 0.1);
    }
    
    .heat-low { 
        background: linear-gradient(135deg, #fefae0 0%, #f4d35e 100%); 
        color: #8c5523; 
        border: 2px solid #d4a373;
    }
    .heat-medium { 
        background: linear-gradient(135deg, #fff3e0 0%, #e8b923 100%); 
        color: #a86e33; 
        border: 2px solid #f4d35e;
    }
    .heat-high { 
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%); 
        color: #d32f2f; 
        border: 2px solid #f44336;
    }
    
    .celebration {
        text pp-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #d4a373 0%, #8c5523 100%);
        color: #fff5e1;
        border-radius: 25px;
        margin: 2rem 0;
        box-shadow: 0 20px 40px rgba(140, 85, 35, 0.3);
        animation: celebrationPulse 2s ease-in-out infinite;
        border: 2px solid #f4d35e;
    }
    
    @keyframes celebrationPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .celebration h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(60, 47, 47, 0.3);
    }
    
    .ingredient-item {
        padding: 1rem;
        margin: 0.5rem 0;
        background: rgba(255, 245, 224, 0.8);
        border-radius: 10px;
        border-left: 4px solid #d4a373;
        position: relative;
        padding-left: 3rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(60, 47, 47, 0.05);
    }
    
    .ingredient-item:hover {
        background: rgba(255, 245, 224, 0.95);
        transform: translateX(5px);
    }
    
    .ingredient-item:before {
        content: "🍵";
        position: absolute;
        left: 1rem;
        top: 1rem;
        font-size: 1.2rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #d4a373 0%, #8c5523 100%);
        color: #fff5e1;
        border: 2px solid #f4d35e;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(140, 85, 35, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(140, 85, 35, 0.4);
        background: linear-gradient(135deg, #e8b923 0%, #a86e33 100%);
    }
    
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid #f4d35e;
        background: rgba(255, 245, 224, 0.9);
        backdrop-filter: blur(12px);
    }
    
    .metric-container {
        background: linear-gradient(135deg, rgba(255, 245, 224, 0.9) 0%, rgba(255, 245, 224, 0.7) 100%);
        backdrop-filter: blur(12px);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(60, 47, 47, 0.1);
        border: 2px solid #f4d35e;
    }
    
    .metric-container h3 {
        color: #8c5523;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .metric-container h2 {
        color: #3c2f2f;
        font-weight: 700;
        font-size: 2.5rem;
    }
    
    .step-instruction {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #3c2f2f;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    .step-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    
    .step-number {
        background: linear-gradient(135deg, #d4a373 0%, #8c5523 100%);
        color: #fff5e1;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(140, 85, 35, 0.3);
    }
    
    .timer-controls {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 1rem;
    }
    
    .timer-btn {
        background: rgba(255, 245, 224, 0.3);
        color: #fff5e1;
        border: 2px solid #f4d35e;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .timer-btn:hover {
        background: rgba(255, 245, 224, 0.5);
        border-color: #e8b923;
    }
    
    .floating-elements {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1000;
    }
    
    .floating-tea {
        position: absolute;
        font-size: 2rem;
        animation: float 6s ease-in-out infinite;
        opacity: 0.15;
        color: #f4d35e;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-30px) rotate(180deg); }
    }
    
    .footer {
        text-align: center;
        padding: 1rem;
        background: rgba(255, 245, 224, 0.95);
        backdrop-filter: blur(12px);
        border-radius: 15px;
        margin: 2rem auto;
        box-shadow: 0 8px 25px rgba(60, 47, 47, 0.2);
        border: 2px solid #f4d35e;
        max-width: 800px;
        font-size: 1.1rem;
        color: #5c4033;
        font-weight: 500;
    }
    
    .footer span {
        color: #8c5523;
        font-weight: 600;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 2.5rem; }
        .timer-display { font-size: 3rem; }
        .step-header { flex-direction: column; align-items: flex-start; }
        .timer-controls { flex-direction: column; }
        .footer { font-size: 1rem; padding: 0.75rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# Add floating tea elements for ambiance
def add_floating_elements():
    st.markdown("""
    <div class="floating-elements">
        <div class="floating-tea" style="top: 10%; left: 10%; animation-delay: 0s;">🍵</div>
        <div class="floating-tea" style="top: 20%; right: 15%; animation-delay: 1s;">🫖</div>
        <div class="floating-tea" style="bottom: 30%; left: 20%; animation-delay: 2s;">☕</div>
        <div class="floating-tea" style="bottom: 10%; right: 10%; animation-delay: 3s;">🍵</div>
        <div class="floating-tea" style="top: 50%; left: 5%; animation-delay: 4s;">🫖</div>
        <div class="floating-tea" style="top: 70%; right: 5%; animation-delay: 5s;">☕</div>
    </div>
    """, unsafe_allow_html=True)

# Load data files with caching
@st.cache_data
def load_recipes():
    try:
        with open('data/all_chai_recipes.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return get_sample_recipes()

@st.cache_data
def load_recommendation_map():
    try:
        with open('data/recommendation_map.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return get_sample_recommendations()

@st.cache_data
def load_translations(lang_code):
    try:
        with open(f'data/lang/{lang_code}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return get_fallback_translations()

# Sample data functions (fallbacks)
def get_sample_recipes():
    return {
        "classic_masala_chai": {
            "name": {
                "en": "Classic Masala Chai",
                "hi": "क्लासिक मसाला चाय",
                "bn": "ক্লাসিক মসলা চা"
            },
            "description": {
                "en": "Traditional Indian spiced tea with aromatic spices",
                "hi": "सुगंधित मसालों के साथ पारंपरिक भारतीय मसाला चाय",
                "bn": "সুগন্ধি মসলার সাথে ঐতিহ্যবাহী ভারতীয় মসলা চা"
            },
            "ingredients": [
                "2 cups water", "1 cup milk", "2 tsp black tea",
                "4 green cardamom", "1 cinnamon stick", "4 cloves",
                "1 inch ginger", "Sugar to taste"
            ],
            "steps": [
                {
                    "instruction": {
                        "en": "Crush spices lightly",
                        "hi": "मसालों को हल्का कुचलें",
                        "bn": "মসলা হালকা থেঁতো করুন"
                    },
                    "duration": 60,
                    "heat": "low"
                },
                {
                    "instruction": {
                        "en": "Boil water with spices",
                        "hi": "मसालों के साथ पानी उबालें",
                        "bn": "মসলা দিয়ে পানি ফুটান"
                    },
                    "duration": 300,
                    "heat": "high"
                },
                {
                    "instruction": {
                        "en": "Add tea leaves and simmer",
                        "hi": "चाय पत्ती डालें और उबालें",
                        "bn": "চা পাতা যোগ করুন এবং জ্বাল দিন"
                    },
                    "duration": 180,
                    "heat": "medium"
                },
                {
                    "instruction": {
                        "en": "Add milk and bring to boil",
                        "hi": "दूध डालें और उबाल लाएं",
                        "bn": "দুধ যোগ করুন এবং ফুটিয়ে নিন"
                    },
                    "duration": 240,
                    "heat": "medium"
                },
                {
                    "instruction": {
                        "en": "Add sugar, strain and serve",
                        "hi": "चीनी डालें, छान लें और परोसें",
                        "bn": "চিনি যোগ করুন, ছেঁকে পরিবেশন করুন"
                    },
                    "duration": 120,
                    "heat": "low"
                }
            ],
            "total_time": 900
        }
    }

def get_sample_recommendations():
    return {
        "happy-normal": ["classic_masala_chai"],
        "sad-normal": ["classic_masala_chai"],
        "tired-normal": ["classic_masala_chai"],
        "stressed-normal": ["classic_masala_chai"],
        "creative-normal": ["classic_masala_chai"]
    }

def get_fallback_translations():
    return {
        "app_title": "Teabuddy",
        "app_subtitle": "Your Personal Chai Assistant",
        "select_language": "Select Language",
        "mood_label": "How are you feeling?",
        "health_label": "How is your health?",
        "get_recommendation": "Get My Chai Recipe",
        "ingredients": "Ingredients",
        "cooking_steps": "Cooking Steps",
        "step": "Step",
        "start_step": "Start Step",
        "pause_step": "Pause",
        "resume_step": "Resume",
        "complete_step": "Complete Step",
        "timer_running": "Timer Running...",
        "step_complete": "Step Complete!",
        "next_step": "Next Step",
        "all_done": "All Done!",
        "bon_appetit": "Bon Appétit!",
        "enjoy_chai": "Enjoy your delicious chai!",
        "total_time": "Total Time",
        "minutes": " minutes",
        "seconds_remaining": "seconds remaining"
    }

# Recommendation logic
def get_recommendation(mood, health, recommendation_map):
    combination_key = f"{mood}-{health}"
    
    if combination_key in recommendation_map:
        recipe_ids = recommendation_map[combination_key]
        if recipe_ids:
            return random.choice(recipe_ids)
    
    # Fallback
    all_recipes = []
    for recipe_list in recommendation_map.values():
        all_recipes.extend(recipe_list)
    
    return random.choice(all_recipes) if all_recipes else list(load_recipes().keys())[0]

# Enhanced timer functionality
def format_time(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"

class TimerManager:
    def __init__(self):
        self.is_running = False
        self.start_time = None
        self.duration = 0
        self.elapsed = 0
        
    def start_timer(self, duration):
        self.duration = duration
        self.start_time = time.time()
        self.is_running = True
        self.elapsed = 0
        
    def pause_timer(self):
        if self.is_running:
            self.elapsed += time.time() - self.start_time
            self.is_running = False
            
    def resume_timer(self):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            
    def get_remaining_time(self):
        if self.is_running:
            current_elapsed = self.elapsed + (time.time() - self.start_time)
        else:
            current_elapsed = self.elapsed
            
        remaining = max(0, self.duration - current_elapsed)
        return int(remaining)
        
    def get_progress(self):
        if self.duration == 0:
            return 0
        if self.is_running:
            current_elapsed = self.elapsed + (time.time() - self.start_time)
        else:
            current_elapsed = self.elapsed
        return min(1.0, current_elapsed / self.duration)
        
    def is_complete(self):
        return self.get_remaining_time() <= 0

# Language selection with tea-themed UI
def language_selector():
    add_floating_elements()
    
    st.markdown('''
    <div class="main-header">
        <h1>🍵 Teabuddy</h1>
        <p>Your Personal Chai Assistant</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("### Choose Your Language / भाषा चुनें / ভাষা নির্বাচন করুন")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🇺🇸 English", key="lang_en", use_container_width=True):
            st.session_state.language = 'en'
            st.rerun()
    
    with col2:
        if st.button("🇮🇳 हिंदी", key="lang_hi", use_container_width=True):
            st.session_state.language = 'hi'
            st.rerun()
    
    with col3:
        if st.button("🇧🇩 বাংলা", key="lang_bn", use_container_width=True):
            st.session_state.language = 'bn'
            st.rerun()
    
    # Add footer
    st.markdown('''
    <div class="footer">
        Crafted with <span>♥</span> by Tuhin
    </div>
    ''', unsafe_allow_html=True)

# Enhanced tea-themed input form
def mood_health_input(translations):
    add_floating_elements()
    
    st.markdown(f'''
    <div class="main-header">
        <h1>🍵 {translations["app_title"]}</h1>
        <p>{translations["app_subtitle"]}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"🌐 {translations.get('change_language', 'Change Language')}", 
                    key="change_lang", use_container_width=True):
            del st.session_state.language
            st.rerun()
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🫖 " + translations["mood_label"])
        mood = st.selectbox(
            "",
            options=["", "happy", "sad", "tired", "stressed", "creative"],
            format_func=lambda x: {
                "": translations.get("select_mood", "Select your mood..."),
                "happy": "😊 " + translations.get("mood_happy", "Happy"),
                "sad": "😢 " + translations.get("mood_sad", "Sad"),
                "tired": "😴 " + translations.get("mood_tired", "Tired"),
                "stressed": "😰 " + translations.get("mood_stressed", "Stressed"),
                "creative": "🎨 " + translations.get("mood_creative", "Creative")
            }.get(x, x),
            key="mood_select"
        )
    
    with col2:
        st.markdown("### ☕ " + translations["health_label"])
        health = st.selectbox(
            "",
            options=["", "normal", "cold", "upset_stomach", "low_energy"],
            format_func=lambda x: {
                "": translations.get("select_health", "Select your health state..."),
                "normal": "💪 " + translations.get("health_normal", "Normal/Healthy"),
                "cold": "🤧 " + translations.get("health_cold", "Cold/Flu"),
                "upset_stomach": "🤢 " + translations.get("health_upset_stomach", "Upset Stomach"),
                "low_energy": "⚡ " + translations.get("health_low_energy", "Low Energy")
            }.get(x, x),
            key="health_select"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🍵 " + translations["get_recommendation"], type="primary", use_container_width=True):
        if mood and health:
            st.session_state.mood = mood
            st.session_state.health = health
            st.session_state.page = 'recipe'
            if 'timer_manager' in st.session_state:
                del st.session_state.timer_manager
            if 'current_step' in st.session_state:
                del st.session_state.current_step
            st.rerun()
        else:
            st.error("🚨 " + translations.get("error_missing_selection", 
                    "Please select both mood and health state."))
    
    # Add footer
    st.markdown('''
    <div class="footer">
        Crafted with <span>♥</span> by Tuhin
    </div>
    ''', unsafe_allow_html=True)

# Enhanced tea-themed recipe interface
def recipe_interface(translations):
    add_floating_elements()
    
    recipes = load_recipes()
    recommendation_map = load_recommendation_map()
    
    recipe_id = get_recommendation(st.session_state.mood, st.session_state.health, recommendation_map)
    
    if recipe_id not in recipes:
        st.error("Recipe not found!")
        return
    
    recipe = recipes[recipe_id]
    lang = st.session_state.language
    
    recipe_name = recipe.get('name', {}).get(lang, recipe.get('name', {}).get('en', 'Unknown Recipe'))
    recipe_desc = recipe.get('description', {}).get(lang, recipe.get('description', {}).get('en', ''))
    
    st.markdown(f'''
    <div class="main-header">
        <h1>🍵 {recipe_name}</h1>
        <p>{recipe_desc}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← " + translations.get("back_to_home", "Back to Home")):
            st.session_state.page = 'input'
            for key in ['timer_manager', 'current_step', 'step_status', 'all_complete']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### 🥄 {translations['ingredients']}")
        st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
        ingredients_html = ""
        for ingredient in recipe.get('ingredients', []):
            ingredients_html += f'<div class="ingredient-item">{ingredient}</div>'
        st.markdown(ingredients_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        total_minutes = recipe.get('total_time', 0) // 60
        st.markdown(f'''
        <div class="metric-container">
            <h3>⏱️ {translations["total_time"]}</h3>
            <h2>{total_minutes}{translations["minutes"]}</h2>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown(f"### 👨‍🍳 {translations['cooking_steps']}")
    
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
        st.session_state.step_status = ['pending'] * len(recipe.get('steps', []))
        st.session_state.timer_manager = TimerManager()
    
    steps = recipe.get('steps', [])
    
    for i, step in enumerate(steps):
        instruction = step.get('instruction', {})
        instruction_text = instruction.get(lang, instruction.get('en', '')) if isinstance(instruction, dict) else instruction
        
        status = st.session_state.step_status[i]
        card_class = f"step-card {status}" if status != 'pending' else "step-card"
        
        with st.container():
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="step-header">
                <div class="step-number">{translations['step']} {i+1}</div>
                <div style="display: flex; gap: 1rem; align-items: center;">
                    <span class="heat-indicator heat-{step.get('heat', 'medium')}">
                        🔥 {translations.get(f"heat_{step.get('heat', 'medium')}", step.get('heat', 'medium').title())}
                    </span>
                    <span style="font-weight: 600; color: #3c2f2f;">
                        ⏱️ {format_time(step.get('duration', 0))}
                    </span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'<div class="step-instruction">{instruction_text}</div>', unsafe_allow_html=True)
            
            if status == 'pending' and i == st.session_state.current_step:
                col1, col2 = st.columns([2, 1])
                with col2:
                    if st.button(f"▶️ {translations['start_step']}", key=f"start_{i}", use_container_width=True):
                        st.session_state.step_status[i] = 'active'
                        st.session_state.timer_manager.start_timer(step.get('duration', 0))
                        st.rerun()
            
            elif status == 'active':
                timer = st.session_state.timer_manager
                remaining = timer.get_remaining_time()
                progress = timer.get_progress()
                
                if timer.is_complete():
                    st.session_state.step_status[i] = 'completed'
                    st.session_state.current_step += 1
                    
                    if st.session_state.current_step >= len(steps):
                        st.session_state.all_complete = True
                    
                    st.success(f"✅ {translations['step_complete']}")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                
                st.markdown(f'''
                <div class="timer-container">
                    <div class="timer-label">{translations.get('timer_running', 'Timer Running...')}</div>
                    <div class="timer-display">{format_time(remaining)}</div>
                    <div class="progress-container">
                        <div class="progress-fill" style="width: {progress * 100}%"></div>
                    </div>
                    <div style="font-size: 1.1rem; opacity: 0.9;">
                        {remaining} {translations.get('seconds_remaining', 'seconds remaining')}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if timer.is_running:
                        if st.button(f"⏸️ {translations.get('pause_step', 'Pause')}", key=f"pause_{i}"):
                            timer.pause_timer()
                            st.rerun()
                    else:
                        if st.button(f"▶️ {translations.get('resume_step', 'Resume')}", key=f"resume_{i}"):
                            timer.resume_timer()
                            st.rerun()
                
                with col2:
                    if st.button(f"⏭️ {translations.get('complete_step', 'Complete Step')}", key=f"complete_{i}"):
                        st.session_state.step_status[i] = 'completed'
                        st.session_state.current_step += 1
                        
                        if st.session_state.current_step >= len(steps):
                            st.session_state.all_complete = True
                        
                        st.success(f"✅ {translations['step_complete']}")
                        st.balloons()
                        st.rerun()
                
                if timer.is_running:
                    time.sleep(1)
                    st.rerun()
            
            elif status == 'completed':
                st.markdown('<div style="text-align: center; padding: 1rem;"><h3 style="color: #4caf50;">✅ Completed</h3></div>', 
                           unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.get('all_complete', False):
        st.markdown(f'''
        <div class="celebration">
            <h1>🎉 {translations["bon_appetit"]} 🎉</h1>
            <h3>✨ {translations.get("enjoy_chai", "Enjoy your delicious chai!")} ✨</h3>
            <p style="font-size: 1.2rem; margin-top: 1rem; opacity: 0.9;">
                Your perfect cup of chai is ready! Savor the warmth and aroma of your handcrafted tea.
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.balloons()
        st.snow()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Make Another Chai", type="primary", use_container_width=True):
                for key in ['current_step', 'step_status', 'timer_manager', 'all_complete', 'mood', 'health']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.page = 'input'
                st.rerun()
    
    # Add footer
    st.markdown('''
    <div class="footer">
        Crafted with <span>♥</span> by Tuhin
    </div>
    ''', unsafe_allow_html=True)

# Main app logic
def main():
    load_css()
    
    if 'language' not in st.session_state:
        st.session_state.language = None
    
    if 'page' not in st.session_state:
        st.session_state.page = 'input'
    
    if st.session_state.language is None:
        language_selector()
        return
    
    translations = load_translations(st.session_state.language)
    
    if st.session_state.page == 'input':
        mood_health_input(translations)
    elif st.session_state.page == 'recipe':
        recipe_interface(translations)

if __name__ == "__main__":
    main()