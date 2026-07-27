"""
Password Strength Analyzer Pro - Optimized Premium Edition
Window Size: 1100x700 | Professional UI with Glow Effects
Author: Enhanced Version
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
import math
import hashlib
import requests
import threading
import random
import sys
from datetime import datetime
from collections import Counter

# ==================== CONFIGURATION ====================
class Config:
    """Application configuration constants"""
    WINDOW_WIDTH = 1100
    WINDOW_HEIGHT = 700
    BG_COLOR = "#0a0a0a"
    CARD_BG = "#141414"
    CARD_BG_LIGHT = "#1a1a1a"
    ACCENT_COLOR = "#00d4ff"
    ACCENT_GLOW = "#00d4ff"
    SUCCESS_COLOR = "#00ff88"
    WARNING_COLOR = "#ffaa00"
    DANGER_COLOR = "#ff4757"
    TEXT_COLOR = "#ffffff"
    SECONDARY_TEXT = "#888888"
    FONT_FAMILY = "Segoe UI"
    
    # HIBP API endpoint
    HIBP_API_URL = "https://api.pwnedpasswords.com/range/"
    
    # Extended common passwords list
    COMMON_PASSWORDS = [
        "123456", "password", "12345678", "qwerty", "123456789",
        "12345", "1234", "111111", "1234567", "dragon",
        "123123", "baseball", "abc123", "football", "monkey",
        "letmein", "696969", "shadow", "master", "666666",
        "qwertyuiop", "123321", "mustang", "1234567890", "michael",
        "654321", "superman", "1qaz2wsx", "7777777",
        "121212", "000000", "qazwsx", "123qwe",
        "killer", "trustno1", "jordan", "jennifer", "zxcvbnm",
        "asdfgh", "hunter", "buster", "soccer", "harley",
        "batman", "andrew", "tigger", "sunshine", "iloveyou",
        "2000", "charlie", "robert", "thomas",
        "hockey", "ranger", "daniel", "starwars",
        "112233", "george", "asshole", "computer", "michelle",
        "jessica", "pepper", "1111", "zxcvbn", "555555",
        "11111111", "131313", "freedom", "777777", "pass",
        "maggie", "159753", "aaaaaa", "ginger",
        "princess", "joshua", "cheese", "amanda", "summer",
        "love", "ashley", "nicole", "chelsea", "biteme",
        "matthew", "access", "yankees", "987654321", "dallas",
        "austin", "thunder", "taylor", "matrix", "minecraft",
        "welcome", "admin", "password1", "login", "solo",
        "admin123", "welcome123", "password123", "passw0rd",
        "secret", "default", "guest", "user", "test", "demo",
        "qwerty123", "azerty", "letmein1", "welcome1",
        "sunshine1", "princess1", "football1", "baseball1",
        "iloveyou1", "trustno1", "dragon1", "master1",
        "shadow1", "ashley1", "michael1", "jesus1", "mustang1",
        "access1", "love123", "pussy1", "6969691", "qwerty1",
        "zaq12wsx", "1qaz2wsx", "qwerty12", "password12",
        "password01", "password!", "password.", "password?",
        "p@ssw0rd", "p@ssword", "passw0rd", "pa$$word",
        "admin1", "admin12", "r00t", "h4ck3r", "1337",
        "letmein123", "iloveyou123", "welcome123", "monkey123",
        "dragon123", "master123", "shadow123", "sunshine123",
        "princess123", "football123", "baseball123", "iloveyou123",
        "trustno123", "jesus123", "mustang123", "access123",
        "love1234", "michael123", "ashley123", "jesus123",
        "password2024", "password2023", "password2022", "password2021",
        "admin2024", "admin2023", "admin2022", "admin2021",
        "user2024", "user2023", "login2024", "login2023",
        "welcome2024", "welcome2023", "letmein2024", "letmein2023",
        "qwerty2024", "qwerty2023", "abc123456", "123abc456",
        "password!", "password@", "password#", "password$",
        "password%", "password^", "password&", "password*",
        "password(", "password)", "password-", "password_",
        "password=", "password+", "password[", "password]",
        "password{", "password}", "password;", "password:",
        "password'", "password\"", "password,", "password.",
        "password/", "password<", "password>", "password?",
        "password`", "password~", "password\\", "password|",
        "P@ssw0rd", "P@ssword", "Passw0rd", "Pa$$word",
        "Admin123", "Admin1234", "Admin12345", "Administrator",
        "Login123", "User123", "Guest123", "Test123",
        "Root123", "Toor123", "Pass123", "Secret123",
        "Welcome1", "Welcome2", "Welcome01", "Welcome001",
        "Password0", "Password00", "Password000",
        "Qwerty123", "Qwerty1234", "Qwerty12345",
        "Abc123", "Abc1234", "Abc12345", "Abcdef123",
        "123Abc", "1234Abc", "12345Abc", "123456Abc",
        "Test1234", "Demo1234", "Temp1234", "Change123",
        "Changeme", "Changeme1", "Changeme123",
        "Fuck123", "Fuckyou1", "Fuckyou123", "Fuckoff",
        "Shit123", "Damn123", "Hell123", "Ass123",
        "Bitch1", "Bitch123", "Bastard", "Bastard1",
        "Google123", "Facebook1", "Amazon123", "Apple123",
        "Microsoft1", "Twitter123", "Instagram1", "Linkedin1",
        "Youtube123", "Netflix1", "Spotify1", "Uber123",
        "Hello123", "World123", "Home123", "Work123",
        "Office1", "School1", "College1", "University1",
        "Summer1", "Winter1", "Spring1", "Autumn1",
        "January1", "February1", "March1", "April1",
        "May123", "June123", "July123", "August1",
        "September1", "October1", "November1", "December1",
        "Monday1", "Tuesday1", "Wednesday1", "Thursday1",
        "Friday1", "Saturday1", "Sunday1", "Weekend1",
        "Morning1", "Afternoon1", "Evening1", "Night123",
        "Today123", "Tomorrow1", "Yesterday1", "Now123",
        "Red123", "Blue123", "Green123", "Yellow1",
        "Black123", "White123", "Purple1", "Orange1",
        "Pink123", "Gray123", "Brown123", "Gold123",
        "Silver1", "Bronze1", "Copper1", "Iron123",
        "Dog123", "Cat123", "Bird123", "Fish123",
        "Lion123", "Tiger123", "Bear123", "Wolf123",
        "Eagle123", "Snake123", "Monkey1", "Panda123",
        "Rabbit1", "Horse123", "Cow123", "Pig123",
        "Chicken1", "Duck123", "Goose1", "Sheep1",
        "Goat123", "Deer123", "Fox123", "Wolf123",
    ]

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
                         'qwerty', 'asdf', 'zxcv', '!@#', '@#$']
        
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
            pool = 0
            if re.search(r'[a-z]', password): pool += 26
            if re.search(r'[A-Z]', password): pool += 26
            if re.search(r'\d', password): pool += 10
            if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password): pool += 32
            
            if pool == 0:
                return "Instant"
            
            combinations = pool ** len(password)
            guesses_per_second = 10_000_000_000
            seconds = combinations / guesses_per_second
            
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
            
            for seq in self.sequences:
                if seq in lower_pass:
                    patterns.append(f"Sequence: '{seq}'")
            
            if re.search(r'(.)\1{2,}', password):
                patterns.append("Repeated characters")
            
            keyboard_patterns = ['qwerty', 'asdf', 'zxcv', 'qaz', 'wsx', 'edc']
            for pat in keyboard_patterns:
                if pat in lower_pass:
                    patterns.append(f"Keyboard pattern: '{pat}'")
            
            if re.search(r'(19|20)\d{2}', password):
                patterns.append("Year pattern detected")
                
            if re.search(r'\d{3}[-.]?\d{3}[-.]?\d{4}', password):
                patterns.append("Phone number pattern")
                
        except:
            pass
        
        return patterns
    
    def check_common(self, password):
        """Check against common passwords"""
        if not password:
            return None
            
        try:
            lower = password.lower()
            
            if lower in self.common_passwords_lower:
                return "Exact match in common passwords!"
            
            for common in self.common_passwords_lower:
                if common in lower or lower in common:
                    if len(common) > 4:
                        return f"Similar to common password: '{common}'"
            
            leet_map = {'@': 'a', '4': 'a', '3': 'e', '1': 'i', '!': 'i', 
                       '0': 'o', '5': 's', '$': 's', '7': 't', '+': 't'}
            normalized = lower
            for char, replacement in leet_map.items():
                normalized = normalized.replace(char, replacement)
            
            if normalized in self.common_passwords_lower:
                return f"Leet-speak variation of: '{normalized}'"
                
            reversed_pass = lower[::-1]
            if reversed_pass in self.common_passwords_lower:
                return f"Reversed common password detected"
                    
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
                recs.append("Use at least 12 characters (16+ recommended)")
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
    """Have I Been Pwned API integration"""
    
    def __init__(self):
        self.api_url = Config.HIBP_API_URL
        self.timeout = 10
    
    def check_breach(self, password, callback):
        """Check password against HIBP database"""
        if not password:
            callback("Not checked", 0)
            return
        
        def check():
            try:
                sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
                prefix = sha1_hash[:5]
                suffix = sha1_hash[5:]
                
                response = requests.get(
                    f"{self.api_url}{prefix}",
                    timeout=self.timeout,
                    headers={"User-Agent": "PasswordStrengthAnalyzer-Pro"}
                )
                
                if response.status_code == 200:
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
        
        thread = threading.Thread(target=check, daemon=True)
        thread.start()

# ==================== MAIN APPLICATION ====================
class PasswordStrengthChecker:
    """Main application class - Optimized for 1100x700"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔐 Password Strength Analyzer Pro")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.configure(bg=Config.BG_COLOR)
        self.root.resizable(False, False)  # Fixed size as requested
        
        # Initialize components
        self.analyzer = PasswordAnalyzer()
        self.breach_detector = BreachDetector()
        
        # State
        self.current_analysis = None
        self.breach_count = 0
        self.breach_status = "Not checked"
        self.show_password = False
        self.is_analyzing = False
        
        self.setup_styles()
        self.create_widgets()
        self.center_window()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.password_var.trace('w', self.on_password_change)
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
    def create_widgets(self):
        """Create all UI widgets - Optimized layout for 1100x700"""
        # Main container
        main_container = tk.Frame(self.root, bg=Config.BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_container)
        
        # Input section
        self.create_input_section(main_container)
        
        # Strength indicator with colored lights
        self.create_strength_indicator(main_container)
        
        # Results section
        self.create_results_section(main_container)
        
        # Recommendations at bottom
        self.create_recommendations_section(main_container)
        
        # Status bar
        self.create_status_bar(main_container)
        
    def create_header(self, parent):
        """Create application header with glow effect"""
        header = tk.Frame(parent, bg=Config.BG_COLOR)
        header.pack(fill=tk.X, pady=(0, 15))
        
        # Title with glow effect
        title_frame = tk.Frame(header, bg=Config.BG_COLOR)
        title_frame.pack()
        
        title = tk.Label(title_frame, 
                        text="🔐 PASSWORD STRENGTH ANALYZER",
                        bg=Config.BG_COLOR,
                        fg=Config.ACCENT_COLOR,
                        font=(Config.FONT_FAMILY, 22, "bold"))
        title.pack()
        
        # Glow effect label (simulated with multiple labels)
        glow = tk.Label(title_frame, 
                       text="🔐 PASSWORD STRENGTH ANALYZER",
                       bg=Config.BG_COLOR,
                       fg="#0088aa",
                       font=(Config.FONT_FAMILY, 22, "bold"))
        glow.place(relx=0.5, rely=0.5, anchor="center")
        glow.lower()
        
        subtitle = tk.Label(header,
                           text="Advanced Cyber Security Tool with Breach Detection",
                           bg=Config.BG_COLOR,
                           fg=Config.SECONDARY_TEXT,
                           font=(Config.FONT_FAMILY, 11))
        subtitle.pack(pady=(5, 0))
        
        # Animated underline
        underline = tk.Canvas(header, height=2, bg=Config.BG_COLOR, 
                             highlightthickness=0)
        underline.pack(fill=tk.X, pady=8)
        underline.create_line(0, 1, 1060, 1, fill=Config.ACCENT_COLOR, width=2)
        
    def create_input_section(self, parent):
        """Create password input section"""
        card = tk.Frame(parent, bg=Config.CARD_BG, padx=20, pady=15)
        card.pack(fill=tk.X, pady=8)
        
        # Label
        tk.Label(card, text="Enter Password to Analyze",
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR,
                font=(Config.FONT_FAMILY, 12, "bold")).pack(anchor=tk.W)
        
        # Input frame
        input_frame = tk.Frame(card, bg=Config.CARD_BG)
        input_frame.pack(fill=tk.X, pady=12)
        
        # Password entry with custom styling
        self.password_var = tk.StringVar()
        
        entry_frame = tk.Frame(input_frame, bg="#2a2a2a", padx=2, pady=2)
        entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.password_entry = tk.Entry(entry_frame,
                                      textvariable=self.password_var,
                                      show="●",
                                      bg="#1a1a1a",
                                      fg=Config.TEXT_COLOR,
                                      font=(Config.FONT_FAMILY, 14),
                                      relief=tk.FLAT,
                                      insertbackground=Config.ACCENT_COLOR)
        self.password_entry.pack(fill=tk.X, ipady=10, padx=10)
        self.password_entry.bind('<Return>', lambda e: self.analyze_password())
        
        # Toggle visibility button
        self.toggle_btn = tk.Button(input_frame, text="👁",
                                   bg=Config.CARD_BG,
                                   fg=Config.SECONDARY_TEXT,
                                   font=(Config.FONT_FAMILY, 12),
                                   relief=tk.FLAT,
                                   command=self.toggle_visibility,
                                   cursor="hand2",
                                   width=4)
        self.toggle_btn.pack(side=tk.LEFT, padx=(8, 0))
        
        # Analyze button with glow
        self.analyze_btn = tk.Button(input_frame, text="ANALYZE",
                                    bg=Config.ACCENT_COLOR,
                                    fg=Config.BG_COLOR,
                                    font=(Config.FONT_FAMILY, 11, "bold"),
                                    relief=tk.FLAT,
                                    command=self.analyze_password,
                                    cursor="hand2",
                                    padx=20)
        self.analyze_btn.pack(side=tk.LEFT, padx=(8, 0))
        
        # Character count
        self.char_count = tk.Label(card, text="0 characters",
                                  bg=Config.CARD_BG,
                                  fg=Config.SECONDARY_TEXT,
                                  font=(Config.FONT_FAMILY, 10))
        self.char_count.pack(anchor=tk.E)
        
    def create_strength_indicator(self, parent):
        """Create prominent colored strength indicator - RED/YELLOW/GREEN lights"""
        card = tk.Frame(parent, bg=Config.CARD_BG, padx=20, pady=15)
        card.pack(fill=tk.X, pady=8)
        
        # Title
        tk.Label(card, text="Password Strength",
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR,
                font=(Config.FONT_FAMILY, 12, "bold")).pack(anchor=tk.W)
        
        # Strength indicator frame with colored lights
        indicator_frame = tk.Frame(card, bg=Config.CARD_BG)
        indicator_frame.pack(fill=tk.X, pady=10)
        
        # Three colored indicator lights
        lights_frame = tk.Frame(indicator_frame, bg=Config.CARD_BG)
        lights_frame.pack(side=tk.LEFT)
        
        # RED light (Weak)
        self.red_light = tk.Canvas(lights_frame, width=60, height=60, 
                                   bg=Config.CARD_BG, highlightthickness=0)
        self.red_light.pack(side=tk.LEFT, padx=(0, 15))
        self.red_circle = self.red_light.create_oval(10, 10, 50, 50, 
                                                       fill="#3a1a1a", outline="#552222", width=2)
        self.red_text = self.red_light.create_text(30, 30, text="WEAK",
                                                   fill="#552222", font=(Config.FONT_FAMILY, 8, "bold"))
        
        # YELLOW light (Medium)
        self.yellow_light = tk.Canvas(lights_frame, width=60, height=60, 
                                      bg=Config.CARD_BG, highlightthickness=0)
        self.yellow_light.pack(side=tk.LEFT, padx=(0, 15))
        self.yellow_circle = self.yellow_light.create_oval(10, 10, 50, 50, 
                                                         fill="#3a3a1a", outline="#555522", width=2)
        self.yellow_text = self.yellow_light.create_text(30, 30, text="NORMAL",
                                                         fill="#555522", font=(Config.FONT_FAMILY, 7, "bold"))
        
        # GREEN light (Strong)
        self.green_light = tk.Canvas(lights_frame, width=60, height=60, 
                                     bg=Config.CARD_BG, highlightthickness=0)
        self.green_light.pack(side=tk.LEFT)
        self.green_circle = self.green_light.create_oval(10, 10, 50, 50, 
                                                         fill="#1a3a1a", outline="#225522", width=2)
        self.green_text = self.green_light.create_text(30, 30, text="STRONG",
                                                       fill="#225522", font=(Config.FONT_FAMILY, 7, "bold"))
        
        # Strength label and score
        info_frame = tk.Frame(indicator_frame, bg=Config.CARD_BG)
        info_frame.pack(side=tk.LEFT, padx=(30, 0))
        
        self.strength_label = tk.Label(info_frame, text="Not Analyzed",
                                      bg=Config.CARD_BG,
                                      fg=Config.SECONDARY_TEXT,
                                      font=(Config.FONT_FAMILY, 20, "bold"))
        self.strength_label.pack(anchor=tk.W)
        
        self.score_label = tk.Label(info_frame, text="Score: 0/100",
                                   bg=Config.CARD_BG,
                                   fg=Config.SECONDARY_TEXT,
                                   font=(Config.FONT_FAMILY, 14))
        self.score_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Progress bar below lights
        self.progress_canvas = tk.Canvas(card, height=25, bg=Config.CARD_BG,
                                         highlightthickness=0)
        self.progress_canvas.pack(fill=tk.X, pady=(10, 0))
        
        # Draw initial empty progress bar
        self.progress_canvas.create_rectangle(0, 5, 1010, 20, 
                                            fill="#2a2a2a", outline="", tags="bg")
        
    def create_results_section(self, parent):
        """Create detailed results cards"""
        results_frame = tk.Frame(parent, bg=Config.BG_COLOR)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=8)
        
        # Left column - Character Analysis
        left_card = tk.Frame(results_frame, bg=Config.CARD_BG, padx=15, pady=12, width=500)
        left_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        left_card.pack_propagate(False)
        
        tk.Label(left_card, text="📊 Character Analysis",
                bg=Config.CARD_BG, fg=Config.ACCENT_COLOR,
                font=(Config.FONT_FAMILY, 12, "bold")).pack(anchor=tk.W)
        
        self.char_analysis = tk.Text(left_card, bg=Config.CARD_BG,
                                     fg=Config.TEXT_COLOR,
                                     font=(Config.FONT_FAMILY, 10),
                                     relief=tk.FLAT, height=8, width=40,
                                     wrap=tk.WORD,
                                     padx=5, pady=5)
        self.char_analysis.pack(fill=tk.BOTH, expand=True, pady=8)
        self.char_analysis.insert(tk.END, "Enter a password to see analysis...")
        self.char_analysis.config(state=tk.DISABLED)
        
        # Right column - Security Info
        right_card = tk.Frame(results_frame, bg=Config.CARD_BG, padx=15, pady=12, width=500)
        right_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        right_card.pack_propagate(False)
        
        tk.Label(right_card, text="🔒 Security Assessment",
                bg=Config.CARD_BG, fg=Config.ACCENT_COLOR,
                font=(Config.FONT_FAMILY, 12, "bold")).pack(anchor=tk.W)
        
        self.security_info = tk.Text(right_card, bg=Config.CARD_BG,
                                     fg=Config.TEXT_COLOR,
                                     font=(Config.FONT_FAMILY, 10),
                                     relief=tk.FLAT, height=8, width=40,
                                     wrap=tk.WORD,
                                     padx=5, pady=5)
        self.security_info.pack(fill=tk.BOTH, expand=True, pady=8)
        self.security_info.insert(tk.END, "Security details will appear here...")
        self.security_info.config(state=tk.DISABLED)
        
    def create_recommendations_section(self, parent):
        """Create recommendations section at bottom"""
        card = tk.Frame(parent, bg=Config.CARD_BG, padx=15, pady=12, height=100)
        card.pack(fill=tk.X, pady=8)
        card.pack_propagate(False)
        
        tk.Label(card, text="💡 Recommendations",
                bg=Config.CARD_BG, fg=Config.WARNING_COLOR,
                font=(Config.FONT_FAMILY, 12, "bold")).pack(anchor=tk.W)
        
        self.recommendations = tk.Text(card, 
                                       bg=Config.CARD_BG,
                                       fg=Config.SECONDARY_TEXT,
                                       font=(Config.FONT_FAMILY, 10),
                                       relief=tk.FLAT,
                                       height=3,
                                       wrap=tk.WORD,
                                       padx=5, pady=5)
        self.recommendations.pack(fill=tk.BOTH, expand=True)
        self.recommendations.insert(tk.END, "Enter a password and click ANALYZE to get recommendations...")
        self.recommendations.config(state=tk.DISABLED)
        
    def create_status_bar(self, parent):
        """Create status bar"""
        status = tk.Frame(parent, bg=Config.BG_COLOR)
        status.pack(fill=tk.X, pady=(5, 0))
        
        self.status_label = tk.Label(status, 
                                    text="Ready | Enter a password to begin analysis",
                                    bg=Config.BG_COLOR,
                                    fg=Config.SECONDARY_TEXT,
                                    font=(Config.FONT_FAMILY, 10))
        self.status_label.pack(side=tk.LEFT)
        
        version = tk.Label(status, text="v5.0 Optimized",
                          bg=Config.BG_COLOR,
                          fg=Config.ACCENT_COLOR,
                          font=(Config.FONT_FAMILY, 10))
        version.pack(side=tk.RIGHT)
        
    def on_password_change(self, *args):
        """Update character count when password changes"""
        password = self.password_var.get()
        self.char_count.config(text=f"{len(password)} characters")
        
    def toggle_visibility(self):
        """Toggle password visibility"""
        self.show_password = not self.show_password
        self.password_entry.config(show="" if self.show_password else "●")
        self.toggle_btn.config(fg=Config.ACCENT_COLOR if self.show_password 
                              else Config.SECONDARY_TEXT)
        
    def update_strength_lights(self, score):
        """Update colored lights based on score - RED/YELLOW/GREEN"""
        # Reset all lights to dim
        self.red_light.itemconfig(self.red_circle, fill="#3a1a1a", outline="#552222")
        self.red_light.itemconfig(self.red_text, fill="#552222")
        
        self.yellow_light.itemconfig(self.yellow_circle, fill="#3a3a1a", outline="#555522")
        self.yellow_light.itemconfig(self.yellow_text, fill="#555522")
        
        self.green_light.itemconfig(self.green_circle, fill="#1a3a1a", outline="#225522")
        self.green_light.itemconfig(self.green_text, fill="#225522")
        
        # Light up appropriate color based on score
        if score < 50:
            # RED - Weak
            self.red_light.itemconfig(self.red_circle, fill=Config.DANGER_COLOR, outline="#ff6666")
            self.red_light.itemconfig(self.red_text, fill="#ffffff")
            self.strength_label.config(fg=Config.DANGER_COLOR)
        elif score < 80:
            # YELLOW - Normal/Medium
            self.yellow_light.itemconfig(self.yellow_circle, fill=Config.WARNING_COLOR, outline="#ffcc66")
            self.yellow_light.itemconfig(self.yellow_text, fill="#000000")
            self.strength_label.config(fg=Config.WARNING_COLOR)
        else:
            # GREEN - Strong
            self.green_light.itemconfig(self.green_circle, fill=Config.SUCCESS_COLOR, outline="#66ff99")
            self.green_light.itemconfig(self.green_text, fill="#000000")
            self.strength_label.config(fg=Config.SUCCESS_COLOR)
        
    def analyze_password(self, event=None):
        """Analyze password and update UI"""
        password = self.password_var.get()
        
        if not password:
            self.status_label.config(text="Please enter a password")
            return
        
        if self.is_analyzing:
            return
        
        self.is_analyzing = True
        self.analyze_btn.config(state=tk.DISABLED, text="Analyzing...")
        self.status_label.config(text="Analyzing password...")
        
        try:
            self.current_analysis = self.analyzer.analyze(password)
            
            if self.current_analysis is None:
                self.show_analysis_failed()
                return
            
            # Update display
            self.update_display()
            
            # Check breach status in background
            def breach_callback(status, count):
                self.root.after(0, lambda: self.update_breach_status(status, count))
            
            self.breach_detector.check_breach(password, breach_callback)
                
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
        self.status_label.config(text="Analysis failed. Please try again.")
        
    def update_breach_status(self, status, count):
        """Update breach status display"""
        self.breach_status = status
        self.breach_count = count
        
        # Add breach info to security text
        self.security_info.config(state=tk.NORMAL)
        current_text = self.security_info.get(1.0, tk.END)
        
        breach_text = f"\n\nBreach Status: {status}"
        if count > 0:
            breach_text += f" ({count:,} occurrences)"
            
        self.security_info.insert(tk.END, breach_text)
        self.security_info.config(state=tk.DISABLED)
        
    def update_display(self):
        """Update all UI elements with analysis results"""
        if not self.current_analysis:
            self.show_analysis_failed()
            return
            
        analysis = self.current_analysis
        
        # Update strength lights (RED/YELLOW/GREEN)
        self.update_strength_lights(analysis['score'])
        
        # Update strength label
        self.strength_label.config(text=analysis['strength'])
        
        # Update score
        self.score_label.config(text=f"Score: {analysis['score']}/100")
        
        # Update progress bar with color
        self.progress_canvas.delete("all")
        
        # Background bar
        self.progress_canvas.create_rectangle(0, 5, 1010, 20, 
                                            fill="#2a2a2a", outline="")
        
        # Colored progress bar
        bar_width = (analysis['score'] / 100) * 1010
        
        if analysis['score'] < 50:
            bar_color = Config.DANGER_COLOR
        elif analysis['score'] < 80:
            bar_color = Config.WARNING_COLOR
        else:
            bar_color = Config.SUCCESS_COLOR
            
        self.progress_canvas.create_rectangle(0, 5, bar_width, 20, 
                                            fill=bar_color, outline="")
        
        # Update character analysis
        self.char_analysis.config(state=tk.NORMAL)
        self.char_analysis.delete(1.0, tk.END)
        
        chars = analysis['char_types']
        char_text = f"""Length: {analysis['length']} characters
Lowercase letters: {chars['lowercase']}
Uppercase letters: {chars['uppercase']}
Digits: {chars['digits']}
Special characters: {chars['special']}
Unique characters: {chars['unique']}
Character variety: {sum(1 for v in [chars['lowercase'], chars['uppercase'], chars['digits'], chars['special']] if v > 0)}/4"""
        self.char_analysis.insert(tk.END, char_text)
        self.char_analysis.config(state=tk.DISABLED)
        
        # Update security info
        self.security_info.config(state=tk.NORMAL)
        self.security_info.delete(1.0, tk.END)
        
        security_text = f"""Estimated crack time:
{analysis['crack_time']}

Entropy: {analysis['entropy']} bits
"""
        if analysis['common_check']:
            security_text += f"\n⚠️ Warning: {analysis['common_check']}\n"
        
        if analysis['patterns']:
            security_text += "\nDetected patterns:\n"
            for pattern in analysis['patterns'][:5]:
                security_text += f"• {pattern}\n"
        
        self.security_info.insert(tk.END, security_text)
        self.security_info.config(state=tk.DISABLED)
        
        # Update recommendations
        self.recommendations.config(state=tk.NORMAL)
        self.recommendations.delete(1.0, tk.END)
        
        if analysis['recommendations']:
            rec_text = "\n".join(f"• {rec}" for rec in analysis['recommendations'])
            self.recommendations.insert(tk.END, rec_text)
            self.recommendations.config(fg=Config.WARNING_COLOR)
        else:
            self.recommendations.insert(tk.END, "✓ Excellent password! No improvements needed.\n\nStrong Password Tips:\n• Use 16+ characters for maximum security\n• Mix uppercase, lowercase, numbers, and symbols\n• Avoid dictionary words and personal information\n• Use a unique password for each account\n• Consider using a password manager")
            self.recommendations.config(fg=Config.SUCCESS_COLOR)
        
        self.recommendations.config(state=tk.DISABLED)
        
        # Update status
        self.status_label.config(text=f"Analysis complete | {datetime.now().strftime('%H:%M:%S')}")
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def on_close(self):
        """Handle window close"""
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