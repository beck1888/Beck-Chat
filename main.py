# Imports block
import streamlit as st
from datetime import datetime
from coders import encrypt, decrypt
import random
import requests
import json
# import os
import socket

# Set up page
st.set_page_config("Beck Chat", "src/chat_icon.png", "centered")

# See which server is used

# Get the hostname to check if running on Streamlit Cloud or localhost
hostname = socket.gethostname()
if "streamlit" in hostname:
    host = "streamlit"
else:
    host = "local"

# Temp bypass login - security setting
bypass_login = True # Set this one
# if bypass_login is True and host == "local":
if bypass_login is True:
    st.session_state["authenticated"] = True
    st.html("<p style=\"color: orange; font-weight: bold; font-size: 20px; text-align: center;\">WARNING: The Lock Screen Is Being Bypassed</p>")
# elif bypass_login is True and host != "local":
#     st.html("<p style=\"color: red; font-weight: bold; font-size: 50px; text-align: center;\">403: Forbidden</p>")
#     st.html("<p style=\"color: black; font-weight: bold; font-size: 20px; text-align: center;\">This app's security settings do not allow for the login page to be skipped on public servers./p>")
#     st.stop()

# Initialize session states
if "special" not in st.session_state:
    st.session_state["special"] = "not active"

# Check if logged in
if "authenticated" not in st.session_state or st.session_state["authenticated"] is False:
    # Login page/lock screen
    st.title("Beck's AI Chatbot")
    with st.form("login", clear_on_submit=False, border=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.form_submit_button("Login"):
            if username == st.secrets["USERNAME"]:
                if password == st.secrets["PASSWORD"]:
                    st.session_state["authenticated"] = True
                    st.session_state.chat_history = [] # Initialize chat history
                    st.session_state.chat_history.append({"message": None, "response": "Welcome back! What can I help you with?"}) # Append a welcome message to history
                    st.rerun()
                else:
                    st.error("Incorrect password")
            else:
                st.error("Incorrect username")
    # Version info
    with open("version.json", "r") as v:
        version = json.load(v)
        version_info = f"""
    Last updated: {version["month"].capitalize()}-{version["day"]}-{version["year"]} at {version["hour"]}:{version["minute"]} {version["meridian"].upper()} | Commit: {version["change-word"].capitalize()}
    Hostname: {hostname}"""
    st.text(version_info)

# Response helper functions
# Function for getting a meme
def get_a_meme():
    # Get the json data
    with open('memes.json', 'r') as f:
        data = json.load(f)

    # List to hold the paths
    paths = []

    # Extract 'path' from each dictionary in the list
    for item in data:
        paths.append(item['path'])

    # Pick a random path
    url_fragment = random.sample(paths, 1)[0]

    # Add start of url to the picked fragment
    full_url = f"https://raw.githubusercontent.com/deep5050/programming-memes/main/{url_fragment}"
    # import os; os.system(f"open -a \"Google Chrome\" {full_url}")
    
    # Return the random url in full
    return full_url

# Reply logic
def reply(message: str):
    # Preserve a copy of the original message
    original_message = message

    # Make the message lowercase for more accurate processing
    message = message.lower()

    # Process special states if any
    if st.session_state["special"] == "called encrypt":
        st.session_state["key"] = message
        st.session_state["special"] = "encrypt - key loaded"
        return "I've loaded your key. Now, please paste the plain text below and press enter."
    elif st.session_state["special"] == "called decrypt":
        st.session_state["key"] = message
        st.session_state["special"] = "decrypt - key loaded"
        return "Awesome, I've learned the key. Please paste your encrypted message below and press enter."
    elif st.session_state["special"] == "encrypt - key loaded":
        encrypted_text = encrypt(message, st.session_state["key"])
        st.session_state["key"] = ""
        st.session_state["special"] = ""
        return f"**Here is the encrypted message:** \n\n {encrypted_text}"
    elif st.session_state["special"] == "decrypt - key loaded":
        decrypted_text = decrypt(message, st.session_state["key"])
        st.session_state["key"] = ""
        st.session_state["special"] = ""
        return f"**Here is the decrypted message:** \n\n {decrypted_text}"
    elif st.session_state["special"] == "punchline_wait":
        punchline = st.session_state["punchline"]
        st.session_state["punchline"] = ""

        st.session_state["special"] = ""

        return punchline
    
    # Response logic (expect lowercase)
    if message == "exit": # Special command
        st.session_state["authenticated"] = False
        st.rerun()
    elif "what time is it" in message or "what's the time" in message or "whats the time" in message or message == "time":
        return f'It is {datetime.now().strftime("%I:%M %p")}'
    elif message == 'bye':
        return 'Did you mean "exit"?'
    elif message in ['hi', 'hi!', 'hello', 'hello!', 'yo', 'yo!']:
        return "Hello!"
    elif message == "cow":
        return "$RESPONSE_TYPE_IMAGE-src/cow.webp-$TEXT_BREAK-Sure, here's a picture of a **cow!**"
    elif "mario" in message:
        return "$RESPONSE_TYPE_IMAGE-src/mario.png-$TEXT_BREAK-Here's an image of **Mario**, *a popular character from Nintendo's many video games and movies.*"
    elif message == "tree":
        return "$RESPONSE_TYPE_IMAGE-src/tree.jpeg-$TEXT_BREAK-This is a **tree**, *a vital life form on earth.*"
    elif  "homer" in message:
        return "$RESPONSE_TYPE_IMAGE-src/homer.jpg-$TEXT_BREAK-**Homer Simpson** is a character from the TV Show 'The Simpsons'. Here is what he looks like."
    elif message[0] in "+-*/": # Check if first char is calling for an operation based on the last result
        # Make sure previous result exists
        if "last_calc" not in st.session_state:
            return "You don't have any past calculation to evaluate!"
        
        operation = message [0]

        num1 = st.session_state["last_calc"]
        part2 = message.split(operation)[1]

        num2 = ''
        for char in part2:
            if char in "0123456789.":
                num2 += char
        num2 = float(num2)

        if operation == "+":
            result = num1 + num2
            operation = "sum"
        elif operation == "*":
            result = num1 * num2
            operation = "product"
        elif operation == "-":
            result = num1 - num2
            operation = "difference"
        elif operation == "/":
            result = num1 / num2
            operation = "quotient"

        if result.is_integer() is True:
            result = int(result)

        st.session_state["last_calc"] = result
        return f"The {operation} is {result}"
    
    elif "+" in message: # Add two numbers - SUM
        part1 = message.split("+")[0]
        part2 = message.split("+")[1]

        num1 = ''
        num2 = ''

        for char in part1:
            if char in "0123456789.":
                num1 += char

        for char in part2:
            if char in "0123456789.":
                num2 += char

        num1 = float(num1)
        num2 = float(num2)
        sum = float(num1 + num2)

        # Try to make result into integer if possible
        if sum.is_integer() is True:
            sum = int(sum)

        st.session_state["last_calc"] = sum
        return f"The sum is **{sum}**"
    elif "*" in message: # Multiply two numbers - PRODUCT
        part1 = message.split("*")[0]
        part2 = message.split("*")[1]

        num1 = ''
        num2 = ''

        for char in part1:
            if char in "0123456789.":
                num1 += char

        for char in part2:
            if char in "0123456789.":
                num2 += char

        num1 = float(num1)
        num2 = float(num2)
        product = float(num1 * num2)

        # Try to make result into integer if possible
        if product.is_integer() is True:
            product = int(product)

        st.session_state["last_calc"] = product
        return f"That product is **{product}**"
    elif "-" in message: # Subtract two numbers - DIFFERENCE
        part1 = message.split("-")[0]
        part2 = message.split("-")[1]

        num1 = ''
        num2 = ''

        for char in part1:
            if char in "0123456789.":
                num1 += char

        for char in part2:
            if char in "0123456789.":
                num2 += char

        num1 = float(num1)
        num2 = float(num2)
        difference = float(num1 - num2)

        # Try to make result into integer if possible
        if difference.is_integer() is True:
            difference = int(difference)

        st.session_state["last_calc"] = difference
        return f"The difference is **{difference}**"
    elif "/" in message: # Divide two numbers - QUOTIENT
        part1 = message.split("/")[0]
        part2 = message.split("/")[1]

        num1 = ''
        num2 = ''

        for char in part1:
            if char in "0123456789.":
                num1 += char

        for char in part2:
            if char in "0123456789.":
                num2 += char

        num1 = float(num1)
        num2 = float(num2)
        quotient = float(num1 / num2)

        # Try to make result into integer if possible
        if quotient.is_integer() is True:
            quotient = int(quotient)

        st.session_state["last_calc"] = quotient
        return f"The quotient is **{quotient}**"
    elif message == "encode" or message == "encrypt":
        return "*This feature is under development*"
        st.session_state["special"] = "called encrypt"
        return "Sure, lets encrypt some text! To start, type your key and press enter."
    elif message == "decode" or message == "decrypt":
        return "*This feature is under development*"
        st.session_state["special"] = "called decrypt"
        return "I can help you decode and encrypted message. To start, please send me your key."
    elif "joke" in message or "laugh" in message:
        r = requests.get("https://official-joke-api.appspot.com/random_joke").json()
        setup = r["setup"]
        st.session_state["special"] = "punchline_wait"
        st.session_state["punchline"] = r["punchline"]
        # Adjust end of setup to indicate a continuation if needed
        last_char = setup[-1]
        setup = setup[:-1]
        if last_char != "?":
            setup = setup + "..."
        else:
            setup = setup + "..?"

        return setup
    elif "haha" in message or "lol" in message or "lmao" in message:
        return "I'm glad you liked my joke!"
    elif message == ".insult me": # Has a dot to prevent accidental usage because some are NSFW and one slash is taken by division
        r = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json").json()
        return f"**Here's what I think of you:** \n\n{r["insult"]}"
    elif "fact" in message:
        r = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=e").json()
        return f"**Here is a, probably useless, fact you probably didn't know:** \n\n{r['text']}"
    elif "meme" in message:
        return f"$RESPONSE_TYPE_IMAGE-{get_a_meme()}-$TEXT_BREAK-Here's a great meme for you. Enjoy!"
    # It's unknown what the user wants - no command found
    else:
        unknown_responses = ["I'm not sure what you mean", "I don't understand what that means", "I can't figure out what you're trying to say", "I'm not sure what to do with that"]

        return random.sample(unknown_responses, 1)[0]

# Chatbox
if "authenticated" in st.session_state:
    if st.session_state["authenticated"] == True: # Run the chat program if the session is authenticated
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        msg = st.chat_input("Message Beck's AI")

        if msg:
            if msg == "clear": # Special clear command

                st.session_state.chat_history.clear()
                st.toast("Chat History Cleared!", icon='🧹')
            else:
                response = reply(msg)
                # Store the message and response in chat history
                st.session_state.chat_history.append({"message": msg, "response": response})

        # Display the chat history with respective display formats
        for chat in st.session_state.chat_history:

            if chat["message"] is None: # Allows for blank messages
                pass
            else:
                with st.chat_message("user", avatar='👨🏻'):
                    st.markdown(chat["message"])

            with st.chat_message("ai", avatar='🤖'):
                if "$RESPONSE_TYPE_IMAGE-" in chat["response"]:
                    ai_reply = chat["response"].split("-$TEXT_BREAK-")
                    file_path = ai_reply[0].removeprefix("$RESPONSE_TYPE_IMAGE-")
                    message = ai_reply[1]
                    st.markdown(message)
                    st.image(file_path)
                else:
                    st.markdown(chat["response"])