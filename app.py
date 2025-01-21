import streamlit as st
import random
import string
from password_strength import PasswordPolicy

# Define password policy
policy = PasswordPolicy.from_names(
    length=12,  # min length: 12
    uppercase=2,  # need min. 2 uppercase letters
    numbers=1,  # need min. 1 digit
    special=1,  # need min. 1 special character
    nonletters=1,  # need min. 1 non-letter character (digits, specials, anything)
)

# Function to check the strength of a password
def check_password_strength(password):
    # Check if the password meets the policy
    violations = policy.test(password)
    strength = "Strong"
    if violations:
        strength = "Weak"
    return strength, violations

# Function to generate a random strong password
def generate_strong_password(length=16):
    # Password with a mix of upper, lower, digits, and special characters
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_characters) for i in range(length))
    return password

# Streamlit App
def app():
    # Reduce top padding using markdown and custom CSS
    st.markdown("""
    <style>
    body { padding-top: 0px; }
    .block-container {
        max-width: 1000px;  /* Increase content width */
        margin: auto;
    }
    .stSlider {
        width: 600px !important;  /* Make the slider shorter */
        margin-right: 20px !important;  /* Add right margin to the slider */
    }
    </style>
""", unsafe_allow_html=True)

    # Title and intro section
    st.title("Password Generator & Strength Analyzer")
    st.markdown(
        """Use the tool below to check the strength of your password and see how you can improve it.
        """
    )

    # Create two columns for better layout: Enter Password and Feedback on the right
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Enter Password to Analyze")
        password_input = st.text_input("Enter Password:", "")

        if password_input:
            # Check password strength and display result
            strength, violations = check_password_strength(password_input)
            if strength == "Strong":
                st.markdown(f"<span style='color:green;'>🔒 Strong password!</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:red;'>⚠️ Weak password!</span>", unsafe_allow_html=True)

    with col2:
        # Feedback and Suggestions (move to the right with the password input)
        st.subheader("Feedbacks")
        if password_input:
            # Check password strength and display result
            strength, violations = check_password_strength(password_input)
            if strength == "Weak":
                st.write("Your password is weak. Consider the following suggestions:")
                for violation in violations:
                    st.write(f"- {violation}")
            else:
                st.write("Great! Your password is strong.")

    # Password generator
    st.subheader("Generate a Strong Password")
    password_length = st.slider("Choose Password Length", min_value=8, max_value=32, value=16)
    
    if st.button("Generate Password"):
        strong_password = generate_strong_password(password_length)
        st.code(strong_password, language="plaintext")
        
    # Security best practices
    st.markdown("### **Security Best Practices**")
    st.write(
        """
        1. Use a mix of uppercase, lowercase, numbers, and special characters.
        2. Avoid using easily guessable words (e.g., "password" or your name).
        3. Make your password at least 12 characters long.
        """
    )

# Run the Streamlit app
if __name__ == "__main__":
    app()
