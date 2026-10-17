# 🤖 JARVIS AI — Complete Voice \& Gesture Control System

> \\\\\\\\\\\\\\\*\\\\\\\\\\\\\\\*Just A Rather Very Intelligent System\\\\\\\\\\\\\\\*\\\\\\\\\\\\\\\* — Built entirely in Python.  
> No API key. No cloud dependency. No limits.

\---

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run Jarvis
python jarvis\\\\\\\\\\\\\\\_ai.py

# 3. Test without microphone/camera
python jarvis\\\\\\\\\\\\\\\_ai.py --demo
```

\---

## 🌟 Feature Overview

|Feature|Details|
|-|-|
|🌍 **Languages**|55+ world languages (English, Tamil, Hindi, Mulayam, Arabic, Japanese, etc.)|
|💻 **Coding Skills**|50+ languages: Python, Java, HTML, CSS, JS, CMD, React, SQL, NodeJS, Kali Linux, Nmap, etc.|
|🎙️ **Voice Listening**|Google STT (free tier) — speaks any language|
|🔊 **Voice Replay**|pyttsx3 (fully offline, zero API key)|
|✋ **Air Mouse**|MediaPipe hand tracking — full gesture mouse control|
|👏 **Clap Detection**|Double clap → opens your chosen app instantly|
|🖥️ **System Control**|Shutdown, restart, lock, sleep via voice|
|📁 **File/Folder Ops**|Create, move, copy, cut, paste, delete, list|
|🌤️ **Weather**|Real-time via wttr.in (no API key!)|
|📊 **System Stats**|CPU, RAM, Disk, Battery, Network, Processes|
|⚙️ **CMD Control**|Execute any shell command by voice|
|🔌 **USB Control**|Detect and list USB/removable devices|
|🔍 **Search**|Google, YouTube, DuckDuckGo, Maps, News|

\---

## ✋ Air Mouse Gestures

Show your hand to the webcam and use these gestures:

|Gesture|Action|
|-|-|
|☝️ **Index finger up**|Move mouse cursor|
|🤏 **Pinch (thumb + index)**|Left click|
|✌️ **Index + Middle fingers**|Scroll mode (move up/down)|
|✊ **Fist (closed hand)**|Hold \& drag|
|🖐️ **Open palm (5 fingers)**|Release / stop drag|
|🤚 **Two hands spread**|Zoom In (Ctrl++)|
|🤲 **Two hands together**|Zoom Out (Ctrl−)|
|➡️ **Swipe right**|Navigate forward (Alt+Right)|
|⬅️ **Swipe left**|Navigate back (Alt+Left)|
|👆 **Peace sign**|Right click|

\---

## 👏 Double Clap

Clap **twice within 1.5 seconds** to instantly open your configured app.  
Set your preferred app at startup when prompted.

\---

## 🗣️ Voice Commands

### System

```
"What time is it?"              → Shows current time and date
"Weather in Chennai"            → Real-time weather (no API key)
"System status"                 → CPU, RAM, Disk, Battery info
"Show drives"                   → List all disk drives
"Show USB devices"              → List connected USB devices
"Take a screenshot"             → Saves screenshot to home folder
"Shutdown computer"             → Powers off in 5 seconds
"Restart computer"              → Reboots system
"Lock screen"                   → Locks workstation
"Sleep computer"                → Suspends system
"Volume up / Volume down"       → Controls system volume
"Mute"                          → Mutes audio
```

### Applications

```
"Open Chrome"                   → Launches Google Chrome
"Open VS Code"                  → Launches VS Code editor
"Open terminal"                 → Launches terminal / CMD
"Open Spotify"                  → Launches Spotify
"Open YouTube"                  → Opens YouTube in browser
"Close Firefox"                 → Kills Firefox process
"Launch calculator"             → Opens calculator app
```

### Files \& Folders

```
"Create file notes.txt"         → Creates a new text file
"Create folder Projects"        → Creates a new directory
"List files"                    → Shows current directory contents
"List files in Documents"       → Shows specific folder
"Search file \\\\\\\\\\\\\\\*.py"              → Finds files by pattern
"Copy src.txt to dst.txt"       → Copies a file
"Move file.txt to /home/user"   → Moves a file
"Delete old\\\\\\\\\\\\\\\_file.txt"           → Deletes a file
```

### Search \& Web

```
"Search Python tutorials"        → Google search
"YouTube React tutorial"         → YouTube search
"Google best restaurants near me"→ Opens Google search
"Search on GitHub Flask API"     → GitHub search
```

### Coding Help

```
"Explain Python"                 → Full Python info
"Show me Java hello world"       → Prints hello world code
"What is React"                  → React.js explanation
"Nmap snippet port scan"         → Nmap port scan command
"Python loop snippet"            → Code snippet example
"How to use Docker"              → Docker info + commands
"List coding languages"          → Shows all 50+ languages
```

### Shell / CMD

```
"Run command ls -la"             → Executes ls -la
"Execute ipconfig"               → Runs ipconfig (Windows)
"Terminal ping google.com"       → Runs ping command
```

### Language Switching

```
"Switch to Tamil"                → Switches to Tamil (ta-IN)
"Switch to Hindi"                → Switches to Hindi (hi-IN)
"Speak Japanese"                 → Switches to Japanese
"Switch to Spanish"              → Cambia al español
```

### Fun

```
"Tell me a joke"                 → Jarvis tells a programmer joke
"Who are you?"                   → Jarvis introduces himself
"What can you do?"               → Lists all skills
"Go to sleep"                    → Jarvis sleeps until woken
"Jarvis wake up"                 → Wake word (while sleeping)
```

\---

## 🌍 Supported Languages (55)

|#|Language|Code|
|-|-|-|
|1|English|en-IN|
|2|Tamil|ta-IN|
|3|Hindi|hi-IN|
|4|Mulayam (Hindi variant)|hi-IN|
|5|Telugu|te-IN|
|6|Kannada|kn-IN|
|7|Malayalam|ml-IN|
|8|Marathi|mr-IN|
|9|Gujarati|gu-IN|
|10|Punjabi|pa-IN|
|11|Bengali|bn-IN|
|12|Urdu|ur-PK|
|13|Nepali|ne-NP|
|14|Sinhala|si-LK|
|15|Spanish|es-ES|
|16|French|fr-FR|
|17|German|de-DE|
|18|Italian|it-IT|
|19|Portuguese|pt-PT|
|20|Russian|ru-RU|
|21|Japanese|ja-JP|
|22|Chinese|zh-CN|
|23|Korean|ko-KR|
|24|Arabic|ar-SA|
|25|Persian|fa-IR|
|26|Hebrew|he-IL|
|27|Turkish|tr-TR|
|28|Thai|th-TH|
|29|Vietnamese|vi-VN|
|30|Indonesian|id-ID|
|...|+ 25 more|(see `LANGUAGES` dict)|

\---

## 💻 Supported Coding Languages (50+)

```
Python      Java        HTML        CSS         JavaScript
TypeScript  React       Vue         Angular     Node.js
SQL         MongoDB     Redis       GraphQL     PHP
Ruby        Go          Rust        Kotlin      Swift
C           C++         C#          Scala       R
Dart        Lua         Perl        Haskell     MATLAB
Bash        PowerShell  Assembly    Ansible     Terraform
Docker      Kubernetes  Flutter     TensorFlow  Pandas
Git         Nmap        Kali Linux  CMD         Full Stack
...and more
```

\---

## 📦 Installation

### Requirements

* Python 3.8+
* Microphone (for voice input)
* Webcam (for gesture control)
* Internet (for Google STT and weather — TTS is fully offline)

### Step-by-step

```bash
# Clone or download this project
git clone <repo-url>
cd jarvis

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\\\\\\\\\\\\\\\\Scripts\\\\\\\\\\\\\\\\activate          # Windows

# Install all dependencies
pip install -r requirements.txt

# On Linux, you may also need:
sudo apt install portaudio19-dev python3-pyaudio espeak
pip install pyaudio

# On Windows, you may also need:
pip install pywin32

# Run
python jarvis\\\\\\\\\\\\\\\_ai.py
```

\---

## 🏗️ Architecture

```
jarvis\\\\\\\\\\\\\\\_ai.py
├── LANGUAGES dict          — 55+ language configs
├── CODING\\\\\\\\\\\\\\\_KNOWLEDGE dict   — 50+ language knowledge base
├── JARVIS\\\\\\\\\\\\\\\_SKILLS dict      — Master skills directory
│
├── VoiceEngine             — STT (Google) + TTS (pyttsx3 offline)
├── SystemController        — OS control, files, drives, USB, web
├── GestureController       — MediaPipe hand tracking + pyautogui
├── ClapDetector            — sounddevice amplitude monitoring
├── CodeGenerator           — Code snippets + language explanations
├── JarvisBrain             — Command parser \\\\\\\\\\\\\\\& skill dispatcher
└── Jarvis                  — Main orchestrator
```

\---

## ⚠️ Platform Notes

|Feature|Windows|Linux|macOS|
|-|-|-|-|
|Voice TTS|✅ SAPI5|✅ eSpeak|✅ NSS|
|Voice STT|✅|✅|✅|
|Gesture|✅|✅|✅|
|Shutdown/Restart|✅|✅|✅|
|Lock Screen|✅|✅|✅|
|Volume Control|✅ (nircmd)|✅ (pactl)|✅|
|USB Detection|✅|✅|✅|

\---

## 🚀 Extending Jarvis

Add commands in `JarvisBrain.process()`:

```python
if "my command" in cmd:
    # your code here
    self.voice.speak("Done!")
    return True
```

Add a new language in `LANGUAGES` dict:

```python
"yoruba": {"code": "yo-NG", "tts": "yo", "flag": "🇳🇬", "greeting": "Ẹ káàárọ̀"},
```

Add a new coding language in `CODING\\\\\\\\\\\\\\\_KNOWLEDGE` dict.

\---

## 📜 License

MIT License — Free to use, modify and distribute.

\---

*Built with ❤️ in Python | No API keys | No cloud lock-in | You own it.*

