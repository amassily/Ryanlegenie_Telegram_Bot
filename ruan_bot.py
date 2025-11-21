from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
import logging
import os # ESSENTIEL pour lire la variable d'environnement

# --- CONFIGURATION PRINCIPALE ---

# Le TOKEN est maintenant lu depuis la variable d'environnement du serveur Render.
# La variable clé est 'BOT_TOKEN', qui contient votre jeton secret.
TOKEN = os.environ.get('BOT_TOKEN') 

# Vérification pour le cas où le TOKEN n'est pas défini (sécurité)
if not TOKEN:
    # Optionnel: si vous voulez garder votre jeton pour des tests LOCAUX (sur PC) seulement
    # Sinon, cette ligne DOIT rester vide ou commentée lors du déploiement sur Render.
    # TOKEN = '8075235573:AAE7TspWJxkgMCrKWlgHqUSfcWjKN7idrvk' 
    logging.error("Le jeton d'API n'a pas été trouvé (variable d'environnement BOT_TOKEN manquante).")
    # Pour le déploiement sur Render, on laisse l'exécution continuer, car Render garantit que la variable existe.

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
    
    # Répond immédiatement pour éviter l'erreur "Query is too old"
    await query.answer()

    data = query.data
    message_text = None # Initialisation du message de réponse

    # --- GESTION DU BOUTON "DÉMARRER" ---
    if data == 'menu_start':
        message_text = "Quel sujet sur La Montante souhaitez-vous consulter ?"
    
    # --- GESTION DES BOUTONS DU MENU PRINCIPAL ---
    
    elif data == 'q_inscription':
        message_text = (
            "📩 **RÉPONSE À LIRE ATTENTIVEMENT** 📩\n\n"
            "Parce que les coupons seront envoyés en code. Si tu n'as pas de compte déjà créé, tu ne pourras pas utiliser le code.\n"
            "Voici le seul site utilisé :\n"
            "🔗 **Lien d'inscription :**\n"
            f"[1XBET | INSCRIPTION OFFICIELLE]({LIEN_INSCRIPTION_1XBET})"
        )
    
    elif data == 'q_video':
        message_text = (
            "📹 **VOICI LA VIDÉO EXPLICATIVE** 📹\n\n"
            "Regarde-la jusqu'à la fin pour comprendre comment t'inscrire correctement.\n\n"
            "Crée ton compte **1XBET** et monte dans le train avec nous 🚆\n"
            "🔗 **Lien d'inscription :**\n"
            f"[1XBET | INSCRIPTION OFFICIELLE]({LIEN_INSCRIPTION_1XBET})\n\n"
        )

    elif data == 'q_coupons':
        coupon_message = (
            "🔔 **RÉPONSE À LIRE ATTENTIVEMENT** 🔔\n\n"
            "Les coupons du *GENIE_RYAN* seront envoyés sous forme de code.\n"
            "Le code ne fonctionne que si tu as un compte créé sur le site :\n"
            "\n"
            "💰 **1XBET** 💰\n"
            "➡️ **LIEN POUR T'INSCRIRE :**\n"
            f"[1XBET | INSCRIPTION OFFICIELLE]({LIEN_INSCRIPTION_1XBET})"
            "\n"
            "🚨 Je n'enverrai pas les captures dans le canal.\n"
            "Le code te permet de miser directement."
        )

    elif data == 'q_dates':
        message_text = (
            "📩 **RÉPONSE À LIRE ATTENTIVEMENT** 📩\n\n"
            "On démarre tous ensemble dans le canal public le **25 novembre**.\n\n"
            "Assure-toi d'avoir ton compte actif avant le début pour pouvoir utiliser le code des coupons :\n"
            "🔗 **Lien d'inscription :**\n"
            f"[1XBET | INSCRIPTION OFFICIELLE]({LIEN_INSCRIPTION_1XBET})"
        )

    elif data == 'q_suivi':
        message_text = (
            "📩 **RÉPONSE À LIRE ATTENTIVEMENT** 📩\n\n"
            "Assure-toi d'avoir ton compte **1XBET** actif sur le site.\n\n"
            "Les coupons seront envoyés en code, tu pourras les utiliser directement via ce lien d'inscription juste en-dessous.\n"
            "🔗 **Lien d'inscription :**\n"
            f"[1XBET | INSCRIPTION OFFICIELLE]({LIEN_INSCRIPTION_1XBET})"
        )

    # --- ÉDITION DU MESSAGE ET GESTION DES ERREURS ---
    if message_text:
        try:
            await query.edit_message_text(
                text=message_text,
                parse_mode='Markdown',
                reply_markup=await menu_principal_keyboard()
            )
        except BadRequest as e:
            # Gère l'erreur "Message is not modified" (clic répété sur le même bouton)
            if "Message is not modified" in e.message:
                logger.info("Message non modifié, ignorer l'erreur.")
                pass
            else:
                logger.error(f"Erreur BadRequest non gérée: {e}")
                raise # Renvoyer les autres erreurs (plus sérieuses)

    else:
        # Gestion de la réponse par défaut si la donnée n'est pas reconnue
        try:
            await query.edit_message_text(
                text=f"Désolé, information non reconnue. Veuillez choisir parmi les options du menu.",
                reply_markup=await menu_principal_keyboard()
            )
        except BadRequest:
             pass # Si le message par défaut ne peut pas être édité, on ignore.


async def hello(update, context):
    """Gère la commande /hello."""
    await update.message.reply_text(f'Bonjour {update.effective_user.first_name} ! Je suis ravi de vous rencontrer.')

async def echo(update, context):
    """Gère les messages texte qui ne sont pas des commandes (fonctionnalité d'écho)."""
    # Si le message vient du canal, on n'y répond pas, sinon le bot boucle.
    if update.message.chat.type == 'private':
        await update.message.reply_text(f"Vous avez dit : {update.message.text}")


# --- FONCTION PRINCIPALE DE DÉMARRAGE DU BOT ---

def main():
    """Démarre le bot et configure ses gestionnaires."""
    
    if not TOKEN:
        logger.error("DÉMARRAGE ÉCHOUÉ : Le jeton d'API est manquant.")
        return

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