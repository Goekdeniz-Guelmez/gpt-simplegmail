# Samantha web search and email

This project consists of a Python script that utilizes the OpenAI API, Gmail API, and the EdgeGPT library to create a conversational assistant capable of managing emails and performing web searches. The script allows you to interact with the assistant through a command-line interface.

## Setup

To run the script, follow these steps:

1. Install the required Python packages by running the command `pip install openai simplegmail edgegpt`.

2. Obtain an OpenAI API key and set it in the `openai.api_key` variable within the script.

3. Set up the Gmail API by using the `simplegmail` library. Follow the instructions provided by the library to authenticate with your Gmail account and authorize access to the Gmail API.

4. Ensure you have the necessary credentials for the EdgeGPT library if required.

## Functionality

The script provides several functions that you can perform through the conversational assistant:

1. **Sending Emails**: The `send_email` function allows you to send emails. Provide the receiver's email address, subject, plain text body, and HTML formatted body as parameters to send an email.

2. **Getting Unread Emails**: The `get_unread_emails` function retrieves all unread emails from the inbox. It returns a JSON representation of the emails, including the email number, sender, subject, and plain text body.

3. **Deleting Unread Emails**: The `delete_unread_email` function deletes an unread email specified by its email number.

4. **Searching the Web**: The `search` function enables you to perform web searches using BingGPT. Pass the desired search query as a parameter, and the function will return a JSON object containing the Bing summary response and sources.

## Assistant Interaction

The script simulates a conversational assistant by using the OpenAI ChatGPT model. It utilizes the EdgeGPT library for conversation-style interactions. When running the script, you can provide prompts through the command line, and the assistant will respond accordingly. The assistant's responses may include relevant summaries, email handling, or web search results.

## Additional Information

The script includes an Assistant prompt, which sets the context for the assistant's behavior and guides its responses. Feel free to modify this prompt to customize the assistant's persona or add specific instructions.

The `conversations.txt` file is used to store the conversation history between the user and the assistant. Each line in the file represents a message in the conversation, including role (user or assistant) and content.

Please ensure that you comply with the terms of use and guidelines provided by the OpenAI API and Gmail API when using this script.

Enjoy your interaction with the conversational assistant and explore its various functionalities!
