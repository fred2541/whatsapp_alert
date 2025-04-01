from playwright.sync_api import Page

def get_discut(page: Page) -> list[dict]:
    """
    Recherche tous les <div role="listitem"> et récupère :
    - Le texte du premier <span> (toujours présent).
    - Le texte du second <span> s'il existe dans un <div>.
    
    Retourne une liste de dictionnaires contenant ces deux valeurs.

    :param page: Instance Playwright de la page.
    :return: Liste des textes extraits sous forme de dictionnaire.
    """
    return page.evaluate("""
        () => {
            const messages = [];
            const listItems = document.querySelectorAll('div[role="listitem"]');  // Sélectionner tous les éléments listitem
            
            listItems.forEach(item => {
                
                const firstSpan = item.querySelector('div > span[dir="auto"]');
                let name = firstSpan ? firstSpan.innerText.trim() : null;

                
                let newmessage = null;
                const gridCell = item.querySelector('div[role="gridcell"][aria-colindex="1"] > span > div');
                
                if (gridCell) {
                    const specialSpan = gridCell.querySelector('span');
                    if (specialSpan) {
                        newmessage = specialSpan.innerText.trim();
                    }
                }

                
                if (name) {
                    messages.push({ name, newmessage });
                }
            });

            return messages;
        }
    """)

