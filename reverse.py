import streamlit as st

def reverse_string(input_string):
    return input_string[::-1].capitalize()

def main():
    st.title("Reverse String App")
    input_string = st.text_input("Enter a string:")
    
    if st.button("Reverse"):
        if input_string.strip():  # Check if the input string is not empty or contains only whitespace
            reversed_string = reverse_string(input_string)
            st.write("Reversed string:", reversed_string)
        else:
            st.warning("Please enter a non-empty string to reverse.")

if __name__ == "__main__":
    main()
