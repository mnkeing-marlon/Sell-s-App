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
# --- SIDEBAR POUR LA NAVIGATION ---
with st.sidebar:
    # En-tête avec style
    st.markdown(
        """
        <div style="padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 10px; margin-bottom: 2rem; text-align: center;">
            <h2 style="color: white; margin: 0; font-size: 1.5rem; font-weight: 600;">Navigation</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Séparateur stylisé
    st.markdown("<hr style='border: none; height: 2px; background: linear-gradient(to right, transparent, #667eea, transparent); margin: 1.5rem 0;'>", 
                unsafe_allow_html=True)
    
    # Style CSS pour les boutons
    st.markdown("""
        <style>
        .nav-button {
            width: 100%;
            padding: 0.75rem 1rem;
            margin: 0.5rem 0;
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            color: #333;
            font-size: 1rem;
            font-weight: 500;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .nav-button:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            border-color: #667eea;
        }
        .nav-button:active {
            transform: translateY(0);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Conteneur pour les boutons
    with st.container():
        # Bouton Accueil
        if st.button("Accueil", key="accueil_btn", 
                     use_container_width=True,
                     type="secondary"):
            st.switch_page("pg/acc.py")
        
        # Bouton Vendre ma maison
        if st.button("Vendre ma maison", key="vendre_btn",
                     use_container_width=True,
                     type="secondary"):
            st.switch_page("pg/vendre.py")
        
        # Bouton Boutique
        if st.button("Boutique", key="boutique_btn",
                     use_container_width=True,
                     type="secondary"):
            st.switch_page("pg/voir.py")
    
    # Séparateur stylisé
    st.markdown("<hr style='border: none; height: 2px; background: linear-gradient(to right, transparent, #667eea, transparent); margin: 1.5rem 0;'>", 
                unsafe_allow_html=True)
    
    # Section contact avec style
    st.markdown(
        """
        <div style="padding: 1.25rem; background: #f8f9fa; border-radius: 10px; 
                    border-left: 4px solid #667eea; margin-top: 1rem;">
            <h3 style="color: #2d3748; margin-top: 0; margin-bottom: 1rem; font-size: 1.1rem;">
                Contactez-nous
            </h3>
            <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                <div style="width: 30px; height: 30px; background: #667eea; border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                    <span style="color: white; font-size: 0.9rem;">T</span>
                </div>
                <span style="color: #4a5568; font-size: 0.95rem;">(+237) 6 97 54 54 88</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 30px; height: 30px; background: #764ba2; border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                    <span style="color: white; font-size: 0.9rem;">@</span>
                </div>
                <span style="color: #4a5568; font-size: 0.95rem;">mnkeing@gmail.com</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Pied de page discret
    st.markdown(
        """
        <div style="text-align: center; margin-top: 2rem; padding-top: 1rem; 
                    border-top: 1px solid #e0e0e0; color: #a0aec0; font-size: 0.8rem;">
            © 2024 Tous droits réservés
        </div>
        """,
        unsafe_allow_html=True
    )



# --- EN-TÊTE ---
st.markdown('<h1 class="main-title">🏠 House Switch</h1>', unsafe_allow_html=True)







# --- pg.run() DOIT ÊTRE À LA FIN ET UNE SEULE FOIS ---

pg.run()

