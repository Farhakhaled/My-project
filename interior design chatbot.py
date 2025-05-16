#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Function to interact with Gemini API
def ask_gemini(prompt, api_key):
    url = "api_key_url"# it is private key 
    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, params=params, json=data)
        response_json = response.json()
        
        if "candidates" in response_json and response_json["candidates"]:
            parts = response_json["candidates"][0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "No response received.")
        return "No response received."
    except Exception as e:
        return f"Error: {str(e)}"

# GUI Implementation
class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Interior Design Chatbot")
        self.root.geometry("500x600")
        self.root.configure(bg="#2C3E50")
        
        self.chat_frame = tk.Frame(root, bg="#2C3E50")
        self.chat_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame, wrap=tk.WORD, bg="#ECF0F1", fg="#2C3E50", 
            font=("Arial", 12), height=20, bd=5, relief=tk.FLAT
        )
        self.chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        self.entry_frame = tk.Frame(root, bg="#2C3E50")
        self.entry_frame.pack(pady=5, padx=10, fill=tk.X)
        
        self.entry = tk.Entry(self.entry_frame, font=("Arial", 14), width=40, bd=3, relief=tk.GROOVE)
        self.entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.entry.bind("<Return>", self.send_message)
        
        self.send_button = tk.Button(
            self.entry_frame, text="Send", font=("Arial", 12), bg="#2980B9", fg="white", 
            activebackground="#3498DB", relief=tk.RAISED, bd=3, padx=10, pady=5,
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT, padx=5)
        
        self.clear_button = tk.Button(
            root, text="Clear Chat", font=("Arial", 12), bg="#E74C3C", fg="white", 
            activebackground="#C0392B", relief=tk.RAISED, bd=3, padx=10, pady=5,
            command=self.clear_chat
        )
        self.clear_button.pack(pady=5, padx=10, fill=tk.X)
        
        self.api_key = "AIzaSyCLMpz2irdNASTsAmWBuVO19kIjTzsWc5U"   
        
    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            messagebox.showwarning("Warning", "Please enter a message first!")
            return
        
        self.entry.delete(0, tk.END)
        self.update_chat(f"🛋️ You: {user_input}", "#3498DB")
        response = ask_gemini(user_input, self.api_key)
        self.update_chat(f"🎨 AI Interior Bot: {response}", "#2ECC71")
        
    def update_chat(self, message, color):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n\n", (color,))
        self.chat_display.tag_configure(color, foreground=color)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)
    
    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()

