import subprocess
import xbmcgui
import urllib.request

# Funktion zum Abrufen der SSIDs mithilfe von nmcli
def get_wifi_ssids():
    try:
        # Führe den nmcli-Befehl aus, um die WLAN-Netzwerke abzurufen
        output = subprocess.check_output(['nmcli', '-t', '-f', 'SSID,SIGNAL,SECURITY', 'device', 'wifi', 'list'], universal_newlines=True)
        
        # Teile die Ausgabe in Zeilen auf und erstelle eine Liste der SSIDs (aus Spalte 1)
        ssids = output.strip().split('\n')
        
        # Entferne eventuell führende oder abschließende Leerzeichen
        ssids = [ssid.strip() for ssid in ssids]
        
        return ssids
    except subprocess.CalledProcessError as e:
        return []
    except Exception as e:
        return []
        
# Öffne ein Begrüßungsfenster
dialog=xbmcgui.Dialog()
dialog.ok("Wi-Fi", "Choose a network and enter the password!")

# SSIDs abrufen
ssids = get_wifi_ssids()

# Erstelle ein Fenster
window = xbmcgui.Window(10000)

# Erstelle eine Listeansicht für die SSIDs
list_items = [ssid for ssid in ssids]

# Zeige die Liste der SSIDs in einem eigenen Fenster an
list_dialog = xbmcgui.Dialog()
selected_index = list_dialog.select('SSID:SIGNAL:SECURITY', list_items)

# Überprüfe die Benutzerauswahl
if selected_index >= 0:
   selected_ssid = ssids[selected_index]

# Fordere den Benutzer zur Eingabe des Passworts auf
try:
    password = list_dialog.input('Password for ' + selected_ssid, '')
except NameError:
    exit()

# Eingabe des Passworts behandeln
if password:
    list_dialog.notification('Info', 'SSID: {} Passwort: {}'.format(selected_ssid, password))
    command = ["nmcli", "device", "wifi", "connect", selected_ssid, "password", password]
else:
    list_dialog.notification('Info', 'Empty Password')
    command = ["nmcli", "device", "wifi", "connect", selected_ssid]

# Befehl ausführen
subprocess.run(command)

def check_internet_connection():
    try:
        urllib.request.urlopen("http://www.google.com", timeout=2)
        return True
    except urllib.error.URLError:
        return False

if check_internet_connection():
    list_dialog.notification('Info', 'Connection established')
else:
    list_dialog.notification('Info', 'Connection failed')
