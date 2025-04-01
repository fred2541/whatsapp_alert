import os

def sanitize_filename(name):
    """Convert name to filename"""
    return "".join(c if c.isalnum() or c in "_-" else "_" for c in name).strip("_")

def save_discussions(discussions, folder_name="contact"):
    """
    Create a unique folder and add a file for each discussion.

    
    :param discussions: List of discussion with champ 'name'
    :param folder_name: Name of folder (default: 'contact')
    """
    # 🔹 Créer le dossier principal s'il n'existe pas
    os.makedirs(folder_name, exist_ok=True)

    for discut in discussions:
        name = discut["name"]  # Récupérer le nom de la discussion

        # 🔹 Nettoyer le nom pour éviter les caractères interdits
        safe_name = sanitize_filename(name)

        # 🔹 Définir le chemin du fichier
        file_path = os.path.join(folder_name, f"{safe_name}.cnf")

        # 🔹 Vérifier si le fichier existe déjà
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("#Conf for this contact\n")
                file.write("#You can use multiple mail address with comma separated\n")
                file.write('mail=""\n')  # Écrire la configuration par défaut