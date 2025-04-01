def get_message(page, number_of_messages):
    """
    Récupère un nombre spécifié de messages (`span[dir="ltr"]`) dans `div[id="main"]` 
    et retourne uniquement leur texte.
    
    :param page: Instance Playwright de la page.
    :param number_of_messages: Nombre de messages à récupérer.
    :return: Liste contenant uniquement les textes des messages.
    """
    return page.evaluate("""
        (number_of_messages) => {
            // Sélectionner l'élément avec l'id "main"
            const mainElement = document.querySelector('div[id="main"]');
            
            // Vérifier si l'élément principal existe
            if (mainElement) {
                // Récupérer tous les span[dir="ltr"] sous l'élément "main"
                const messageContainers = mainElement.querySelectorAll('div[tabindex="-1"] span[dir="ltr"]');
                
                // Limiter au nombre spécifié
                const limitedContainers = Array.from(messageContainers).slice(-number_of_messages);
                
                // Retourner uniquement le texte des messages
                return limitedContainers.map(el => el.innerText.trim());
            }
            return [];  // Retourner une liste vide si "main" n'est pas trouvé
        }
    """, number_of_messages)
