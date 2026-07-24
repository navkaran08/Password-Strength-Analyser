"""
Password Strength Checker - Premium Edition
Author: Navkaran Singh
Advanced Cyber Security Tool with Animations
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
import math
import hashlib
import requests
import threading
import json
from datetime import datetime
from collections import Counter
import random

# ==================== CONFIGURATION ====================
class Config:
    """Application configuration constants"""
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    BG_COLOR = "#0a0a0a"
    CARD_BG = "#141414"
    ACCENT_COLOR = "#00d4ff"
    SUCCESS_COLOR = "#00ff88"
    WARNING_COLOR = "#ffaa00"
    DANGER_COLOR = "#ff4757"
    TEXT_COLOR = "#ffffff"
    SECONDARY_TEXT = "#888888"
    FONT_FAMILY = "Segoe UI"
    
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
        canvas.create_rectangle(x1 + fill_width - 20, y1, x1 + fill_width, y2,
                               fill=color, stipple="gray50", tags="progress")
        
        # Percentage text
        canvas.create_text(x2 + 30, y1 + height//2, text=f"{int(value)}%",
                          fill=Config.TEXT_COLOR, font=(Config.FONT_FAMILY, 11, "bold"),
                          tags="progress")
    
    def _get_strength_color(self, value):
        """Get color based on strength percentage"""
        if value < 30:
            return Config.DANGER_COLOR
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
            current = widget.cget("bg")
            new_color = color2 if current == color1 else color1
            widget.config(bg=new_color)
            self.root.after(duration // 2, pulse)
        pulse()
    
    def shake_widget(self, widget, intensity=5, duration=300):
        """Shake animation for weak passwords"""
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
    
    def fade_in(self, widget, duration=500):
        """Fade in animation"""
        alpha = 0.0
        steps = 20
        increment = 1.0 / steps
        delay = duration // steps
        
        def fade(step=0):
            if step >= steps:
                return
            # Simulate fade by changing text color brightness
            brightness = int(136 + (119 * (step / steps)))  # From #888 to #fff
            color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            if hasattr(widget, 'config'):
                widget.config(fg=color)
            self.root.after(delay, lambda: fade(step + 1))
        
        fade()
    
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
    
    def calculate_entropy(self, password):
        """Calculate Shannon entropy"""
        if not password:
            return 0
        
        entropy = 0
        length = len(password)
        freq = Counter(password)
        
        for count in freq.values():
            p = count / length
            entropy -= p * math.log2(p)
        
        return round(entropy * length, 2)
    
    def estimate_crack_time(self, password):
        """Estimate time to crack password"""
        if not password:
            return "Instant"
        
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
    
    def find_patterns(self, password):
        """Find problematic patterns"""
        patterns = []
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
        
        return patterns
    
    def check_common(self, password):
        """Check against common passwords"""
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
        
        return None
    
    def analyze_characters(self, password):
        """Analyze character composition"""
        return {
            'lowercase': len(re.findall(r'[a-z]', password)),
            'uppercase': len(re.findall(r'[A-Z]', password)),
            'digits': len(re.findall(r'\d', password)),
            'special': len(re.findall(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password)),
            'unique': len(set(password))
        }
    
    def calculate_score(self, analysis):
        """Calculate overall strength score (0-100)"""
        score = 0
        chars = analysis['char_types']
        
        # Length scoring (max 30)
        length = analysis['length']
        if length >= 16: score += 30
        elif length >= 12: score += 25
        elif length >= 10: score += 20
        elif length >= 8: score += 15
        else: score += length
        
        # Character variety (max 40)
        variety = sum(1 for v in [chars['lowercase'], chars['uppercase'], 
                                  chars['digits'], chars['special']] if v > 0)
        score += variety * 10
        
        # Entropy bonus (max 20)
        entropy = analysis['entropy']
        if entropy > 80: score += 20
        elif entropy > 60: score += 15
        elif entropy > 40: score += 10
        elif entropy > 20: score += 5
        
        # Pattern penalties
        if analysis['patterns']:
            score -= len(analysis['patterns']) * 5
        if analysis['common_check']:
            score -= 30
        
        # Unique character bonus
        unique_ratio = chars['unique'] / max(length, 1)
        score += int(unique_ratio * 10)
        
        return max(0, min(100, score))
    
    def get_strength_label(self, score):
        """Get strength label from score"""
        if score >= 90: return "Excellent"
        elif score >= 80: return "Very Strong"
        elif score >= 70: return "Strong"
        elif score >= 60: return "Moderate"
        elif score >= 40: return "Weak"
        elif score >= 20: return "Very Weak"
        else: return "Critical"
    
    def generate_recommendations(self, analysis, password):
        """Generate improvement recommendations"""
        recs = []
        chars = analysis['char_types']
        
        if analysis['length'] < 12:
            recs.append("Use at least 12 characters")
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
            recs.append("Avoid common passwords")
        if chars['unique'] < len(password) * 0.5:
            recs.append("Use more unique characters")
        
        return recs

# ==================== MAIN APPLICATION ====================
class PasswordStrengthChecker:
    """Main application class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔐 Password Strength Analyzer Pro - Navkaran Singh")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.configure(bg=Config.BG_COLOR)
        self.root.resizable(False, False)
        
        # Initialize components
        self.animator = AnimationEngine(self.root)
        self.analyzer = PasswordAnalyzer()
        
        # State
        self.current_analysis = None
        self.show_password = False
        
        self.setup_styles()
        self.create_widgets()
        self.center_window()
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure("Card.TFrame", background=Config.CARD_BG)
        style.configure("Title.TLabel", 
                      background=Config.BG_COLOR,
                      foreground=Config.ACCENT_COLOR,
                      font=(Config.FONT_FAMILY, 24, "bold"))
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg=Config.BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Input section
        self.create_input_section(main_frame)
        
        # Strength meter
        self.create_strength_meter(main_frame)
        
        # Results cards
        self.create_results_section(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_header(self, parent):
        """Create application header"""
        header = tk.Frame(parent, bg=Config.BG_COLOR)
        header.pack(fill=tk.X, pady=(0, 20))
        
        # Title with gradient effect
        title = tk.Label(header, 
                        text="🔐 PASSWORD STRENGTH ANALYZER",
                        bg=Config.BG_COLOR,
                        fg=Config.ACCENT_COLOR,
                        font=(Config.FONT_FAMILY, 28, "bold"))
        title.pack()
        
        subtitle = tk.Label(header,
                           text="Advanced Cyber Security Tool by Navkaran Singh",
                           bg=Config.BG_COLOR,
                           fg=Config.SECONDARY_TEXT,
                           font=(Config.FONT_FAMILY, 12))
        subtitle.pack(pady=(5, 0))
        
        # Animated underline
        underline = tk.Canvas(header, height=3, bg=Config.BG_COLOR, 
                             highlightthickness=0)
        underline.pack(fill=tk.X, pady=10)
        underline.create_line(0, 1, 900, 1, fill=Config.ACCENT_COLOR, width=2)
        
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
        self.password_var.trace('w', self.on_password_change)
        
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
                                     relief=tk.FLAT, height=10, width=35)
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
                                     relief=tk.FLAT, height=10, width=35)
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
                                       text="Start typing to get recommendations...",
                                       bg=Config.CARD_BG,
                                       fg=Config.SECONDARY_TEXT,
                                       font=(Config.FONT_FAMILY, 11),
                                       wraplength=800,
                                       justify=tk.LEFT)
        self.recommendations.pack(fill=tk.X, pady=10)
        
    def create_status_bar(self, parent):
        """Create status bar"""
        status = tk.Frame(parent, bg=Config.BG_COLOR)
        status.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(status, 
                                    text="Ready | Real-time analysis enabled",
                                    bg=Config.BG_COLOR,
                                    fg=Config.SECONDARY_TEXT,
                                    font=(Config.FONT_FAMILY, 10))
        self.status_label.pack(side=tk.LEFT)
        
        version = tk.Label(status, text="v2.0 Pro",
                          bg=Config.BG_COLOR,
                          fg=Config.ACCENT_COLOR,
                          font=(Config.FONT_FAMILY, 10))
        version.pack(side=tk.RIGHT)
        
    def on_password_change(self, *args):
        """Handle password input changes"""
        password = self.password_var.get()
        self.char_count.config(text=f"{len(password)} characters")
        
        # Real-time analysis
        if len(password) > 0:
            self.analyze_password(silent=True)
        
    def toggle_visibility(self):
        """Toggle password visibility"""
        self.show_password = not self.show_password
        self.password_entry.config(show="" if self.show_password else "●")
        self.toggle_btn.config(fg=Config.ACCENT_COLOR if self.show_password 
                              else Config.SECONDARY_TEXT)
        
    def analyze_password(self, silent=False):
        """Analyze password and update UI"""
        password = self.password_var.get()
        
        if not password:
            return
        
        # Run analysis
        self.current_analysis = self.analyzer.analyze(password)
        
        if not silent:
            self.animator.shake_widget(self.entry_frame, intensity=3)
        
        self.update_display()
        
    def update_display(self):
        """Update all UI elements with analysis results"""
        if not self.current_analysis:
            return
            
        analysis = self.current_analysis
        
        # Update strength label with color
        strength = analysis['strength']
        score = analysis['score']
        
        color = Config.DANGER_COLOR
        if score >= 80: color = Config.SUCCESS_COLOR
        elif score >= 60: color = Config.WARNING_COLOR
        elif score >= 40: color = "#ffdd00"
        
        self.strength_label.config(text=f"Strength: {strength}",
                                   fg=color)
        
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
            for pattern in analysis['patterns']:
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
        self.status_label.config(text=f"Last analyzed: {datetime.now().strftime('%H:%M:%S')}")
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def run(self):
        """Start the application"""
        self.root.mainloop()
        self.animator.stop()

# ==================== OPTIMIZATION COMMANDS ====================
"""
OPTIMIZATION & PROFESSIONAL ENHANCEMENT COMMANDS:

1. COMPILE TO EXECUTABLE (PyInstaller):
   pip install pyinstaller
   pyinstaller --onefile --windowed --icon=lock.ico --name="PasswordAnalyzer" password_checker.py

2. OPTIMIZED BUILD (Smaller, Faster):
   pyinstaller --onefile --windowed --strip --upx-dir=/path/to/upx --name="PasswordAnalyzer" password_checker.py

3. CREATE REQUIREMENTS FILE:
   pip freeze > requirements.txt

4. OPTIMIZE WITH CYPTHON:
   pip install cython
   cythonize -i password_checker.py

5. MEMORY PROFILING:
   pip install memory_profiler
   python -m memory_profiler password_checker.py

6. PERFORMANCE PROFILING:
   python -m cProfile -o stats.prof password_checker.py

7. CODE QUALITY CHECK:
   pip install pylint black flake8
   pylint password_checker.py
   black password_checker.py
   flake8 password_checker.py

8. SECURITY SCAN:
   pip install bandit
   bandit -r password_checker.py

9. CREATE INSTALLER (Windows):
   pip install innosetup
   # Create .iss script and compile

10. VIRTUAL ENVIRONMENT SETUP:
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    pip install -r requirements.txt
"""

# ==================== ENTRY POINT ====================
if __name__ == "__main__":
    app = PasswordStrengthChecker()
    app.run()