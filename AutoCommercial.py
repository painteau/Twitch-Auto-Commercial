from PIL import Image
from twitch import TwitchClient
import time
import cv2
import os
import logging
from logging.handlers import RotatingFileHandler
 from config import * 
 
clear = lambda: os.system('cls')

 
# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)
 
# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
 
# création d'un second handler qui va rediriger chaque écriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

pause = 1



clear()

while True:
    logger.info("Début du script")
    clear()
    # Preparing Twitch check
    client = TwitchClient(client_id, oauth_token)
    # FINDING ID of that twitch channel
    users = client.users.translate_usernames_to_ids(channel_name)
    for user in users:
        Current_ID = user.id
        Current_Name = user.display_name

    # HANDLING DATA
    channel = client.streams.get_stream_by_user(Current_ID)

    if channel is None:
        logger.info("%s est offline", Current_Name)
    else:
        logger.info("%s est live", Current_Name)
        channel = client.channels.get()
        channel_id = channel.id
        # CAPTURE DE LA FRAME DU STREAM
        # on efface la capture précédente
        if os.path.exists('capture.jpg'):
            os.remove('capture.jpg')
        else:
            logger.warning("Impossible de supprimer le fichier car il n'existe pas")
        urlrtmp = "ffmpeg -i {} -timeout 20 -r 1 capture.jpg".format(rtmp)
        try:
            os.system(urlrtmp)
        except:
            pass
        clear()
        # COMPARAISON DES IMAGES
        i1 = Image.open("capture.jpg")
        i2 = Image.open("reference.png")
        assert i1.mode == i2.mode, "Different kinds of images."
        assert i1.size == i2.size, "Different sizes."
        print ("Comparaison des deux images...")
        pairs = zip(i1.getdata(), i2.getdata())
        if len(i1.getbands()) == 1:
  	  # for gray-scale jpegs
            dif = sum(abs(p1-p2) for p1,p2 in pairs)
        else:
            dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
 
        ncomponents = i1.size[0] * i1.size[1] * 3
        difference = (dif / 255.0 * 100) / ncomponents
        similitude = 100-difference
        logger.info("Similitude de l'image : %s", similitude)
        if difference > difftrigger:
            logger.info("ce n'est pas une pause...")
        else:
            logger.info("C'est une pause...")
            print ("LANCEMENT DE LA PUB DE 180s")            
            try:
                lapub = client.channels.start_commercial(channel.id,180)
                logger.info("Connexion reussie...")
                print ("Pause de 180 secondes...")
                pause = 181
                while pause > 31:
                    pause = pause - 1
                    print ("Restart dans", pause, "secondes...")
                    time.sleep(1)
                logger.info("fin du break")
            except:
                logger.error("Echec du lancement de pub...")
            
                
    bigpause = 31
    while bigpause > 1:
                bigpause = bigpause - 1
                print ("Restart dans", bigpause, "secondes...")
                time.sleep(1) 
    logger.info("restart")
