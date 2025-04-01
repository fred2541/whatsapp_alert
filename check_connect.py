from playwright.sync_api import Page

def check_connect(page: Page) -> str | None:
    """
    Recherche un <div> suivi d'un autre <div> contenant un attribut 'data-ref'.
    Retourne la valeur de 'data-ref' si trouvée, sinon None.

    :param page: Instance Playwright de la page.
    :return: La valeur de 'data-ref' si trouvée, sinon None.
    """
    return page.evaluate("""
        () => {
            const divs = document.querySelectorAll('div');
            for (let i = 0; i < divs.length - 1; i++) {
                const currentDiv = divs[i];
                const nextDiv = divs[i + 1];  // Prend directement le div suivant dans la liste

                if (nextDiv.hasAttribute('data-ref')) {
                    return nextDiv.getAttribute('data-ref');
                }
            }
            return null;  // Aucun <div> suivi d'un <div data-ref> trouvé
        }
    """)
