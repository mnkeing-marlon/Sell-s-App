import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Bienvenue", layout="wide")


# --- CONTENU PRINCIPAL ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)
# --- TEXTE ---
st.markdown("""<div class="warm-text">Chez <span class="highlight">House Switch</span>, nous croyons que chaque maison a une histoire, est un foyer de souvenirs. Tourner une nouvelle page en vendant votre maison avec sérénité<br><br>Notre mission va au-delà de la simple transaction immobilière :<br> nous révolutionnons le marché immobilier avec <span class="highlight">notre technologie de prédiction de prix intelligente<br><br> Ici, vendez votre maison a un prix qui la merite.</div>""", unsafe_allow_html=True)

# --- BOUTONS DÉCORATIFS VERTICAUX ---
st.markdown('<div class="services-title">🎯 Nos Services Premium</div>', unsafe_allow_html=True)

st.markdown("""
<div class="buttons-container">
    <button class="decorative-button-primary">VENDRE MA MAISON<br><small>Estimation précise et vente rapide</small></button>
    <button class="decorative-button-secondary">ACHETER UNE MAISON<br><small>Votre futur chez-vous vous attend</small></button>
</div>
""", unsafe_allow_html=True)

# --- MESSAGE POUR LA NAVIGATION ---
st.info("💡 **Utilisez la sidebar sur la gauche pour naviguer vers nos services**")
# Le reste de votre code (formulaire, etc.) va ici

# --- GALERIE D'IMAGES ---
st.markdown('<div class="gallery-title"> Dernieres ventes </div>', unsafe_allow_html=True)

@st.cache_data
def load_image_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        image = Image.open(BytesIO(response.content))
        return image
    except Exception as e:
        st.error(f"Erreur de chargement de l'image : {e}")
        return None

# --- DÉBUT de la section de chargement ---
# Un spinner s'affiche pendant les opérations de cette section
with st.spinner('Chargement des images...'):
    # Télécharger et mettre en cache toutes les images nécessaires
    image_urls = [
        "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg",
        "https://images.pexels.com/photos/280222/pexels-photo-280222.jpeg",
        "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg"
    ]
    
    loaded_images = []
    for url in image_urls:
        img = load_image_from_url(url)
        if img is not None:
            loaded_images.append(img)
# --- FIN de la section de chargement ---


# Afficher les images maintenant qu'elles sont chargées
cols = st.columns(3)
price = [("Maryland","240.000 $"),("Newyork","301.500 $"),("Miami","456.870 $")]
for idx, col in enumerate(cols):
    with col:
        if idx < len(loaded_images):
            st.image(loaded_images[idx], caption=f"{price[idx][0]} : {price[idx][1]}", width="stretch")

st.markdown('</div>', unsafe_allow_html=True)