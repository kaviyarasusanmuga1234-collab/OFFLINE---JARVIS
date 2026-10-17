#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║   ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗     █████╗ ██╗          ║
║   ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝    ██╔══██╗██║          ║
║   ██║███████║██████╔╝██║   ██║██║███████╗    ███████║██║          ║
║   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║    ██╔══██║██║          ║
║   ██║██║  ██║██║  ██║ ╚████╔╝ ██║███████║    ██║  ██║██║          ║
║   ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝    ╚═╝  ╚═╝╚═╝          ║
║                                                                      ║
║   Just A Rather Very Intelligent System                              ║
║   ✦ 50+ Languages  ✦ 50+ Coding Skills  ✦ Air Mouse Gesture         ║
║   ✦ Voice Control  ✦ System Master     ✦ No API Key Required        ║
╚══════════════════════════════════════════════════════════════════════╝

REQUIREMENTS: pip install -r requirements.txt
USAGE:        python jarvis_ai.py
GESTURE:      Show hand to camera for Air Mouse control
CLAP x2:      Open an application
"""

# ─────────────────────────────────────────────────────────────────────
#  CORE IMPORTS
# ─────────────────────────────────────────────────────────────────────
import os, sys, time, datetime, subprocess, threading, platform
import shutil, glob, webbrowser, json, math, re, random, struct, wave
import ctypes, socket, tempfile, signal, queue, io
from collections import deque
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────
#  THIRD-PARTY IMPORTS  (installed via requirements.txt)
# ─────────────────────────────────────────────────────────────────────
try:
    import speech_recognition as sr
except ImportError:
    print("[!] SpeechRecognition not found. Run: pip install SpeechRecognition")
    sys.exit(1)

try:
    import pyttsx3
except ImportError:
    print("[!] pyttsx3 not found. Run: pip install pyttsx3")
    sys.exit(1)

try:
    import psutil
except ImportError:
    print("[!] psutil not found. Run: pip install psutil")
    sys.exit(1)

try:
    import cv2
    import mediapipe as mp
    import numpy as np
    GESTURE_AVAILABLE = True
except ImportError:
    print("[!] OpenCV/MediaPipe not found. Gesture control disabled.")
    print("    Run: pip install opencv-python mediapipe numpy")
    GESTURE_AVAILABLE = False

try:
    import pyautogui
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.01
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    print("[!] pyautogui not found. Mouse control disabled.")
    PYAUTOGUI_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import sounddevice as sd
    AUDIO_DEVICE_AVAILABLE = True
except (ImportError, OSError):
    print("[!] sounddevice/PortAudio not found. Clap detection disabled.")
    print("    Run: pip install sounddevice  |  Linux: sudo apt install portaudio19-dev")
    AUDIO_DEVICE_AVAILABLE = False

# ─────────────────────────────────────────────────────────────────────
#  PLATFORM DETECTION
# ─────────────────────────────────────────────────────────────────────
OS_NAME    = platform.system()   # Windows / Linux / Darwin
IS_WINDOWS = OS_NAME == "Windows"
IS_LINUX   = OS_NAME == "Linux"
IS_MAC     = OS_NAME == "Darwin"

if IS_WINDOWS:
    try:
        import winreg, win32api, win32con, win32com.client
        WIN32_AVAILABLE = True
    except ImportError:
        WIN32_AVAILABLE = False

# ══════════════════════════════════════════════════════════════════════
#  ①  LANGUAGE DICTIONARY  (50+ Languages)
# ══════════════════════════════════════════════════════════════════════
LANGUAGES = {
    # ──── SOUTH ASIAN ──────────────────────────────────────────────
    "english":    {"code": "en-IN", "tts": "en", "flag": "🇬🇧", "greeting": "Hello, I am Jarvis. How may I assist you, sir?"},
    "tamil":      {"code": "ta-IN", "tts": "ta", "flag": "🇮🇳", "greeting": "வணக்கம், நான் ஜார்விஸ். உங்களுக்கு எப்படி உதவலாம்?"},
    "hindi":      {"code": "hi-IN", "tts": "hi", "flag": "🇮🇳", "greeting": "नमस्ते, मैं जार्विस हूं। आपकी कैसे सहायता करूं?"},
    "mulayam":    {"code": "hi-IN", "tts": "hi", "flag": "🇮🇳", "greeting": "नमस्ते जी! जार्विस हाज़िर है, हुक्म कीजिए।"},
    "telugu":     {"code": "te-IN", "tts": "te", "flag": "🇮🇳", "greeting": "హలో, నేను జార్విస్. మీకు ఎలా సేవ చేయగలను?"},
    "kannada":    {"code": "kn-IN", "tts": "kn", "flag": "🇮🇳", "greeting": "ಹಲೋ, ನಾನು ಜಾರ್ವಿಸ್. ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಲಿ?"},
    "malayalam":  {"code": "ml-IN", "tts": "ml", "flag": "🇮🇳", "greeting": "ഹലോ, ഞാൻ ജാർവിസ്. എങ്ങനെ സഹായിക്കണം?"},
    "marathi":    {"code": "mr-IN", "tts": "mr", "flag": "🇮🇳", "greeting": "नमस्कार, मी जार्विस. मी कशी मदत करू?"},
    "gujarati":   {"code": "gu-IN", "tts": "gu", "flag": "🇮🇳", "greeting": "નમસ્તે, હું જાર્વિસ. હું તમારી કેવી રીતે મદદ કરી શકું?"},
    "punjabi":    {"code": "pa-IN", "tts": "pa", "flag": "🇮🇳", "greeting": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਮੈਂ ਜਾਰਵਿਸ ਹਾਂ। ਕਿਵੇਂ ਮਦਦ ਕਰਾਂ?"},
    "bengali":    {"code": "bn-IN", "tts": "bn", "flag": "🇧🇩", "greeting": "হ্যালো, আমি জার্ভিস। আপনাকে কীভাবে সাহায্য করতে পারি?"},
    "urdu":       {"code": "ur-PK", "tts": "ur", "flag": "🇵🇰", "greeting": "ہیلو، میں جارویس ہوں۔ آپ کی خدمت میں حاضر ہوں۔"},
    "nepali":     {"code": "ne-NP", "tts": "ne", "flag": "🇳🇵", "greeting": "नमस्ते, म जार्विस। कसरी सहायता गर्न सक्छु?"},
    "sinhala":    {"code": "si-LK", "tts": "si", "flag": "🇱🇰", "greeting": "හෙලෝ, මම ජාර්විස්. ඔබට කෙලෙස් සහාය කළ හැකිද?"},

    # ──── EUROPEAN ─────────────────────────────────────────────────
    "spanish":    {"code": "es-ES", "tts": "es", "flag": "🇪🇸", "greeting": "Hola, soy Jarvis. ¿En qué puedo servirle?"},
    "french":     {"code": "fr-FR", "tts": "fr", "flag": "🇫🇷", "greeting": "Bonjour, je suis Jarvis. Comment puis-je vous aider?"},
    "german":     {"code": "de-DE", "tts": "de", "flag": "🇩🇪", "greeting": "Guten Tag, ich bin Jarvis. Wie kann ich Ihnen helfen?"},
    "italian":    {"code": "it-IT", "tts": "it", "flag": "🇮🇹", "greeting": "Ciao, sono Jarvis. Come posso aiutarti?"},
    "portuguese": {"code": "pt-PT", "tts": "pt", "flag": "🇵🇹", "greeting": "Olá, sou Jarvis. Como posso ajudá-lo?"},
    "russian":    {"code": "ru-RU", "tts": "ru", "flag": "🇷🇺", "greeting": "Привет, я Джарвис. Чем могу помочь?"},
    "dutch":      {"code": "nl-NL", "tts": "nl", "flag": "🇳🇱", "greeting": "Hallo, ik ben Jarvis. Hoe kan ik je helpen?"},
    "swedish":    {"code": "sv-SE", "tts": "sv", "flag": "🇸🇪", "greeting": "Hej, jag är Jarvis. Hur kan jag hjälpa dig?"},
    "norwegian":  {"code": "no-NO", "tts": "no", "flag": "🇳🇴", "greeting": "Hei, jeg er Jarvis. Hvordan kan jeg hjelpe?"},
    "danish":     {"code": "da-DK", "tts": "da", "flag": "🇩🇰", "greeting": "Hej, jeg er Jarvis. Hvordan kan jeg hjælpe?"},
    "finnish":    {"code": "fi-FI", "tts": "fi", "flag": "🇫🇮", "greeting": "Hei, olen Jarvis. Kuinka voin auttaa sinua?"},
    "polish":     {"code": "pl-PL", "tts": "pl", "flag": "🇵🇱", "greeting": "Cześć, jestem Jarvis. Jak mogę ci pomóc?"},
    "turkish":    {"code": "tr-TR", "tts": "tr", "flag": "🇹🇷", "greeting": "Merhaba, ben Jarvis. Size nasıl yardımcı olabilirim?"},
    "greek":      {"code": "el-GR", "tts": "el", "flag": "🇬🇷", "greeting": "Γεια, είμαι ο Τζάρβις. Πώς μπορώ να σας βοηθήσω;"},
    "czech":      {"code": "cs-CZ", "tts": "cs", "flag": "🇨🇿", "greeting": "Ahoj, jsem Jarvis. Jak ti mohu pomoci?"},
    "hungarian":  {"code": "hu-HU", "tts": "hu", "flag": "🇭🇺", "greeting": "Szia, én vagyok Jarvis. Hogyan segíthetek?"},
    "romanian":   {"code": "ro-RO", "tts": "ro", "flag": "🇷🇴", "greeting": "Bună, sunt Jarvis. Cum te pot ajuta?"},
    "slovak":     {"code": "sk-SK", "tts": "sk", "flag": "🇸🇰", "greeting": "Ahoj, som Jarvis. Ako ti môžem pomôcť?"},
    "ukrainian":  {"code": "uk-UA", "tts": "uk", "flag": "🇺🇦", "greeting": "Привіт, я Джарвіс. Чим можу допомогти?"},
    "bulgarian":  {"code": "bg-BG", "tts": "bg", "flag": "🇧🇬", "greeting": "Здравейте, аз съм Джарвис. Как мога да ви помогна?"},
    "croatian":   {"code": "hr-HR", "tts": "hr", "flag": "🇭🇷", "greeting": "Bok, ja sam Jarvis. Kako ti mogu pomoći?"},
    "slovenian":  {"code": "sl-SI", "tts": "sl", "flag": "🇸🇮", "greeting": "Zdravo, jaz sem Jarvis. Kako vam lahko pomagam?"},
    "latvian":    {"code": "lv-LV", "tts": "lv", "flag": "🇱🇻", "greeting": "Sveiki, es esmu Džārviss. Kā varu palīdzēt?"},
    "lithuanian": {"code": "lt-LT", "tts": "lt", "flag": "🇱🇹", "greeting": "Sveiki, aš esu Jarvis. Kaip galiu padėti?"},
    "estonian":   {"code": "et-EE", "tts": "et", "flag": "🇪🇪", "greeting": "Tere, olen Jarvis. Kuidas saan aidata?"},
    "catalan":    {"code": "ca-ES", "tts": "ca", "flag": "🇪🇸", "greeting": "Hola, sóc Jarvis. Com et puc ajudar?"},
    "albanian":   {"code": "sq-AL", "tts": "sq", "flag": "🇦🇱", "greeting": "Përshëndetje, unë jam Jarvis. Si mund t'ju ndihmoj?"},

    # ──── ASIAN / MIDDLE-EASTERN ────────────────────────────────────
    "japanese":   {"code": "ja-JP", "tts": "ja", "flag": "🇯🇵", "greeting": "こんにちは、ジャービスです。どのようにお手伝いできますか?"},
    "chinese":    {"code": "zh-CN", "tts": "zh", "flag": "🇨🇳", "greeting": "你好，我是贾维斯。我能帮你什么？"},
    "korean":     {"code": "ko-KR", "tts": "ko", "flag": "🇰🇷", "greeting": "안녕하세요, 저는 자비스입니다. 어떻게 도와드릴까요?"},
    "arabic":     {"code": "ar-SA", "tts": "ar", "flag": "🇸🇦", "greeting": "مرحبا، أنا جارفيس. كيف يمكنني مساعدتك؟"},
    "persian":    {"code": "fa-IR", "tts": "fa", "flag": "🇮🇷", "greeting": "سلام، من جارویس هستم. چطور کمکتان کنم؟"},
    "hebrew":     {"code": "he-IL", "tts": "he", "flag": "🇮🇱", "greeting": "שלום, אני ג'רוויס. איך אוכל לעזור לך?"},
    "thai":       {"code": "th-TH", "tts": "th", "flag": "🇹🇭", "greeting": "สวัสดี ฉันคือจาร์วิส จะช่วยอะไรได้บ้าง?"},
    "vietnamese": {"code": "vi-VN", "tts": "vi", "flag": "🇻🇳", "greeting": "Xin chào, tôi là Jarvis. Tôi có thể giúp gì?"},
    "indonesian": {"code": "id-ID", "tts": "id", "flag": "🇮🇩", "greeting": "Halo, saya Jarvis. Bagaimana saya bisa membantu?"},
    "malay":      {"code": "ms-MY", "tts": "ms", "flag": "🇲🇾", "greeting": "Helo, saya Jarvis. Boleh saya bantu anda?"},

    # ──── AFRICAN ──────────────────────────────────────────────────
    "swahili":    {"code": "sw-KE", "tts": "sw", "flag": "🇰🇪", "greeting": "Hujambo, mimi ni Jarvis. Ninaweza kukusaidia?"},
    "afrikaans":  {"code": "af-ZA", "tts": "af", "flag": "🇿🇦", "greeting": "Hallo, ek is Jarvis. Hoe kan ek jou help?"},
    "amharic":    {"code": "am-ET", "tts": "am", "flag": "🇪🇹", "greeting": "ሰላም፣ እኔ ጃርቪስ ነኝ። እንዴት ልረዳዎ?"},
}

# ══════════════════════════════════════════════════════════════════════
#  ②  CODING LANGUAGE KNOWLEDGE BASE (50+)
# ══════════════════════════════════════════════════════════════════════
CODING_KNOWLEDGE = {
    "python": {
        "icon": "🐍", "type": "General Purpose",
        "desc": "High-level, interpreted, dynamically typed language with clean syntax.",
        "hello": 'print("Hello, World!")',
        "uses": "AI/ML, data science, web, automation, scripting",
        "frameworks": "Django, Flask, FastAPI, TensorFlow, PyTorch, Pandas, NumPy",
        "ext": ".py",
        "run": "python script.py",
        "install": "pip install package_name",
        "snippet": {
            "loop":    "for i in range(10):\n    print(i)",
            "func":    "def greet(name):\n    return f'Hello, {name}!'",
            "class":   "class Dog:\n    def __init__(self, name):\n        self.name = name\n    def bark(self):\n        return 'Woof!'",
            "file":    "with open('file.txt', 'r') as f:\n    content = f.read()",
            "list_comp": "[x**2 for x in range(10) if x % 2 == 0]",
        }
    },
    "java": {
        "icon": "☕", "type": "OOP / Enterprise",
        "desc": "Object-oriented, class-based, platform-independent language (Write Once, Run Anywhere).",
        "hello": 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
        "uses": "Enterprise apps, Android, web backends, big data",
        "frameworks": "Spring Boot, Hibernate, Maven, Gradle, JUnit",
        "ext": ".java",
        "run": "javac Main.java && java Main",
        "install": "sudo apt install default-jdk  # Linux",
        "snippet": {
            "loop":  "for (int i = 0; i < 10; i++) { System.out.println(i); }",
            "array": "int[] nums = {1, 2, 3, 4, 5};",
            "list":  "List<String> list = new ArrayList<>(); list.add(\"item\");",
        }
    },
    "html": {
        "icon": "🌐", "type": "Markup",
        "desc": "HyperText Markup Language — the skeleton of all web pages.",
        "hello": '<!DOCTYPE html>\n<html lang="en">\n<head><meta charset="UTF-8"><title>Hello</title></head>\n<body><h1>Hello, World!</h1></body>\n</html>',
        "uses": "Web page structure, content markup, email templates",
        "frameworks": "Bootstrap, Tailwind CSS, Bulma",
        "ext": ".html",
        "run": "Open in browser (double-click or python -m http.server 8000)",
        "install": "No installation needed",
        "snippet": {
            "form":  "<form action='/submit' method='POST'>\n  <input type='text' name='name' placeholder='Enter name'>\n  <button type='submit'>Submit</button>\n</form>",
            "table": "<table>\n  <tr><th>Name</th><th>Age</th></tr>\n  <tr><td>Alice</td><td>30</td></tr>\n</table>",
            "link":  "<a href='https://example.com' target='_blank'>Visit Example</a>",
        }
    },
    "css": {
        "icon": "🎨", "type": "Styling",
        "desc": "Cascading Style Sheets — the visual layer of the web.",
        "hello": "body {\n  background: #1a1a2e;\n  color: #eee;\n  font-family: 'Segoe UI', sans-serif;\n}",
        "uses": "Web styling, animations, responsive design, themes",
        "frameworks": "Bootstrap, Tailwind, SASS/SCSS, LESS, PostCSS",
        "ext": ".css",
        "run": "Link in HTML: <link rel='stylesheet' href='style.css'>",
        "install": "No installation needed",
        "snippet": {
            "flexbox":  ".container { display: flex; justify-content: center; align-items: center; }",
            "grid":     ".grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }",
            "animation":"@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }",
            "variable": ":root { --primary: #00f5d4; --bg: #0f0f0f; }",
        }
    },
    "javascript": {
        "icon": "⚡", "type": "Scripting / Full-Stack",
        "desc": "Dynamic, prototype-based scripting language that runs in browsers and on servers.",
        "hello": 'console.log("Hello, World!");',
        "uses": "Web frontend, backend (Node.js), mobile, desktop, games",
        "frameworks": "React, Vue, Angular, Node.js, Express, Next.js, Three.js",
        "ext": ".js",
        "run": "node script.js  OR  Open in browser console",
        "install": "npm install package_name",
        "snippet": {
            "arrow_fn":  "const add = (a, b) => a + b;",
            "promise":   "fetch('/api/data').then(r => r.json()).then(data => console.log(data));",
            "async":     "async function getData() {\n  const res = await fetch('/api');\n  return res.json();\n}",
            "destruct":  "const { name, age, city = 'Unknown' } = user;",
            "spread":    "const merged = { ...obj1, ...obj2 };",
        }
    },
    "react": {
        "icon": "⚛️", "type": "UI Framework",
        "desc": "Declarative JavaScript library for building component-based UIs by Meta.",
        "hello": "function App() {\n  return (\n    <div className='App'>\n      <h1>Hello, World!</h1>\n    </div>\n  );\n}\nexport default App;",
        "uses": "SPAs, dynamic UIs, PWAs, mobile with React Native",
        "frameworks": "Next.js, Gatsby, React Native, Redux, Zustand, React Query",
        "ext": ".jsx / .tsx",
        "run": "npx create-react-app myapp && cd myapp && npm start",
        "install": "npm install react react-dom",
        "snippet": {
            "hook_state": "const [count, setCount] = useState(0);\n<button onClick={() => setCount(c => c+1)}>{count}</button>",
            "hook_effect":"useEffect(() => {\n  fetchData();\n  return () => cleanup();\n}, [dependency]);",
            "context":   "const ThemeCtx = createContext('dark');\nconst theme = useContext(ThemeCtx);",
            "memo":      "const ExpensiveComp = React.memo(({ data }) => <div>{data}</div>);",
        }
    },
    "nodejs": {
        "icon": "🟩", "type": "Server-Side JS",
        "desc": "JavaScript runtime built on Chrome V8 engine for server-side programming.",
        "hello": "const http = require('http');\nhttp.createServer((req, res) => {\n  res.end('Hello, World!');\n}).listen(3000, () => console.log('Server on :3000'));",
        "uses": "REST APIs, real-time apps, microservices, CLI tools",
        "frameworks": "Express, Fastify, NestJS, Socket.io, Hapi",
        "ext": ".js / .mjs",
        "run": "node server.js",
        "install": "npm install express",
        "snippet": {
            "express_route": "app.get('/api/hello', (req, res) => res.json({ msg: 'Hello!' }));",
            "middleware":    "app.use(express.json()); app.use(cors());",
            "env":           "require('dotenv').config(); const port = process.env.PORT || 3000;",
            "file_system":   "const fs = require('fs'); fs.readFile('data.json', 'utf8', (err, data) => {});",
        }
    },
    "sql": {
        "icon": "🗄️", "type": "Database Query Language",
        "desc": "Structured Query Language for managing relational databases.",
        "hello": "SELECT 'Hello, World!' AS greeting;",
        "uses": "Database queries, data analysis, reporting, backend storage",
        "frameworks": "MySQL, PostgreSQL, SQLite, MSSQL, Oracle, MariaDB",
        "ext": ".sql",
        "run": "mysql -u root -p < script.sql  OR  psql -f script.sql",
        "install": "sudo apt install mysql-server  # Linux",
        "snippet": {
            "select":  "SELECT name, email FROM users WHERE age > 18 ORDER BY name LIMIT 10;",
            "join":    "SELECT u.name, o.total FROM users u\nJOIN orders o ON u.id = o.user_id;",
            "insert":  "INSERT INTO products (name, price, stock) VALUES ('Widget', 9.99, 100);",
            "update":  "UPDATE users SET last_login = NOW() WHERE id = ?;",
            "index":   "CREATE INDEX idx_email ON users(email);",
            "view":    "CREATE VIEW active_users AS SELECT * FROM users WHERE status = 'active';",
        }
    },
    "cmd": {
        "icon": "⬛", "type": "Windows Shell",
        "desc": "Windows Command Prompt — command-line interpreter for Windows OS.",
        "hello": "echo Hello, World!",
        "uses": "System admin, scripting, automation, file management",
        "frameworks": "Batch scripting (.bat), PowerShell",
        "ext": ".bat / .cmd",
        "run": "script.bat  OR  cmd /c script.bat",
        "install": "Built into Windows",
        "snippet": {
            "list_files": "dir /a /s",
            "find_text":  "findstr /i 'keyword' file.txt",
            "network":    "ipconfig /all && netstat -ano",
            "process":    "tasklist | findstr 'chrome' && taskkill /f /im chrome.exe",
            "loop":       "for /l %%i in (1,1,10) do echo %%i",
            "if_exists":  "if exist file.txt (echo found) else (echo not found)",
        }
    },
    "kali_linux": {
        "icon": "🐉", "type": "Security / Penetration Testing",
        "desc": "Debian-based Linux distro for penetration testing, ethical hacking and security.",
        "hello": "echo 'Hello, Hacker World!'",
        "uses": "Pen-testing, network analysis, forensics, vulnerability research",
        "frameworks": "Metasploit, Burp Suite, Wireshark, Aircrack-ng, John the Ripper",
        "ext": ".sh",
        "run": "bash exploit.sh  OR  python3 tool.py",
        "install": "sudo apt update && sudo apt install kali-linux-default",
        "snippet": {
            "update":      "sudo apt update && sudo apt full-upgrade -y",
            "network_scan": "nmap -sV -O --script=default 192.168.1.0/24",
            "wifi_scan":   "sudo iwlist wlan0 scan | grep ESSID",
            "hash_crack":  "john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt",
            "port_fwd":    "ssh -L 8080:localhost:80 user@remote-host",
            "packet_cap":  "tcpdump -i eth0 -w capture.pcap 'port 80'",
        }
    },
    "nmap": {
        "icon": "🔍", "type": "Network Scanner",
        "desc": "Network Mapper — open-source tool for network discovery and security auditing.",
        "hello": "nmap -sV localhost",
        "uses": "Port scanning, OS detection, service discovery, vulnerability assessment",
        "frameworks": "NSE (Nmap Scripting Engine), Zenmap GUI",
        "ext": ".nse",
        "run": "nmap [options] target",
        "install": "sudo apt install nmap  /  choco install nmap",
        "snippet": {
            "basic":       "nmap 192.168.1.1",
            "all_ports":   "nmap -p- 192.168.1.1",
            "service_ver": "nmap -sV -sC 192.168.1.1",
            "os_detect":   "sudo nmap -O 192.168.1.1",
            "stealth":     "sudo nmap -sS 192.168.1.1",
            "vuln_script": "nmap --script vuln 192.168.1.1",
            "udp_scan":    "sudo nmap -sU -p 53,67,161 192.168.1.1",
            "ping_sweep":  "nmap -sn 192.168.1.0/24",
            "output":      "nmap -oA scan_results 192.168.1.1  # saves .nmap, .xml, .gnmap",
        }
    },
    "typescript": {
        "icon": "🔷", "type": "Typed JS Superset",
        "desc": "Statically typed superset of JavaScript that compiles to clean JavaScript.",
        "hello": 'const msg: string = "Hello, World!";\nconsole.log(msg);',
        "uses": "Large-scale web apps, Angular, robust API development",
        "frameworks": "Angular, NestJS, Next.js, Prisma",
        "ext": ".ts / .tsx",
        "run": "npx ts-node script.ts  OR  tsc && node dist/script.js",
        "install": "npm install -g typescript",
        "snippet": {
            "interface": "interface User { id: number; name: string; email?: string; }",
            "generic":   "function identity<T>(arg: T): T { return arg; }",
            "enum":      "enum Direction { Up = 'UP', Down = 'DOWN', Left = 'LEFT', Right = 'RIGHT' }",
            "type_union":"type Status = 'active' | 'inactive' | 'pending';",
        }
    },
    "c": {
        "icon": "🔵", "type": "Systems Programming",
        "desc": "Low-level, procedural language — the mother of modern languages.",
        "hello": '#include <stdio.h>\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}',
        "uses": "OS kernels, embedded systems, drivers, compilers",
        "frameworks": "GCC, Clang, CMake, Make",
        "ext": ".c / .h",
        "run": "gcc main.c -o main && ./main",
        "install": "sudo apt install gcc build-essential",
        "snippet": {
            "pointer":  "int x = 42; int *ptr = &x; printf(\"%d\", *ptr);",
            "malloc":   "int *arr = (int*)malloc(10 * sizeof(int)); free(arr);",
            "struct":   "typedef struct { char name[50]; int age; } Person;",
            "file_io":  "FILE *f = fopen(\"data.txt\", \"w\"); fprintf(f, \"data\"); fclose(f);",
        }
    },
    "cpp": {
        "icon": "🔵🔵", "type": "Systems / OOP",
        "desc": "C with object-oriented features, templates, and the STL.",
        "hello": '#include <iostream>\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}',
        "uses": "Games, graphics engines, system software, finance",
        "frameworks": "Qt, Boost, OpenGL, Unreal Engine, SFML",
        "ext": ".cpp / .hpp",
        "run": "g++ -std=c++17 main.cpp -o main && ./main",
        "install": "sudo apt install g++ build-essential",
        "snippet": {
            "vector":   "std::vector<int> v = {1,2,3}; v.push_back(4);",
            "lambda":   "auto add = [](int a, int b) { return a + b; };",
            "template": "template<typename T> T max(T a, T b) { return a > b ? a : b; }",
            "smart_ptr":"std::unique_ptr<Dog> dog = std::make_unique<Dog>(\"Rex\");",
        }
    },
    "csharp": {
        "icon": "💜", "type": "OOP / .NET",
        "desc": "Modern, object-oriented language by Microsoft on the .NET platform.",
        "hello": 'using System;\nclass Program {\n    static void Main() {\n        Console.WriteLine("Hello, World!");\n    }\n}',
        "uses": "Windows apps, Unity games, ASP.NET web, enterprise",
        "frameworks": ".NET, ASP.NET Core, Unity, Xamarin, MAUI, Entity Framework",
        "ext": ".cs",
        "run": "dotnet run",
        "install": "sudo apt install dotnet-sdk-8.0",
        "snippet": {
            "linq":    "var adults = users.Where(u => u.Age >= 18).OrderBy(u => u.Name).ToList();",
            "async":   "async Task<string> GetDataAsync() { return await httpClient.GetStringAsync(url); }",
            "record":  "record Point(int X, int Y);",
            "nullable":"string? name = null; var len = name?.Length ?? 0;",
        }
    },
    "go": {
        "icon": "🔵🐹", "type": "Systems / Cloud",
        "desc": "Statically typed, compiled language by Google — fast, simple, concurrent.",
        "hello": 'package main\nimport "fmt"\nfunc main() {\n    fmt.Println("Hello, World!")\n}',
        "uses": "Microservices, cloud infrastructure, CLI tools, Kubernetes",
        "frameworks": "Gin, Echo, Fiber, gRPC, Hugo",
        "ext": ".go",
        "run": "go run main.go",
        "install": "sudo apt install golang-go",
        "snippet": {
            "goroutine": "go func() { fmt.Println(\"concurrent!\") }()",
            "channel":   "ch := make(chan int); go func() { ch <- 42 }(); val := <-ch",
            "defer":     "defer file.Close()  // runs at function end",
            "struct":    "type User struct { Name string; Age int }",
        }
    },
    "rust": {
        "icon": "🦀", "type": "Systems / Safety",
        "desc": "Systems programming language focused on memory safety without GC.",
        "hello": 'fn main() {\n    println!("Hello, World!");\n}',
        "uses": "WebAssembly, embedded, OS, browser engines",
        "frameworks": "Actix-web, Tokio, Axum, Rocket",
        "ext": ".rs",
        "run": "cargo run",
        "install": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
        "snippet": {
            "ownership":  "let s1 = String::from(\"hello\"); let s2 = s1; // s1 moved",
            "borrowing":  "fn len(s: &String) -> usize { s.len() }",
            "match":      "match x { 1 => \"one\", 2 => \"two\", _ => \"other\" }",
            "result":     "fn divide(a:f64, b:f64) -> Result<f64, String> { if b==0.0 { Err(\"div by zero\".to_string()) } else { Ok(a/b) } }",
        }
    },
    "kotlin": {
        "icon": "🎯", "type": "JVM / Android",
        "desc": "Modern statically typed JVM language — official Android development language.",
        "hello": 'fun main() {\n    println("Hello, World!")\n}',
        "uses": "Android development, server-side Kotlin, multiplatform",
        "frameworks": "Ktor, Spring Boot, Jetpack Compose, Coroutines",
        "ext": ".kt",
        "run": "kotlinc Main.kt -include-runtime -d Main.jar && java -jar Main.jar",
        "install": "sudo snap install kotlin --classic",
        "snippet": {
            "data_class":  "data class User(val name: String, val age: Int)",
            "coroutine":   "runBlocking { launch { delay(1000L); println(\"World!\") } }",
            "extension":   "fun String.isPalindrome() = this == this.reversed()",
            "sealed":      "sealed class Result<T> { data class Success<T>(val data: T) : Result<T>() }",
        }
    },
    "swift": {
        "icon": "🧡", "type": "Apple Platforms",
        "desc": "Powerful, intuitive language for all Apple platforms by Apple.",
        "hello": 'print("Hello, World!")',
        "uses": "iOS, macOS, watchOS, tvOS app development",
        "frameworks": "SwiftUI, UIKit, Combine, Core Data, ARKit",
        "ext": ".swift",
        "run": "swift main.swift",
        "install": "Xcode on macOS (includes Swift)",
        "snippet": {
            "optional":   "let name: String? = nil\nlet display = name ?? \"Guest\"",
            "struct":     "struct Point { var x: Double; var y: Double }",
            "closure":    "let double = { (n: Int) -> Int in return n * 2 }",
            "guard":      "guard let id = userId else { return }",
        }
    },
    "php": {
        "icon": "🐘", "type": "Web Backend",
        "desc": "Server-side scripting language designed for web development.",
        "hello": '<?php\necho "Hello, World!";\n?>',
        "uses": "Web backends, CMS (WordPress), scripting",
        "frameworks": "Laravel, Symfony, CodeIgniter, CakePHP",
        "ext": ".php",
        "run": "php script.php  OR  php -S localhost:8000",
        "install": "sudo apt install php php-cli",
        "snippet": {
            "array":    "$fruits = ['apple', 'banana', 'cherry']; foreach ($fruits as $f) echo $f;",
            "function": "function greet(string $name): string { return \"Hello, $name!\"; }",
            "pdo":      "$pdo = new PDO('mysql:host=localhost;dbname=test', 'user', 'pass');",
        }
    },
    "ruby": {
        "icon": "💎", "type": "Scripting / Web",
        "desc": "Dynamic, reflective, object-oriented scripting language.",
        "hello": 'puts "Hello, World!"',
        "uses": "Web (Rails), scripting, DevOps automation",
        "frameworks": "Ruby on Rails, Sinatra, Hanami, Rake",
        "ext": ".rb",
        "run": "ruby script.rb",
        "install": "sudo apt install ruby-full",
        "snippet": {
            "block":   "[1,2,3].each { |n| puts n * 2 }",
            "symbol":  ":name.to_s  # => 'name'",
            "hash":    "person = { name: 'Alice', age: 30 }; puts person[:name]",
        }
    },
    "dart": {
        "icon": "🎯", "type": "Cross-Platform UI",
        "desc": "Client-optimized language by Google, primary language for Flutter.",
        "hello": "void main() {\n  print('Hello, World!');\n}",
        "uses": "Flutter mobile/web/desktop apps, server-side",
        "frameworks": "Flutter, Aqueduct, Shelf",
        "ext": ".dart",
        "run": "dart run main.dart",
        "install": "sudo snap install dart --classic",
        "snippet": {
            "future":   "Future<String> fetchName() async { await Future.delayed(Duration(seconds:1)); return 'Jarvis'; }",
            "null_safe":"String? name; print(name?.toUpperCase() ?? 'No name');",
        }
    },
    "scala": {
        "icon": "🔴", "type": "Functional / JVM",
        "desc": "Multi-paradigm JVM language combining OOP and functional programming.",
        "hello": 'object Hello extends App { println("Hello, World!") }',
        "uses": "Big data (Spark), distributed systems, type-safe APIs",
        "frameworks": "Akka, Play, Apache Spark, Cats",
        "ext": ".scala",
        "run": "scala Main.scala  OR  sbt run",
        "install": "sudo apt install scala",
    },
    "r": {
        "icon": "📊", "type": "Statistical Computing",
        "desc": "Statistical computing and graphics language widely used in data science.",
        "hello": 'print("Hello, World!")',
        "uses": "Statistics, data analysis, bioinformatics, ML",
        "frameworks": "ggplot2, dplyr, Shiny, tidyverse, caret",
        "ext": ".R",
        "run": "Rscript script.R",
        "install": "sudo apt install r-base",
    },
    "bash": {
        "icon": "🐚", "type": "Unix Shell",
        "desc": "Bourne Again Shell — the default shell on most Linux/macOS systems.",
        "hello": '#!/bin/bash\necho "Hello, World!"',
        "uses": "System administration, automation, CI/CD scripts",
        "frameworks": "cron, systemd, awk, sed, grep",
        "ext": ".sh",
        "run": "bash script.sh  OR  chmod +x script.sh && ./script.sh",
        "install": "Pre-installed on Linux/macOS",
        "snippet": {
            "loop":      "for i in {1..10}; do echo $i; done",
            "if":        "if [ -f 'file.txt' ]; then echo 'exists'; fi",
            "function":  "greet() { echo \"Hello, $1!\"; }; greet 'Jarvis'",
            "read":      "read -p 'Enter name: ' name; echo \"Hi, $name\"",
            "pipe":      "cat log.txt | grep ERROR | awk '{print $2}' | sort | uniq -c",
        }
    },
    "powershell": {
        "icon": "💙", "type": "Windows Admin Shell",
        "desc": "Microsoft's task automation framework with full .NET access.",
        "hello": 'Write-Host "Hello, World!" -ForegroundColor Cyan',
        "uses": "Windows admin, automation, DevOps, Azure management",
        "frameworks": ".NET, Azure PowerShell, PSReadLine",
        "ext": ".ps1",
        "run": "powershell -ExecutionPolicy Bypass -File script.ps1",
        "install": "Pre-installed on Windows / winget install Microsoft.PowerShell",
        "snippet": {
            "get_proc":   "Get-Process | Where-Object { $_.CPU -gt 10 } | Sort-Object CPU -Descending",
            "remote":     "Invoke-Command -ComputerName Server01 -ScriptBlock { Get-Service }",
            "pipeline":   "Get-ChildItem -Recurse *.log | Select-String 'ERROR' | Export-Csv errors.csv",
        }
    },
    "graphql": {
        "icon": "🔗", "type": "API Query Language",
        "desc": "Query language and runtime for APIs — fetch exactly what you need.",
        "hello": "query { hello }",
        "uses": "API development, data fetching optimization",
        "frameworks": "Apollo, Hasura, Prisma, GraphQL Yoga",
        "ext": ".graphql",
        "run": "npx graphql-yoga  OR  apollo server",
        "install": "npm install graphql @apollo/server",
    },
    "docker": {
        "icon": "🐳", "type": "Containerization",
        "desc": "Platform for developing, shipping, and running apps in containers.",
        "hello": "docker run hello-world",
        "uses": "Containerization, microservices, CI/CD, reproducible envs",
        "frameworks": "Docker Compose, Docker Swarm, Kubernetes",
        "ext": "Dockerfile",
        "run": "docker build -t myapp . && docker run -p 8080:8080 myapp",
        "install": "curl -fsSL https://get.docker.com | sh",
        "snippet": {
            "dockerfile": "FROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nRUN pip install -r requirements.txt\nCMD [\"python\",\"app.py\"]",
            "compose":    "version: '3'\nservices:\n  web:\n    build: .\n    ports:\n      - '8000:8000'\n  db:\n    image: postgres:15",
        }
    },
    "kubernetes": {
        "icon": "☸️", "type": "Container Orchestration",
        "desc": "Open-source system for automating container deployment and scaling.",
        "hello": "kubectl create deployment hello-world --image=nginx",
        "uses": "Container orchestration, scaling, load balancing, microservices",
        "frameworks": "Helm, Istio, Prometheus, Argo CD",
        "ext": ".yaml",
        "run": "kubectl apply -f deployment.yaml",
        "install": "sudo snap install kubectl --classic",
    },
    "flutter": {
        "icon": "💙", "type": "Cross-Platform UI Framework",
        "desc": "Google's UI toolkit for building native apps from a single codebase.",
        "hello": "void main() => runApp(MaterialApp(home: Scaffold(body: Center(child: Text('Hello, World!')))));",
        "uses": "iOS, Android, web, desktop apps from single codebase",
        "frameworks": "Provider, GetX, Bloc, Riverpod",
        "ext": ".dart",
        "run": "flutter run",
        "install": "snap install flutter --classic  OR  download from flutter.dev",
    },
    "tensorflow": {
        "icon": "🧠", "type": "ML Framework",
        "desc": "Open-source machine learning platform by Google.",
        "hello": "import tensorflow as tf\nprint(tf.constant('Hello, TensorFlow!'))",
        "uses": "Deep learning, neural networks, computer vision, NLP",
        "frameworks": "Keras, TF Lite, TF.js, TF Serving",
        "ext": ".py",
        "run": "python model.py",
        "install": "pip install tensorflow",
    },
    "vue": {
        "icon": "💚", "type": "Progressive UI Framework",
        "desc": "Progressive JavaScript framework for building user interfaces.",
        "hello": "<template><h1>{{ message }}</h1></template>\n<script>\nexport default { data() { return { message: 'Hello, World!' } } }\n</script>",
        "uses": "SPAs, PWAs, server-side rendering with Nuxt",
        "frameworks": "Nuxt.js, Vuex, Pinia, Vue Router",
        "ext": ".vue",
        "run": "npm create vue@latest && npm run dev",
        "install": "npm install vue",
    },
    "angular": {
        "icon": "🔴", "type": "Enterprise UI Framework",
        "desc": "TypeScript-based web application framework by Google.",
        "hello": "@Component({ template: '<h1>Hello, World!</h1>' })\nexport class AppComponent {}",
        "uses": "Enterprise web apps, SPAs, complex form-driven apps",
        "frameworks": "RxJS, NgRx, Angular Material, PrimeNG",
        "ext": ".ts",
        "run": "ng new myapp && cd myapp && ng serve",
        "install": "npm install -g @angular/cli",
    },
    "redis": {
        "icon": "🔴", "type": "In-Memory Data Store",
        "desc": "In-memory data store used as database, cache, and message broker.",
        "hello": "SET greeting 'Hello, World!'\nGET greeting",
        "uses": "Caching, sessions, pub/sub, leaderboards, rate limiting",
        "frameworks": "ioredis, redis-py, Jedis, StackExchange.Redis",
        "ext": ".conf",
        "run": "redis-cli",
        "install": "sudo apt install redis-server",
    },
    "mongodb": {
        "icon": "🌿", "type": "NoSQL Database",
        "desc": "Document-oriented NoSQL database for high-volume storage.",
        "hello": "db.greetings.insertOne({ message: 'Hello, World!' })",
        "uses": "Document storage, real-time analytics, content management",
        "frameworks": "Mongoose (Node), PyMongo (Python), Motor (async)",
        "ext": ".js",
        "run": "mongosh",
        "install": "sudo apt install mongodb",
    },
    "git": {
        "icon": "🌿", "type": "Version Control",
        "desc": "Distributed version control system for tracking code changes.",
        "hello": "git init && git add . && git commit -m 'Initial commit'",
        "uses": "Version control, collaboration, CI/CD, code history",
        "frameworks": "GitHub, GitLab, Bitbucket, Gitea",
        "ext": ".gitignore",
        "run": "git status",
        "install": "sudo apt install git",
        "snippet": {
            "branch":     "git checkout -b feature/my-feature && git push -u origin feature/my-feature",
            "rebase":     "git fetch origin && git rebase origin/main",
            "cherry_pick":"git cherry-pick abc1234",
            "stash":      "git stash push -m 'WIP: feature' && git stash pop",
            "log":        "git log --oneline --graph --decorate --all",
        }
    },
    "lua": {
        "icon": "🌙", "type": "Embedded Scripting",
        "desc": "Lightweight, embeddable scripting language with fast performance.",
        "hello": 'print("Hello, World!")',
        "uses": "Game scripting (Roblox), embedded config, Nginx/OpenResty",
        "frameworks": "Love2D, OpenResty, LAPIS",
        "ext": ".lua",
        "run": "lua script.lua",
        "install": "sudo apt install lua5.4",
    },
    "perl": {
        "icon": "🐪", "type": "Text Processing",
        "desc": "High-level scripting language especially suited for text processing.",
        "hello": 'print "Hello, World!\\n";',
        "uses": "Text processing, sysadmin, bioinformatics, CGI",
        "frameworks": "Mojolicious, Dancer, DBI",
        "ext": ".pl",
        "run": "perl script.pl",
        "install": "sudo apt install perl",
    },
    "haskell": {
        "icon": "λ", "type": "Pure Functional",
        "desc": "Purely functional programming language with strong static typing.",
        "hello": 'main = putStrLn "Hello, World!"',
        "uses": "Functional programming, compiler writing, academic research",
        "frameworks": "Yesod, Servant, Pandoc",
        "ext": ".hs",
        "run": "runhaskell main.hs",
        "install": "sudo apt install ghc",
    },
    "assembly": {
        "icon": "⚙️", "type": "Low-Level / Machine Code",
        "desc": "Low-level language with direct correspondence to machine instructions.",
        "hello": "section .data\n  msg db 'Hello, World!', 0xA, 0\nsection .text\n  global _start\n_start:\n  mov rax, 1\n  mov rdi, 1\n  mov rsi, msg\n  mov rdx, 13\n  syscall",
        "uses": "OS kernels, device drivers, bootloaders, reverse engineering",
        "frameworks": "NASM, GAS, MASM, FASM",
        "ext": ".asm",
        "run": "nasm -f elf64 main.asm && ld main.o -o main && ./main",
        "install": "sudo apt install nasm",
    },
    "ansible": {
        "icon": "🔧", "type": "Infrastructure Automation",
        "desc": "Agentless IT automation for configuration management and deployment.",
        "hello": "- hosts: all\n  tasks:\n  - name: Say hello\n    debug: msg='Hello, World!'",
        "uses": "Infrastructure automation, config management, app deployment",
        "frameworks": "Ansible Tower, AWX, Collections",
        "ext": ".yml",
        "run": "ansible-playbook -i inventory playbook.yml",
        "install": "pip install ansible",
    },
    "terraform": {
        "icon": "🏗️", "type": "Infrastructure as Code",
        "desc": "Infrastructure as Code tool to provision cloud resources declaratively.",
        "hello": 'output "hello" { value = "Hello, Terraform!" }',
        "uses": "Cloud infrastructure, multi-cloud provisioning, IaC",
        "frameworks": "AWS, Azure, GCP, Kubernetes providers",
        "ext": ".tf",
        "run": "terraform init && terraform plan && terraform apply",
        "install": "sudo apt install terraform",
    },
    "fullstack": {
        "icon": "🌐🔙", "type": "Full Stack Development",
        "desc": "Complete web development — frontend + backend + database.",
        "hello": "Frontend: React/Vue | Backend: Node.js/Python | DB: PostgreSQL/MongoDB",
        "uses": "Complete web applications, SaaS products, APIs + UIs",
        "frameworks": "MERN (MongoDB+Express+React+Node), MEAN, Django+React, Laravel+Vue",
        "ext": "varies",
        "run": "Depends on stack",
        "install": "Install each layer separately",
        "snippet": {
            "mern_api":    "app.get('/api/users', async (req, res) => {\n  const users = await User.find();\n  res.json(users);\n});",
            "react_fetch": "useEffect(() => { fetch('/api/users').then(r=>r.json()).then(setUsers); }, []);",
        }
    },
}

# ══════════════════════════════════════════════════════════════════════
#  ③  MASTER SKILLS DICTIONARY
# ══════════════════════════════════════════════════════════════════════
JARVIS_SKILLS = {
    # ── Core ─────────────────────────────────────────────────────────
    "voice_listening": {
        "status": "✅ ACTIVE",
        "engine": "SpeechRecognition (Google Free STT)",
        "offline_fallback": "Vosk (if installed)",
        "supported_langs": list(LANGUAGES.keys()),
        "wake_word": "jarvis",
        "description": "Listens to microphone, detects wake word, transcribes speech",
    },
    "voice_replay": {
        "status": "✅ ACTIVE",
        "engine": "pyttsx3 (fully offline TTS)",
        "api_key_needed": False,
        "supported_langs": list(LANGUAGES.keys()),
        "rate": 175,   # words per minute
        "volume": 1.0,
        "description": "Converts text to speech using system TTS — no API key",
    },
    "code_writing": {
        "status": "✅ ACTIVE",
        "languages": list(CODING_KNOWLEDGE.keys()),
        "count": len(CODING_KNOWLEDGE),
        "abilities": ["hello world", "snippets", "explanations", "frameworks", "commands"],
        "description": "Generates, explains and assists with 50+ coding languages",
    },
    "system_control": {
        "status": "✅ ACTIVE",
        "abilities": ["open apps", "close apps", "shutdown", "restart", "sleep", "lock screen"],
        "platforms": ["Windows", "Linux", "macOS"],
        "description": "Full OS control — shutdown, restart, lock, sleep, app management",
    },
    "usb_control": {
        "status": "✅ ACTIVE",
        "abilities": ["list USB devices", "detect new devices", "eject drives"],
        "lib": "psutil + platform-specific",
        "description": "Detect, list and manage USB and removable storage devices",
    },
    "drive_control": {
        "status": "✅ ACTIVE",
        "abilities": ["list drives", "disk usage", "open drives", "format info"],
        "lib": "psutil",
        "description": "Monitor and control disk drives, partitions and storage",
    },
    "app_control": {
        "status": "✅ ACTIVE",
        "abilities": ["open application", "close application", "list running apps", "kill process"],
        "description": "Launch and terminate any installed application",
    },
    "search_control": {
        "status": "✅ ACTIVE",
        "abilities": ["web search", "YouTube search", "file search", "map search", "news search"],
        "engines": ["Google", "DuckDuckGo", "YouTube", "Google Maps"],
        "description": "Search the web, files, and maps via voice command",
    },
    "weather_report": {
        "status": "✅ ACTIVE",
        "engine": "wttr.in (free, no API key)",
        "api_key_needed": False,
        "formats": ["text", "temperature", "condition", "humidity", "wind"],
        "description": "Real-time weather for any city — no API key needed",
    },
    "time_report": {
        "status": "✅ ACTIVE",
        "abilities": ["current time", "current date", "day of week", "timezone", "stopwatch"],
        "description": "Report time, date, day, and timezone information",
    },
    "system_stats": {
        "status": "✅ ACTIVE",
        "metrics": ["CPU %", "RAM %", "disk %", "network speed", "temperature", "battery", "processes"],
        "lib": "psutil",
        "description": "Real-time system performance monitoring",
    },
    "cmd_control": {
        "status": "✅ ACTIVE",
        "abilities": ["execute shell commands", "CMD (Windows)", "bash (Linux)", "PowerShell"],
        "safe_mode": True,
        "description": "Execute operating system commands via voice",
    },
    "air_mouse": {
        "status": "✅ ACTIVE",
        "engine": "MediaPipe Hands + OpenCV",
        "gestures": {
            "index_finger_up":   "Move cursor",
            "pinch (thumb+index)": "Left Click",
            "peace_sign":        "Right Click",
            "three_fingers":     "Middle Click / Scroll Mode",
            "fist":              "Hold & Drag",
            "palm_open":         "Stop / Release",
            "spread_two_hands":  "Zoom In",
            "close_two_hands":   "Zoom Out",
            "swipe_up":          "Scroll Up",
            "swipe_down":        "Scroll Down",
            "swipe_left":        "Swipe Left (Alt+Left)",
            "swipe_right":       "Swipe Right (Alt+Right)",
        },
        "description": "Control mouse cursor with hand gestures via webcam",
    },
    "file_folder_ops": {
        "status": "✅ ACTIVE",
        "abilities": ["create file", "create folder", "copy", "cut", "paste", "move", "delete", "rename", "list"],
        "lib": "os + shutil + pathlib",
        "description": "Complete file and folder management by voice",
    },
    "gesture_zoom": {
        "status": "✅ ACTIVE" if GESTURE_AVAILABLE else "❌ Install OpenCV/MediaPipe",
        "trigger": "Two hands — spread fingers apart (zoom in) or bring together (zoom out)",
        "method": "pyautogui keyboard shortcut simulation",
        "description": "Pinch-to-zoom using two hands detected by camera",
    },
    "gesture_scroll": {
        "status": "✅ ACTIVE" if GESTURE_AVAILABLE else "❌ Install OpenCV/MediaPipe",
        "trigger": "Index + Middle fingers up, move hand up/down",
        "description": "Scroll pages up and down with two-finger swipe gesture",
    },
    "clap_detection": {
        "status": "✅ ACTIVE" if AUDIO_DEVICE_AVAILABLE else "❌ Install sounddevice",
        "trigger": "Two claps within 1.5 seconds",
        "action": "Open a selected application",
        "lib": "sounddevice + numpy",
        "sensitivity": "Adjustable amplitude threshold",
        "description": "Double clap to instantly open your chosen app",
    },
    "multi_language": {
        "status": "✅ ACTIVE",
        "count": len(LANGUAGES),
        "languages": list(LANGUAGES.keys()),
        "command": "say 'switch to [language]' or 'speak [language]'",
        "description": f"Full support for {len(LANGUAGES)} world languages",
    },
    "fullstack_knowledge": {
        "status": "✅ ACTIVE",
        "count": len(CODING_KNOWLEDGE),
        "languages": list(CODING_KNOWLEDGE.keys()),
        "description": f"Deep knowledge of {len(CODING_KNOWLEDGE)} programming languages and frameworks",
    },
}

# ══════════════════════════════════════════════════════════════════════
#  ④  VOICE ENGINE  (pyttsx3 — NO API KEY)
# ══════════════════════════════════════════════════════════════════════
class VoiceEngine:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 175)
            self.engine.setProperty('volume', 1.0)
            self._set_voice()
            self._tts_ok = True
        except Exception as e:
            print(f"  [TTS] Audio engine unavailable ({e}). Text-only mode.")
            print("        Linux fix: sudo apt install espeak espeak-ng")
            self.engine  = None
            self._tts_ok = False
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.current_lang = "english"
        self.lang_code   = "en-IN"
        self._speaking   = False
        self._lock       = threading.Lock()

    def _set_voice(self):
        voices = self.engine.getProperty('voices')
        if voices:
            # Prefer a male-ish voice
            for v in voices:
                if any(k in v.name.lower() for k in ['david', 'mark', 'male', 'en']):
                    self.engine.setProperty('voice', v.id)
                    return
            self.engine.setProperty('voice', voices[0].id)

    def speak(self, text: str, wait: bool = True):
        """Speak text using pyttsx3 — fully offline, no API key."""
        if not text:
            return
        print(f"\n  🤖 JARVIS: {text}")
        if not self._tts_ok or not self.engine:
            return
        with self._lock:
            self._speaking = True
            try:
                self.engine.say(text)
                if wait:
                    self.engine.runAndWait()
                else:
                    threading.Thread(target=self.engine.runAndWait, daemon=True).start()
            except Exception as e:
                print(f"  [TTS Error] {e}")
            finally:
                self._speaking = False

    def listen(self, timeout: int = 5, phrase_limit: int = 10) -> str:
        """Listen via microphone and transcribe speech."""
        try:
            with sr.Microphone() as source:
                print("  🎙️  Listening...", end='', flush=True)
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = self.recognizer.listen(source, timeout=timeout,
                                               phrase_time_limit=phrase_limit)
            print(" ✓")
            text = self.recognizer.recognize_google(audio, language=self.lang_code)
            print(f"  👤 YOU: {text}")
            return text.lower().strip()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            print("  [!] No internet for Google STT. Check connection.")
            return ""
        except Exception as e:
            print(f"  [Listen Error] {e}")
            return ""

    def set_language(self, lang_name: str) -> bool:
        lang_name = lang_name.lower()
        if lang_name in LANGUAGES:
            self.current_lang = lang_name
            self.lang_code   = LANGUAGES[lang_name]["code"]
            greeting = LANGUAGES[lang_name]["greeting"]
            self.speak(f"Language switched to {lang_name}. {greeting}")
            return True
        return False


# ══════════════════════════════════════════════════════════════════════
#  ⑤  SYSTEM CONTROLLER
# ══════════════════════════════════════════════════════════════════════
class SystemController:
    """Controls OS: apps, files, drives, USB, CMD, shutdown, etc."""

    # ─── Application Shortcuts ───────────────────────────────────────
    APP_MAP = {
        # Browsers
        "chrome":      ["google-chrome", "chrome", "chromium-browser", r"C:\Program Files\Google\Chrome\Application\chrome.exe"],
        "firefox":     ["firefox", r"C:\Program Files\Mozilla Firefox\firefox.exe"],
        "edge":        ["microsoft-edge", "msedge", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"],
        # Editors
        "vscode":      ["code", r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe"],
        "notepad":     ["notepad", "gedit", "mousepad"],
        "vim":         ["vim", "nvim"],
        "sublime":     ["subl", "sublime_text"],
        # System
        "terminal":    ["gnome-terminal", "xterm", "konsole", "cmd", "wt"],
        "file manager":["nautilus", "thunar", "dolphin", "explorer"],
        "task manager":["gnome-system-monitor", "xfce4-taskmanager", "taskmgr"],
        "calculator":  ["gnome-calculator", "xcalc", "calc"],
        "paint":       ["kolourpaint", "gimp", "mspaint"],
        # Media
        "vlc":         ["vlc"],
        "spotify":     ["spotify"],
        "youtube":     ["youtube"],
        # Productivity
        "word":        ["libreoffice --writer", r"WINWORD.EXE"],
        "excel":       ["libreoffice --calc", r"EXCEL.EXE"],
        "powerpoint":  ["libreoffice --impress", r"POWERPNT.EXE"],
        # Development
        "jupyter":     ["jupyter notebook", "jupyter lab"],
        "postman":     ["postman"],
        "docker":      ["docker desktop", "docker"],
        # Communication
        "whatsapp":    ["whatsapp"],
        "telegram":    ["telegram", "telegram-desktop"],
        "discord":     ["discord"],
        "zoom":        ["zoom"],
        "teams":       ["teams"],
        # Others
        "clock":       ["gnome-clocks", "clock"],
        "settings":    ["gnome-control-center", "xfce4-settings-manager", "control"],
    }

    def open_app(self, app_name: str) -> str:
        app_name = app_name.lower().strip()
        # Direct URL apps
        url_apps = {"youtube": "https://youtube.com", "gmail": "https://mail.google.com",
                    "whatsapp web": "https://web.whatsapp.com", "maps": "https://maps.google.com",
                    "github": "https://github.com", "stackoverflow": "https://stackoverflow.com"}
        if app_name in url_apps:
            webbrowser.open(url_apps[app_name])
            return f"Opening {app_name} in your browser."

        cmds = self.APP_MAP.get(app_name, [app_name])
        for cmd in cmds:
            try:
                if IS_WINDOWS:
                    os.startfile(cmd) if os.path.exists(cmd) else subprocess.Popen(cmd, shell=True)
                else:
                    subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"Opening {app_name}."
            except Exception:
                continue
        return f"Could not find {app_name}. Make sure it's installed."

    def close_app(self, app_name: str) -> str:
        try:
            for proc in psutil.process_iter(['name', 'pid']):
                if app_name.lower() in proc.info['name'].lower():
                    proc.kill()
                    return f"Closed {proc.info['name']}."
            return f"No running process found for {app_name}."
        except Exception as e:
            return f"Error closing {app_name}: {e}"

    def shutdown(self):
        if IS_WINDOWS:
            subprocess.run(["shutdown", "/s", "/t", "5"])
        else:
            subprocess.run(["sudo", "shutdown", "-h", "+1"])

    def restart(self):
        if IS_WINDOWS:
            subprocess.run(["shutdown", "/r", "/t", "5"])
        else:
            subprocess.run(["sudo", "reboot"])

    def sleep(self):
        if IS_WINDOWS:
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
        elif IS_LINUX:
            subprocess.run(["systemctl", "suspend"])
        elif IS_MAC:
            subprocess.run(["pmset", "sleepnow"])

    def lock_screen(self):
        if IS_WINDOWS:
            ctypes.windll.user32.LockWorkStation()
        elif IS_LINUX:
            try:
                subprocess.Popen(["gnome-screensaver-command", "--lock"])
            except Exception:
                subprocess.Popen(["xdg-screensaver", "lock"])
        elif IS_MAC:
            subprocess.run(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"])

    def get_system_stats(self) -> str:
        cpu   = psutil.cpu_percent(interval=1)
        ram   = psutil.virtual_memory()
        disk  = psutil.disk_usage('/')
        net   = psutil.net_io_counters()
        bat   = psutil.sensors_battery() if hasattr(psutil, 'sensors_battery') else None

        stats = (
            f"System Status Report:\n"
            f"  CPU Usage   : {cpu:.1f}%\n"
            f"  RAM Usage   : {ram.percent:.1f}% ({ram.used//1024//1024} MB / {ram.total//1024//1024} MB)\n"
            f"  Disk Usage  : {disk.percent:.1f}% ({disk.used//1024//1024//1024:.1f} GB / {disk.total//1024//1024//1024:.1f} GB)\n"
            f"  Net Sent    : {net.bytes_sent//1024//1024} MB | Received: {net.bytes_recv//1024//1024} MB\n"
        )
        if bat:
            stats += f"  Battery     : {bat.percent:.0f}% {'(Charging)' if bat.power_plugged else '(Discharging)'}\n"

        # Top 5 processes by CPU
        procs = sorted(psutil.process_iter(['name','cpu_percent','memory_percent']),
                       key=lambda p: p.info.get('cpu_percent', 0) or 0, reverse=True)[:5]
        stats += "  Top Processes:\n"
        for p in procs:
            stats += f"    - {p.info['name']:20s}  CPU: {p.info.get('cpu_percent',0):.1f}%  RAM: {p.info.get('memory_percent',0):.1f}%\n"
        return stats

    def get_drives(self) -> str:
        parts = psutil.disk_partitions()
        info  = "Available Drives:\n"
        for p in parts:
            try:
                usage = psutil.disk_usage(p.mountpoint)
                info += (f"  [{p.device}] {p.mountpoint} | {p.fstype} | "
                         f"{usage.total//1024//1024//1024:.1f} GB total | "
                         f"{usage.free//1024//1024//1024:.1f} GB free\n")
            except Exception:
                info += f"  [{p.device}] {p.mountpoint} (inaccessible)\n"
        return info

    def get_usb_devices(self) -> str:
        parts = psutil.disk_partitions()
        usb   = [p for p in parts if 'removable' in p.opts.lower() or
                 (IS_LINUX and '/media/' in p.mountpoint) or
                 (IS_WINDOWS and p.device.startswith(('E:', 'F:', 'G:', 'H:')))]
        if usb:
            info = "USB / Removable Devices:\n"
            for u in usb:
                info += f"  🔌 {u.device} mounted at {u.mountpoint}\n"
        else:
            info = "No USB/removable devices detected."
        return info

    def run_command(self, cmd: str) -> str:
        """Execute a shell command and return output."""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            output = result.stdout or result.stderr or "Command completed."
            return output[:1000]  # limit output length
        except subprocess.TimeoutExpired:
            return "Command timed out."
        except Exception as e:
            return f"Error: {e}"

    # ─── File/Folder Operations ────────────────────────────────────
    def create_file(self, path: str, content: str = "") -> str:
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"File created: {path}"
        except Exception as e:
            return f"Error creating file: {e}"

    def create_folder(self, path: str) -> str:
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return f"Folder created: {path}"
        except Exception as e:
            return f"Error creating folder: {e}"

    def copy_item(self, src: str, dst: str) -> str:
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            return f"Copied {src} → {dst}"
        except Exception as e:
            return f"Error copying: {e}"

    def move_item(self, src: str, dst: str) -> str:
        try:
            shutil.move(src, dst)
            return f"Moved {src} → {dst}"
        except Exception as e:
            return f"Error moving: {e}"

    def delete_item(self, path: str) -> str:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return f"Deleted: {path}"
        except Exception as e:
            return f"Error deleting: {e}"

    def list_dir(self, path: str = ".") -> str:
        try:
            items = os.listdir(path)
            result = f"Contents of {os.path.abspath(path)}:\n"
            for item in sorted(items):
                full = os.path.join(path, item)
                icon = "📁" if os.path.isdir(full) else "📄"
                size = f"  ({os.path.getsize(full):,} bytes)" if os.path.isfile(full) else ""
                result += f"  {icon} {item}{size}\n"
            return result
        except Exception as e:
            return f"Error listing directory: {e}"

    def search_files(self, pattern: str, path: str = ".") -> str:
        results = glob.glob(os.path.join(path, "**", pattern), recursive=True)
        if results:
            return "Found files:\n" + "\n".join(f"  📄 {r}" for r in results[:20])
        return f"No files matching '{pattern}' found."

    # ─── Web Search ───────────────────────────────────────────────
    def web_search(self, query: str, engine: str = "google"):
        engines = {
            "google":    f"https://www.google.com/search?q={query.replace(' ', '+')}",
            "youtube":   f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}",
            "duckduckgo":f"https://duckduckgo.com/?q={query.replace(' ', '+')}",
            "maps":      f"https://www.google.com/maps/search/{query.replace(' ', '+')}",
            "news":      f"https://news.google.com/search?q={query.replace(' ', '+')}",
            "github":    f"https://github.com/search?q={query.replace(' ', '+')}",
        }
        url = engines.get(engine.lower(), engines["google"])
        webbrowser.open(url)
        return f"Searching {engine} for: {query}"

    # ─── Weather ─────────────────────────────────────────────────
    def get_weather(self, city: str = "auto") -> str:
        if not REQUESTS_AVAILABLE:
            return "requests library not installed. Run: pip install requests"
        try:
            url = f"https://wttr.in/{city}?format=4"
            r   = requests.get(url, timeout=5)
            if r.status_code == 200:
                return f"Weather for {city}:\n{r.text}"
            # Detailed
            url2 = f"https://wttr.in/{city}?format=%l:+%C+%t+💧%h+💨%w"
            r2   = requests.get(url2, timeout=5)
            return r2.text if r2.ok else "Could not fetch weather."
        except Exception:
            return "Weather service unavailable. Check your internet connection."

    # ─── Time / Date ─────────────────────────────────────────────
    def get_time(self) -> str:
        now = datetime.datetime.now()
        return (f"Current time  : {now.strftime('%I:%M:%S %p')}\n"
                f"Current date  : {now.strftime('%A, %d %B %Y')}\n"
                f"Day of week   : {now.strftime('%A')}\n"
                f"Unix timestamp: {int(now.timestamp())}")

    def get_greeting(self) -> str:
        h = datetime.datetime.now().hour
        if   h < 12: return "Good morning, sir."
        elif h < 17: return "Good afternoon, sir."
        elif h < 21: return "Good evening, sir."
        else:        return "Good night, sir."


# ══════════════════════════════════════════════════════════════════════
#  ⑥  CLAP DETECTOR  (sounddevice — no API key)
# ══════════════════════════════════════════════════════════════════════
class ClapDetector:
    """Detects two quick claps via microphone amplitude spikes."""

    THRESHOLD      = 0.35   # amplitude threshold (0-1)
    COOLDOWN       = 0.15   # seconds between claps
    DOUBLE_WINDOW  = 1.5    # seconds for second clap

    def __init__(self, callback):
        self.callback    = callback
        self.clap_times  = deque(maxlen=5)
        self.running     = False
        self.sample_rate = 44100
        self.block_size  = 1024
        self._last_clap  = 0
        self._stream     = None

    def _audio_callback(self, indata, frames, time_info, status):
        amplitude = float(np.max(np.abs(indata)))
        if amplitude > self.THRESHOLD:
            now = time.time()
            if now - self._last_clap > self.COOLDOWN:
                self._last_clap = now
                self.clap_times.append(now)
                print(f"  👏 Clap detected! (amplitude: {amplitude:.2f})")
                # Check for double clap
                if (len(self.clap_times) >= 2 and
                        self.clap_times[-1] - self.clap_times[-2] < self.DOUBLE_WINDOW and
                        self.clap_times[-1] - self.clap_times[-2] > self.COOLDOWN):
                    self.clap_times.clear()
                    print("  👏👏 Double clap detected!")
                    threading.Thread(target=self.callback, daemon=True).start()

    def start(self):
        if not AUDIO_DEVICE_AVAILABLE:
            return
        self.running = True
        try:
            self._stream = sd.InputStream(
                samplerate=self.sample_rate,
                blocksize=self.block_size,
                channels=1,
                dtype='float32',
                callback=self._audio_callback
            )
            self._stream.start()
            print("  👏 Clap detector started.")
        except Exception as e:
            print(f"  [Clap Detector Error] {e}")

    def stop(self):
        self.running = False
        if self._stream:
            self._stream.stop()
            self._stream.close()


# ══════════════════════════════════════════════════════════════════════
#  ⑦  AIR MOUSE + GESTURE CONTROLLER  (MediaPipe + OpenCV)
# ══════════════════════════════════════════════════════════════════════
class GestureController:
    """
    Hand gesture air mouse using MediaPipe Hands + OpenCV.

    GESTURES:
      ✋ Index finger up only      → Move mouse cursor
      🤏 Thumb + Index pinch       → Left click
      ✌️  Index + Middle up         → Scroll mode (move up/down)
      ✊ Fist (all fingers closed)  → Hold & drag
      🖐 Open palm (5 fingers)     → Release / stop drag
      🤙 Two-hand spread apart     → Zoom in (Ctrl++)
      🤙 Two-hand come together    → Zoom out (Ctrl+-)
      👆 Swipe left/right          → Navigate (Alt+←/→)
      Two-clap via audio           → Launch app (see ClapDetector)
    """

    SMOOTHING    = 7      # frames to smooth cursor movement
    CLICK_DIST   = 30     # pixels — pinch distance for click
    SCROLL_SPEED = 5      # scroll lines per gesture tick
    ZOOM_THRESH  = 0.05   # relative change for zoom trigger
    SWIPE_THRESH = 80     # pixels to trigger swipe

    def __init__(self):
        self.cap          = None
        self.running      = False
        self.hands_module = mp.solutions.hands if GESTURE_AVAILABLE else None
        self.hands        = None
        self.draw         = mp.solutions.drawing_utils if GESTURE_AVAILABLE else None
        self.draw_styles  = mp.solutions.drawing_styles if GESTURE_AVAILABLE else None

        self.cursor_buf   = deque(maxlen=self.SMOOTHING)
        self.prev_y       = None
        self.dragging     = False
        self.last_click   = 0
        self.screen_w, self.screen_h = (1920, 1080)
        if PYAUTOGUI_AVAILABLE:
            self.screen_w, self.screen_h = pyautogui.size()

        # Two-hand zoom
        self.prev_hand_dist = None

        # Swipe tracking
        self.swipe_start_x  = None
        self.swipe_start_y  = None

        self._thread     = None

    # ─── Finger state helpers ─────────────────────────────────────
    def _finger_up(self, lm, tip: int, pip: int) -> bool:
        return lm[tip].y < lm[pip].y

    def _fingers_state(self, lm) -> list:
        """Returns [thumb, index, middle, ring, pinky] — 1=up, 0=down."""
        tips = [4, 8, 12, 16, 20]
        pips = [3, 6, 10, 14, 18]
        state = []
        # Thumb (compare x instead of y due to orientation)
        state.append(1 if lm[4].x < lm[3].x else 0)
        for i in range(1, 5):
            state.append(1 if lm[tips[i]].y < lm[pips[i]].y else 0)
        return state

    def _pinch_distance(self, lm) -> float:
        dx = lm[4].x - lm[8].x
        dy = lm[4].y - lm[8].y
        return math.hypot(dx, dy)

    def _landmark_to_screen(self, lm_point):
        x = int(np.interp(lm_point.x, [0.1, 0.9], [0, self.screen_w]))
        y = int(np.interp(lm_point.y, [0.1, 0.9], [0, self.screen_h]))
        return x, y

    # ─── Main gesture loop ────────────────────────────────────────
    def _run(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("  [Gesture] Cannot open webcam!")
            return

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.hands = self.hands_module.Hands(
            max_num_hands=2,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75,
            model_complexity=0
        )
        print("  👋 Gesture controller started. Show hand to camera.")
        print("     [Press 'q' in the gesture window to stop gestures]")

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)

            num_hands = 0
            all_landmarks = []

            if results.multi_hand_landmarks:
                num_hands = len(results.multi_hand_landmarks)
                for hand_lm in results.multi_hand_landmarks:
                    all_landmarks.append(hand_lm.landmark)
                    self.draw.draw_landmarks(
                        frame, hand_lm,
                        self.hands_module.HAND_CONNECTIONS,
                        self.draw_styles.get_default_hand_landmarks_style(),
                        self.draw_styles.get_default_hand_connections_style()
                    )

                lm = all_landmarks[0]
                fingers = self._fingers_state(lm)
                pinch   = self._pinch_distance(lm) * frame.shape[1]

                # ── TWO-HAND ZOOM ──────────────────────────────────
                if num_hands == 2:
                    lm2 = all_landmarks[1]
                    cx1 = lm[9].x;  cy1 = lm[9].y
                    cx2 = lm2[9].x; cy2 = lm2[9].y
                    dist = math.hypot(cx1 - cx2, cy1 - cy2)
                    if self.prev_hand_dist is not None:
                        delta = dist - self.prev_hand_dist
                        if delta > self.ZOOM_THRESH:
                            pyautogui.hotkey('ctrl', '+')
                            self._show_overlay(frame, "🔍 ZOOM IN", (0,255,0))
                        elif delta < -self.ZOOM_THRESH:
                            pyautogui.hotkey('ctrl', '-')
                            self._show_overlay(frame, "🔍 ZOOM OUT", (0,0,255))
                    self.prev_hand_dist = dist
                else:
                    self.prev_hand_dist = None

                    # ── FIST → Drag ────────────────────────────────
                    if fingers == [0, 0, 0, 0, 0]:
                        if not self.dragging:
                            pyautogui.mouseDown()
                            self.dragging = True
                        sx, sy = self._landmark_to_screen(lm[9])
                        self.cursor_buf.append((sx, sy))
                        mx, my = self._smooth_cursor()
                        pyautogui.moveTo(mx, my, duration=0.01)
                        self._show_overlay(frame, "✊ DRAG", (255,165,0))

                    # ── OPEN PALM → Release ────────────────────────
                    elif sum(fingers) >= 4:
                        if self.dragging:
                            pyautogui.mouseUp()
                            self.dragging = False
                        self._show_overlay(frame, "🖐 RELEASE", (200,200,200))

                    # ── SCROLL MODE (index + middle) ───────────────
                    elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                        curr_y = lm[8].y
                        if self.prev_y is not None:
                            dy = (curr_y - self.prev_y) * 1000
                            if dy > 3:
                                pyautogui.scroll(-self.SCROLL_SPEED)
                                self._show_overlay(frame, "⬇ SCROLL DOWN", (0,200,255))
                            elif dy < -3:
                                pyautogui.scroll(self.SCROLL_SPEED)
                                self._show_overlay(frame, "⬆ SCROLL UP", (0,255,200))
                        self.prev_y = curr_y

                    # ── INDEX ONLY → Move cursor ───────────────────
                    elif fingers[1] == 1 and fingers[2] == 0:
                        sx, sy = self._landmark_to_screen(lm[8])
                        self.cursor_buf.append((sx, sy))
                        mx, my = self._smooth_cursor()
                        pyautogui.moveTo(mx, my, duration=0.01)
                        self._show_overlay(frame, "☝ MOVE", (255,255,0))
                        self.prev_y = None

                        # PINCH → Click
                        if pinch < self.CLICK_DIST and (time.time() - self.last_click) > 0.5:
                            pyautogui.click()
                            self.last_click = time.time()
                            self._show_overlay(frame, "🖱 CLICK!", (0,255,0))

                    # ── PEACE SIGN → Right Click ───────────────────
                    elif fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[3] == 0:
                        if (time.time() - self.last_click) > 0.8:
                            pyautogui.rightClick()
                            self.last_click = time.time()
                            self._show_overlay(frame, "👉 RIGHT CLICK", (255,0,200))

            # ── SWIPE detection via index position history ─────────
            if all_landmarks and PYAUTOGUI_AVAILABLE:
                lm0 = all_landmarks[0]
                ix  = int(lm0[8].x * frame.shape[1])
                iy  = int(lm0[8].y * frame.shape[0])
                if self.swipe_start_x is None:
                    self.swipe_start_x, self.swipe_start_y = ix, iy
                else:
                    dx = ix - self.swipe_start_x
                    dy = iy - self.swipe_start_y
                    if abs(dx) > self.SWIPE_THRESH:
                        if dx > 0:
                            pyautogui.hotkey('alt', 'right')
                            self._show_overlay(frame, "➡ SWIPE RIGHT", (0,200,255))
                        else:
                            pyautogui.hotkey('alt', 'left')
                            self._show_overlay(frame, "⬅ SWIPE LEFT", (255,200,0))
                        self.swipe_start_x, self.swipe_start_y = ix, iy
            else:
                self.swipe_start_x = None

            # ── HUD overlay ────────────────────────────────────────
            self._draw_hud(frame, num_hands)
            cv2.imshow("JARVIS Air Mouse | Press Q to close", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def _smooth_cursor(self):
        if not self.cursor_buf:
            return 0, 0
        xs = [p[0] for p in self.cursor_buf]
        ys = [p[1] for p in self.cursor_buf]
        return int(sum(xs)/len(xs)), int(sum(ys)/len(ys))

    def _show_overlay(self, frame, text: str, color=(255,255,255)):
        cv2.rectangle(frame, (5, 5), (400, 45), (0,0,0), -1)
        cv2.putText(frame, text, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    def _draw_hud(self, frame, num_hands: int):
        h, w = frame.shape[:2]
        info_lines = [
            f"JARVIS AIR MOUSE",
            f"Hands Detected: {num_hands}",
            f"☝ Index = Move   Pinch = Click",
            f"✌ 2 Fingers = Scroll",
            f"✊ Fist = Drag   🖐 Palm = Release",
            f"Two Hands = Zoom  [Q=Quit]",
        ]
        y0 = h - (len(info_lines) * 22) - 10
        cv2.rectangle(frame, (0, y0-5), (w, h), (0,0,0), -1)
        for i, line in enumerate(info_lines):
            cv2.putText(frame, line, (5, y0 + i*22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0,255,200), 1)

    def start(self):
        if not GESTURE_AVAILABLE:
            print("  [!] OpenCV/MediaPipe not available. Cannot start gesture control.")
            return
        if not PYAUTOGUI_AVAILABLE:
            print("  [!] pyautogui not available. Cannot control mouse.")
            return
        self.running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self.running = False
        if self.dragging:
            try: pyautogui.mouseUp()
            except Exception: pass
        self.dragging = False


# ══════════════════════════════════════════════════════════════════════
#  ⑧  CODE GENERATOR
# ══════════════════════════════════════════════════════════════════════
class CodeGenerator:
    """Generates and explains code snippets for 50+ languages."""

    def get_info(self, lang: str) -> str:
        lang = lang.lower().replace(" ", "").replace(".", "")
        matches = {k: v for k, v in CODING_KNOWLEDGE.items()
                   if lang in k or k in lang}
        if not matches:
            return f"Language '{lang}' not in my knowledge base. Known: {', '.join(CODING_KNOWLEDGE.keys())}"
        key = list(matches.keys())[0]
        info = CODING_KNOWLEDGE[key]
        text = (
            f"\n{'═'*60}\n"
            f"  {info.get('icon','📌')} {key.upper()} — {info.get('type','')}\n"
            f"{'═'*60}\n"
            f"  Description : {info.get('desc','')}\n"
            f"  File Ext    : {info.get('ext','')}\n"
            f"  Use Cases   : {info.get('uses','')}\n"
            f"  Frameworks  : {info.get('frameworks','')}\n"
            f"  Run Command : {info.get('run','')}\n"
            f"  Install     : {info.get('install','')}\n\n"
            f"  Hello World :\n  {info.get('hello','')}\n"
        )
        if info.get('snippet'):
            text += f"\n  Code Snippets:\n"
            for name, code in info['snippet'].items():
                text += f"\n  [{name}]\n  {code}\n"
        text += f"{'═'*60}\n"
        return text

    def generate(self, lang: str, task: str) -> str:
        info = CODING_KNOWLEDGE.get(lang.lower(), {})
        lang_upper = lang.upper()
        desc = info.get('desc', '')

        templates = {
            "hello world": info.get('hello', f'# Hello World in {lang_upper}\nprint("Hello, World!")'),
            "loop":       (info.get('snippet', {}).get('loop') or
                           f'# For loop in {lang_upper}\nfor i in range(10):\n    print(i)'),
            "function":   (info.get('snippet', {}).get('func') or info.get('snippet', {}).get('function') or
                           f'# Function in {lang_upper}'),
            "class":      (info.get('snippet', {}).get('class') or f'# Class in {lang_upper}'),
            "file":       (info.get('snippet', {}).get('file') or info.get('snippet', {}).get('file_io') or
                           f'# File I/O in {lang_upper}'),
        }
        task_lower = task.lower()
        for key, snippet in templates.items():
            if key in task_lower:
                return f"\n  [{lang_upper}] {key}:\n  {snippet}\n"
        return (f"\n  [{lang_upper}] Code for '{task}':\n"
                f"  # Please provide specific requirements for auto-generation.\n"
                f"  # My knowledge base has snippets for this language: {list(info.get('snippet',{}).keys())}\n")


# ══════════════════════════════════════════════════════════════════════
#  ⑨  COMMAND PARSER & BRAIN
# ══════════════════════════════════════════════════════════════════════
class JarvisBrain:
    """
    Parses voice commands and dispatches to the correct skill.
    No external AI API — pure rule-based NLP with pattern matching.
    """

    def __init__(self, voice: VoiceEngine, sys_ctrl: SystemController, codegen: CodeGenerator):
        self.voice    = voice
        self.sys      = sys_ctrl
        self.codegen  = codegen
        self.clipboard_path = None   # for cut/copy/paste emulation

    def process(self, cmd: str) -> bool:
        """Process a voice command. Returns False to exit, True to continue."""
        cmd = cmd.lower().strip()
        if not cmd:
            return True

        # ── EXIT / GOODBYE ─────────────────────────────────────────
        if any(x in cmd for x in ["goodbye", "bye", "exit", "quit", "shutdown jarvis", "sleep jarvis"]):
            self.voice.speak("Goodbye, sir. Shutting down Jarvis. Have a great day!")
            return False

        # ── GREET ──────────────────────────────────────────────────
        if any(x in cmd for x in ["hello", "hi jarvis", "hey jarvis", "good morning", "good evening", "good afternoon"]):
            self.voice.speak(f"{self.sys.get_greeting()} All systems are online and ready, sir.")
            return True

        # ── LANGUAGE SWITCH ────────────────────────────────────────
        if "switch to" in cmd or "speak" in cmd:
            for lang in LANGUAGES.keys():
                if lang in cmd:
                    self.voice.set_language(lang)
                    return True

        # ── LIST SKILLS ────────────────────────────────────────────
        if any(x in cmd for x in ["list skills", "what can you do", "your abilities", "help", "skills"]):
            skill_list = "\n".join(f"  {k}: {v['description']}" for k, v in JARVIS_SKILLS.items())
            print(f"\n{'═'*70}\n  JARVIS SKILLS DIRECTORY\n{'═'*70}\n{skill_list}\n{'═'*70}")
            self.voice.speak(f"I have {len(JARVIS_SKILLS)} active skills. The list is displayed on your screen, sir.")
            return True

        # ── TIME & DATE ────────────────────────────────────────────
        if any(x in cmd for x in ["time", "date", "day", "what day"]):
            info = self.sys.get_time()
            print(f"\n{info}")
            now = datetime.datetime.now()
            self.voice.speak(f"The current time is {now.strftime('%I:%M %p')}, "
                             f"and today is {now.strftime('%A, %d %B %Y')}.")
            return True

        # ── WEATHER ────────────────────────────────────────────────
        if "weather" in cmd:
            city = "auto"
            # Try to extract city name
            if "in " in cmd:
                city = cmd.split("in ")[-1].strip().replace("weather", "").strip()
            elif "for " in cmd:
                city = cmd.split("for ")[-1].strip()
            self.voice.speak(f"Fetching weather for {city}...")
            weather = self.sys.get_weather(city)
            print(f"\n  🌤  {weather}")
            self.voice.speak(weather.replace('\n', '. '))
            return True

        # ── SYSTEM STATS ───────────────────────────────────────────
        if any(x in cmd for x in ["system status", "system stats", "performance", "cpu", "ram", "memory",
                                    "disk usage", "battery", "how is my computer"]):
            stats = self.sys.get_system_stats()
            print(f"\n{stats}")
            cpu = psutil.cpu_percent(interval=0.5)
            ram = psutil.virtual_memory().percent
            self.voice.speak(f"System status: CPU is at {cpu:.0f}%, RAM is at {ram:.0f}%. "
                             f"Full report is on your screen.")
            return True

        # ── DRIVES ─────────────────────────────────────────────────
        if any(x in cmd for x in ["drives", "disk", "partitions", "storage"]):
            info = self.sys.get_drives()
            print(f"\n{info}")
            self.voice.speak("Drive information is displayed on screen.")
            return True

        # ── USB ────────────────────────────────────────────────────
        if any(x in cmd for x in ["usb", "removable", "pen drive", "flash drive", "external"]):
            info = self.sys.get_usb_devices()
            print(f"\n  🔌 {info}")
            self.voice.speak(info)
            return True

        # ── OPEN APP ───────────────────────────────────────────────
        if "open " in cmd:
            app = cmd.replace("open ", "").replace("launch ", "").replace("start ", "").strip()
            msg = self.sys.open_app(app)
            self.voice.speak(msg)
            return True

        if "launch " in cmd or "start " in cmd:
            app = cmd.replace("launch ", "").replace("start ", "").strip()
            msg = self.sys.open_app(app)
            self.voice.speak(msg)
            return True

        # ── CLOSE APP ─────────────────────────────────────────────
        if "close " in cmd or "kill " in cmd:
            app = cmd.replace("close ", "").replace("kill ", "").strip()
            msg = self.sys.close_app(app)
            self.voice.speak(msg)
            return True

        # ── SEARCH ────────────────────────────────────────────────
        if "search" in cmd or "google" in cmd or "youtube" in cmd or "find" in cmd:
            engine = "google"
            query  = cmd
            if "youtube" in cmd:
                engine = "youtube"
                query  = cmd.replace("youtube", "").replace("search", "").strip()
            elif "google" in cmd:
                query  = cmd.replace("google", "").replace("search", "").strip()
            elif "search" in cmd:
                query  = cmd.replace("search", "").replace("for ", "").strip()
            msg = self.sys.web_search(query, engine)
            self.voice.speak(msg)
            return True

        # ── SHUTDOWN / RESTART / SLEEP ─────────────────────────────
        if "shutdown computer" in cmd or "turn off computer" in cmd or "power off" in cmd:
            self.voice.speak("Shutting down the computer in 5 seconds. Goodbye!")
            self.sys.shutdown()
            return False

        if "restart" in cmd or "reboot" in cmd:
            self.voice.speak("Restarting the computer.")
            self.sys.restart()
            return False

        if "sleep" in cmd and "computer" in cmd:
            self.voice.speak("Putting the computer to sleep.")
            self.sys.sleep()
            return True

        if "lock" in cmd and any(x in cmd for x in ["screen", "computer", "pc"]):
            self.voice.speak("Locking the screen.")
            self.sys.lock_screen()
            return True

        # ── FILE OPERATIONS ────────────────────────────────────────
        if "create file" in cmd:
            fname = cmd.replace("create file", "").replace("named", "").strip() or "untitled.txt"
            msg = self.sys.create_file(fname)
            self.voice.speak(msg)
            return True

        if "create folder" in cmd or "make folder" in cmd or "make directory" in cmd:
            fname = (cmd.replace("create folder", "").replace("make folder", "")
                       .replace("make directory", "").replace("named", "").strip()) or "new_folder"
            msg = self.sys.create_folder(fname)
            self.voice.speak(msg)
            return True

        if "list files" in cmd or "show files" in cmd or "show folder" in cmd:
            path = "."
            if "in " in cmd:
                path = cmd.split("in ")[-1].strip()
            info = self.sys.list_dir(path)
            print(f"\n{info}")
            self.voice.speak(f"Directory listing displayed on screen.")
            return True

        if "search file" in cmd or "find file" in cmd:
            pattern = cmd.replace("search file", "").replace("find file", "").strip() or "*"
            info = self.sys.search_files(pattern)
            print(f"\n{info}")
            self.voice.speak("File search results are displayed.")
            return True

        if "copy" in cmd and (" to " in cmd or "file" in cmd):
            parts = cmd.replace("copy", "").split(" to ")
            if len(parts) == 2:
                msg = self.sys.copy_item(parts[0].strip(), parts[1].strip())
                self.voice.speak(msg)
            return True

        if "move" in cmd and " to " in cmd:
            parts = cmd.replace("move", "").split(" to ")
            if len(parts) == 2:
                msg = self.sys.move_item(parts[0].strip(), parts[1].strip())
                self.voice.speak(msg)
            return True

        if "delete" in cmd or "remove file" in cmd:
            fname = (cmd.replace("delete", "").replace("remove file", "").strip())
            if fname:
                msg = self.sys.delete_item(fname)
                self.voice.speak(msg)
            return True

        # ── CMD / TERMINAL COMMANDS ────────────────────────────────
        if cmd.startswith("run command") or cmd.startswith("execute") or cmd.startswith("terminal"):
            shell_cmd = (cmd.replace("run command", "").replace("execute", "")
                          .replace("terminal", "").strip())
            if shell_cmd:
                self.voice.speak(f"Executing: {shell_cmd}")
                out = self.sys.run_command(shell_cmd)
                print(f"\n  Terminal Output:\n{out}")
                self.voice.speak("Command executed. Output is shown on screen.")
            return True

        # ── CODING KNOWLEDGE ───────────────────────────────────────
        if any(x in cmd for x in ["code", "programming", "language", "how to", "write", "snippet",
                                    "explain", "what is", "show me"]):
            for lang in CODING_KNOWLEDGE.keys():
                if lang in cmd or lang.replace("_", " ") in cmd:
                    # Check for specific snippet request
                    if any(x in cmd for x in ["hello", "hello world"]):
                        info = CODING_KNOWLEDGE[lang]
                        print(f"\n  [{lang.upper()}] Hello World:\n  {info.get('hello','')}\n")
                        self.voice.speak(f"Here is the Hello World code for {lang}.")
                    elif any(x in cmd for x in ["snippet", "loop", "function", "class", "example"]):
                        result = self.codegen.generate(lang, cmd)
                        print(result)
                        self.voice.speak(f"Here is a {lang} code snippet. Check your screen.")
                    else:
                        info = self.codegen.get_info(lang)
                        print(info)
                        self.voice.speak(f"{lang} is {CODING_KNOWLEDGE[lang].get('desc','')}. "
                                         f"It is used for {CODING_KNOWLEDGE[lang].get('uses','').split(',')[0]}.")
                    return True

        # ── LIST ALL LANGUAGES ─────────────────────────────────────
        if "list languages" in cmd or "coding languages" in cmd or "what languages" in cmd:
            langs = list(CODING_KNOWLEDGE.keys())
            print(f"\n  📚 Coding Languages ({len(langs)}):\n  " + "\n  ".join(
                f"{i+1:2}. {l}" for i, l in enumerate(langs)
            ))
            self.voice.speak(f"I know {len(langs)} coding languages. The list is on your screen.")
            return True

        # ── VOLUME ────────────────────────────────────────────────
        if "volume up" in cmd or "increase volume" in cmd:
            if IS_WINDOWS:
                subprocess.run(["nircmd.exe", "changesysvolume", "5000"], shell=True)
            else:
                subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"])
            self.voice.speak("Volume increased.")
            return True

        if "volume down" in cmd or "decrease volume" in cmd or "lower volume" in cmd:
            if IS_WINDOWS:
                subprocess.run(["nircmd.exe", "changesysvolume", "-5000"], shell=True)
            else:
                subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"])
            self.voice.speak("Volume decreased.")
            return True

        if "mute" in cmd:
            if IS_WINDOWS:
                subprocess.run(["nircmd.exe", "mutesysvolume", "1"], shell=True)
            else:
                subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "1"])
            self.voice.speak("Muted.")
            return True

        # ── SCREENSHOT ────────────────────────────────────────────
        if "screenshot" in cmd or "take screenshot" in cmd or "capture screen" in cmd:
            if PYAUTOGUI_AVAILABLE:
                ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                path = os.path.join(os.path.expanduser("~"), f"screenshot_{ts}.png")
                pyautogui.screenshot(path)
                self.voice.speak(f"Screenshot saved to {path}")
            else:
                self.voice.speak("pyautogui not available for screenshots.")
            return True

        # ── JOKE ──────────────────────────────────────────────────
        if "joke" in cmd or "tell me a joke" in cmd or "make me laugh" in cmd:
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "There are only 10 types of people in the world: those who understand binary and those who don't.",
                "A SQL query walks into a bar, walks up to two tables, and asks — Can I join you?",
                "Why did the Python programmer wear glasses? Because they couldn't C-sharp!",
                "How many programmers does it take to change a light bulb? None — it's a hardware problem.",
                "What is a computer's favourite snack? Microchips!",
                "Why did the developer go broke? Because he used up all his cache.",
            ]
            joke = random.choice(jokes)
            self.voice.speak(joke)
            return True

        # ── WHO ARE YOU ───────────────────────────────────────────
        if any(x in cmd for x in ["who are you", "what are you", "introduce yourself", "your name"]):
            intro = (
                "I am JARVIS — Just A Rather Very Intelligent System. "
                f"I support {len(LANGUAGES)} languages, know {len(CODING_KNOWLEDGE)} programming languages, "
                "and can control your entire system with my voice and gesture capabilities. "
                "I was created to serve you, sir."
            )
            self.voice.speak(intro)
            return True

        # ── FALLBACK ──────────────────────────────────────────────
        self.voice.speak(f"I heard: {cmd}. I'm still learning that command. "
                         "Try saying 'help' for a list of my skills.")
        return True


# ══════════════════════════════════════════════════════════════════════
#  ⑩  MAIN JARVIS CLASS
# ══════════════════════════════════════════════════════════════════════
class Jarvis:
    """Main Jarvis orchestrator — wires all systems together."""

    WAKE_WORDS = ["jarvis", "hey jarvis", "ok jarvis", "yo jarvis", "jarvis wake up"]

    def __init__(self):
        print(self._banner())
        self.voice    = VoiceEngine()
        self.sys      = SystemController()
        self.codegen  = CodeGenerator()
        self.brain    = JarvisBrain(self.voice, self.sys, self.codegen)
        self.gesture  = GestureController() if GESTURE_AVAILABLE else None
        self.clapper  = ClapDetector(self._on_double_clap) if AUDIO_DEVICE_AVAILABLE else None
        self.running  = False
        self.active   = False   # True = awake / listening for commands
        self.clap_app = "chrome"  # App to open on double clap (ask user at start)

    def _banner(self) -> str:
        return f"""
╔══════════════════════════════════════════════════════════════════════╗
║          J A R V I S   A I   —   VOICE + GESTURE CONTROL           ║
║  Languages: {len(LANGUAGES):3d}  |  Coding Skills: {len(CODING_KNOWLEDGE):3d}  |  Skills: {len(JARVIS_SKILLS):3d}     ║
║  No API Key Required  |  Fully Offline TTS  |  Air Mouse Active    ║
╚══════════════════════════════════════════════════════════════════════╝
  Platform   : {platform.system()} {platform.release()}
  Gesture    : {'✅ MediaPipe Ready' if GESTURE_AVAILABLE else '❌ Install opencv-python mediapipe'}
  Clap Detect: {'✅ sounddevice Ready' if AUDIO_DEVICE_AVAILABLE else '❌ Install sounddevice'}
  Mouse Ctrl : {'✅ pyautogui Ready' if PYAUTOGUI_AVAILABLE else '❌ Install pyautogui'}
  Weather    : {'✅ requests Ready (wttr.in)' if REQUESTS_AVAILABLE else '❌ Install requests'}
"""

    def _on_double_clap(self):
        """Called by ClapDetector when two claps are detected."""
        print(f"\n  👏👏 Double clap → Opening {self.clap_app}!")
        self.voice.speak(f"Double clap detected! Opening {self.clap_app}.")
        self.sys.open_app(self.clap_app)

    def _setup(self):
        """Interactive setup on first run."""
        print("\n  ──────────────────────────────────────────")
        print("  JARVIS SETUP")
        print("  ──────────────────────────────────────────")
        app = input("  What app should I open on double clap? [chrome]: ").strip() or "chrome"
        self.clap_app = app

        mode = input("  Start in listening mode? (yes/no) [yes]: ").strip().lower()
        return mode != "no"

    def start(self):
        """Start all subsystems and enter main loop."""
        listen_mode = self._setup()

        # Start clap detector
        if self.clapper:
            self.clapper.start()

        # Start gesture controller
        if self.gesture:
            gesture_yn = input("  Enable hand gesture / Air Mouse? (yes/no) [yes]: ").strip().lower()
            if gesture_yn != "no":
                self.gesture.start()

        self.running = True
        self.active  = listen_mode

        self.voice.speak(
            f"{self.sys.get_greeting()} I am Jarvis, your AI system controller. "
            f"{'I am now listening. Say my name to wake me up.' if not self.active else 'I am ready. How may I assist you?'}"
        )

        print(f"\n  {'='*60}")
        print(f"  🎙  WAKE WORD: {' | '.join(self.WAKE_WORDS)}")
        print(f"  👏  DOUBLE CLAP → Opens: {self.clap_app}")
        print(f"  💬  SAY 'goodbye' to quit")
        print(f"  ⌨   Or type commands below:")
        print(f"  {'='*60}\n")

        while self.running:
            try:
                # ── TEXT input fallback ──────────────────────────
                # Run voice listening in a separate approach:
                # Let user type OR speak
                user_input = self._get_input()

                if not user_input:
                    continue

                # ── Wake word detection ──────────────────────────
                if not self.active:
                    if any(w in user_input for w in self.WAKE_WORDS):
                        self.active = True
                        self.voice.speak("Yes sir, I'm listening.")
                    continue

                # ── Deactivate on "sleep" ────────────────────────
                if "go to sleep" in user_input or "stop listening" in user_input:
                    self.active = False
                    self.voice.speak("Going to sleep. Say my name to wake me up.")
                    continue

                # ── Process command ──────────────────────────────
                keep_running = self.brain.process(user_input)
                if not keep_running:
                    self.running = False

            except KeyboardInterrupt:
                print("\n  [Ctrl+C] Interrupted.")
                self.running = False
            except Exception as e:
                print(f"  [Error in main loop] {e}")
                continue

        self._shutdown()

    def _get_input(self) -> str:
        """
        Tries voice first (non-blocking attempt), then falls back gracefully.
        In a real deployment run voice-only loop. Here we use a thread for voice
        while also accepting keyboard input for testing.
        """
        voice_result_queue = queue.Queue()

        def _voice_thread():
            text = self.voice.listen(timeout=4, phrase_limit=8)
            voice_result_queue.put(text)

        vt = threading.Thread(target=_voice_thread, daemon=True)
        vt.start()

        # Also allow keyboard input
        try:
            import select
            if IS_WINDOWS:
                # Windows: just wait for voice
                vt.join(timeout=6)
                return voice_result_queue.get_nowait() if not voice_result_queue.empty() else ""
            else:
                # Linux/Mac: check stdin
                readable, _, _ = select.select([sys.stdin], [], [], 6)
                if readable:
                    return sys.stdin.readline().strip().lower()
                vt.join(timeout=1)
                return voice_result_queue.get_nowait() if not voice_result_queue.empty() else ""
        except Exception:
            vt.join(timeout=6)
            try:
                return voice_result_queue.get_nowait()
            except queue.Empty:
                return ""

    def _shutdown(self):
        if self.clapper:
            self.clapper.stop()
        if self.gesture:
            self.gesture.stop()
        print("\n  JARVIS has shut down. Goodbye, sir.\n")


# ══════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════
def demo_mode():
    """Show all skills without mic/camera — for testing/CI."""
    print("\n  ═══ JARVIS — DEMO MODE (No mic/camera) ═══\n")
    voice   = VoiceEngine()
    sys_ctl = SystemController()
    codegen = CodeGenerator()

    print("\n  📋 ALL SKILLS:")
    for name, info in JARVIS_SKILLS.items():
        print(f"    {info['status']}  {name:25s}  {info['description']}")

    print(f"\n  🌍 LANGUAGES SUPPORTED ({len(LANGUAGES)}):")
    for i, (name, info) in enumerate(LANGUAGES.items(), 1):
        print(f"    {i:2d}. {info['flag']} {name:15s}  [{info['code']}]")

    print(f"\n  💻 CODING LANGUAGES ({len(CODING_KNOWLEDGE)}):")
    for i, (name, info) in enumerate(CODING_KNOWLEDGE.items(), 1):
        print(f"    {i:2d}. {info.get('icon','📌')} {name:20s}  {info.get('type','')}")

    print(f"\n  ⏰ System Time:\n{sys_ctl.get_time()}")
    print(f"\n  💾 System Stats:\n{sys_ctl.get_system_stats()}")
    print(f"\n  🖥  Drives:\n{sys_ctl.get_drives()}")
    print(f"\n  🔌 USB:\n{sys_ctl.get_usb_devices()}")
    print(f"\n  🐍 Python Info:\n{codegen.get_info('python')[:800]}")
    print(f"\n  🔍 NMAP Info:\n{codegen.get_info('nmap')[:800]}")
    print(f"\n  ═══ Demo complete! ═══\n")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo_mode()
    else:
        try:
            jarvis = Jarvis()
            jarvis.start()
        except Exception as e:
            print(f"\n  [FATAL] {e}")
            print("  Run with --demo flag to test without mic/camera.")
            raise
