import requests
import subprocess
import os
import json

key = "AIzaSyDQGJkcR7kNC7H_uyFQQW-f39fRpvBbTvE"
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + key

def speak(text):
    try:
        subprocess.run(['espeak', text])
    except:
        pass

def flashlight_on():
    try:
        subprocess.run(['termux-torch', 'on'])
        return "Flashlight activated Sir"
    except:
        return "Cannot control flashlight Sir"

def flashlight_off():
    try:
        subprocess.run(['termux-torch', 'off'])
        return "Flashlight deactivated Sir"
    except:
        return "Cannot control flashlight Sir"

def check_battery():
    try:
        result = subprocess.run(['termux-battery-status'], capture_output=True, text=True)
        return "Battery status: " + result.stdout
    except:
        return "Cannot check battery Sir"

def vibrate_phone():
    try:
        subprocess.run(['termux-vibrate'])
        return "Phone vibrated Sir"
    except:
        return "Cannot vibrate phone Sir"

def volume_up():
    try:
        subprocess.run(['termux-volume', 'music', '+5'])
        return "Volume increased Sir"
    except:
        return "Cannot control volume Sir"

def volume_down():
    try:
        subprocess.run(['termux-volume', 'music', '-5'])
        return "Volume decreased Sir"
    except:
        return "Cannot control volume Sir"

def take_photo():
    try:
        subprocess.run(['termux-camera-photo', 'jarvis_photo.jpg'])
        return "Photo captured Sir"
    except:
        return "Cannot access camera Sir"

def get_location():
    try:
        result = subprocess.run(['termux-location'], capture_output=True, text=True)
        return "Location: " + result.stdout
    except:
        return "Cannot get location Sir"

def send_notification(title, message):
    try:
        subprocess.run(['termux-notification', '--title', title, '--content', message])
        return "Notification sent Sir"
    except:
        return "Cannot send notification Sir"

def device_control(command):
    cmd = command.lower()
    
    if "flashlight on" in cmd or "torch on" in cmd:
        return flashlight_on()
    elif "flashlight off" in cmd or "torch off" in cmd:
        return flashlight_off()
    elif "battery" in cmd:
        return check_battery()
    elif "vibrate" in cmd:
        return vibrate_phone()
    elif "volume up" in cmd:
        return volume_up()
    elif "volume down" in cmd:
        return volume_down()
    elif "take photo" in cmd or "camera" in cmd:
        return take_photo()
    elif "location" in cmd:
        return get_location()
    elif "notification" in cmd:
        return send_notification("JARVIS", "Test notification from JARVIS")
    
    return None

def ask_gemini(message):
    device_response = device_control(message)
    if device_response:
        return device_response
    
    system_prompt = "You are JARVIS, Tony Stark's AI assistant. You are intelligent, helpful, and slightly witty. Address the user as 'Sir' occasionally. Keep responses concise but informative."
    
    full_prompt = system_prompt + " User question: " + message
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": full_prompt
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "API error Sir. Status: " + str(response.status_code)
    except requests.exceptions.RequestException:
        return "Connection error Sir. Please check internet."
    except Exception as e:
        return "Unexpected error Sir: " + str(e)

def show_help():
    return """JARVIS Commands Available:

AI Features:
- Ask any question for intelligent responses
- Get help with tasks and planning  
- Have natural conversations

Device Control:
- 'flashlight on/off' or 'torch on/off' - Control flashlight
- 'battery' - Check battery status and level
- 'vibrate' - Make phone vibrate
- 'volume up/down' - Adjust media volume
- 'take photo' or 'camera' - Capture image
- 'location' - Get current GPS location
- 'notification' - Send test notification

System Commands:
- 'help' - Show this help menu
- 'mute' - Toggle voice output on/off
- 'clear' - Clear screen
- 'exit', 'quit', 'bye' - Shutdown JARVIS

Examples:
- What's the weather like?
- flashlight on
- tell me a joke
- battery status
- help me plan my day"""

def main():
    os.system('clear')
    
    print("=" * 60)
    print("        JARVIS AI Assistant - Full Version")
    print("=" * 60)
    print("Status: Online and ready for commands")
    print("Voice: Enabled (say 'mute' to toggle)")
    print("AI Model: Google Gemini 1.5 Flash")
    print("Device Control: Active")
    print("")
    print("Hello Sir! I'm JARVIS, your personal AI assistant.")
    print("I can answer questions, control your device, and assist")
    print("with various tasks. Say 'help' for available commands.")
    print("=" * 60)
    
    voice_enabled = True
    conversation_history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                response = "I'm listening Sir. Please give me a command or question."
                print("JARVIS:", response)
                if voice_enabled:
                    speak("I'm listening Sir")
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye', 'shutdown']:
                response = "Shutting down all systems. It was a pleasure serving you, Sir. Goodbye!"
                print("JARVIS:", response)
                if voice_enabled:
                    speak(response)
                break
            
            elif user_input.lower() == 'mute':
                voice_enabled = not voice_enabled
                status = "enabled" if voice_enabled else "disabled"
                response = "Voice output " + status + " Sir."
                print("JARVIS:", response)
                if voice_enabled:
                    speak(response)
                continue
            
            elif user_input.lower() == 'help':
                help_info = show_help()
                print("JARVIS:", help_info)
                if voice_enabled:
                    speak("Help information displayed Sir")
                continue
            
            elif user_input.lower() == 'clear':
                os.system('clear')
                print("JARVIS: Screen cleared Sir.")
                if voice_enabled:
                    speak("Screen cleared Sir")
                continue
            
            elif user_input.lower() == 'history':
                if conversation_history:
                    print("JARVIS: Recent conversation history:")
                    for i, item in enumerate(conversation_history[-5:], 1):
                        print(str(i) + ". " + item)
                else:
                    print("JARVIS: No conversation history yet Sir.")
                continue
            
            print("JARVIS: Processing your request Sir...")
            
            response = ask_gemini(user_input)
            print("JARVIS:", response)
            
            conversation_history.append("Q: " + user_input[:50] + "...")
            conversation_history.append("A: " + response[:50] + "...")
            
            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]
            
            if voice_enabled:
                speak(response)
                
        except KeyboardInterrupt:
            print("
JARVIS: Keyboard interrupt detected. Shutting down gracefully.")
            print("JARVIS: Until next time Sir!")
            break
        
        except Exception as e:
            error_message = "An unexpected error occurred Sir. System still operational."
            print("JARVIS:", error_message)
            if voice_enabled:
                speak(error_message)

if __name__ == "__main__":
    main()
