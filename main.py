import streamlit as st
from datetime import datetime
from coders import encrypt, decrypt
import random

# Set up page
st.set_page_config("Beck Chat", "src/chat_icon.png", "centered")

# Initialize session states
if "special" not in st.session_state:
    st.session_state["special"] = "not active"

# Check if logged in
if "authenticated" not in st.session_state or st.session_state["authenticated"] is False:
    # Login page
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

# if "authenticated" in st.session_state and st.session_state["authenticated"] is True:
#     # Show the content under the chat input element if logged in
#     st.html('<p style="text-align: center; font-style: italic;">This chat may be saved for quality control.</p>')