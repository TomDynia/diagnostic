import streamlit as st
import os

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Dynia IA : Diagnostic d'Automatisation",
    page_icon="📊",
    layout="centered"
)

# 2. CHARTE GRAPHIQUE DYNIA (CSS)
st.markdown("""
    <style>
    :root {
        --brand-deep: #0c2461;
        --brand-primary: #1e3799;
        --brand-accent: #00d2ff;
        --bg-light: #f8fafc;
    }
    
    .main { background-color: var(--bg-light); }
    
    h1, h2, h3 { color: var(--brand-deep) !important; font-weight: 700 !important; }
    
    .stForm {
        background-color: white;
        padding: 2rem;
        border-radius: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    .result-card {
        background-color: white;
        padding: 2rem;
        border-radius: 1.5rem;
        border-top: 10px solid var(--brand-primary);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
    }
    
    .advice-box {
        background-color: #f0f7ff;
        border-left: 5px solid var(--brand-accent);
        padding: 1rem;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    .score-display {
        font-size: 4rem;
        font-weight: 800;
        color: var(--brand-primary);
        text-align: center;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. EN-TÊTE (LOGO LOCAL ET TITRE)
col_logo, col_title = st.columns([1, 4])
with col_logo:
    # Utilisation du fichier local logo.png
    if os.path.exists("logo.png"):
        st.image("logo.png", width=150)
    else:
        st.title("DYNIA")

with col_title:
    st.title("📊 Audit de Maturité IA & Automatisation")
    st.write("Évaluez le potentiel d'automatisation de votre entreprise en 2 minutes.")

st.divider()

# 4. DÉFINITION DES QUESTIONS
QUESTIONS = {
    "emails": {
        "q": "Niveau d'automatisation de vos emails (Tri & Réponses) ?",
        "options": ["Tout manuel (0)", "Quelques modèles (3)", "IA génère des brouillons (7)", "Entièrement automatisé (10)"],
        "advice": "Automatisation des Emails : Utilisez Claude Code pour créer un agent de tri intelligent sur n8n."
    },
    "devis": {
        "q": "Processus de création de vos devis ?",
        "options": ["Saisie manuelle Word/Excel (0)", "Logiciel de facturation simple (4)", "Génération auto via CRM (8)", "IA analyse & génère le devis (10)"],
        "advice": "Gestion des Devis : Connectez votre CRM à n8n pour générer des PDF personnalisés en un clic."
    },
    "usage_ia": {
        "q": "Fréquence d'utilisation de Claude ou ChatGPT ?",
        "options": ["Jamais (0)", "Rarement (3)", "Hebdomadaire (6)", "Quotidien (10)"],
        "advice": "Usage IA : Installez le 'Cockpit Dynia' pour intégrer l'IA au cœur de vos outils de travail."
    },
    "connectivite": {
        "q": "Vos outils communiquent-ils entre eux (n8n/Zapier) ?",
        "options": ["Silos isolés (0)", "Quelques imports manuels (3)", "Quelques automatisations (7)", "Écosystème fluide (10)"],
        "advice": "Connectivité : Déployez n8n pour faire circuler vos données sans intervention humaine."
    },
    "crm": {
        "q": "État de votre base de données clients ?",
        "options": ["Inexistante / Papier (0)", "Fichier Excel (4)", "CRM peu utilisé (7)", "CRM à jour & synchronisé (10)"],
        "advice": "Base de Données : Automatisez la mise à jour de votre CRM via vos formulaires et emails."
    },
    "reunions": {
        "q": "Gestion de vos comptes-rendus de réunions ?",
        "options": ["Notes manuscrites (0)", "Notes tapées manuellement (4)", "Enregistrement simple (7)", "Synthèse IA automatique (10)"],
        "advice": "Synthèse de Réunion : Utilisez une IA de transcription couplée à Claude pour vos comptes-rendus."
    },
    "contenu": {
        "q": "Création de contenu (Réseaux, Newsletters) ?",
        "options": ["Page blanche (0)", "Inspiration manuelle (4)", "IA aide à la rédaction (8)", "Flux de contenu automatisé (10)"],
        "advice": "Contenu : Créez une 'Usine à Contenu' avec n8n pour planifier vos publications."
    },
    "prospection": {
        "q": "Méthode de prospection commerciale ?",
        "options": ["Recherche manuelle (0)", "Achat de listes (4)", "Scraping manuel (7)", "Prospection IA automatisée (10)"],
        "advice": "Prospection : Automatisez le scraping et l'enrichissement de leads pour vos commerciaux."
    },
    "support": {
        "q": "Réponse aux questions récurrentes des clients ?",
        "options": ["Réponse manuelle systématique (0)", "FAQ statique (4)", "Quelques macros (7)", "Base de connaissance IA (10)"],
        "advice": "Support Client : Implantez un assistant IA capable de répondre à 80% des questions courantes."
    },
    "documentation": {
        "q": "Accès à la documentation interne (Process) ?",
        "options": ["Mémoire humaine uniquement (0)", "Documents éparpillés (4)", "Wiki structuré (8)", "Wiki IA consultable (10)"],
        "advice": "Documentation : Centralisez vos process dans un Wiki IA pour une recherche instantanée."
    }
}

# 5. QUESTIONNAIRE (FORMULAIRE)
with st.form("audit_form"):
    st.subheader("📝 Votre Diagnostic")
    responses = {}
    for key, data in QUESTIONS.items():
        responses[key] = st.select_slider(data["q"], options=data["options"], value=data["options"][0])
    submitted = st.form_submit_button("Générer mon rapport de maturité")

# 6. LOGIQUE DE RÉSULTATS
if submitted:
    total_score = 0
    scores_list = []
    for key, val in responses.items():
        score = int(val.split('(')[-1].split(')')[0])
        total_score += score
        scores_list.append((key, score))
    
    scores_list.sort(key=lambda x: x[1])
    top_3_priorities = scores_list[:3]

    if total_score <= 40:
        profile, focus, color = "Débutant IA", "Installation des outils de base (Le Cockpit)", "#e53e3e"
    elif total_score <= 70:
        profile, focus, color = "Intermédiaire", "Connexion des outils & Workflows (n8n)", "#dd6b20"
    else:
        profile, focus, color = "Avancé", "Optimisation stratégique (Claude Code)", "#38a169"

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center;'>Votre Score de Maturité :</h2>", unsafe_allow_html=True)
    st.markdown(f'<div class="score-display">{total_score}/100</div>', unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-bottom:2rem;'><span style='background-color:{color}; color:white; padding:10px 20px; border-radius:30px; font-weight:bold;'>Profil : {profile}</span></div>", unsafe_allow_html=True)
    st.write(f"**Analyse stratégique :** Votre priorité actuelle est : **{focus}**.")
    st.divider()
    st.subheader("💡 Le Conseil de Tom : Vos 3 chantiers prioritaires")
    for key, score in top_3_priorities:
        st.markdown(f'<div class="advice-box"><strong>{QUESTIONS[key]["advice"]}</strong></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.button("📥 Télécharger mon rapport (PDF)", use_container_width=True)
    with c2: st.link_button("📅 Réserver ma session de coaching", "mailto:thomas@dynia.fr", type="primary", use_container_width=True)

# 7. PIED DE PAGE
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #94a3b8; font-size: 0.8rem;">© 2024 DYNIA IA - Diagnostic de Performance Opérationnelle</div>', unsafe_allow_html=True)