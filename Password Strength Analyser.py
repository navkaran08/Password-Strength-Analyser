"""
Password Strength Analyzer Pro - Enhanced Edition
Author: Navkaran Singh (Enhanced Version)
Advanced Cyber Security Tool with Breach Detection, Animations & Extended Weak Password Database
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
import math
import hashlib
import requests
import threading
import json
import os
import sqlite3
from datetime import datetime
from collections import Counter
import random
import sys
import time

# ==================== CONFIGURATION ====================
class Config:
    """Application configuration constants"""
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 850
    BG_COLOR = "#0a0a0a"
    CARD_BG = "#141414"
    ACCENT_COLOR = "#00d4ff"
    SUCCESS_COLOR = "#00ff88"
    WARNING_COLOR = "#ffaa00"
    DANGER_COLOR = "#ff4757"
    TEXT_COLOR = "#ffffff"
    SECONDARY_TEXT = "#888888"
    FONT_FAMILY = "Segoe UI"
    
    # HIBP API endpoint
    HIBP_API_URL = "https://api.pwnedpasswords.com/range/"
    
    # Database file
    DB_FILE = "password_history.db"
    
    # Extended common passwords list (top 1000+ most common)
    COMMON_PASSWORDS = [
        # Original 100
        "123456", "password", "12345678", "qwerty", "123456789",
        "12345", "1234", "111111", "1234567", "dragon",
        "123123", "baseball", "abc123", "football", "monkey",
        "letmein", "696969", "shadow", "master", "666666",
        "qwertyuiop", "123321", "mustang", "1234567890", "michael",
        "654321", "pussy", "superman", "1qaz2wsx", "7777777",
        "fuckyou", "121212", "000000", "qazwsx", "123qwe",
        "killer", "trustno1", "jordan", "jennifer", "zxcvbnm",
        "asdfgh", "hunter", "buster", "soccer", "harley",
        "batman", "andrew", "tigger", "sunshine", "iloveyou",
        "fuckme", "2000", "charlie", "robert", "thomas",
        "hockey", "ranger", "daniel", "starwars", "klaster",
        "112233", "george", "asshole", "computer", "michelle",
        "jessica", "pepper", "1111", "zxcvbn", "555555",
        "11111111", "131313", "freedom", "777777", "pass",
        "fuck", "maggie", "159753", "aaaaaa", "ginger",
        "princess", "joshua", "cheese", "amanda", "summer",
        "love", "ashley", "nicole", "chelsea", "biteme",
        "matthew", "access", "yankees", "987654321", "dallas",
        "austin", "thunder", "taylor", "matrix", "minecraft",
        
        # Extended list - Top 1000 most common passwords
        "welcome", "admin", "password1", "1234567890", "qwerty123",
        "login", "princess", "solo", "starwars", "admin123",
        "welcome123", "password123", "password12", "password01",
        "passw0rd", "pass123", "mypassword", "default", "guest",
        "user", "test", "demo", "temp", "changeme",
        "password!", "password.", "password?", "password*",
        "secret", "password2", "password3", "password4", "password5",
        "password6", "password7", "password8", "password9", "password0",
        "qwerty1", "qwerty2", "qwerty3", "qwerty4", "qwerty5",
        "qwerty6", "qwerty7", "qwerty8", "qwerty9", "qwerty0",
        "qwerty12", "qwerty21", "qwerty1234", "qwertyuiop[]",
        "azerty", "azertyuiop", "azerty123", "azertyuiop123",
        "qwertz", "qwertz123", "yxcvbn", "dvorak", "colemak",
        
        # Names
        "anthony", "andrew", "angel", "angela", "ashley", "amanda",
        "brandon", "brian", "brittany", "benjamin", "barbara",
        "christopher", "chris", "charles", "catherine", "christine",
        "daniel", "david", "donald", "diana", "dorothy",
        "edward", "elizabeth", "emily", "eric", "emma",
        "frank", "franklin", "fiona", "fred", "faith",
        "george", "gary", "grace", "gregory", "gina",
        "henry", "heather", "hannah", "harry", "helen",
        "isaac", "isabella", "ian", "irene", "ivan",
        "james", "john", "jason", "jeff", "jennifer",
        "jessica", "jack", "jacob", "joseph", "joshua",
        "kevin", "kelly", "karen", "kenneth", "kyle",
        "laura", "linda", "lisa", "lily", "logan",
        "michael", "mark", "matthew", "mary", "michelle",
        "nancy", "natalie", "nathan", "noah", "nicholas",
        "oliver", "olivia", "oscar", "owen", "oprah",
        "peter", "patricia", "paul", "pamela", "patrick",
        "quincy", "quinn", "queen", "quentin",
        "robert", "richard", "ryan", "rachel", "rebecca",
        "steven", "stephen", "sarah", "sandra", "samantha",
        "thomas", "timothy", "taylor", "tiffany", "tracy",
        "ursula", "ulysses",
        "victor", "vincent", "vanessa", "vera", "valerie",
        "william", "wendy", "walter", "wayne", "wanda",
        "xavier", "xena",
        "yolanda", "yvonne", "yasmine", "yusuf", "yuri",
        "zachary", "zoe", "zara", "zebra",
        
        # Sports teams
        "lakers", "yankees", "cowboys", "steelers", "patriots",
        "redsox", "cubs", "cardinals", "giants", "eagles",
        "raiders", "packers", "bears", "broncos", "seahawks",
        "chelsea", "arsenal", "liverpool", "manchester", "barcelona",
        "real madrid", "juventus", "bayern", "psg", "milan",
        
        # Keyboard patterns
        "qweasd", "wasd", "qazwsxedc", "qazxsw", "wsxedc",
        "1q2w3e", "1q2w3e4r", "1q2w3e4r5t", "qwertyui",
        "asdfghjkl", "asdfgh", "asdfg", "sdfgh", "dfghj",
        "zxcvbn", "zxcvb", "xcvbn", "poiuyt", "lkjhgf",
        "mnbvcx", "mnbvcxz", "rewq", "fdsa", "gfds",
        
        # Number sequences
        "012345", "0123456", "01234567", "012345678", "0123456789",
        "098765", "0987654", "09876543", "0987654321",
        "13579", "24680", "111222", "222333", "333444",
        "444555", "555666", "666777", "777888", "888999",
        "101010", "202020", "303030", "404040", "505050",
        "606060", "707070", "808080", "909090",
        "123654", "321456", "456123", "654321", "789456",
        "147258", "147258369", "369258", "258147", "741852",
        
        # Dates and years
        "2024", "2023", "2022", "2021", "2020", "2019", "2018",
        "2017", "2016", "2015", "2014", "2013", "2012", "2011",
        "2010", "2009", "2008", "2007", "2006", "2005", "2004",
        "2003", "2002", "2001", "2000", "1999", "1998", "1997",
        "1996", "1995", "1994", "1993", "1992", "1991", "1990",
        "1989", "1988", "1987", "1986", "1985", "1984", "1983",
        "1982", "1981", "1980", "1979", "1978", "1977", "1976",
        "1975", "1974", "1973", "1972", "1971", "1970",
        
        # Common words
        "hello", "world", "test", "demo", "sample", "example",
        "home", "work", "office", "school", "college", "university",
        "summer", "winter", "spring", "autumn", "fall",
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december",
        "monday", "tuesday", "wednesday", "thursday", "friday",
        "saturday", "sunday", "weekend", "weekday",
        "morning", "afternoon", "evening", "night", "midnight",
        "today", "tomorrow", "yesterday", "now", "later",
        
        # Leet speak variations
        "p@ssw0rd", "p@ssword", "passw0rd", "pa$$w0rd", "pa$$word",
        "p@$$w0rd", "p@$$word", "p@ssw0rd123", "p@ssword123",
        "admin1", "admin12", "admin123", "admin1234", "admin12345",
        "r00t", "t00r", "r007", "t007", "h4ck3r", "hacker",
        "l33t", "1337", "31337", "n00b", "noob", "5cr1pt",
        
        # Common phrases
        "letmein1", "letmein2", "letmein123", "letmeinnow",
        "iloveyou1", "iloveyou2", "iloveyou123", "iloveyoubaby",
        "trustno1", "trustnoone", "trustnobody",
        "nopassword", "nopass", "passwordno", "nopassword1",
        "forgotpassword", "forgotpass", "resetpassword", "newpassword",
        "oldpassword", "mypassword1", "mypassword2", "mypassword123",
        "yourpassword", "thepassword", "apassword", "thispassword",
        
        # Company names
        "google", "facebook", "amazon", "apple", "microsoft",
        "twitter", "instagram", "linkedin", "youtube", "netflix",
        "spotify", "uber", "airbnb", "snapchat", "whatsapp",
        "tesla", "spacex", "nasa", "spacex123", "tesla123",
        
        # Colors
        "red123", "blue123", "green123", "yellow123", "black123",
        "white123", "purple123", "orange123", "pink123", "gray123",
        "redpassword", "bluepassword", "greenpassword",
        
        # Animals
        "dog123", "cat123", "bird123", "fish123", "lion123",
        "tiger123", "bear123", "wolf123", "eagle123", "snake123",
        "monkey123", "dragon123", "panda123", "rabbit123", "horse123",
        
        # Misc
        "qwerty12345", "qwerty123456", "qwerty1234567",
        "passwordqwerty", "qwertypassword", "123qweasd",
        "1qazxsw2", "1qaz2wsx3edc", "zaq12wsx", "zaq1xsw2",
        "password!@#", "password123!@#", "admin!@#",
        "root123", "toor", "toor123", "user123", "test123",
        "guest123", "demo123", "temp123", "changeme123",
        "password1!", "password2@", "password3#", "password4$",
        "password5%", "password6^", "password7&", "password8*",
        "password9(", "password0)", "password!1", "password@2",
        "welcome1", "welcome2", "welcome123", "welcome01",
        "login1", "login2", "login123", "login01",
        "master1", "master2", "master123", "master01",
        "shadow1", "shadow2", "shadow123", "shadow01",
        "secret1", "secret2", "secret123", "secret01",
        "access1", "access2", "access123", "access01",
        "pass1", "pass2", "pass12", "pass123", "passw1",
        "word1", "word12", "word123", "wordpass",
        
        # Phone/keyboard patterns
        "1478963", "3698741", "2580", "0852", "753951",
        "159357", "357951", "456852", "258456", "789123",
        
        # Doubled/Tripled
        "abcabc", "abcabcabc", "xyzxyz", "xyzxyzxyz",
        "123123123", "456456", "789789", "000111", "111000",
        "12121212", "13131313", "212121", "232323", "343434",
        "454545", "565656", "676767", "787878", "898989",
        
        # Reversed
        "drowssap", "drowssap1", "drowssap123",
        "ytrewq", "ytrewq123", "ytrewq321",
        "6543210", "0987654321", "9876543210",
        
        # Common suffixes/prefixes
        "password2024", "password2023", "password2022",
        "password2021", "password2020", "password2019",
        "admin2024", "admin2023", "admin2022",
        "user2024", "user2023", "user2022",
        "login2024", "login2023", "login2022",
        
        # Famous passwords from breaches
        "adobe123", "linkedin", "myspace1", "rockyou",
        "linkedin123", "dropbox", "yahoo123", "gmail123",
        "hotmail1", "outlook1", "aol123", "icloud1",
        
        # Gaming references
        "minecraft1", "minecraft123", "fortnite", "fortnite1",
        "roblox", "roblox123", "steam123", "origin123",
        "playstation", "xbox123", "nintendo", "pokemon",
        "pokemon123", "mario123", "zelda123", "link123",
        
        # Movie/TV references
        "starwars1", "starwars123", "startrek", "startrek1",
        "harrypotter", "potter123", "voldemort", "dumbledore",
        "batman1", "batman123", "superman1", "superman123",
        "spiderman", "spiderman1", "ironman", "ironman1",
        "avengers", "avengers123", "thanos", "thanos123",
        
        # Music references
        "beatles", "beatles1", "beatles123", "johnlennon",
        "elvis", "elvis1", "elvis123", "madonna", "madonna1",
        "eminem", "eminem123", "tupac", "tupac123", "biggie",
        
        # Internet culture
        "lol123", "omg123", "wtf123", "lmao", "lmao123",
        "rofl", "rofl123", "brb123", "ttyl", "ttyl123",
        "idk123", "idc123", "imo123", "imho", "imho123",
        "ftw123", "fml123", "smh123", "tbh", "tbh123",
        
        # Common first names + numbers
        "john123", "john1234", "john12345",
        "jane123", "jane1234", "jane12345",
        "mary123", "mary1234", "mary12345",
        "mike123", "mike1234", "mike12345",
        "sarah123", "sarah1234", "sarah12345",
        
        # Common last names + numbers
        "smith123", "smith1234", "johnson123",
        "williams123", "brown123", "jones123",
        "davis123", "miller123", "wilson123",
        
        # Cities
        "london123", "paris123", "tokyo123", "berlin123",
        "sydney123", "madrid123", "rome123", "dubai123",
        "newyork", "newyork1", "newyork123", "nyc123",
        "losangeles", "la123", "chicago", "chicago123",
        "houston", "houston123", "phoenix", "phoenix123",
        
        # Countries
        "usa123", "america1", "america123", "uk123", "britain",
        "canada123", "mexico123", "germany1", "france1",
        "italy123", "spain123", "brazil123", "india123",
        "china123", "japan123", "russia123", "australia1",
        
        # Months + years
        "january2024", "february2024", "march2024",
        "april2024", "may2024", "june2024",
        "july2024", "august2024", "september2024",
        "october2024", "november2024", "december2024",
        
        # Days + numbers
        "monday1", "tuesday1", "wednesday1",
        "thursday1", "friday1", "saturday1", "sunday1",
        
        # Seasons + years
        "summer2024", "winter2024", "spring2024", "fall2024",
        "summer2023", "winter2023", "spring2023", "fall2023",
        
        # Profanity (censored for code but common in passwords)
        "fuck123", "fuckyou1", "fuckyou123", "fuckoff",
        "shit123", "damn123", "hell123", "ass123",
        "bitch1", "bitch123", "bastard", "bastard1",
        
        # More variations
        "password..", "password...", "password!!!!",
        "????????", "!!!!!!!!", "........", ",,,,,,,,",
        "++++++++", "========", "--------", "________",
        
        # Phone patterns
        "5555555", "7777777", "8888888", "9999999",
        "0000000", "1111111", "2222222", "3333333",
        "4444444", "6666666",
        
        # License plate style
        "abc1234", "xyz1234", "aaa1111", "bbb2222",
        "abc12345", "abc123456",
        
        # Simple patterns
        "abcd1234", "abcd12345", "xyz12345",
        "qwerty1!", "qwerty2@", "qwerty3#",
        "asdf1!", "asdf2@", "asdf3#",
        "zxcv1!", "zxcv2@", "zxcv3#",
        
        # Common PINs extended
        "0000", "1111", "2222", "3333", "4444",
        "5555", "6666", "7777", "8888", "9999",
        "1230", "1231", "1232", "1233", "1235",
        "1236", "1237", "1238", "1239",
        "00000", "11111", "22222", "33333", "44444",
        "55555", "66666", "77777", "88888", "99999",
        "12340", "12341", "12342", "12343", "12344",
        "12345", "12346", "12347", "12348", "12349",
        
        # Extended sequences
        "abcdef", "abcdefg", "abcdefgh", "abcdefghi",
        "zyxwv", "zyxwvu", "zyxwvuts", "zyxwvutsr",
        "aaaa1111", "bbbb2222", "cccc3333", "dddd4444",
        
        # Work related
        "office1", "office123", "work123", "business1",
        "company1", "company123", "corp123", "inc123",
        "ltd123", "llc123", "corp1", "inc1",
        
        # Family related
        "family1", "family123", "mom123", "dad123",
        "sister1", "brother1", "child123", "kids123",
        "home123", "house123", "apartment1",
        
        # Love/Romance
        "love123", "loveme", "loveme1", "loveme123",
        "sweetheart", "honey123", "baby123", "darling",
        "beautiful", "beautiful1", "sexy123", "hot123",
        
        # Money related
        "money1", "money123", "cash123", "dollar1",
        "rich123", "wealth", "gold123", "silver1",
        "bank123", "credit", "credit123", "visa123",
        
        # Food related
        "pizza1", "pizza123", "burger1", "burger123",
        "chicken1", "steak123", "food123", "eat123",
        "coffee1", "coffee123", "beer123", "wine123",
        
        # Sports
        "soccer1", "soccer123", "football1", "basketball",
        "baseball1", "tennis123", "golf123", "hockey1",
        "nfl123", "nba123", "mlb123", "nhl123",
        
        # Car brands
        "ford123", "chevy123", "toyota1", "honda123",
        "bmw123", "audi123", "mercedes1", "volvo123",
        "jeep123", "dodge123", "gmc123", "tesla1",
        
        # Technology
        "computer1", "laptop123", "phone123", "mobile1",
        "tech123", "gadget1", "device123", "pc123",
        "mac123", "windows1", "linux123", "android1",
        
        # Social media
        "facebook1", "twitter1", "instagram1", "snapchat1",
        "youtube1", "tiktok123", "reddit123", "linkedin1",
        
        # Extended keyboard walks
        "1qaz2wsx3edc4rfv", "1qaz2wsx3edc4rfv5tgb",
        "zaq12wsxcde3", "zaq12wsxcde34rfv",
        "qazwsxedcrfvtgbyhnujm", "qazwsxedcrfvtgbyhnujmikolp",
        
        # Palindromes
        "abcba", "abccba", "abcdcba", "abcddcba",
        "12321", "123321", "1234321", "12344321",
        
        # Repeating patterns
        "ababab", "abababab", "cdcdcd", "cdcdcdcd",
        "xyxyxy", "xyxyxyxy", "rfrfrf", "rfrfrfrf",
        
        # Common misspellings
        "pasword", "pasword1", "pasword123",
        "passward", "passward1", "passward123",
        "passsword", "passsword1", "passsword123",
        "passwordd", "passwordd1", "passwordd123",
        
        # Famous people/characters
        "superman1", "batman1", "spiderman1", "ironman1",
        "thor123", "hulk123", "wonderwoman", "flash123",
        "supergirl", "batgirl1", "robin123", "joker123",
        
        # More date patterns
        "01012024", "02022024", "03032024", "04042024",
        "05052024", "06062024", "07072024", "08082024",
        "09092024", "10102024", "11112024", "12122024",
        
        # Birth years common
        "1980", "1981", "1982", "1983", "1984", "1985",
        "1986", "1987", "1988", "1989", "1990", "1991",
        "1992", "1993", "1994", "1995", "1996", "1997",
        "1998", "1999", "2000", "2001", "2002", "2003",
        "2004", "2005", "2006", "2007", "2008", "2009",
        "2010", "2011", "2012", "2013", "2014", "2015",
        "2016", "2017", "2018", "2019", "2020", "2021",
        "2022", "2023", "2024", "2025",
    ]

# ==================== DATABASE MANAGER ====================
class DatabaseManager:
    """Manages password history database"""
    
    def __init__(self):
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database"""
        try:
            self.conn = sqlite3.connect(Config.DB_FILE, check_same_thread=False)
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS password_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    password_preview TEXT NOT NULL,
                    strength TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    breach_status TEXT NOT NULL,
                    entropy REAL NOT NULL,
                    crack_time TEXT NOT NULL
                )
            ''')
            self.conn.commit()
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    def add_entry(self, password_preview, strength, score, breach_status, entropy, crack_time):
        """Add new history entry"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO password_history 
                (timestamp, password_preview, strength, score, breach_status, entropy, crack_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                  password_preview, strength, score, breach_status, entropy, crack_time))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding entry: {e}")
            return False
    
    def update_breach_status(self, entry_id, breach_status):
        """Update breach status for an entry"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE password_history 
                SET breach_status = ?
                WHERE id = ?
            ''', (breach_status, entry_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating breach status: {e}")
            return False
    
    def get_last_entry_id(self):
        """Get the ID of the most recent entry"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id FROM password_history ORDER BY id DESC LIMIT 1')
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting last entry: {e}")
            return None
    
    def get_history(self, limit=50):
        """Retrieve history entries"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT timestamp, password_preview, strength, score, breach_status, entropy, crack_time
                FROM password_history ORDER BY id DESC LIMIT ?
            ''', (limit,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving history: {e}")
            return []
    
    def clear_history(self):
        """Clear all history"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM password_history')
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

# ==================== ENHANCED ANIMATION ENGINE ====================
class AnimationEngine:
    """Handles smooth animations for UI elements"""
    
    def __init__(self, root):
        self.root = root
        self.animations = {}
        self.running = True
        self._after_ids = []
        
    def animate_progress(self, canvas, target_value, duration=800):
        """Smooth progress bar animation"""
        current = getattr(canvas, 'current_value', 0)
        steps = 30
        increment = (target_value - current) / steps
        delay = duration // steps
        
        def step(count=0):
            if count >= steps or not self.running:
                canvas.current_value = target_value
                return
            
            new_val = current + (increment * (count + 1))
            canvas.current_value = new_val
            self._draw_progress(canvas, new_val)
            after_id = self.root.after(delay, lambda: step(count + 1))
            self._after_ids.append(after_id)
        
        step()
    
    def _draw_progress(self, canvas, value):
        """Draw animated progress arc"""
        canvas.delete("progress")
        width = 400
        height = 20
        x1, y1 = 50, 10
        x2, y2 = x1 + width, y1 + height
        
        # Background bar
        canvas.create_rectangle(x1, y1, x2, y2, 
                               fill="#2a2a2a", outline="", tags="bg")
        
        # Progress bar with gradient effect
        fill_width = (value / 100) * width
        color = self._get_strength_color(value)
        
        # Main bar
        canvas.create_rectangle(x1, y1, x1 + fill_width, y2,
                               fill=color, outline="", tags="progress")
        
        # Glow effect
        if fill_width > 20:
            canvas.create_rectangle(x1 + fill_width - 20, y1, x1 + fill_width, y2,
                                   fill=color, stipple="gray50", tags="progress")
        
        # Percentage text
        canvas.create_text(x2 + 30, y1 + height//2, text=f"{int(value)}%",
                          fill=Config.TEXT_COLOR, font=(Config.FONT_FAMILY, 11, "bold"),
                          tags="progress")
    
    def _get_strength_color(self, value):
        """Get color based on strength percentage"""
        if value < 20:
            return Config.DANGER_COLOR
        elif value < 40:
            return "#ff6b6b"
        elif value < 60:
            return Config.WARNING_COLOR
        elif value < 80:
            return "#ffdd00"
        else:
            return Config.SUCCESS_COLOR
    
    def pulse_animation(self, widget, color1, color2, duration=1000, times=3):
        """Create pulsing glow effect with limited repetitions"""
        count = [0]
        
        def pulse():
            if not self.running or count[0] >= times * 2:
                try:
                    widget.config(bg=color1)
                except:
                    pass
                return
            
            try:
                current = widget.cget("bg")
                new_color = color2 if current == color1 else color1
                widget.config(bg=new_color)
                count[0] += 1
                after_id = self.root.after(duration // 2, pulse)
                self._after_ids.append(after_id)
            except:
                pass
        
        pulse()
    
    def shake_widget(self, widget, intensity=5, duration=300):
        """Shake animation for weak passwords - FIXED: Uses place with remembered position"""
        try:
            # Get current position
            info = widget.place_info()
            original_x = int(info.get('x', 0))
            original_y = int(info.get('y', 0))
            
            # If not placed, use pack/grid info or skip
            if not info:
                return
                
            steps = 10
            delay = duration // steps
            
            def shake_step(step=0):
                if step >= steps:
                    widget.place(x=original_x, y=original_y)
                    return
                
                offset_x = random.randint(-intensity, intensity) * (steps - step) // steps
                offset_y = random.randint(-intensity//2, intensity//2) * (steps - step) // steps
                widget.place(x=original_x + offset_x, y=original_y + offset_y)
                after_id = self.root.after(delay, lambda: shake_step(step + 1))
                self._after_ids.append(after_id)
            
            shake_step()
        except Exception as e:
            print(f"Shake animation error: {e}")
    
    def fade_in(self, widget, duration=500, steps=20):
        """Fade in animation for widgets"""
        try:
            # Store original colors
            if not hasattr(widget, '_original_bg'):
                widget._original_bg = widget.cget("bg")
            
            delay = duration // steps
            
            def fade_step(step=0):
                if step >= steps or not self.running:
                    try:
                        widget.config(bg=widget._original_bg)
                    except:
                        pass
                    return
                
                # Calculate alpha
                alpha = step / steps
                
                # Interpolate color
                original = widget._original_bg
                if original.startswith('#'):
                    r = int(int(original[1:3], 16) * alpha)
                    g = int(int(original[3:5], 16) * alpha)
                    b = int(int(original[5:7], 16) * alpha)
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    try:
                        widget.config(bg=color)
                    except:
                        pass
                
                after_id = self.root.after(delay, lambda: fade_step(step + 1))
                self._after_ids.append(after_id)
            
            # Start from black
            try:
                widget.config(bg="#000000")
            except:
                pass
            fade_step()
        except Exception as e:
            print(f"Fade in error: {e}")
    
    def slide_in(self, widget, direction='left', distance=50, duration=400):
        """Slide in animation"""
        try:
            info = widget.place_info()
            if not info:
                return
                
            original_x = int(info.get('x', 0))
            original_y = int(info.get('y', 0))
            
            start_x = original_x - distance if direction == 'left' else original_x + distance
            start_y = original_y
            
            steps = 20
            delay = duration // steps
            
            # Start position
            widget.place(x=start_x, y=start_y)
            
            def slide_step(step=0):
                if step >= steps or not self.running:
                    widget.place(x=original_x, y=original_y)
                    return
                
                progress = step / steps
                # Easing function (ease-out)
                ease = 1 - (1 - progress) ** 2
                current_x = start_x + (original_x - start_x) * ease
                
                widget.place(x=int(current_x), y=original_y)
                after_id = self.root.after(delay, lambda: slide_step(step + 1))
                self._after_ids.append(after_id)
            
            slide_step()
        except Exception as e:
            print(f"Slide in error: {e}")
    
    def typing_effect(self, text_widget, text, delay=30):
        """Type text with typing animation"""
        try:
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            
            def type_char(index=0):
                if index >= len(text) or not self.running:
                    text_widget.config(state=tk.DISABLED)
                    return
                
                text_widget.insert(tk.END, text[index])
                after_id = self.root.after(delay, lambda: type_char(index + 1))
                self._after_ids.append(after_id)
            
            type_char()
        except Exception as e:
            print(f"Typing effect error: {e}")
    
    def bounce_effect(self, widget, duration=500):
        """Bounce animation for buttons"""
        try:
            info = widget.place_info()
            if not info:
                # Try to get pack info
                try:
                    widget_info = widget.pack_info()
                    original_y = 0  # Relative packing
                except:
                    return
            else:
                original_y = int(info.get('y', 0))
            
            steps = 20
            delay = duration // steps
            
            def bounce_step(step=0):
                if step >= steps or not self.running:
                    if info:
                        widget.place(y=original_y)
                    return
                
                # Bounce curve
                progress = step / steps
                bounce = math.sin(progress * math.pi) * 10
                if info:
                    widget.place(y=original_y - int(bounce))
                
                after_id = self.root.after(delay, lambda: bounce_step(step + 1))
                self._after_ids.append(after_id)
            
            bounce_step()
        except Exception as e:
            print(f"Bounce effect error: {e}")
    
    def loading_spinner(self, canvas, duration=2000):
        """Create a loading spinner animation"""
        try:
            canvas.delete("spinner")
            cx, cy = 25, 25
            radius = 20
            
            def draw_spinner(angle=0):
                if angle >= 360 or not self.running:
                    canvas.delete("spinner")
                    return
                
                canvas.delete("spinner")
                # Draw arc
                canvas.create_arc(cx-radius, cy-radius, cx+radius, cy+radius,
                                 start=angle, extent=60, fill=Config.ACCENT_COLOR,
                                 outline="", tags="spinner")
                
                after_id = self.root.after(50, lambda: draw_spinner(angle + 30))
                self._after_ids.append(after_id)
            
            draw_spinner()
        except Exception as e:
            print(f"Spinner error: {e}")
    
    def color_transition(self, widget, from_color, to_color, duration=500):
        """Smooth color transition"""
        try:
            steps = 20
            delay = duration // steps
            
            # Parse colors
            def hex_to_rgb(hex_color):
                hex_color = hex_color.lstrip('#')
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            def rgb_to_hex(rgb):
                return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
            
            from_rgb = hex_to_rgb(from_color)
            to_rgb = hex_to_rgb(to_color)
            
            def transition_step(step=0):
                if step >= steps or not self.running:
                    widget.config(fg=to_color)
                    return
                
                progress = step / steps
                current_rgb = tuple(
                    int(from_rgb[i] + (to_rgb[i] - from_rgb[i]) * progress)
                    for i in range(3)
                )
                color = rgb_to_hex(current_rgb)
                widget.config(fg=color)
                
                after_id = self.root.after(delay, lambda: transition_step(step + 1))
                self._after_ids.append(after_id)
            
            transition_step()
        except Exception as e:
            print(f"Color transition error: {e}")
    
    def stop(self):
        """Stop all animations and clean up"""
        self.running = False
        for after_id in self._after_ids:
            try:
                self.root.after_cancel(after_id)
            except:
                pass
        self._after_ids.clear()

# ==================== PASSWORD ANALYZER ====================
class PasswordAnalyzer:
    """Advanced password security analysis"""
    
    def __init__(self):
        self.common_passwords = set(Config.COMMON_PASSWORDS)
        self.common_passwords_lower = set(p.lower() for p in Config.COMMON_PASSWORDS)
        self.sequences = ['123', '234', '345', '456', '567', '678', '789', '890',
                         'abc', 'bcd', 'cde', 'def', 'efg', 'fgh', 'ghi', 'hij',
                         'ijk', 'jkl', 'klm', 'lmn', 'mno', 'nop', 'opq', 'pqr',
                         'qrs', 'rst', 'stu', 'tuv', 'uvw', 'vwx', 'wxy', 'xyz',
                         'qwerty', 'asdf', 'zxcv', '!@#', '@#$', '$$$', '%%%']
        
    def analyze(self, password):
        """Complete password analysis"""
        if not password:
            return None
            
        try:
            analysis = {
                'length': len(password),
                'entropy': self.calculate_entropy(password),
                'crack_time': self.estimate_crack_time(password),
                'patterns': self.find_patterns(password),
                'common_check': self.check_common(password),
                'char_types': self.analyze_characters(password),
                'score': 0,
                'strength': 'Very Weak',
                'recommendations': []
            }
            
            # Calculate score
            analysis['score'] = self.calculate_score(analysis)
            analysis['strength'] = self.get_strength_label(analysis['score'])
            analysis['recommendations'] = self.generate_recommendations(analysis, password)
            
            return analysis
        except Exception as e:
            print(f"Analysis error: {e}")
            return None
    
    def calculate_entropy(self, password):
        """Calculate Shannon entropy"""
        if not password:
            return 0
        
        try:
            entropy = 0
            length = len(password)
            freq = Counter(password)
            
            for count in freq.values():
                p = count / length
                entropy -= p * math.log2(p)
            
            return round(entropy * length, 2)
        except:
            return 0
    
    def estimate_crack_time(self, password):
        """Estimate time to crack password"""
        if not password:
            return "Instant"
        
        try:
            # Calculate pool size
            pool = 0
            if re.search(r'[a-z]', password): pool += 26
            if re.search(r'[A-Z]', password): pool += 26
            if re.search(r'\d', password): pool += 10
            if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password): pool += 32
            
            if pool == 0:
                return "Instant"
            
            combinations = pool ** len(password)
            
            # Assume 10 billion guesses per second (distributed attack)
            guesses_per_second = 10_000_000_000
            seconds = combinations / guesses_per_second
            
            # Format time
            if seconds < 1:
                return "Instant"
            elif seconds < 60:
                return f"{seconds:.2f} seconds"
            elif seconds < 3600:
                return f"{seconds/60:.2f} minutes"
            elif seconds < 86400:
                return f"{seconds/3600:.2f} hours"
            elif seconds < 31536000:
                return f"{seconds/86400:.2f} days"
            elif seconds < 3153600000:
                return f"{seconds/31536000:.2f} years"
            elif seconds < 315360000000:
                return f"{seconds/3153600000:.2f} centuries"
            else:
                return "Millennia"
        except:
            return "Unknown"
    
    def find_patterns(self, password):
        """Find problematic patterns"""
        patterns = []
        if not password:
            return patterns
            
        try:
            lower_pass = password.lower()
            
            # Check sequences
            for seq in self.sequences:
                if seq in lower_pass:
                    patterns.append(f"Sequence: '{seq}'")
            
            # Check repeated characters
            if re.search(r'(.)\1{2,}', password):
                patterns.append("Repeated characters")
            
            # Check keyboard patterns
            keyboard_patterns = ['qwerty', 'asdf', 'zxcv', 'qaz', 'wsx', 'edc']
            for pat in keyboard_patterns:
                if pat in lower_pass:
                    patterns.append(f"Keyboard pattern: '{pat}'")
            
            # Check dates
            if re.search(r'(19|20)\d{2}', password):
                patterns.append("Year pattern detected")
                
            # Check phone patterns
            if re.search(r'\d{3}[-.]?\d{3}[-.]?\d{4}', password):
                patterns.append("Phone number pattern")
                
            # Check email-like patterns
            if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', password):
                patterns.append("Email-like pattern")
                
        except:
            pass
        
        return patterns
    
    def check_common(self, password):
        """Check against common passwords - ENHANCED with more checks"""
        if not password:
            return None
            
        try:
            lower = password.lower()
            
            # Exact match
            if lower in self.common_passwords_lower:
                return "Exact match in common passwords!"
            
            # Partial match
            for common in self.common_passwords_lower:
                if common in lower or lower in common:
                    if len(common) > 4:
                        return f"Similar to common password: '{common}'"
            
            # Leet speak variations
            leet_map = {'@': 'a', '4': 'a', '3': 'e', '1': 'i', '!': 'i', 
                       '0': 'o', '5': 's', '$': 's', '7': 't', '+': 't',
                       '2': 'z', '(': 'c', ')': 'd', '?': 'q', '8': 'b',
                       '9': 'g', '6': 'g', '1': 'l', '|': 'l', '3': 'b'}
            normalized = lower
            for char, replacement in leet_map.items():
                normalized = normalized.replace(char, replacement)
            
            if normalized in self.common_passwords_lower:
                return f"Leet-speak variation of: '{normalized}'"
                
            # Check for reversed common passwords
            reversed_pass = lower[::-1]
            if reversed_pass in self.common_passwords_lower:
                return f"Reversed common password detected"
                
            # Check for doubled common passwords
            for common in self.common_passwords_lower:
                if len(common) >= 4 and common + common in lower:
                    return f"Doubled pattern detected: '{common}'"
                    
        except:
            pass
        
        return None
    
    def analyze_characters(self, password):
        """Analyze character composition"""
        if not password:
            return {'lowercase': 0, 'uppercase': 0, 'digits': 0, 'special': 0, 'unique': 0}
            
        try:
            return {
                'lowercase': len(re.findall(r'[a-z]', password)),
                'uppercase': len(re.findall(r'[A-Z]', password)),
                'digits': len(re.findall(r'\d', password)),
                'special': len(re.findall(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password)),
                'unique': len(set(password))
            }
        except:
            return {'lowercase': 0, 'uppercase': 0, 'digits': 0, 'special': 0, 'unique': 0}
    
    def calculate_score(self, analysis):
        """Calculate overall strength score (0-100)"""
        try:
            score = 0
            chars = analysis['char_types']
            length = analysis['length']
            
            # Length scoring (max 30)
            if length >= 20: score += 30
            elif length >= 16: score += 28
            elif length >= 14: score += 25
            elif length >= 12: score += 22
            elif length >= 10: score += 18
            elif length >= 8: score += 12
            else: score += max(0, length)
            
            # Character variety (max 40)
            variety = sum(1 for v in [chars['lowercase'], chars['uppercase'], 
                                      chars['digits'], chars['special']] if v > 0)
            score += variety * 10
            
            # Entropy bonus (max 20)
            entropy = analysis['entropy']
            if entropy > 100: score += 20
            elif entropy > 80: score += 18
            elif entropy > 60: score += 14
            elif entropy > 40: score += 10
            elif entropy > 20: score += 5
            
            # Pattern penalties
            if analysis['patterns']:
                score -= min(25, len(analysis['patterns']) * 5)
            if analysis['common_check']:
                score -= 30
            
            # Unique character bonus
            unique_ratio = chars['unique'] / max(length, 1)
            score += int(unique_ratio * 10)
            
            return max(0, min(100, score))
        except:
            return 0
    
    def get_strength_label(self, score):
        """Get strength label from score"""
        if score >= 90: return "Excellent"
        elif score >= 80: return "Very Strong"
        elif score >= 65: return "Strong"
        elif score >= 50: return "Medium"
        elif score >= 30: return "Weak"
        else: return "Very Weak"
    
    def generate_recommendations(self, analysis, password):
        """Generate improvement recommendations"""
        recs = []
        try:
            chars = analysis['char_types']
            
            if analysis['length'] < 12:
                recs.append("Use at least 12 characters")
            elif analysis['length'] < 16:
                recs.append("Consider using 16+ characters for maximum security")
                
            if chars['uppercase'] == 0:
                recs.append("Add uppercase letters")
            if chars['lowercase'] == 0:
                recs.append("Add lowercase letters")
            if chars['digits'] == 0:
                recs.append("Add numbers")
            if chars['special'] == 0:
                recs.append("Add special characters (!@#$%)")
            if analysis['patterns']:
                recs.append("Avoid predictable patterns")
            if analysis['common_check']:
                recs.append("Avoid common passwords and dictionary words")
            if chars['unique'] < len(password) * 0.5:
                recs.append("Use more unique characters")
                
            # Additional recommendations
            if len(password) > 0 and password[0].isdigit():
                recs.append("Avoid starting with a number")
            if len(password) > 0 and password[-1].isdigit():
                recs.append("Avoid ending with a number")
            if re.search(r'(.)\1{3,}', password):
                recs.append("Avoid 4+ repeated characters")
                
        except:
            pass
        
        return recs

# ==================== BREACH DETECTOR ====================
class BreachDetector:
    """Have I Been Pwned API integration using k-Anonymity"""
    
    def __init__(self):
        self.api_url = Config.HIBP_API_URL
        self.timeout = 10
    
    def check_breach(self, password, callback):
        """Check password against HIBP database using k-Anonymity"""
        if not password:
            callback("Not checked", 0)
            return
        
        def check():
            try:
                # Generate SHA-1 hash of password
                sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
                prefix = sha1_hash[:5]
                suffix = sha1_hash[5:]
                
                # Make API request (only sending prefix - k-Anonymity)
                response = requests.get(
                    f"{self.api_url}{prefix}",
                    timeout=self.timeout,
                    headers={"User-Agent": "PasswordStrengthAnalyzer-Pro"}
                )
                
                if response.status_code == 200:
                    # Parse response to find matching suffix
                    hashes = response.text.splitlines()
                    for line in hashes:
                        if ':' in line:
                            hash_suffix, count = line.split(':')
                            if hash_suffix == suffix:
                                callback(f"Found in Data Breaches", int(count))
                                return
                    callback("Not Found in Known Data Breaches", 0)
                else:
                    callback("API Error", -1)
            except requests.exceptions.Timeout:
                callback("Timeout - Check Failed", -1)
            except requests.exceptions.ConnectionError:
                callback("No Internet Connection", -1)
            except Exception as e:
                callback(f"Error: {str(e)[:30]}", -1)
        
        # Run in background thread
        thread = threading.Thread(target=check, daemon=True)
        thread.start()

# ==================== MAIN APPLICATION ====================
class PasswordStrengthChecker:
    """Main application class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔐 Password Strength Analyzer Pro - Enhanced Edition")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.configure(bg=Config.BG_COLOR)
        self.root.minsize(1000, 750)
        
        # Initialize components
        self.animator = AnimationEngine(self.root)
        self.analyzer = PasswordAnalyzer()
        self.breach_detector = BreachDetector()
        self.db = DatabaseManager()
        
        # State
        self.current_analysis = None
        self.breach_count = 0
        self.breach_status = "Not checked"
        self.show_password = False
        self.is_analyzing = False
        self.last_entry_id = None
        
        self.setup_styles()
        self.create_widgets()
        self.center_window()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Bind character count update
        self.password_var.trace('w', self.on_password_change)
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Card.TFrame", background=Config.CARD_BG)
        style.configure("Title.TLabel", 
                      background=Config.BG_COLOR,
                      foreground=Config.ACCENT_COLOR,
                      font=(Config.FONT_FAMILY, 24, "bold"))
        
    def create_widgets(self):
        """Create all UI widgets - FIXED: Consistent sizing to prevent layout shifts"""
        # Main container with horizontal layout
        main_container = tk.Frame(self.root, bg=Config.BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (main content)
        left_panel = tk.Frame(main_container, bg=Config.BG_COLOR)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Right panel (history sidebar)
        right_panel = tk.Frame(main_container, bg=Config.CARD_BG, width=320)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20), pady=20)
        right_panel.pack_propagate(False)
        
        # Header
        self.create_header(left_panel)
        
        # Input section
        self.create_input_section(left_panel)
        
        # Strength meter - FIXED: Fixed height to prevent shifting
        self.create_strength_meter(left_panel)
        
        # Results cards - FIXED: Fixed heights to prevent shifting
        self.create_results_section(left_panel)
        
        # Breach status
        self.create_breach_section(left_panel)
        
        # Status bar
        self.create_status_bar(left_panel)
        
        # History panel
        self.create_history_panel(right_panel)
        
    def create_header(self, parent):
        """Create application header"""
        header = tk.Frame(parent, bg=Config.BG_COLOR)
        header.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(header, 
                        text="🔐 PASSWORD STRENGTH ANALYZER PRO",
                        bg=Config.BG_COLOR,
                        fg=Config.ACCENT_COLOR,
                        font=(Config.FONT_FAMILY, 26, "bold"))
        title.pack()
        
        subtitle = tk.Label(header,
                           text="Advanced Cyber Security Tool with 1000+ Weak Password Detection",
                           bg=Config.BG_COLOR,
                           fg=Config.SECONDARY_TEXT,
                           font=(Config.FONT_FAMILY, 12))
        subtitle.pack(pady=(5, 0))
        
        # Animated underline
        underline = tk.Canvas(header, height=3, bg=Config.BG_COLOR, 
                             highlightthickness=0)
        underline.pack(fill=tk.X, pady=10)
        underline.create_line(0, 1, 800, 1, fill=Config.ACCENT_COLOR, width=2)
        
    def create_input_section(self, parent):
        """Create password input section"""
        card = tk.Frame(parent, bg=Config.CARD_BG, padx=20, pady=20)
        card.pack(fill=tk.X, pady=10)
        card.configure(highlightbackground=Config.ACCENT_COLOR, 
                      highlightthickness=1)
        
        # Label
        tk.Label(card, text="Enter Password to Analyze",
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR,
                font=(Config.FONT_FAMILY, 14, "bold")).pack(anchor=tk.W)
        
        # Input frame
        input_frame = tk.Frame(card, bg=Config.CARD_BG)
        input_frame.pack(fill=tk.X, pady=15)
        
        # Password entry with custom styling
        self.password_var = tk.StringVar()
        
        self.entry_frame = tk.Frame(input_frame, bg="#2a2a2a", padx=2, pady=2)
        self.entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.password_entry = tk.Entry(self.entry_frame,
                                      textvariable=self.password_var,
                                      show="●",
                                      bg="#1a1a1a",
                                      fg=Config.TEXT_COLOR,
                                      font=(Config.FONT_FAMILY, 16),
                                      relief=tk.FLAT,
                                      insertbackground=Config.ACCENT_COLOR)
        self.password_entry.pack(fill=tk.X, ipady=12, padx=10)
        self.password_entry.bind('<Return>', lambda e: self.analyze_password())
        
        # Toggle visibility button
        self.toggle_btn = tk.Button(input_frame, text="👁",
                                   bg=Config.CARD_BG,
                                   fg=Config.SECONDARY_TEXT,
                                   font=(Config.FONT_FAMILY, 14),
                                   relief=tk.FLAT,
                                   command=self.toggle_visibility,
                                   cursor="hand2")
        self.toggle_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Analyze button
        self.analyze_btn = tk.Button(input_frame, text="ANALYZE",
                                    bg=Config.ACCENT_COLOR,
                                    fg=Config.BG_COLOR,
                                    font=(Config.FONT_FAMILY, 12, "bold"),
                                    relief=tk.FLAT,
                                    command=self.analyze_password,
                                    cursor="hand2",
                                    padx=20)
        self.analyze_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Validation message label
        self.validation_label = tk.Label(card, text="",
                                        bg=Config.CARD_BG,
                                        fg=Config.DANGER_COLOR,
                                        font=(Config.FONT_FAMILY, 11))
        self.validation_label.pack(anchor=tk.W)
        
        # Character count
        self.char_count = tk.Label(card, text="0 characters",
                                  bg=Config.CARD_BG,
                                  fg=Config.SECONDARY_TEXT,
                                  font=(Config.FONT_FAMILY, 10))
        self.char_count.pack(anchor=tk.E)
        
    def create_strength_meter(self, parent):
        """Create animated strength meter - FIXED: Fixed height"""
        card = tk.Frame(parent, bg=Config.CARD_BG, padx=20, pady=20, height=120)
        card.pack(fill=tk.X, pady=10)
        card.pack_propagate(False)  # FIXED: Prevent resizing
        
        # Strength label
        self.strength_label = tk.Label(card, text="Strength: Not Analyzed",
                                      bg=Config.CARD_BG,
                                      fg=Config.SECONDARY_TEXT,
                                      font=(Config.FONT_FAMILY, 16, "bold"))
        self.strength_label.pack(anchor=tk.W)
        
        # Progress canvas
        self.progress_canvas = tk.Canvas(card, height=40, bg=Config.CARD_BG,
                                         highlightthickness=0)
        self.progress_canvas.pack(fill=tk.X, pady=15)
        self.progress_canvas.current_value = 0
        
        # Score display
        self.score_frame = tk.Frame(card, bg=Config.CARD_BG)
        self.score_frame.pack(fill=tk.X)
        
        self.score_label = tk.Label(self.score_frame, text="Score: 0/100",
                                   bg=Config.CARD_BG,
                                   fg=Config.SECONDARY_TEXT,
                                   font=(Config.FONT_FAMILY, 14))
        self.score_label.pack(side=tk.LEFT)
        
        self.entropy_label = tk.Label(self.score_frame, text="Entropy: 0 bits",
                                     bg=Config.CARD_BG,
                                     fg=Config.SECONDARY_TEXT,
                                     font=(Config.FONT_FAMILY, 14))
        self.entropy_label.pack(side=tk.RIGHT)
        
    def create_results_section(self, parent):
        """Create detailed results cards - FIXED: Fixed heights to prevent shifting"""
        results_frame = tk.Frame(parent, bg=Config.BG_COLOR)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left column - Character Analysis
        left_card = tk.Frame(results_frame, bg=Config.CARD_BG, padx=15, pady=15, height=200)
        left_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        left_card.pack_propagate(False)  # FIXED: Fixed height
        
        tk.Label(left_card, text="📊 Character Analysis",
                bg=Config.CARD_BG, fg=Config.ACCENT_COLOR,
                font=(Config.FONT_FAMILY, 13, "bold")).pack(anchor=tk.W)
        
        # FIXED: Use Text widget with fixed height and wrap
        self.char_analysis = tk.Text(left_card, bg=Config.CARD_BG,
                                     fg=Config.TEXT_COLOR,
                                     font=(Config.FONT_FAMILY, 11),
                                     relief=tk.FLAT, height=8, width=35,
                                     wrap=tk.WORD,  # FIXED: Word wrap
                                     padx=5, pady=5)
        self.char_analysis.pack(fill=tk.BOTH, expand=True, pady=10)
        self.char_analysis.insert(tk.END, "Enter a password to see analysis...")
        self.char_analysis.config(state=tk.DISABLED)
        
        # Right column - Security Info
        right_card = tk.Frame(results_frame, bg=Config.CARD_BG, padx=15, pady=15, height=200)
        right_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        right_card.pack_propagate(False)  # FIXED: Fixed height
        
        tk.Label(right_card, text="🔒 Security Assessment",
                bg=Config.CARD_BG, fg=Config.ACCENT_COLOR,
                font=(Config.FONT_FAMILY, 13, "bold")).pack(anchor=tk.W)
        
        # FIXED: Use Text widget with fixed height and wrap
        self.security_info = tk.Text(right_card, bg=Config.CARD_BG,
                                     fg=Config.TEXT_COLOR,
                                     font=(Config.FONT_FAMILY, 11),
                                     relief=tk.FLAT, height=8, width=35,
                                     wrap=tk.WORD,  # FIXED: Word wrap
                                     padx=5, pady=5)
        self.security_info.pack(fill=tk.BOTH, expand=True, pady=10)
        self.security_info.insert(tk.END, "Security details will appear here...")
        self.security_info.config(state=tk.DISABLED)
        
        # Bottom card - Recommendations - FIXED: Fixed height
        bottom_card = tk.Frame(parent, bg=Config.CARD_BG, padx=15, pady=15, height=100)
        bottom_card.pack(fill=tk.X, pady=10)
        bottom_card.pack_propagate(False)  # FIXED: Fixed height
        
        tk.Label(bottom_card, text="💡 Recommendations",
                bg=Config.CARD_BG, fg=Config.WARNING_COLOR,
                font=(Config.FONT_FAMILY, 13, "bold")).pack(anchor=tk.W)
        
        # FIXED: Use Text widget instead of Label for consistent height
        self.recommendations = tk.Text(bottom_card, 
                                       bg=Config.CARD_BG,
                                       fg=Config.SECONDARY_TEXT,
                                       font=(Config.FONT_FAMILY, 11),
                                       relief=tk.FLAT,
                                       height=3,
                                       wrap=tk.WORD,
                                       padx=5, pady=5)
        self.recommendations.pack(fill=tk.BOTH, expand=True)
        self.recommendations.insert(tk.END, "Enter a password and click ANALYZE to get recommendations...")
        self.recommendations.config(state=tk.DISABLED)
        
    def create_breach_section(self, parent):
        """Create breach detection section - FIXED: Fixed height"""
        card = tk.Frame(parent, bg=Config.CARD_BG, padx=15, pady=15, height=120)
        card.pack(fill=tk.X, pady=10)
        card.pack_propagate(False)  # FIXED: Fixed height
        
        tk.Label(card, text="🌐 Breach Detection (Have I Been Pwned)",
                bg=Config.CARD_BG, fg=Config.ACCENT_COLOR,
                font=(Config.FONT_FAMILY, 13, "bold")).pack(anchor=tk.W)
        
        # Loading spinner canvas
        self.breach_spinner = tk.Canvas(card, width=50, height=50, 
                                        bg=Config.CARD_BG, highlightthickness=0)
        self.breach_spinner.pack(side=tk.LEFT, padx=(0, 10))
        self.breach_spinner.pack_forget()  # Hide initially
        
        self.breach_label = tk.Label(card, 
                                    text="Not checked - Click ANALYZE to check against data breaches",
                                    bg=Config.CARD_BG,
                                    fg=Config.SECONDARY_TEXT,
                                    font=(Config.FONT_FAMILY, 11))
        self.breach_label.pack(anchor=tk.W, pady=10)
        
        self.breach_detail = tk.Label(card, 
                                     text="Uses k-Anonymity (SHA-1) - Your password is never sent to the API",
                                     bg=Config.CARD_BG,
                                     fg="#555555",
                                     font=(Config.FONT_FAMILY, 9))
        self.breach_detail.pack(anchor=tk.W)
        
    def create_history_panel(self, parent):
        """Create password history panel"""
        tk.Label(parent, text="📜 Analysis History",
                bg=Config.CARD_BG, fg=Config.ACCENT_COLOR,
                font=(Config.FONT_FAMILY, 14, "bold")).pack(pady=15)
        
        # History listbox with scrollbar
        list_frame = tk.Frame(parent, bg=Config.CARD_BG)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(list_frame,
                                          bg="#1a1a1a",
                                          fg=Config.TEXT_COLOR,
                                          font=(Config.FONT_FAMILY, 9),
                                          relief=tk.FLAT,
                                          yscrollcommand=scrollbar.set,
                                          selectmode=tk.SINGLE,
                                          height=20)  # FIXED: Fixed height
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Clear history button
        self.clear_btn = tk.Button(parent, text="Clear History",
                                  bg=Config.DANGER_COLOR,
                                  fg=Config.TEXT_COLOR,
                                  font=(Config.FONT_FAMILY, 10, "bold"),
                                  relief=tk.FLAT,
                                  command=self.clear_history,
                                  cursor="hand2")
        self.clear_btn.pack(pady=10)
        
        # Refresh history
        self.refresh_history()
        
    def create_status_bar(self, parent):
        """Create status bar"""
        status = tk.Frame(parent, bg=Config.BG_COLOR)
        status.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(status, 
                                    text="Ready | Enter a password to begin analysis",
                                    bg=Config.BG_COLOR,
                                    fg=Config.SECONDARY_TEXT,
                                    font=(Config.FONT_FAMILY, 10))
        self.status_label.pack(side=tk.LEFT)
        
        version = tk.Label(status, text="v4.0 Enhanced",
                          bg=Config.BG_COLOR,
                          fg=Config.ACCENT_COLOR,
                          font=(Config.FONT_FAMILY, 10))
        version.pack(side=tk.RIGHT)
        
    def on_password_change(self, *args):
        """Update character count when password changes"""
        password = self.password_var.get()
        self.char_count.config(text=f"{len(password)} characters")
        
    def validate_password(self, password):
        """Validate password input"""
        # Clear previous validation message
        self.validation_label.config(text="")
        
        # Check if empty
        if not password:
            self.validation_label.config(text="Please enter your password.")
            return False
        
        # Check if only spaces
        if password.strip() == "":
            self.validation_label.config(text="Invalid password. Spaces only are not allowed.")
            return False
        
        return True
        
    def toggle_visibility(self):
        """Toggle password visibility"""
        self.show_password = not self.show_password
        self.password_entry.config(show="" if self.show_password else "●")
        self.toggle_btn.config(fg=Config.ACCENT_COLOR if self.show_password 
                              else Config.SECONDARY_TEXT)
        
    def analyze_password(self, event=None):
        """Analyze password and update UI - FIXED: Proper state management"""
        password = self.password_var.get()
        
        # Validate input
        if not self.validate_password(password):
            self.animator.shake_widget(self.entry_frame, intensity=5)
            return
        
        # Prevent multiple simultaneous analyses
        if self.is_analyzing:
            return
        
        self.is_analyzing = True
        self.analyze_btn.config(state=tk.DISABLED, text="Analyzing...")
        self.status_label.config(text="Analyzing password...")
        
        # Show loading spinner for breach check
        self.breach_spinner.pack(side=tk.LEFT, padx=(0, 10))
        self.animator.loading_spinner(self.breach_spinner)
        self.breach_label.config(text="Checking breach databases...", fg=Config.WARNING_COLOR)
        
        # Run analysis
        try:
            self.current_analysis = self.analyzer.analyze(password)
            
            if self.current_analysis is None:
                self.show_analysis_failed()
                return
            
            # Update display
            self.update_display()
            
            # Check breach status in background
            self.breach_status = "Checking..."
            
            def breach_callback(status, count):
                self.root.after(0, lambda: self.update_breach_status(status, count))
            
            self.breach_detector.check_breach(password, breach_callback)
            
            # Save to history (without breach status initially)
            self.save_to_history(password)
            
            # Animation for weak passwords
            if self.current_analysis['score'] < 50:
                self.animator.shake_widget(self.entry_frame, intensity=3)
                self.animator.pulse_animation(self.strength_label, Config.CARD_BG, 
                                             Config.DANGER_COLOR, duration=500, times=2)
            elif self.current_analysis['score'] >= 80:
                # Success animation
                self.animator.bounce_effect(self.analyze_btn)
                self.animator.pulse_animation(self.strength_label, Config.CARD_BG,
                                             Config.SUCCESS_COLOR, duration=500, times=2)
                
        except Exception as e:
            self.show_analysis_failed()
            self.status_label.config(text=f"Error: {str(e)[:40]}")
        finally:
            self.is_analyzing = False
            self.analyze_btn.config(state=tk.NORMAL, text="ANALYZE")
            
    def show_analysis_failed(self):
        """Display analysis failed message"""
        self.strength_label.config(text="Analysis Failed", fg=Config.DANGER_COLOR)
        self.score_label.config(text="Score: N/A")
        self.entropy_label.config(text="Entropy: N/A")
        self.breach_label.config(text="Analysis Failed - Unable to complete", fg=Config.DANGER_COLOR)
        self.status_label.config(text="Analysis failed. Please try again.")
        self.breach_spinner.pack_forget()
        
    def update_breach_status(self, status, count):
        """Update breach status display - FIXED: Update database too"""
        self.breach_status = status
        self.breach_count = count
        
        # Hide spinner
        self.breach_spinner.pack_forget()
        
        if count > 0:
            self.breach_label.config(
                text=f"⚠️ Found in Data Breaches ({count:,} occurrences)",
                fg=Config.DANGER_COLOR
            )
            # Animation for breach found
            self.animator.color_transition(self.breach_label, Config.SECONDARY_TEXT, Config.DANGER_COLOR)
        elif "Not Found" in status:
            self.breach_label.config(
                text="✓ Not Found in Known Data Breaches",
                fg=Config.SUCCESS_COLOR
            )
            self.animator.color_transition(self.breach_label, Config.SECONDARY_TEXT, Config.SUCCESS_COLOR)
        elif "Error" in status or "Timeout" in status or "Connection" in status:
            self.breach_label.config(
                text=f"⚠️ {status}",
                fg=Config.WARNING_COLOR
            )
        else:
            self.breach_label.config(
                text=f"Status: {status}",
                fg=Config.SECONDARY_TEXT
            )
        
        # Update history with breach status - FIXED
        if self.last_entry_id:
            self.db.update_breach_status(self.last_entry_id, status)
            self.refresh_history()
        
    def update_display(self):
        """Update all UI elements with analysis results - FIXED: No layout shifts"""
        if not self.current_analysis:
            self.show_analysis_failed()
            return
            
        analysis = self.current_analysis
        
        # Update strength label with color
        strength = analysis['strength']
        score = analysis['score']
        
        color = Config.DANGER_COLOR
        if score >= 90: color = Config.SUCCESS_COLOR
        elif score >= 80: color = "#00ccff"
        elif score >= 65: color = "#88ff00"
        elif score >= 50: color = Config.WARNING_COLOR
        
        self.strength_label.config(text=f"Strength: {strength}", fg=color)
        
        # Animate progress bar
        self.animator.animate_progress(self.progress_canvas, score)
        
        # Update score and entropy
        self.score_label.config(text=f"Score: {score}/100")
        self.entropy_label.config(text=f"Entropy: {analysis['entropy']} bits")
        
        # Update character analysis - FIXED: Use config instead of insert/delete for Text widget
        self.char_analysis.config(state=tk.NORMAL)
        self.char_analysis.delete(1.0, tk.END)
        
        chars = analysis['char_types']
        char_text = f"""Length: {analysis['length']}
Lowercase: {chars['lowercase']}
Uppercase: {chars['uppercase']}
Digits: {chars['digits']}
Special: {chars['special']}
Unique chars: {chars['unique']}
Variety score: {sum(1 for v in [chars['lowercase'], chars['uppercase'], chars['digits'], chars['special']] if v > 0)}/4"""
        self.char_analysis.insert(tk.END, char_text)
        self.char_analysis.config(state=tk.DISABLED)
        
        # Update security info - FIXED
        self.security_info.config(state=tk.NORMAL)
        self.security_info.delete(1.0, tk.END)
        
        security_text = f"""Estimated crack time:
{analysis['crack_time']}

"""
        if analysis['common_check']:
            security_text += f"⚠️ Warning:\n{analysis['common_check']}\n\n"
        
        if analysis['patterns']:
            security_text += "Detected patterns:\n"
            for pattern in analysis['patterns'][:5]:
                security_text += f"• {pattern}\n"
        
        self.security_info.insert(tk.END, security_text)
        self.security_info.config(state=tk.DISABLED)
        
        # Update recommendations - FIXED: Use Text widget
        self.recommendations.config(state=tk.NORMAL)
        self.recommendations.delete(1.0, tk.END)
        
        if analysis['recommendations']:
            rec_text = " • ".join(analysis['recommendations'])
            self.recommendations.insert(tk.END, rec_text)
            self.recommendations.config(fg=Config.WARNING_COLOR)
        else:
            self.recommendations.insert(tk.END, "✓ Excellent password! No improvements needed.")
            self.recommendations.config(fg=Config.SUCCESS_COLOR)
        
        self.recommendations.config(state=tk.DISABLED)
        
        # Update status
        self.status_label.config(text=f"Analysis complete | {datetime.now().strftime('%H:%M:%S')}")
        
    def save_to_history(self, password):
        """Save analysis to history - FIXED: Track entry ID for breach update"""
        if not self.current_analysis:
            return
            
        try:
            # Create password preview (first 3 chars + asterisks)
            preview = password[:3] + "*" * (len(password) - 3) if len(password) > 3 else "*" * len(password)
            
            self.db.add_entry(
                preview,
                self.current_analysis['strength'],
                self.current_analysis['score'],
                "Checking...",  # Initial status, will be updated
                self.current_analysis['entropy'],
                self.current_analysis['crack_time']
            )
            
            # Get the ID of the entry we just created
            self.last_entry_id = self.db.get_last_entry_id()
            
            # Refresh history display
            self.refresh_history()
        except Exception as e:
            print(f"Error saving to history: {e}")
            
    def refresh_history(self):
        """Refresh history display"""
        try:
            self.history_listbox.delete(0, tk.END)
            history = self.db.get_history(limit=20)
            
            for entry in history:
                timestamp, preview, strength, score, breach, entropy, crack_time = entry
                display_text = f"{timestamp} | {preview} | {strength} ({score}) | {breach[:20]}"
                self.history_listbox.insert(tk.END, display_text)
                
                # Color code based on score
                if score >= 80:
                    self.history_listbox.itemconfig(tk.END, {'fg': Config.SUCCESS_COLOR})
                elif score >= 50:
                    self.history_listbox.itemconfig(tk.END, {'fg': Config.WARNING_COLOR})
                else:
                    self.history_listbox.itemconfig(tk.END, {'fg': Config.DANGER_COLOR})
        except Exception as e:
            print(f"Error refreshing history: {e}")
            
    def clear_history(self):
        """Clear all history"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all history?"):
            if self.db.clear_history():
                self.refresh_history()
                messagebox.showinfo("Success", "History cleared successfully!")
            else:
                messagebox.showerror("Error", "Failed to clear history.")
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def on_close(self):
        """Handle window close - FIXED: Clean up animations"""
        self.animator.stop()
        self.db.close()
        self.root.destroy()
        
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Fatal Error", f"Application error: {e}")
            sys.exit(1)

# ==================== ENTRY POINT ====================
if __name__ == "__main__":
    try:
        app = PasswordStrengthChecker()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)