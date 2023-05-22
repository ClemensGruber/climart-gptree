import json, os,sys, time, platform, subprocess

def load_json(filename):
    file_path = os.path.join(sys.path[0], filename)
    if os.path.exists(file_path):
        with open(file_path) as json_file:
            json_data = json.load(json_file)
        return json_data
    else:
        print("File not found: " + filename + "")
        return None


def save_json(filename, data):
    with open(os.path[0] + '/' + filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def clear():
    # clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')

def display(text: str, x: int = None, y: int = None, color: str = None) -> None:
    """
    Schreibt den angegebenen Text in der angegebenen Farbe und Position im Terminal.

    :param text: Der Text, der im Terminal angezeigt werden soll.
    :param x: Die horizontale Position, an der der Text im Terminal angezeigt werden soll (optional).
    :param y: Die vertikale Position, an der der Text im Terminal angezeigt werden soll (optional).
    :param color: Die Farbe, in der der Text im Terminal angezeigt werden soll (optional).
    :return: None
    """

    # ANSI Farbcodes für verschiedene Farben
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }

    # Setzt den Cursor an die angegebene Position
    
    if x != None and y != None:
        position = f"\033[{y};{x}H"
        print(x,y)
    else:
        position = ""

    if color:
        color_code = colors[color]
    else:
        color_code = ""

    # Schreibt den Text an die Position mit der angegebenen Farbe
    print(f"{position}{color_code}{text}{colors['reset']}")


def play_sound(filename, blocking=True):
    """
    Spielt eine Sounddatei unter Verwendung des entsprechenden Audioplayers ab,
    abhängig vom Betriebssystem.
    
    Argumente:
    - filename: Der Dateiname der Sounddatei.
    - blocking (optional): Gibt an, ob die Wiedergabe blockierend ist oder nicht.
                           Standardmäßig ist es True, was bedeutet, dass die Funktion
                           erst zurückkehrt, wenn die Wiedergabe abgeschlossen ist.
                           Wenn es auf False gesetzt wird, wird die Wiedergabe im Hintergrund
                           gestartet und die Funktion kehrt sofort zurück.
    """
    current_os = platform.system()
    
    if current_os == 'Linux':
        audio_lib = "aplay"  
    elif current_os == 'Darwin':
        audio_lib = "afplay"
    else:
        print("Unsupported operating system.")
        return
    
    if blocking:
        os.system(audio_lib + " " + filename)
    else:
        subprocess.Popen([audio_lib, filename])


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} dauerte {end - start} Sekunden.")
        return result
    return wrapper