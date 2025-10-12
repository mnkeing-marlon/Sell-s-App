import streamlit as st
from datetime import datetime
import pickle
import joblib
import numpy as np
import pandas as pd

st.set_page_config(page_title="Vendre ma maison", layout="wide")

st.markdown("<p style='text-align:center'> Pour estimer le prix actuel de votre maison, nous aurons besoin des informations suivantes </p>", unsafe_allow_html=True)

# ===== DICTIONNAIRE LOCALISATIONS =====
LOCATION_TO_ZIPCODE = {
    ('Seattle', 'Vallée Rainier'): '98178',
    ('Seattle', 'Lake City'): '98125',
    ('Kenmore', 'Centre-ville'): '98028',
    ('Seattle', 'Alki Beach'): '98136',
    ('Sammamish', 'Sammamish'): '98074',
    ('Redmond', 'Redmond'): '98053',
    ('Federal Way', 'Federal Way'): '98003',
    ('Des Moines', 'Des Moines'): '98198',
    ('Seattle', 'Bryant'): '98146',
    ('Maple Valley', 'Maple Valley'): '98038',
    ('Bellevue', 'Bellevue'): '98007',
    ('Seattle', 'Wedgewood'): '98115',
    ('Seattle', 'Ballard'): '98107',
    ('Seattle', 'West Seattle'): '98126',
    ('Duvall', 'Duvall'): '98019',
    ('Seattle', 'Green Lake'): '98103',
    ('Auburn', 'Auburn'): '98002',
    ('Seattle', 'Northgate'): '98133',
    ('Mercer Island', 'Mercer Island'): '98040',
    ('Auburn', 'Auburn Sud'): '98092',
    ('Kent', 'Kent'): '98030',
    ('Seattle', 'Queen Anne'): '98119',
    ('Seattle', 'Montlake'): '98112',
    ('Redmond', 'Redmond'): '98052',
    ('Issaquah', 'Issaquah'): '98027',
    ('Seattle', 'Sunset Hill'): '98117',
    ('Renton', 'Renton'): '98058',
    ('Auburn', 'Auburn'): '98001',
    ('Renton', 'Renton'): '98056',
    ('Seattle', 'Skyway'): '98166',
    ('Federal Way', 'Federal Way'): '98023',
    ('Vashon', 'Vashon Island'): '98070',
    ('Seattle', 'White Center'): '98148',
    ('Seattle', 'University District'): '98105',
    ('Kent', 'Kent'): '98042',
    ('Bellevue', 'Bellevue'): '98008',
    ('Renton', 'Renton'): '98059',
    ('Seattle', 'Capitol Hill'): '98122',
    ('Seattle', 'Mount Baker'): '98144',
    ('Bellevue', 'Bellevue'): '98004',
    ('Bellevue', 'Bellevue'): '98005',
    ('Kirkland', 'Kirkland'): '98034',
    ('Sammamish', 'Sammamish'): '98075',
    ('Seattle', 'Alki'): '98116',
    ('Black Diamond', 'Black Diamond'): '98010',
    ('Seattle', 'Rainier Beach'): '98118',
    ('Seattle', 'Magnolia'): '98199',
    ('Kent', 'Kent'): '98032',
    ('North Bend', 'North Bend'): '98045',
    ('Seattle', 'Eastlake'): '98102',
    ('Woodinville', 'Woodinville'): '98077',
    ('Seattle', 'Georgetown'): '98108',
    ('Seattle', 'Highline'): '98168',
    ('Seattle', 'Richmond Beach'): '98177',
    ('Snoqualmie', 'Snoqualmie'): '98065',
    ('Issaquah', 'Issaquah'): '98029',
    ('Bellevue', 'Bellevue'): '98006',
    ('Seattle', 'South Lake Union'): '98109',
    ('Enumclaw', 'Enumclaw'): '98022',
    ('Kirkland', 'Kirkland'): '98033',
    ('Seattle', 'Shoreline'): '98155',
    ('Fall City', 'Fall City'): '98024',
    ('Bothell', 'Bothell'): '98011',
    ('Kent', 'Kent'): '98031',
    ('Seattle', 'High Point'): '98106',
    ('Woodinville', 'Woodinville'): '98072',
    ('Seattle', 'Tukwila'): '98188',
    ('Carnation', 'Carnation'): '98014',
    ('Renton', 'Renton'): '98055',
    ('Medina', 'Medina'): '98039'
}

# ===== DICTIONNAIRE RENOVATION =====
RENOVATION_MAPPING = {
    "Aucune rénovation": 0,
    "Rénovation avant 2010": 1, 
    "Rénovation recente": 2
}

# Extraction des villes uniques pour le dropdown
villes_uniques = sorted(list(set([ville for ville, _ in LOCATION_TO_ZIPCODE.keys()])))

# Formulaire
# === PREMIÈRE RANGÉE : Localisation (HORS FORMULAIRE) ===
st.subheader("📍 Localisation")
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    ville_choisie = st.selectbox("Ville", options=villes_uniques, index=0, key='ville')

with row1_col2:
    quartiers_filtres = sorted([quartier for ville, quartier in LOCATION_TO_ZIPCODE.keys() if ville == st.session_state.ville])
    quartier_choisi = st.selectbox("Quartier", options=quartiers_filtres, index=0, key='quartier')

# Récupération du zipcode
zipcode = int(LOCATION_TO_ZIPCODE.get((st.session_state.ville, st.session_state.quartier), '00000'))

# === FORMULAIRE POUR LE RESTE ===
with st.form("prediction_form"):
    
    # === DEUXIÈME RANGÉE : Dates ===
    st.subheader("📅 Dates")
    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        date_construction = st.date_input("Date de construction", value=datetime(2000, 1, 1))
        
    with row2_col2:
        date_vente = st.date_input("Date de vente prévue", value=datetime.now())
        # Calcul de l'âge
        age = date_vente.year - date_construction.year
        age_u = date_construction.year - 2015
    
    # === DEUXIÈME RANGÉE : Surfaces ===
    st.subheader("📐 Surfaces")
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    
    with row2_col1:
        sqft_lot = st.slider("Surface du terrain (sqft)", min_value=0, max_value=50000, value=5000, step=100)
        st.metric("Surface terrain", f"{sqft_lot:,}")
        
    with row2_col2:
        sqft_living = st.slider("Surface habitable (sqft)", min_value=0, max_value=10000, value=2000, step=50)
        st.metric("Surface habitable", f"{sqft_living:,}")
        
    with row2_col3:
        sqft_basement = st.slider("Surface du sous-sol (sqft)", min_value=0, max_value=5000, value=500, step=50)
        st.metric("Surface sous-sol", f"{sqft_basement:,}")
    
    # === TROISIÈME RANGÉE : Caractéristiques ===
    st.subheader("🏠 Caractéristiques de la maison")
    row3_col1, row3_col2, row3_col3 = st.columns(3)
    
    with row3_col1:
        # Chambres et salles de bain
        bedrooms = st.slider("Nombre de chambres", min_value=0, max_value=10, value=3)
        bathrooms = st.slider("Nombre de salles de bain", min_value=0.0, max_value=8.0, value=2.0, step=0.5)
        floors = st.slider("Nombre d'étages", min_value=0.0, max_value=4.0, value=1.0, step=0.5)
        piece = bedrooms + bathrooms
        
    with row3_col2:
        # Évaluations
        view = st.slider("Vue (score 0-4)", min_value=0, max_value=4, value=0)
        condition = st.slider("État (score 1-5)", min_value=1, max_value=5, value=3)
        grade = st.slider("Qualité (score 1-13)", min_value=1, max_value=13, value=7)
        grade_combo = grade*sqft_living

        
    with row3_col3:
        # Autres
        periode_date = st.date_input("Date vente (mois et année)", 
                            value=datetime(2024, 1, 1),
                            min_value=datetime(1900, 1, 1),
                            max_value=datetime(2030, 12, 31))
        # Conversion selon ta règle : janvier 2014 = 1, janvier 2015 = 13, etc.
        periode = (periode_date.year - 2014) * 12 + periode_date.month

        renovation_cat_affichage = st.selectbox(
            "Catégorie de rénovation", 
            options=list(RENOVATION_MAPPING.keys())
        )
        renovation_cat = RENOVATION_MAPPING[renovation_cat_affichage]
    
    # === BOUTON DE PRÉDICTION ===

    # === BOUTON DE PRÉDICTION ===
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        predict_button = st.form_submit_button(
            "🔮 Prédire le prix", 
            use_container_width=True, 
            type="primary", 
            key="main_prediction_button"
        )

# Affichage des valeurs pour debug (optionnel)
if predict_button:

    columns=['periode', 'sqft_lot', 'floors', 'view', 'condition', 'grade_combo',
       'sqft_basement', 'age', 'renovation_cat', 'zipcode', 'piece']

    infos=[periode,sqft_lot,floors,view,condition,grade_combo,sqft_basement,age_u,renovation_cat
           ,zipcode,piece]
    df_initial = pd.DataFrame([infos], columns=columns)
    st.write(df_initial)

    grade_combo = np.log1p(grade_combo)
    #standard = [[age_u,grade_combo]]
  

    # Charger le scaler sauvegardé
    scaler_garde = joblib.load('scaler_garde.pkl')
    #age_uf, grade_combof = scaler_garde.transform(standard)[0]
    
    #Autres transformations
    sqft_lotf = np.log1p(np.sqrt(sqft_lot))
    sqft_basementf = np.log1p(np.sqrt(sqft_basement))

    infosf=[periode,sqft_lotf,floors,view,condition,grade_combo,sqft_basementf,age_u,renovation_cat
           ,zipcode,piece]
    df_model = pd.DataFrame([infosf], columns=columns)
    df_model[['age', 'grade_combo']]=scaler_garde.transform(df_model[['age', 'grade_combo']])
    st.write(df_model)


    st.success("Formulaire soumis avec succès !")

    # Recap des informations
    st.subheader("📋 Récapitulatif de vos informations")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Code postal :**    {zipcode}")
        st.write(f"**Âge de la maison:**    {age} ans")
        st.write(f"**Surface habitable:**    {sqft_living} ")
    with col2:
        st.write(f"**Surface terrain:**    {sqft_lot} ")
        st.write(f"**Nombre de pièces:**    {piece}")
        st.write(f"**Rénovation:**    {renovation_cat_affichage}")

    # Animation de chargement
    with st.spinner('🔮 Calcul de la prédiction en cours...'):
        import time
        time.sleep(3)  # Simulation du temps de calcul
        
        # Chargement du modèle et prédiction
        model = joblib.load('xgboost_model.pkl')
        prediction = model.predict(df_model)
        prix_predits = np.expm1(prediction)[0]

    # Affichage centré et stylisé du résultat
    st.markdown("---")

    # Div centrée avec texte centré
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
        margin: 20px auto;
        text-align: center;
        max-width: 600px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    '>
        <h2 style='margin: 0 0 20px 0; color: white; text-align: center;'>🏠 Estimation du prix</h2>
        <h1 style='font-size: 3em; margin: 20px 0; color: white; text-align: center;'>${prix_predits:,.0f}</h1>
        <p style='margin: 0; opacity: 0.9; text-align: center; font-size: 1.2em;'>Prix prédit pour votre propriété</p>
    </div>
    """, unsafe_allow_html=True)



    