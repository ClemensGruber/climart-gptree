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

def clear_input_buffer():
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        # Read and discard the input
        _ = sys.stdin.readline()
        
def clear():
    # clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')

def add_line_breaks(text, cols):
    """ 
    Trennt längere Texte in mehrere Zeilen auf, damit sie in die Sprechblase passen.
    """
    
    if len(text) > cols:
        words = text.split()  # Trennt den Text in Wörter auf
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= cols:
                current_line += word + " "
            else:
                lines.append(current_line.strip())  # Fügt die aktuelle Zeile zu den Zeilen hinzu
                current_line = word + " "
        
        lines.append(current_line.strip())  # Fügt die letzte Zeile hinzu
        
        return lines
    else:
        return [text]
    
def chat_bubble(text,who=None):
    cols = 55 # Breite der Chatbubble
    text = add_line_breaks(text, cols)
    
    bubble = "\n"
    bubble += "\033[97m"
    
    if who:
        bubble += "╭" + "─" * (len(who)+2) + "╮\n"
        bubble += "│ " + who + " " + "╰" + "─" * (cols - (len(who))-2) + "╮\n"
        bubble += "│" + " " * (cols+1) + "│\n"
    else:
        bubble += "╭" + "─" * (cols+1) + "╮\n"

    for line in text:
        add_spaces = cols - len(line) 
        bubble += "│ " + line + " " * add_spaces + "│\n"
    bubble += "╰" + "─" * (cols+1) + "╯"
    bubble +="\033[0m"
    bubble += "\n"
    print(bubble)


def chat_bubble_user(text):
    cols = 30 # Breite der Chatbubble
    indent = 30
    text = add_line_breaks(text, cols)
    
    bubble = "\n"
    bubble += "\033[93m"
    bubble += " "* indent + " "* (cols-4) + "╭" + "─" * 4 + "╮\n"
    bubble += " "* indent + "╭" + "─" * (cols-5) + "╯ Du " + "│\n"
    bubble += " "* indent + "│" + " " * cols + "│\n"

    for line in text:
        add_spaces = cols - len(line) - 1
        bubble += " "* indent + "│ " + line + " " * add_spaces + "│\n"
    bubble += " "* indent + "╰" + "─" * cols + "╯"
    bubble +="\033[0m"
    bubble += "\n"
    print(bubble)


def welcome():
    text = "     .---.\n"
    text+= "    } n n {       _     _             _\n"
    text+= "     \_-_/       | |   (_)           | |           _ \n"
    text+= ".'c .'|_|'. n`.  | |  _ _ _____ _____| |__   ___ _| |_ \n"
    text+= "'--'  /_\  `--'  | |_/ ) | ___ (___  )  _ \ / _ (_   _)\n"
    text+= "     /| |\       |  _ (| | ____|/ __/| |_) ) |_| || |_ \n"
    text+= "    [_] [_]      |_| \_)_|_____|_____)____/ \___/  \__)\n"
    return text


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
        audio_lib = "mpg123"
        params = " -q"  
    elif current_os == 'Darwin':
        audio_lib = "afplay"
        params = ""
    else:
        print("Unsupported operating system.")
        return
    
    if blocking:
        os.system(audio_lib + params + " " + filename)
    else:
        subprocess.Popen(f"{audio_lib}{params} {filename}", shell=True)


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__}: {round((end - start),2)} Sekunden.")
        return result
    return wrapper