# GPTree, der sprechende Baum
## Data Flow und Services

Wir verwenden ein Python-Skript, um Sprach-Aufnahmen eines users an die APIs verschiedener KI-Services zu senden:
- [Whisper](https://openai.com/research/whisper), um Sprache in Text umzuwandeln (speech-to-text)
- [ChatGPT 3.5](https://platform.openai.com/docs/models/gpt-3-5) als LLM, das die Antworten generiert
- [Google Cloud text-to-speech service](https://cloud.google.com/text-to-speech), um die Antwort wieder als Sprache auszugeben

![Data Flow and Services](./img/workflow-gptree.png)


## Installation 
### Raspberry Pi OS installieren

Zuerst kopieren wir das Betriebssystem des RasPis auf eine SD-Karte, dazu: 
- **Raspberry Pi Imager** von https://www.raspberrypi.com/software/ downloaden und auf PC / Mac installieren
- SD-Kate in PC / Mac einstecken (wir verwenden eine mit 32 GB) und Imager starten. 


#### Einstellungen beim Pi Imager 

- **RasPi-Modell**  
  RasPi 4 oder RasPi 5 je nach Modell 
- **Betriebssystem**  
  -&nbsp;Raspberry Pi OS <br>
  -&nbsp;64 bit

Mit `Strg + Umsch + X` Konfiguration aufzurufen

**Allgemein**
- **hostname**  
  `gptree-[treeName]` (.local) <br>
  (z.B. `gptree-ahorn`)
  
- **Benutzername und Passwort**  
  Benutzer: `[set-your-username]` <br>
  Passwort: `[set-your-password]`

- **Wifi einrichten**  
  SSID:       `[specify-your-local-ssid]` <br>
  Passwort:   `[specify-password-for-ssid]` <br>
  Wifi-Land:  `DE`

- **Spracheinstellungen**  
  Zeitzone:        `Europa/Berlin` <br>
  Tastaturlayout:  `DE`

**Dienste**
- **SSH aktivieren**  
  Passwort zur Authentifizierung
  
Nun Betriebssystem auf SD-Karte schreiben. 

Wenn fertig, SD-Karte mit Raspberry Pi OS in RasPi einsetzen. 


### RasPi initial starten und SSH oder Terminal starten

- RasPi mit **Strom** versorgen. 
- Über den WLAN-Router die **IP des RasPis** herausfinden, oder RasPi kurz an Monitor / Tastatur anschließen und von dort die IP notieren.
- Sich per **SSH-Client** (z.B. PuTTY, https://www.putty.org/) mit gerade herausgefundener IP und (via Pi Imager gesetztem, siehe oben) **Benutzername und Passwort anmelden**. 


### ggf. weiteres WLAN einrichten

Weitere WLAN-Netze &ndash; zusätzlich zu dem per Pi Imager eingerichteten &ndash; konfigurieren: 

`sudo nmcli connection add type wifi ssid "YOUR-SSID" wifi-sec.key-mgmt wpa-psk wifi-sec.psk "YOUR-PASSWORD" connection.id "YOUR-ID"`

- `YOUR-ID` ist Teil des Dateinamens unter der die Konfiguration gespeichert wird

Hinweis: Die neu generierte connection und die des ggf. über den RaspberryPi Imager eingerichteten WLANs findet man im Verzeichnis <br>
`/etc/NetworkManager/system-connections/`


### ggf. VNC einrichten 
#### a) VNC auf RasPi aktivieren 

`sudo raspi-config`

- 3 Interface Options
- I2 VNC
- yes / enable

Ggf. `sudo reboot` wenn man gleich VNC nutzen möchte. 


#### b) VNC client auf Windows-Rechner installieren

Siehe https://www.realvnc.com/en/connect/download/viewer/windows/


### System updaten 

```
sudo apt update
sudo apt full-upgrade
```

ggf. `sudo reboot` 


### Verzeichnis erstellen und aktuellen code von GitHub holen

Ins eigene Heimatverzeichnis wechslen (meist ist man schon da :)

`cd`

Verzeicnis `gptree` erstellen und dort hin wechseln 

```
mkdir gptree
cd gptree
```

Git initialisieren und code von GitHub holen 

```
git init
git pull https://github.com/ClemensGruber/climart_gptree raspi
```

[für spätere updates dies hier verwenden]
Achtung! lokale Änderungen gehen damit verloren!!

```
git reset --hard HEAD
git pull https://github.com/ClemensGruber/climart_gptree raspi
```

### OpenAI-API-Key hinterlegen

**OpenAI Account** anlegen &ndash; falls noch nicht passiert! 
- http://platform.openai.com/signup 

**API-Key** von OpenAI erzeugen 
- über https://platform.openai.com/api-keys API-Key erzeugen 
- API-Key speichern / merken / in Zwischenablage kopieren

Nun geht es wieder **auf dem RasPi** weiter: 
Im Verzeichnis `gptree` die Datei `.env` anlegen und eigenen OpenAI-API-Key hinterlegen: 

```
cd ~/gptree
nano .env
```

Nano ist ein Editor unter Linux, in die leere `.env`-Datei diese Zeile einfügen:<br>
`OPENAI_API_KEY="your-key"`

und `your-key` mit den gerade erzeugten **OpenAI-Key** ersetzen. 

Wer mit nano noch nicht gearbeitet hat findet die wichtigsten Tastenkombinationen unter https://www.nano-editor.org/dist/latest/cheatsheet.html


### Benötigte Bibliotheken installieren

Folgende Bibliotheken brauchen wir für **PyAudio**

`sudo apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev`


### Virtuelle Python-Umgebung 'venv-gptree' erzeugen 

Falls man noch nicht im gptree-Verzeichnis ist dort hin wechsen und `venv-gptree` erzeugen

```
cd ~/gptree
python -m venv venv-gptree
```


### Requirements intallieren

Nun in der virtuellen Umgebung die notwendigen Bibliotheken installieren:

`venv-gptree/bin/pip3 install -r requirements.txt`


### Google Cloud Plattform (GCP) Account

Wir nutzen den Google Cloud Service zur Sprachausgabe (TTS, text-to-speech) für GPTree.

Dazu muss ein Google Cloud Account angelegt werden &ndash; falls noch nicht vorhanden.
- https://cloud.google.com 

Ein **Projekt erstellen**
- gehe zu https://console.cloud.google.com/cloud-resource-manager
- nun ein neues Projekt erstellen, z.B. "gptree" 

**API text-to-speech aktivieren**
- zum API-Bibliothek gehen  
  https://console.cloud.google.com/apis/library 
- gerade erstelltes Projekt wählen, oben in der drop-down-Auswahl
- **Text-to-Speech** im zentralen Suchformular (Nach APIs und Diensten suchen) eintippen 
- **Cloud Text-to-Speech API** auswählen  
  Bitte aufpassen: Cloud Text-to-Speech API" hier wählen, und **NICHT** Speech-to-Text! 
- **Aktivieren** anklicken


### gcloud-CLI auf RasPi einrichten 

-> Detailierte Dokumentation auch unter: https://cloud.google.com/sdk/docs/install?hl=de#linux


#### gcloud-CLI installieren

GCloud CLI for **Linux 64-Bit (Arm)** herunterladen und entpacken
- die aktuellste Version findet man auf  
  https://cloud.google.com/sdk/docs/install?hl=de#linux
- wir brauchen die Version für  
  -&nbsp;Linux 64-Bit <br>
  -&nbsp;Arm (**NICHT** x86) 
- als letztes haben wir verwendet / getestet:  
  `google-cloud-cli-linux-arm.tar.gz` / https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-arm.tar.gz

Das ganze muss im **root-Verzeichnis** installiert werden, also wechslen wir dort hin 

`cd /`

Gerne nochmal testen, ob man tatsächlich in root und nicht in home ist! :-) 

**Archiv herunterladen ...**

`sudo curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-arm.tar.gz`

... und **entpacken**

`sudo tar -xf google-cloud-cli-linux-arm.tar.gz`

Nun das **Installations-Skript ausführen** mit

`sudo ./google-cloud-sdk/install.sh`

dabei
- "Do you want to help improve the Google Cloud CLI"  
  -> N(o)
- "Modify profile to update your $PATH and enable shell command completion?
  Do you want to continue (Y/n)?"  
  -> Y(es)
- "Enter a path to an rc file to update, or leave blank to use ..."  
  -> ändern in <br>
     `/home/[your-linux-username]/.bashrc` <br>
     dabei `[your-linux-username]` mit dem auf dem RasPi verwendeten Benutzernamen ersetzen      
     
Falls man **später im Betrieb updaten** will geht das mit 

`sudo /google-cloud-sdk/bin/gcloud components update`

**Neue shell starten**, damit die Änderungen oben wirksam werden! 


#### gcloud-CLI konfigurieren

gcloud-CLI initial konfigurieren und Projekt auswählen

`gcloud init`

dabei 
- den Anweisoungen folgen 
- "gptree" bzw. das vorher angelegte Projekt auswählen. 

Google Cloud-Dienste lokal authentifizieren

`gcloud auth application-default login`

... dabei den Anweisoungen folgen 

Wenn alles geklappt hat sollte dieser Befehl einen access token ausspucken:

`gcloud auth application-default print-access-token`


#### Dienstkonto aka "service account" erstellen 

-> Doku auch unter https://cloud.google.com/iam/docs/service-accounts-create?hl=de

> It is important to understand, that some APIs of Google Cloud cannot be used with the end user credentials aka. not with your login credentials. The text-to-speech API is one of them which is why you have to create a service account! 

Das kann man *alternativ* über die Google Cloud-Website machen: https://console.cloud.google.com/iam-admin/serviceaccounts/ 
oder &ndash; wie wir hier &ndash; über die Konsole auf dem RasPi: 

Alle Projekte in unserem Google-Accoutn anzeigen

`gcloud projects list`

**gptree** als core-Projekt setzen, wenn vorher ein anderes Projekt eingerichtet wurde, `gptree` durch den anderen Namen ersetzen

`gcloud config set project gptree`

Wenn man wissen möchte, welche / ob schon service account existieren

`gcloud iam service-accounts list`


##### service account erzeugen

`gcloud iam service-accounts create [set-service-account-name] --display-name="[set-display-name]"

um z.B. einen service account mit dem 
- Namen **gptree-service** und dem 
- beschreibenden Namen ebenfalls **gptree-service** 

zu erzeugen verwendet man

`gcloud iam service-accounts create gptree-service --display-name="gptree-service"


##### key für service account erzeugen

`gcloud iam service-accounts keys create key.json --iam-account [your-service-account-name]@[your-gcloud-project].iam.gserviceaccount.com`

um z.B. für einen service account mit dem 
- Namen **gptree-service** und dem 
- gcloud-Projekt **gptree** 

ein key zu erzeugen verwendet man

`gcloud iam service-accounts keys create key.json --iam-account gptree-service@gptree.iam.gserviceaccount.com`


##### Dienstkonto eine IAM-Rolle zuzuweisen (policy run)

`gcloud projects add-iam-policy-binding [your-gcloud-project] --member=serviceAccount:[your-service-account-name]@[your-gcloud-project].iam.gserviceaccount.com --role=roles/owner`

um z.B. für einen service account mit dem 
- Namen **gptree-service** und dem 
- gcloud-Projekt **gptree** 

eine policy zuzuweisen verwendet man 

`gcloud projects add-iam-policy-binding gptree --member=serviceAccount:gptree-service@gptree.iam.gserviceaccount.com --role=roles/owner`


##### service account aktivieren

`gcloud auth activate-service-account [your-service-account-name]@[your-gcloud-project].iam.gserviceaccount.com --key-file=key.json`

z.B.
`gcloud auth activate-service-account gptree-service@gptree.iam.gserviceaccount.com --key-file=key.json`

Nun sollte der frisch erstellte service account als ACTIVE ACCOUNT angezeit werden (Sternchen vor dem Namen):

`gcloud auth list`

Testen, ob file erzeugt wird 
(geht ggf. nicht direkt danach, dann etwas waren)  

```
curl -X POST \
-H "Authorization: Bearer "$(gcloud auth print-access-token) \
-H "Content-Type: application/json; charset=utf-8" \
-d '{"audioConfig": {"audioEncoding":"LINEAR16","effectsProfileId": ["small-bluetooth-speaker-class-device"], "pitch": 10.8, "speakingRate": 1.3}, "input": {"text": "Hello little Google API. How is it today?"}, "voice": {"languageCode": "de-DE", "name": "de-DE-Wavenet-F"}}' \
"https://texttospeech.googleapis.com/v1/text:synthesize" -o test-gcloud-tts.wav
```

Damit wird eine Datei `test-gcloud-tts.wav` im selben verzeichnis erstellt. 

[todo audio-output testen]


### Vorproduziertes Audio generieren

Zur Begrüßung und zwischen der Unterhaltung verwendet GPTree vorproduzierte MP3-Dateien, diese müssen vorproduziert werden mit: 

```
cd ~/gptree/
venv-gptree/bin/python3 utils/audiofile-generator.py
```

### GPTree starten

Nun können wir GPTree starten mit:

```
cd ~/gptree
venv-gptree/bin/python main.py
```

oder 

`bash start.sh`


## Credits

Danke an das CityLab Berlin! 
- Projekt [Kiezbot](https://citylab-berlin.org/de/exhibition/kiezbot/)
- Initialer code: https://github.com/technologiestiftung/kiezbot

<table>
    <td>
      Im Rahmen des ClimArt-Projekts von
      <br/>
    </td>
    <td>
      Initialer code vom 
      <br/>
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://www.zku-berlin.org/de/">
        <img width="50" src="./img/zku-logo.png" />
      </a>
    </td>
    <td>
      <a href="https://citylab-berlin.org/de/start/">
        <img width="200" src="https://citylab-berlin.org/wp-content/uploads/2021/05/citylab-logo.svg" />
      </a>
    </td>
  </tr>
</table>

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-0-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
