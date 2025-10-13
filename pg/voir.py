import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# --- GALERIE D'IMAGES ---
st.markdown('<div class="gallery-title"> Boutique </div>', unsafe_allow_html=True)

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
with st.spinner('Chargement des images...'):
    image_urls = [
        "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg",
        "https://images.pexels.com/photos/280222/pexels-photo-280222.jpeg",
        "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg",
        "https://images.pexels.com/photos/164558/pexels-photo-164558.jpeg",
        "https://images.pexels.com/photos/1396122/pexels-photo-1396122.jpeg",
        "https://images.pexels.com/photos/1732414/pexels-photo-1732414.jpeg",
        "https://images.pexels.com/photos/221024/pexels-photo-221024.jpeg",
        "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg",
        "https://images.pexels.com/photos/53610/large-home-residential-house-architecture-53610.jpeg",
        "https://images.pexels.com/photos/1115804/pexels-photo-1115804.jpeg",
        "https://images.pexels.com/photos/2581922/pexels-photo-2581922.jpeg",
        "https://images.pexels.com/photos/2102587/pexels-photo-2102587.jpeg",
    ]
    
    loaded_images = []
    for url in image_urls:
        img = load_image_from_url(url)
        if img is not None:
            loaded_images.append(img)

price = [
    ("Maryland", "240.000 $"),
    ("Newyork", "301.500 $"),
    ("Miami", "456.870 $"),
    ("California", "589.200 $"),
    ("Texas", "325.750 $"),
    ("Florida", "278.900 $"),
    ("Illinois", "265.300 $"),
    ("Georgia", "219.600 $"),
    ("Arizona", "342.800 $"),
    ("Colorado", "412.500 $"),
    ("Washington", "485.000 $"),
    ("Virginia", "338.400 $")
]
# --- FIN de la section de chargement ---

# Afficher les images 3 par ligne
for i in range(0, len(loaded_images), 3):
    cols = st.columns(3)
    for j in range(3):
        idx = i + j
        if idx < len(loaded_images):
            with cols[j]:
                st.image(loaded_images[idx], caption=f"{price[idx][0]} : {price[idx][1]}", use_container_width=True)


st.markdown('</div>', unsafe_allow_html=True)
st.info("💡 **Utilisez la sidebar sur la gauche pour naviguer vers nos services**")
