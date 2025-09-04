#!/usr/bin/env python3
"""
Empathetic Journaling App - Terminal MVP
A simple, reliable terminal-based journaling app.
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models"
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Check if token is available
if not HF_TOKEN:
    print("ERROR: HUGGINGFACE_TOKEN environment variable not set!")
    print("Please create a .env file with: HUGGINGFACE_TOKEN=your_token_here")
    print("Or set the environment variable directly.")
    exit(1)

# Models
SENTIMENT_MODEL = "VinMir/GordonAI-emotion_detection"
TEXT_GENERATION_MODEL = "facebook/blenderbot-400M-distill" # More reliable, faster model

def analyze_sentiment(text):
    """Analyze sentiment using Hugging Face API with fallback"""
    try:
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json",
        }
        
        payload = {"inputs": text}
        
        print("Analyzing sentiment...")
        response = requests.post(
            f"{HF_API_URL}/{SENTIMENT_MODEL}",
            headers=headers,
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0 and len(data[0]) > 0:
                sentiment = max(data[0], key=lambda x: x['score'])
                label = sentiment['label']
                
                if label in ['LABEL_2', 'POSITIVE']:
                    return 'POSITIVE'
                elif label in ['LABEL_0', 'NEGATIVE']:
                    return 'NEGATIVE'
                else:
                    return 'NEUTRAL'
        
        print(f"Sentiment API failed: {response.status_code}")
        return 'NEUTRAL'
        
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return 'NEUTRAL'

def generate_ai_reflection(responses, sentiment):
    """Generate AI reflection using microsoft/chatbench-distilgpt2"""
    try:
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json",
        }
        
        # Create a simple prompt
        user_a = responses[0] if len(responses) > 0 else "uncertain"
        user_b = responses[1] if len(responses) > 1 else "various factors"
        user_c = responses[2] if len(responses) > 2 else "limited"
        user_d = responses[3] if len(responses) > 3 else "a while"
        user_e = responses[4] if len(responses) > 4 else "taking care of yourself"
        
        # Create a simple prompt for chatbench-distilgpt2
        prompt = f"I feel {user_a} about {user_b}. I have {user_c} control over this situation that has been going on for {user_d}. My positive action today is to {user_e}. A compassionate reflection would be:"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 100,
                "temperature": 0.8,
                "do_sample": True,
                "top_p": 0.9
            }
        }
        
        print("Generating AI reflection...")
        print(f"   Using model: {TEXT_GENERATION_MODEL}")
        print(f"   Prompt: {prompt[:100]}...")
        
        # Try with retry logic for better reliability
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    f"{HF_API_URL}/{TEXT_GENERATION_MODEL}",
                    headers=headers,
                    json=payload,
                    timeout=45  # Longer timeout
                )
                break
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"   Timeout on attempt {attempt + 1}, retrying...")
                    continue
                else:
                    print("   Max retries reached, giving up")
                    return None
        
        print(f"   Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response data: {data}")
            if data and len(data) > 0:
                generated_text = data[0].get('generated_text', '')
                print(f"   Generated text: {generated_text}")
                
                # Clean up the text - remove the prompt
                reflection = generated_text.replace(prompt, "").strip()
                reflection = reflection.replace("\n", " ").strip()
                
                if reflection and len(reflection) > 10:
                    print(f"AI generation successful!")
                    print(f"   Generated: {reflection}")
                    return reflection
                else:
                    print(f"   Generated text too short: '{reflection}'")

        
        print(f"AI generation failed: {response.status_code}")
        if response.status_code != 200:
            print(f"   Error response: {response.text}")
        return None
        
    except Exception as e:
        print(f"AI generation error: {e}")
        return None

def generate_template_reflection(responses, sentiment):
    """Generate a template-based reflection"""
    user_a = responses[0] if len(responses) > 0 else "uncertain"
    user_b = responses[1] if len(responses) > 1 else "various factors"
    user_c = responses[2] if len(responses) > 2 else "limited"
    user_d = responses[3] if len(responses) > 3 else "a while"
    user_e = responses[4] if len(responses) > 4 else "taking care of yourself"
    
    return f"""Today, it seems like your heart is feeling a bit {user_a}. This feeling has been lingering for {user_d}, and it seems to be tied to {user_b}. It's completely understandable to feel stressed when you believe you have {user_c} control over the situation. But it's great that you've thought about a small action to take for yourself: {user_e}. That's a powerful first step towards taking care of yourself and moving forward with compassion."""

def show_menu():
    """Display the main menu"""
    print("=" * 60)
    print("EMPATHETIC JOURNALING APP")
    print("=" * 60)
    print()
    print("What would you like to do today?")
    print()
    print("1. Make your own entry")
    print("2. Unwind")
    print()
    print("=" * 60)

def make_own_entry():
    """Let user write their own journal entry"""
    print("\nMAKE YOUR OWN ENTRY")
    print("-" * 30)
    print("Write whatever is on your mind...")
    print("(Press Enter twice when finished)")
    print()
    
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    
    entry = "\n".join(lines[:-1])  # Remove the last empty line
    print(f"\nYour entry has been saved!")
    print(f"Entry: {entry[:100]}{'...' if len(entry) > 100 else ''}")
    print("\nThank you for sharing your thoughts!")

def unwind_session():
    """Guided unwind session with AI responses"""
    print("\nUNWIND SESSION")
    print("-" * 30)
    print("Let's take a moment to reflect and unwind...")
    print()
    
    # Unwind prompts
    prompts = [
        "How are you feeling right now? (e.g., anxious, sad, overwhelmed, hopeful, etc.)",
        "What's causing you stress or concern today?",
        "How much control do you feel you have over this situation? (e.g., none, some, a lot)",
        "How long have you been feeling this way? (e.g., a few hours, days, weeks)",
        "What's one small positive action you can take for yourself today?"
    ]
    
    responses = []
    
    # Collect responses
    for i, prompt in enumerate(prompts, 1):
        print(f"Question {i}/5:")
        print(f"   {prompt}")
        response = input("   Your response: ").strip()
        responses.append(response)
        print()
    
    # Analyze sentiment
    combined_text = " ".join(responses)
    sentiment = analyze_sentiment(combined_text)
    print(f"Detected sentiment: {sentiment}")
    print()
    
    # Generate reflection
    print("Generating your personalized reflection...")
    print("-" * 40)
    
    # Try AI generation first
    ai_reflection = generate_ai_reflection(responses, sentiment)
    
    if ai_reflection:
        print("AI-Generated Reflection:")
        print(ai_reflection)
    else:
        print("Template-Based Reflection:")
        template_reflection = generate_template_reflection(responses, sentiment)
        print(template_reflection)
    
    print()
    print("-" * 40)
    print("Thank you for taking time to unwind today!")
    print("Remember: Every small step towards self-care matters.")

def main():
    """Main application loop"""
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1 or 2): ").strip()
            
            if choice == "1":
                make_own_entry()
            elif choice == "2":
                unwind_session()
            else:
                print("\nInvalid choice. Please enter 1 or 2.")
                continue
            
            print("\n" + "=" * 60)
            another = input("Would you like to do something else? (y/n): ").strip().lower()
            if another not in ['y', 'yes']:
                break
                
        except KeyboardInterrupt:
            print("\n\nGoodbye! Take care of yourself.")
            break
        except EOFError:
            print("\n\nGoodbye! Take care of yourself.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.")
    
    print("\nThank you for using the Empathetic Journaling App!")
    print("Take care of yourself!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! Take care of yourself.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please try again later.")
        