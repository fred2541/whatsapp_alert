import qrcode

def generate_qr(data: str, filename="qrcode.png"):
    """
    Génère un QR code à partir des données fournies et l'enregistre dans un fichier.
    
    :param data: Données à encoder dans le QR code.
    :param filename: Nom du fichier de sortie (par défaut 'qrcode.png').
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img.save(filename)

    print(f"QR code généré et sauvegardé sous : {filename}")
