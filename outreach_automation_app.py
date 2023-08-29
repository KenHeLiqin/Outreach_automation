# app.py
import streamlit as st
import pandas as pd
from io import StringIO
import re


def remove_special_characters_and_numbers(input_str):
    # Remove all characters that are not alphabets
    clean_str = re.sub(r'[^a-zA-Z\s]', '', input_str)
    return clean_str

def create_outreach_record_df(input_data, include_greet_meesage=False, greet_message=""):
    """
    This function takes in a string of outreach data and returns a DataFrame with the parsed data.
    """

    # Initialize an empty list to store the names
    names_list, url_list = [],[]

    # Split the input string by lines
    for line in input_data.split("\n"):
        # Split each line by the '|' character
        parts = line.split(" | ")

        # The name is the second element in the 'parts' list, strip leading and trailing whitespaces
        url = parts[0].strip()
        name = remove_special_characters_and_numbers(parts[1]).strip()
        
        # Append the name to the list
        names_list.append(name)
        url_list.append(url)

    # Create a DataFrame with the names list
    outreach_record_df = pd.DataFrame({"Name":names_list, "Who?":by_who, "LinkedIn Profile":url_list})

    # Add a column with the greet message
    if include_greet_meesage:
        outreach_record_df['greet_message'] = outreach_record_df['Name'].apply(lambda x: greet_message.replace('[firstname]', x.split(' ')[0]) if type(x) == str else np.nan)

    return outreach_record_df

greet_message = ""
by_who = ""

### Streamlit App ###

# Create a title and text
st.title("Automate Your Linkedin Outreach")
st.text("Need to download the One Tap extension first")


st.markdown("## Step 1: Create a greet message")

# Create a selectbox with a label and options


# Options for the user selected_option
include_greet_message = st.checkbox("Include a greet message?")


if include_greet_message:
    user_input = st.text_input("")

    if user_input == "esger":
        selected_option = st.selectbox('You are?', ('Others', 'Ken'))

        if selected_option == "Ken":
            by_who = "Ken"
            greet_message = "Hi, [firstname]! I am Ken, the co-founder at Esger, an NYC startup. We just raised $250k+ and support from top institutions like Cornell, Microsoft, and ERA. As we are using AI to tackle the heart of sustainability issues, the supply chain, I love to connect with experts in the field (like you!)."
        elif selected_option == "Others":
            by_who = st.text_input("Whats your name:")
            greet_message = st.text_area("(optional) Whats your greet message: Need to contain [firstname]")

        # check if greet_message is empty
        if greet_message == "":
            greet_message = f"Hi, [firstname]! I am {by_who}, the co-founder at Esger, an NYC startup. We just raised $250k+ and support from top institutions like Cornell, Microsoft, and ERA. As we are using AI to tackle the heart of sustainability issues, the supply chain, I love to connect with experts in the field (like you!)."
            st.write("Greet message (default):", greet_message)
        else :
            st.write("The greet message is:", greet_message)
else:
    by_who = st.text_input("You are?")


st.write("")
st.markdown("## Step 2: Paste the URL and Export the CSV file")

user_input = st.text_area("Exported URL from One Tap:")

if st.button('Process the outreach data'):
    outreach_record_df = create_outreach_record_df(user_input, include_greet_message, greet_message)
    # Display the DataFrame
    st.write('Dataframe:', outreach_record_df)

    # Generate a CSV file
    csv_buffer = StringIO()
    outreach_record_df.to_csv(csv_buffer, index=False)
    csv_str = csv_buffer.getvalue()

    # Add a button to download the CSV file
    st.download_button(
        'Download Outreach Record',
        csv_str,
        file_name='Outreach_Record.csv',
        mime='text/csv'
    )




