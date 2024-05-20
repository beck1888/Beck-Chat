import streamlit as st
from datetime import datetime

# Set up page
st.set_page_config("Beck Chat", "src/chat_icon.png", "centered")

# Check if logged in
if "authenticated" not in st.session_state or st.session_state["authenticated"] is False:
    # Login page
    st.title("Beck's Ai Chatbot")
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

        return f"The quotient is **{quotient}**"
    else:
        return "**Error - Command not found:** \"" + original_message + "\""

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