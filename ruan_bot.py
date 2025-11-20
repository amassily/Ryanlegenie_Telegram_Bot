from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

# --- CONFIGURATION PRINCIPALE ---

# Jeton d'API de votre bot : @RuanPCS_bot
import os
# ... autres imports

# --- CONFIGURATION PRINCIPALE ---

# Le TOKEN est maintenant récupéré depuis la variable d'environnement du serveur
TOKEN = os.environ.get('BOT_TOKEN') # Doit correspondre à la CLÉ que vous avez définie sur Render (ici 'BOT_TOKEN')
# ... le reste du code est inchangé

# URL de l'image à afficher à l'accueil
IMAGE_URL_ACCUEIL = 'https://th.bing.com/th/id/OIP.VIDJY1jRyPxMpe8L1QOJXwHaB6?w=301&h=90&c=7&r=0&o=7&pid=1.7&rm=3' 

# Lien d'inscription UNIQUE pour 1XBET (utilisé dans toutes les réponses)
LIEN_INSCRIPTION_1XBET = 'https://affpa.top/L?tag=d_2295205m_97c_&site=2295205&ad=97'

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- FONCTIONS UTILITAIRES : CRÉATION DE CLAVIERS ---

async def menu_principal_keyboard():
    """Crée le clavier avec les boutons de questions (menu principal)."""
    keyboard = [
        [InlineKeyboardButton("Inscription", callback_data='q_inscription')],
        [InlineKeyboardButton("Vidéo Explicative", callback_data='q_video')],
        [InlineKeyboardButton("Coupons / Offres", callback_data='q_coupons')],
        [InlineKeyboardButton("Dates du Projet", callback_data='q_dates')],
        [InlineKeyboardButton("Suivi du Projet", callback_data='q_suivi')],
    ]
    return InlineKeyboardMarkup(keyboard)

# --- FONCTIONS ASYNCHRONES DE GESTION ---

async def start(update, context):
    """Envoie une image, puis le message d'introduction avec le bouton 'Démarrer'."""
    
    # 1. Envoi de l'image (si une URL est configurée)
    if IMAGE_URL_ACCUEIL:
        await update.message.reply_photo(
            photo=IMAGE_URL_ACCUEIL,
            caption="Bienvenue sur le canal de La GENIE_RYAN !"
        )

    # 2. Le texte d'accueil avec description
    message_text = (
        "**Auteur GENIE_RYAN**\n\n"
        "Ici, tu retrouves toutes les informations sur la GENIE_RYAN : inscription, vidéo explicative, coupons, "
        "dates et suivi complet du projet.\n\n"
        "Sélectionne simplement la question affichée sur ton clavier — le bot te répond automatiquement sans que tu aies à écrire."
    )

    # Création du bouton "Démarrer"
    keyboard = [
        [InlineKeyboardButton("Démarrer", callback_data='menu_start')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def button_handler(update, context):
    """Gère le clic sur tous les boutons en ligne."""
    query = update.callback_query
    
    await query.answer()

    data = query.data
    
    # --- GESTION DU BOUTON "DÉMARRER" ---
    if data == 'menu_start':
        await query.edit_message_text(
            text="Quel sujet sur La Montante souhaitez-vous consulter ?",
            reply_markup=await menu_principal_keyboard()
        )
    
    # --- GESTION DES BOUTONS DU MENU PRINCIPAL ---
    
    # Réponse pour "Inscription" (q_inscription)
    elif data == 'q_inscription':
        inscription_message = (
            "📩 **RÉPONSE À LIRE ATTENTIVEMENT** 📩\n\n"
            "Parce que les coupons seront envoyés en code. Si tu n'as pas de compte déjà créé, tu ne pourras pas utiliser le code.\n"
            "Voici le seul site utilisé :\n"
            "🔗 **Lien d'inscription :**\n"
            f"[1XBET | INSCRIPTION OFFICIELLE](https://affpa.top/L?tag=d_2295205m_97c_&site=2295205&ad=97)"
        )
        await query.edit_message_text(
            text=inscription_message,
            parse_mode='Markdown',
            reply_markup=await menu_principal_keyboard()
        )
    
    # Réponse pour "Vidéo Explicative" (q_video)
    elif data == 'q_video':
        video_message = (
            "📹 **VOICI LA VIDÉO EXPLICATIVE** 📹\n\n"
            "Regarde-la jusqu'à la fin pour comprendre comment t'inscrire correctement.\n\n"
            "Crée ton compte **1XBET** et monte dans le train avec nous 🚆\n"
            "🔗 **Lien d'inscription :**\n"
            f"[1XBET | INSCRIPTION OFFICIELLE](https://affpa.top/L?tag=d_2295205m_97c_&site=2295205&ad=97)\n\n"
        )
        await query.edit_message_text(
            text=video_message,
            parse_mode='Markdown',
            reply_markup=await menu_principal_keyboard()
        )

    # Réponse pour "Coupons / Offres" (q_coupons) - Déjà mis à jour
    elif data == 'q_coupons':
        coupon_message = (
            "🔔 **RÉPONSE À LIRE ATTENTIVEMENT** 🔔\n\n"
            "Les coupons du *GENIE_RYAN* seront envoyés sous forme de code.\n"
            "Le code ne fonctionne que si tu as un compte créé sur le site :\n"
            "\n"
            "💰 **1XBET** 💰\n"
            "➡️ **LIEN POUR T'INSCRIRE :**\n"
            "[1XBET | INSCRIPTION OFFICIELLE](https://affpa.top/L?tag=d_2295205m_97c_&site=2295205&ad=97)" # J'ai conservé le lien spécifique que vous aviez donné ici
            "\n"
            "🚨 Je n'enverrai pas les captures dans le canal.\n"
            "Le code te permet de miser directement ."
        )

        await query.edit_message_text(
            text=coupon_message,
            parse_mode='Markdown',
            reply_markup=await menu_principal_keyboard()
        )

    # Réponse pour "Dates du Projet" (q_dates)
    elif data == 'q_dates':
        dates_message = (
            "📩 **RÉPONSE À LIRE ATTENTIVEMENT** 📩\n\n"
            "On démarre tous ensemble dans le canal public le **25 novembre**.\n\n"
            "Assure-toi d'avoir ton compte actif avant le début pour pouvoir utiliser le code des coupons :\n"
            "🔗 **Lien d'inscription :**\n"
            f"[1XBET | INSCRIPTION OFFICIELLE](https://affpa.top/L?tag=d_2295205m_97c_&site=2295205&ad=97)"
        )
        await query.edit_message_text(
            text=dates_message,
            parse_mode='Markdown',
            reply_markup=await menu_principal_keyboard()
        )

    # Réponse pour "Suivi du Projet" (q_suivi)
    elif data == 'q_suivi':
        suivi_message = (
            "📩 **RÉPONSE À LIRE ATTENTIVEMENT** 📩\n\n"
            "Assure-toi d'avoir ton compte **1XBET** actif sur le site.\n\n"
            "Les coupons seront envoyés en code, tu pourras les utiliser directement via ce lien d'inscription juste en-dessous.\n"
            "🔗 **Lien d'inscription :**\n"
            f"[1XBET | INSCRIPTION OFFICIELLE](https://affpa.top/L?tag=d_2295205m_97c_&site=2295205&ad=97)"
        )
        await query.edit_message_text(
            text=suivi_message,
            parse_mode='Markdown',
            reply_markup=await menu_principal_keyboard()
        )

    # Gestion de la réponse par défaut
    else:
        await query.edit_message_text(
            text=f"Désolé, information non reconnue. Veuillez choisir parmi les options du menu.",
            reply_markup=await menu_principal_keyboard()
        )


async def hello(update, context):
    """Gère la commande /hello."""
    await update.message.reply_text(f'Bonjour {update.effective_user.first_name} ! Je suis ravi de vous rencontrer.')

async def echo(update, context):
    """Gère les messages texte qui ne sont pas des commandes (fonctionnalité d'écho)."""
    await update.message.reply_text(f"Vous avez dit : {update.message.text}")


# --- FONCTION PRINCIPALE DE DÉMARRAGE DU BOT ---

def main():
    """Démarre le bot et configure ses gestionnaires."""
    
    application = Application.builder().token(TOKEN).build()

    # Ajout des gestionnaires de commandes standard
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hello", hello))

    # Ajout du gestionnaire de Requêtes de Rappel (pour gérer les clics sur les boutons en ligne)
    application.add_handler(CallbackQueryHandler(button_handler))

    # Ajout du gestionnaire de Messages (texte qui n'est pas une commande)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    )

    logger.info("RuanPCS_bot est démarré et écoute...")
    application.run_polling()

if __name__ == '__main__':
    main()