import tkinter as tk
import threading
import vlc
from gpiozero import Button

# Définir la broche GPIO que vous souhaitez surveiller
broche_17 = Button(17)
broche_22 = Button(22)
broche_27 = Button(27)

# Créer une instance VLC globale
instance = vlc.Instance()
player = vlc.MediaPlayer(instance)

# Flag pour arrêter le lecteur
stop_flag = threading.Event()

# Verrou pour s'assurer qu'une seule vidéo prioritaire est jouée à la fois
play_lock = threading.Lock()

# Variable pour suivre la vidéo actuelle
current_video = "video1"  # par défaut, on commence avec la vidéo 1

# Flag pour gérer le verrouillage des signaux après le lancement d'une vidéo
signal_lock = threading.Event()

def stop_current_stream():
    """Arrête le lecteur actuel."""
    stop_flag.set()
    player.stop()

def start_signal_lock_timer(timer):
    """Active un verrou de 1 minute et 10 secondes après le lancement d'une vidéo."""
    signal_lock.set()  # Activer le verrou
    threading.Timer(timer, signal_lock.clear).start()  # Délai de secondes pour relâcher le verrou

def signal_detecte_17():
    """Fonction appelée lorsque le bouton 17 est pressé pour démarrer la vidéo 2."""
    global current_video
    if play_lock.locked() or current_video == "video2" or signal_lock.is_set():
        print("Vidéo prioritaire en cours ou déjà jouée, signal ignoré.")
        return
    stop_current_stream()  # Arrêter le lecteur actuel si nécessaire
    stop_flag.clear()  # Réinitialiser le flag pour le nouveau flux
    
    # Démarrer la vidéo 2
    current_video = "video2"
    threading.Thread(target=stream_2).start()

    # Démarrer le timer de verrouillage
    start_signal_lock_timer(62)

def signal_detecte_22():
    """Fonction appelée lorsque le bouton 22 est pressé pour démarrer la vidéo 3."""
    global current_video
    if play_lock.locked() or current_video == "video3" or signal_lock.is_set():
        print("Vidéo prioritaire en cours ou déjà jouée, signal ignoré.")
        return
    stop_current_stream()  # Arrêter le lecteur actuel si nécessaire
    stop_flag.clear()  # Réinitialiser le flag pour le nouveau flux
    
    # Démarrer la vidéo 3
    current_video = "video3"
    threading.Thread(target=stream_3).start()

    # Démarrer le timer de verrouillage
    start_signal_lock_timer(61)

def signal_detecte_27():
    """Fonction appelée lorsque le bouton 27 est pressé pour démarrer la vidéo 4."""
    global current_video
    if play_lock.locked() or current_video == "video4" or signal_lock.is_set():
        print("Vidéo prioritaire en cours ou déjà jouée, signal ignoré.")
        return
    stop_current_stream()  # Arrêter le lecteur actuel si nécessaire
    stop_flag.clear()  # Réinitialiser le flag pour le nouveau flux
    
    # Démarrer la vidéo 4
    current_video = "video4"
    threading.Thread(target=stream_4).start()

    # Démarrer le timer de verrouillage
    start_signal_lock_timer(73)

# Attacher une fonction de rappel pour détecter les changements
broche_17.when_released = signal_detecte_17
broche_22.when_released = signal_detecte_22
broche_27.when_released = signal_detecte_27

# Interface graphique
fenetre = tk.Tk()
fenetre.geometry('1920x1080')
fenetre.title('App Vidéo en plein écran')
fenetre.resizable(height=False, width=False)
fenetre.attributes('-fullscreen', True)
fenetre.config(cursor="")

def stream():
    """Joue la première vidéo dans VLC en boucle."""
    global player, current_video, fenetre
    fenetre.attributes('-fullscreen', True)
    fenetre.config(cursor="")
    current_video = "video1"  # Mettre à jour la vidéo actuelle
    stop_flag.clear()
    
    fenetre.attributes('-fullscreen', True)
    fenetre.config(cursor="")
    
    media = vlc.Media(video_name)
    player.set_media(media)
    win_id = fenetre.winfo_id()
    player.set_xwindow(win_id)  # Utiliser set_xwindow pour Unix-like systèmes
    player.play()
    player.set_fullscreen(True)
    
    # Configurer un rappel pour redémarrer la vidéo 1 lorsqu'elle se termine
    player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, on_media_end_video1)

def stream_2():
    """Joue la vidéo 2 dans VLC et configure un rappel pour revenir à la vidéo 1."""
    with play_lock:  # Acquérir le verrou pour s'assurer qu'aucune autre vidéo n'est jouée
        global player
        stop_flag.clear()
        
        media = vlc.Media(video_name_2)
        player.set_media(media)
        win_id = fenetre.winfo_id()
        player.set_xwindow(win_id)  # Utiliser set_xwindow pour Unix-like systèmes
        player.play()
        player.set_fullscreen(True)
        
        # Configurer un rappel pour revenir à la vidéo 1 lorsque la vidéo 2 est terminée
        player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, on_media_end_video2)

def stream_3():
    """Joue la vidéo 3 dans VLC et configure un rappel pour revenir à la vidéo 1."""
    with play_lock:  # Acquérir le verrou
        global player
        stop_flag.clear()
        
        media = vlc.Media(video_name_3)
        player.set_media(media)
        win_id = fenetre.winfo_id()
        player.set_xwindow(win_id)  # Utiliser set_xwindow pour Unix-like systèmes
        player.play()
        player.set_fullscreen(True)
        
        player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, on_media_end_video3)

def stream_4():
    """Joue la vidéo 4 dans VLC et configure un rappel pour revenir à la vidéo 1."""
    with play_lock:  # Acquérir le verrou
        global player
        stop_flag.clear()
        
        media = vlc.Media(video_name_4)
        player.set_media(media)
        win_id = fenetre.winfo_id()
        player.set_xwindow(win_id)  # Utiliser set_xwindow pour Unix-like systèmes
        player.play()
        player.set_fullscreen(True)
        
        player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, on_media_end_video4)

def on_media_end_video1(event):
    """Fonction appelée lorsque la vidéo 1 se termine."""
    global current_video
    if not stop_flag.is_set():  # Si le flag d'arrêt n'est pas activé
        player.stop()  # Arrêter la vidéo en cours
        player.play()  # Redémarrer la vidéo 1
    current_video = "video1"

def on_media_end_video2(event):
    """Fonction appelée lorsque la vidéo 2 se termine."""
    global current_video
    if not stop_flag.is_set():  # Si le flag d'arrêt n'est pas activé
        player.stop()
        stream()  # Revenir à la vidéo 1 sans utiliser de thread
    current_video = "video1"

def on_media_end_video3(event):
    """Fonction appelée lorsque la vidéo 3 se termine."""
    global current_video
    if not stop_flag.is_set():  # Si le flag d'arrêt n'est pas activé
        player.stop()
        stream()  # Revenir à la vidéo 1 sans utiliser de thread
    current_video = "video1"

def on_media_end_video4(event):
    """Fonction appelée lorsque la vidéo 4 se termine."""
    global current_video
    if not stop_flag.is_set():  # Si le flag d'arrêt n'est pas activé
        player.stop()
        stream()  # Revenir à la vidéo 1 sans utiliser de thread
    current_video = "video1"

# Chemin vers les vidéos
video_name = "/home/micromachine/Desktop/folder/video1.mp4"
video_name_2 = "/home/micromachine/Desktop/folder/video2.mp4"
video_name_3 = "/home/micromachine/Desktop/folder/video3.mp4"
video_name_4 = "/home/micromachine/Desktop/folder/video4.mp4"

# Lancer le thread pour lire la vidéo 1 en boucle
threading.Thread(target=stream).start()

# Lancer la boucle principale Tkinter
fenetre.mainloop()

# Libérer les ressources VLC à la fin
player.release()