import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="House Switch", layout="wide", page_icon="🏠")

# --- CONFIGURATION DES PAGES DOIT ÊTRE EN HAUT ---
pages = [
    st.Page("pg/acc.py", title = "Accueil", icon="🏠"),
    st.Page("pg/vendre.py", title="Vendre", icon="💵"),
    st.Page("pg/voir.py", title="Voir", icon="🔍"),    
]

# Navigation HIDDEN - DOIT ÊTRE APRÈS LA CONFIG DES PAGES
pg = st.navigation(pages, position="hidden")

# --- CSS AMÉLIORÉ ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.96), rgba(255,255,255,0.96)),
                    url('https://images.pexels.com/photos/3768131/pexels-photo-3768131.jpeg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }
    
    .main-container {
        background: transparent;
        padding: 2rem;
        margin: 0 auto;
        max-width: 900px;
        text-align: center;
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
    }
    
    /* Texte simple et lisible */
    .warm-text {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 3rem;
        color: #333;
        line-height: 1.7;
        font-weight: 400;
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        border-left: 4px solid #667eea;
        border-right: 4px solid #4ECDC4;
    }
    
    .highlight {
        color: #667eea;
        font-weight: 700;
    }
    
    /* Container pour boutons centrés VERTICALEMENT */
    .buttons-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.5rem;
        margin: 3rem 0 4rem 0;
    }
    
    /* Boutons GROS et STYLÉS (décoratifs) */
    .decorative-button-primary {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%) !important;
        border: none !important;
        border-radius: 18px !important;
        padding: 1.5rem 3rem !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        transition: all 0.4s ease !important;
        color: white !important;
        min-width: 320px !important;
        box-shadow: 0 12px 30px rgba(255, 107, 107, 0.4) !important;
        letter-spacing: 0.5px !important;
        cursor: pointer;
        opacity: 0.9;
    }
    
    .decorative-button-secondary {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%) !important;
        border: none !important;
        border-radius: 18px !important;
        padding: 1.5rem 3rem !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        transition: all 0.4s ease !important;
        color: white !important;
        min-width: 320px !important;
        box-shadow: 0 12px 30px rgba(78, 205, 196, 0.4) !important;
        letter-spacing: 0.5px !important;
        cursor: pointer;
        opacity: 0.9;
    }
    
    .decorative-button-primary:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 20px 40px rgba(255, 107, 107, 0.5) !important;
        opacity: 1 !important;
    }
    
    .decorative-button-secondary:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 20px 40px rgba(78, 205, 196, 0.5) !important;
        opacity: 1 !important;
    }
    
    .services-title {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        text-align: center;
        margin: 2rem 0 1rem 0;
        color: #333;
        font-weight: 700;
        background: linear-gradient(135deg, #333 0%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .gallery-title {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        text-align: center;
        margin: 3rem 0 2rem 0;
        color: #333;
        font-weight: 700;
        background: linear-gradient(135deg, #333 0%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR POUR LA NAVIGATION ---
with st.sidebar:
    st.title("Navigation")
    st.markdown("---")
    if st.button("Accueil", width='stretch'):
        st.switch_page("pg/acc.py")
    if st.button("Vendre ma maison", width='stretch'):
        st.switch_page("pg/vendre.py")
    if st.button("Boutique", width='stretch'):
        st.switch_page("pg/voir.py")

    st.markdown("---")
    st.markdown("**Contactez-nous**")
    st.markdown("📞 (+237) 6 97 54 54 88")
    st.markdown("📧 mnkeing@gmail.com")



# --- EN-TÊTE ---
st.markdown('<h1 class="main-title">🏠 House Switch</h1>', unsafe_allow_html=True)







# --- pg.run() DOIT ÊTRE À LA FIN ET UNE SEULE FOIS ---

pg.run()
