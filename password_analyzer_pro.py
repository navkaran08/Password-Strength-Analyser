"""
Password Strength Analyzer Pro
Author: Navkaran Singh (Enhanced Version)
Advanced Cyber Security Tool with Breach Detection & History
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

# ==================== CONFIGURATION ====================
class Config:
    """Application configuration constants"""
    WINDOW_WIDTH = 1100
    WINDOW_HEIGHT = 800
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
    
    # Common passwords list (top 1000 most common)
    COMMON_PASSWORDS = [
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
        "austin", "thunder", "taylor", "matrix", "minecraft"
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

# ==================== ANIMATION ENGINE ====================
class AnimationEngine:
    """Handles smooth animations for UI elements"""
    
    def __init__(self, root):
        self.root = root
        self.animations = {}
        self.running = True
        
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
            self.root.after(delay, lambda: step(count + 1))
        
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
    
    def pulse_animation(self, widget, color1, color2, duration=1000):
        """Create pulsing glow effect"""
        def pulse():
            if not self.running:
                return
            try:
                current = widget.cget("bg")
                new_color = color2 if current == color1 else color1
                widget.config(bg=new_color)
                self.root.after(duration // 2, pulse)
            except:
                pass
        pulse()
    
    def shake_widget(self, widget, intensity=5, duration=300):
        """Shake animation for weak passwords"""
        try:
            original_x = widget.winfo_x()
            original_y = widget.winfo_y()
            steps = 10
            delay = duration // steps
            
            def shake_step(step=0):
                if step >= steps:
                    widget.place(x=original_x, y=original_y)
                    return
                
                offset_x = random.randint(-intensity, intensity) * (steps - step) // steps
                offset_y = random.randint(-intensity//2, intensity//2) * (steps - step) // steps
                widget.place(x=original_x + offset_x, y=original_y + offset_y)
                self.root.after(delay, lambda: shake_step(step + 1))
            
            shake_step()
        except:
            pass
    
    def stop(self):
        """Stop all animations"""
        self.running = False

# ==================== PASSWORD ANALYZER ====================
class PasswordAnalyzer:
    """Advanced password security analysis"""
    
    def __init__(self):
        self.common_passwords = set(Config.COMMON_PASSWORDS)
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
        except:
            pass
        
        return patterns
    
    def check_common(self, password):
        """Check against common passwords"""
        if not password:
            return None
            
        try:
            lower = password.lower()
            
            # Exact match
            if lower in self.common_passwords:
                return "Exact match in common passwords!"
            
            # Partial match
            for common in self.common_passwords:
                if common in lower or lower in common:
                    if len(common) > 4:
                        return f"Similar to common password: '{common}'"
            
            # Leet speak variations
            leet_map = {'@': 'a', '4': 'a', '3': 'e', '1': 'i', '0': 'o', 
                       '5': 's', '$': 's', '7': 't', '+': 't'}
            normalized = lower
            for char, replacement in leet_map.items():
                normalized = normalized.replace(char, replacement)
            
            if normalized in self.common_passwords:
                return f"Leet-speak variation of: '{normalized}'"
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
        self.root.title("🔐 Password Strength Analyzer Pro - Navkaran Singh")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.configure(bg=Config.BG_COLOR)
        self.root.minsize(1000, 700)
        
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
        
        self.setup_styles()
        self.create_widgets()
        self.center_window()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
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
        """Create all UI widgets"""
        # Main container with horizontal layout
        main_container = tk.Frame(self.root, bg=Config.BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (main content)
        left_panel = tk.Frame(main_container, bg=Config.BG_COLOR)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Right panel (history sidebar)
        right_panel = tk.Frame(main_container, bg=Config.CARD_BG, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20), pady=20)
        right_panel.pack_propagate(False)
        
        # Header
        self.create_header(left_panel)
        
        # Input section
        self.create_input_section(left_panel)
        
        # Strength meter
        self.create_strength_meter(left_panel)
        
        # Results cards
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
                           text="Advanced Cyber Security Tool with Breach Detection",
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
        """Create animated strength meter"""
        card = tk.Frame(parent, bg=Config.CARD_BG, padx=20, pady=20)
        card.pack(fill=tk.X, pady=10)
        
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
        """Create detailed results cards"""
        results_frame = tk.Frame(parent, bg=Config.BG_COLOR)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left column - Character Analysis
        left_card = tk.Frame(results_frame, bg=Config.CARD_BG, padx=15, pady=15)
        left_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(left_card, text="📊 Character Analysis",
                bg=Config.CARD_BG, fg=Config.ACCENT_COLOR,
                font=(Config.FONT_FAMILY, 13, "bold")).pack(anchor=tk.W)
        
        self.char_analysis = tk.Text(left_card, bg=Config.CARD_BG,
                                     fg=Config.TEXT_COLOR,
                                     font=(Config.FONT_FAMILY, 11),
                                     relief=tk.FLAT, height=8, width=35)
        self.char_analysis.pack(fill=tk.BOTH, expand=True, pady=10)
        self.char_analysis.insert(tk.END, "Enter a password to see analysis...")
        self.char_analysis.config(state=tk.DISABLED)
        
        # Right column - Security Info
        right_card = tk.Frame(results_frame, bg=Config.CARD_BG, padx=15, pady=15)
        right_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(right_card, text="🔒 Security Assessment",
                bg=Config.CARD_BG, fg=Config.ACCENT_COLOR,
                font=(Config.FONT_FAMILY, 13, "bold")).pack(anchor=tk.W)
        
        self.security_info = tk.Text(right_card, bg=Config.CARD_BG,
                                     fg=Config.TEXT_COLOR,
                                     font=(Config.FONT_FAMILY, 11),
                                     relief=tk.FLAT, height=8, width=35)
        self.security_info.pack(fill=tk.BOTH, expand=True, pady=10)
        self.security_info.insert(tk.END, "Security details will appear here...")
        self.security_info.config(state=tk.DISABLED)
        
        # Bottom card - Recommendations
        bottom_card = tk.Frame(parent, bg=Config.CARD_BG, padx=15, pady=15)
        bottom_card.pack(fill=tk.X, pady=10)
        
        tk.Label(bottom_card, text="💡 Recommendations",
                bg=Config.CARD_BG, fg=Config.WARNING_COLOR,
                font=(Config.FONT_FAMILY, 13, "bold")).pack(anchor=tk.W)
        
        self.recommendations = tk.Label(bottom_card, 
                                       text="Enter a password and click ANALYZE to get recommendations...",
                                       bg=Config.CARD_BG,
                                       fg=Config.SECONDARY_TEXT,
                                       font=(Config.FONT_FAMILY, 11),
                                       wraplength=700,
                                       justify=tk.LEFT)
        self.recommendations.pack(fill=tk.X, pady=10)
        
    def create_breach_section(self, parent):
        """Create breach detection section"""
        card = tk.Frame(parent, bg=Config.CARD_BG, padx=15, pady=15)
        card.pack(fill=tk.X, pady=10)
        
        tk.Label(card, text="🌐 Breach Detection (Have I Been Pwned)",
                bg=Config.CARD_BG, fg=Config.ACCENT_COLOR,
                font=(Config.FONT_FAMILY, 13, "bold")).pack(anchor=tk.W)
        
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
                                          selectmode=tk.SINGLE)
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
        
        version = tk.Label(status, text="v3.0 Pro",
                          bg=Config.BG_COLOR,
                          fg=Config.ACCENT_COLOR,
                          font=(Config.FONT_FAMILY, 10))
        version.pack(side=tk.RIGHT)
        
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
        """Analyze password and update UI"""
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
        
        # Update character count
        self.char_count.config(text=f"{len(password)} characters")
        
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
            self.breach_label.config(text="Checking breach databases...", fg=Config.WARNING_COLOR)
            
            def breach_callback(status, count):
                self.root.after(0, lambda: self.update_breach_status(status, count))
            
            self.breach_detector.check_breach(password, breach_callback)
            
            # Save to history
            self.save_to_history(password)
            
            # Animation for weak passwords
            if self.current_analysis['score'] < 50:
                self.animator.shake_widget(self.entry_frame, intensity=3)
                
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
        
    def update_breach_status(self, status, count):
        """Update breach status display"""
        self.breach_status = status
        self.breach_count = count
        
        if count > 0:
            self.breach_label.config(
                text=f"⚠️ Found in Data Breaches ({count:,} occurrences)",
                fg=Config.DANGER_COLOR
            )
        elif "Not Found" in status:
            self.breach_label.config(
                text="✓ Not Found in Known Data Breaches",
                fg=Config.SUCCESS_COLOR
            )
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
        
        # Update history with breach status
        self.update_history_breach_status(status)
        
    def update_display(self):
        """Update all UI elements with analysis results"""
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
        
        # Update character analysis
        self.char_analysis.config(state=tk.NORMAL)
        self.char_analysis.delete(1.0, tk.END)
        
        chars = analysis['char_types']
        self.char_analysis.insert(tk.END, f"Length: {analysis['length']}\n")
        self.char_analysis.insert(tk.END, f"Lowercase: {chars['lowercase']}\n")
        self.char_analysis.insert(tk.END, f"Uppercase: {chars['uppercase']}\n")
        self.char_analysis.insert(tk.END, f"Digits: {chars['digits']}\n")
        self.char_analysis.insert(tk.END, f"Special: {chars['special']}\n")
        self.char_analysis.insert(tk.END, f"Unique chars: {chars['unique']}\n")
        self.char_analysis.insert(tk.END, f"Variety score: {sum(1 for v in [chars['lowercase'], chars['uppercase'], chars['digits'], chars['special']] if v > 0)}/4")
        self.char_analysis.config(state=tk.DISABLED)
        
        # Update security info
        self.security_info.config(state=tk.NORMAL)
        self.security_info.delete(1.0, tk.END)
        
        self.security_info.insert(tk.END, f"Estimated crack time:\n")
        self.security_info.insert(tk.END, f"{analysis['crack_time']}\n\n")
        
        if analysis['common_check']:
            self.security_info.insert(tk.END, f"⚠️ Warning:\n{analysis['common_check']}\n\n")
        
        if analysis['patterns']:
            self.security_info.insert(tk.END, "Detected patterns:\n")
            for pattern in analysis['patterns'][:5]:  # Limit to 5 patterns
                self.security_info.insert(tk.END, f"• {pattern}\n")
        
        self.security_info.config(state=tk.DISABLED)
        
        # Update recommendations
        if analysis['recommendations']:
            rec_text = " • ".join(analysis['recommendations'])
            self.recommendations.config(text=rec_text, fg=Config.WARNING_COLOR)
        else:
            self.recommendations.config(text="✓ Excellent password! No improvements needed.", 
                                       fg=Config.SUCCESS_COLOR)
        
        # Update status
        self.status_label.config(text=f"Analysis complete | {datetime.now().strftime('%H:%M:%S')}")
        
    def save_to_history(self, password):
        """Save analysis to history"""
        if not self.current_analysis:
            return
            
        try:
            # Create password preview (first 3 chars + asterisks)
            preview = password[:3] + "*" * (len(password) - 3) if len(password) > 3 else "*" * len(password)
            
            self.db.add_entry(
                preview,
                self.current_analysis['strength'],
                self.current_analysis['score'],
                self.breach_status,
                self.current_analysis['entropy'],
                self.current_analysis['crack_time']
            )
            
            # Refresh history display
            self.refresh_history()
        except Exception as e:
            print(f"Error saving to history: {e}")
            
    def update_history_breach_status(self, status):
        """Update the breach status in the most recent history entry"""
        self.refresh_history()
            
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
        """Handle window close"""
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