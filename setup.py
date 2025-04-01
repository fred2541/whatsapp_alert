import subprocess
import sys

def check_and_install():
    try:
        import playwright  # Vérifie si Playwright est installé
    except ImportError:
        print("Playwright n'est pas installé. Installation en cours...")
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
        print("Installation de Playwright terminée.")

        print("Installation des navigateurs Playwright...")
        subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
        print("Installation des navigateurs terminée.")
    
    try:
        import qrcode  # Vérifie si Playwright est installé
    except ImportError:
        print("qrcode n'est pas installé. Installation en cours...")
        subprocess.run([sys.executable, "-m", "pip", "install", "qrcode[pil]"], check=True)
        print("Installation de Playwright qrcode.")

# Si ce fichier est exécuté directement
if __name__ == "__main__":
    check_and_install_playwright()
