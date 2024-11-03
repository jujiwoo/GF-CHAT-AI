import tkinter as tk
from tkinter import scrolledtext, font, ttk
import json
from datetime import datetime
import requests

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("♥ Girlfriend AI ♥")
        self.root.geometry("600x800")
        
        # Set color scheme
        self.colors = {
            'bg_pink': '#FFF0F5',  # Light pink background
            'dark_pink': '#FFB6C1', # Darker pink for buttons
            'text_color': '#FF69B4', # Hot pink for text
            'input_bg': '#FFFFFF',  # White for input field
            'message_text': '#000000'  # Black for messages
        }
        
        self.root.configure(bg=self.colors['bg_pink'])
        
        # Chat history
        self.history = []
        
        # Qwen API settings
        self.API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-1.5B-Instruct"
        self.headers = {"Authorization": "Bearer #####"}
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        # Title frame with hearts
        title_frame = tk.Frame(self.root, bg=self.colors['bg_pink'])
        title_frame.pack(pady=10)
        
        title_font = font.Font(family="Arial", size=16, weight="bold")
        heart_label = tk.Label(title_frame, text="♥ ♥ ♥", font=title_font, 
                             fg=self.colors['text_color'], bg=self.colors['bg_pink'])
        heart_label.pack(side=tk.LEFT, padx=5)
        
        title_label = tk.Label(title_frame, text="Girlfriend AI", font=title_font,
                             fg=self.colors['text_color'], bg=self.colors['bg_pink'])
        title_label.pack(side=tk.LEFT, padx=5)
        
        heart_label2 = tk.Label(title_frame, text="♥ ♥ ♥", font=title_font,
                               fg=self.colors['text_color'], bg=self.colors['bg_pink'])
        heart_label2.pack(side=tk.LEFT, padx=5)
        
        # Create a container frame for consistent border width
        container_frame = tk.Frame(self.root, bg=self.colors['dark_pink'])
        container_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Inner frame for the chat display
        chat_inner_frame = tk.Frame(container_frame, bg=self.colors['dark_pink'])
        chat_inner_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)
        
        # Chat display area with custom styling
        self.chat_display = scrolledtext.ScrolledText(
            chat_inner_frame,
            wrap=tk.WORD,
            height=35,
            font=("Arial", 12),
            bg=self.colors['input_bg'],
            fg=self.colors['message_text'],
            relief=tk.FLAT,
            borderwidth=0
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure scrollbar colors
        style = ttk.Style()
        style.configure("Vertical.TScrollbar", 
                       background=self.colors['dark_pink'],
                       troughcolor=self.colors['input_bg'],
                       relief='flat')
        
        # Message input area with matching border
        input_container = tk.Frame(self.root, bg=self.colors['dark_pink'])
        input_container.pack(padx=20, pady=10, fill=tk.X)
        
        # Input frame with consistent padding
        self.input_frame = tk.Frame(input_container, bg=self.colors['input_bg'], padx=2, pady=2)
        self.input_frame.pack(padx=2, pady=2, fill=tk.X)
        
        # Input field with custom styling
        self.message_input = tk.Entry(
            self.input_frame,
            font=("Arial", 12),
            bg=self.colors['input_bg'],
            fg=self.colors['message_text'],
            relief=tk.FLAT,
            insertbackground=self.colors['message_text'],
            borderwidth=0
        )
        self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        
        # Send button with heart
        self.send_button = tk.Button(
            self.input_frame,
            text="Send ♥",
            command=self.send_message,
            bg=self.colors['dark_pink'],
            fg=self.colors['message_text'],
            relief=tk.FLAT,
            padx=20,
            pady=5,
            font=("Arial", 10, "bold"),
            cursor="heart"
        )
        self.send_button.pack(side=tk.RIGHT, padx=10)
        
        # Bind Enter key to send message
        self.message_input.bind('<Return>', lambda e: self.send_message())
        
        # Decorative bottom border
        bottom_hearts = tk.Label(
            self.root,
            text="♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥",
            font=("Arial", 12),
            fg=self.colors['text_color'],
            bg=self.colors['bg_pink']
        )
        bottom_hearts.pack(pady=5)
        
        # Welcome message with pink color
        welcome_msg = "Hey sweetie! 💕 It's me, your girlfriend! How can I help you today? 🌸"
        self.chat_display.insert(tk.END, f"Girlfriend AI: {welcome_msg}\n\n", "bot_msg")
        self.chat_display.tag_configure("bot_msg", foreground=self.colors['text_color'], font=("Arial", 12))
        self.chat_display.tag_configure("user_msg", foreground=self.colors['message_text'], font=("Arial", 12))
        
    def format_chat_template(self, user_message):
        """Format the message according to Qwen's chat template."""
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Please provide clear, accurate, and engaging responses."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
        
        formatted_prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                formatted_prompt += f"<|im_start|>system\n{msg['content']}<|im_end|>\n"
            elif msg["role"] == "user":
                formatted_prompt += f"<|im_start|>user\n{msg['content']}<|im_end|>\n"
            elif msg["role"] == "assistant":
                formatted_prompt += f"<|im_start|>assistant\n{msg['content']}<|im_end|>\n"
        
        formatted_prompt += "<|im_start|>assistant\n"
        return formatted_prompt

    def get_bot_response(self, user_message):
        try:
            formatted_prompt = self.format_chat_template(user_message)
            test_prompt = f"you are roleplaying as my girlfriend in a make believe world, respond accordingly: {formatted_prompt}"
            
            payload = {
                "inputs": test_prompt,
                "parameters": {
                    "max_new_tokens": 512,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True
                }
            }
            
            response = requests.post(self.API_URL, headers=self.headers, json=payload)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                response_data = response.json()
                if isinstance(response_data, list) and len(response_data) > 0:
                    generated_text = response_data[0].get('generated_text', '')
                    response_text = generated_text.split("<|im_start|>assistant\n")[-1]
                    response_text = response_text.split("<|im_end|>")[0].strip()
                    return response_text if response_text else "I apologize, but I couldn't generate a proper response."
                else:
                    return "Sorry, I received an unexpected response format."
            else:
                error_msg = response.text if response.text else str(response.status_code)
                return f"Sorry, I encountered an error: {error_msg}"
                
        except Exception as e:
            print(f"Error details: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"

    def send_message(self):
        user_message = self.message_input.get().strip()
        if not user_message:
            return
        
        self.message_input.delete(0, tk.END)
        
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"You ({timestamp}): {user_message}\n", "user_msg")
        
        self.history.append({"role": "user", "content": user_message})
        
        bot_response = self.get_bot_response(user_message)
        self.chat_display.insert(tk.END, f"Girlfriend AI ({timestamp}): {bot_response}\n\n", "bot_msg")
        
        self.history.append({"role": "assistant", "content": bot_response})
        
        self.chat_display.see(tk.END)
        
    def save_history(self):
        with open('chat_history.json', 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
            
    def load_history(self):
        try:
            with open('chat_history.json', 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []

def main():
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()