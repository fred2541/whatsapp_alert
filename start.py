import time
from setup import check_and_install

# Check dependency
check_and_install()

from mail_sender import send_mail, read_contact_email
from playwright.sync_api import sync_playwright
import qrcode
from qr_generator import generate_qr
from check_connect import check_connect
from get_discut import get_discut
from whatsapp_utils import get_message
from file_manager import sanitize_filename, save_discussions


USER_DATA_DIR = "./whatsapp_profile"


with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(USER_DATA_DIR, headless=True, args=["--headless=new", "--disable-gpu", "--disable-blink-features=AutomationControlled"])

    page = browser.new_page()
    page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
    page.evaluate("() => { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); }")
    page.evaluate("""
    () => {
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(param) {
            if (param === 37445) return "Intel Inc.";  // Fake GPU Vendor
            if (param === 37446) return "Intel Iris OpenGL Engine";  // Fake GPU Renderer
            return getParameter(param);
        };
    }
""")
    page.goto("https://web.whatsapp.com/")
    page.wait_for_load_state("networkidle")

    # Wait to charge and generate qrcode if necessary
    time.sleep(7)

    data_ref = check_connect(page)

    if data_ref:
        # Génération et affichage du QR code pour la connexion
        generate_qr(data_ref, "qrcode.png")
        print("Demande de connexion détectée")
        print("Scanner le QR Code généré dans 'qrcode.png' (Valable ~20 secondes !!!)")
        print("Puis redemarrer l'application")
    else:
        print("Connecté")
        discussions = get_discut(page)
        if discussions:
            # print("Discussions trouvées :")
            save_discussions(discussions)
            for i, discut in enumerate(discussions, start=1):
                # print(f"{i}. {discut['name']}")
                if discut['newmessage'] is not None:
                    # print(f"nouveau message")
                    discussion_selector = f"div[role='listitem']:has(span[dir='auto']:has-text('{discut['name']}'))"
                    try:
                        # wait for element interact
                        page.locator(discussion_selector).wait_for(state="visible", timeout=5000)
                        page.wait_for_load_state("networkidle")
                        time.sleep(2)
                        # CLick
                        page.locator(discussion_selector).click()
                        # Get the message
                        number_of_messages = int(discut['newmessage'])
                        message = get_message(page, number_of_messages)
                        message_list = []
                        safe_name = sanitize_filename(discut['name'])
                        contact_file = f"contact/{safe_name}.cnf"
                        email = read_contact_email(contact_file)
                        for i, html in enumerate(message, start=1):
                            # print(f"\nÉlément {i} :\n{html}\n")
                            formatted_message = f"Message {i} : {html}"
                            message_list.append(formatted_message)
                        if email:
                            send_mail(email, f"Nouveaux messages de {discut['name']}", message_list)
                    except Exception as e:
                        print(f"Erreur lors du clic sur {discut['name']} : {e}")


    # Maintenir la session ouverte
    # input("Push Enter to close navogator")

    browser.close()
