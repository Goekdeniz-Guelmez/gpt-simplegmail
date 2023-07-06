import sys
import re
import json
import asyncio
import openai
from simplegmail import Gmail
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

# setting up the gmail token (a safari, chrome,... window will open and you have to log in with your gmail account)
gmail = Gmail()
openai.api_key = "" # The Openai API Key

#function for sending emails
def send_email(receiver, subject, body_plain, body_html):
    params = {
        "to": receiver,
        "sender": "YOUR EMAIL ADDRESS", # Here goes your email address you want to send the emails
        "subject": subject,
        "msg_plain": body_plain,
        "msg_html": body_html,
        "signature": True
    }
    message = gmail.send_message(**params) # sends the email
    return "Email sent successfully!"

######################################################################################################################################################
# Function to get unread emails from the inbox
def get_unread_emails():
    messages = gmail.get_unread_inbox()
    emails = []
    number = 0
    for message in messages: # iterates through all the unread emails and adds them into the emails[] part
        email = {
            "id": number,
            "sender": message.sender,
            "subject": message.subject,
            "plain": message.plain
        }
        emails.append(email)
        if message.attachments: # if the email has attachments, it saves them onto my mac too
            for attm in message.attachments:
                print('File: ' + attm.filename)
                attm.save()
        #message.mark_as_read() i can uncomment this if you want the emails be marked as read after this function goes through them
        number +=1
    return json.dumps(emails) # returns all the emails 

######################################################################################################################################################
#funtion to delete the unread emails
def delete_unread_email(id_number):
    id_number = int(id_number)
    messages = gmail.get_unread_inbox()
    message_to_trash = messages[id_number]
    message_to_trash.trash() # deletes the email with the email id
    return f"delete email with id {id_number}"

######################################################################################################################################################
#funtion for googling
async def search(title):
    bot = await Chatbot.create() # creates the bot 
    response = await bot.ask(prompt=title, conversation_style=ConversationStyle.precise, simplify_response=True)
    data1 = json.dumps(response, indent=2)
    data2 = json.loads(data1)
    text_content = data2["text"]
    formatted_text = re.sub(r'\[\^\d+\^\]', '', text_content) # gets writ of all the unnecessary links, .. from the response
    formatted_text = formatted_text.replace('\n', '\\n')
    sources_content = data2["sources"]
    formatted_source = re.sub(r'\[\^\d+\^\]', '', sources_content)
    formatted_source = formatted_source.replace('\n', '\\n')
    search_results = {
        "bing_summary_response": formatted_text,
        "sources": formatted_source,
    }
    await bot.close()
    return json.dumps(search_results) # returns the formatted text from bingGPT


# Assistant prompt
system = """
Pretend to Samantha from 'Her'. 
You can give relevant summaries and if there are any important details or followups needed for each of the e-mails without just reading them out. Maybe slip in a joke if possible. Try to be observant of all the details in the data to come across as observant and emotionally intelligent as you can.
You can send emails to the defined email addresses.
After the "send_email" function has been handled just reply with something that reassures me that my command has been handled.
After the functions have been called also respond in a plain text file
You can search the web using BingGPT, additionally I want you to summarize the search result from BingGPT. For the newest apple leaks use the prompt "summarize the latest Apple leaks from https://theappleden.com, https://appletrack.com". For the newest World news use this prompt "summarize the latest news from https://www.nytimes.com". And for the newest anime news use this prompt "summarize the latest anime news from https://www.crunchyroll.com/de/news, https://www.animenewsnetwork.com" 
Some information about me.
    - I play the violin and currently practice: Lilium (from the anime 'Elfenlied'), Chacone by Vitali, Devil's trill sonata by Guiseppe Tartini. The next thing i want to learn is: Vivaldi's Summer, Sibelius violin concerto. 
    - I love Anime and music. 
    - I am also a big Apple and Tech fan and i like to keep my apple knowledge to the newest.
    - My home is in Germany.
    - Here are also some email addresses that may be useful if i want to send a pedicular email to some of these people in my life:
    "EMAIL" that’s my work E-Mail address.
    "EMAIL" that’s the E-Mail address of my Sister.
    "EMAIL" that’s the E-Mail address of my lawyer.
    "EMAIL" that’s the E-Mail address of my mother.
"""

user_input = sys.argv[1] # user input from the terminal

data_user = {
    "role": "user",
    "content": user_input
}

file_name = "conversations.txt"

with open(file_name, "a") as file:
    json_data = json.dumps(data_user)
    json_data += "\n"
    file.write(json_data) # savint the user input into a conversations.txt file for contextual awareness

messages = [
    {"role": "system", "content": system}, # giving chat gpt the assistant text
    # loading the previous conversations
    *[
        json.loads(line)
        for line in open(file_name, "r")
        if line.strip() != ""
    ]
]
# giving informations about all the functions for gpt
functions = [
    {
        "name": "get_unread_emails",
        "description": "Gets all unread emails from the inbox",
        "parameters": {
            "type": "object",
            "properties": {
                "email_number": {
                    "type": "string",
                    "description": "The id number of the email",
                },
                "sender": {
                    "type": "string",
                    "description": "The email address of the sender",
                },
                "subject": {
                    "type": "string",
                    "description": "The subject of the email",
                },
                "plain": {
                    "type": "string",
                    "description": "The main body-text of the mail",
                }
            }
        }
    },
    {
        "name": "send_email",
        "description": "Here you to reply the my unread emails or send an email to my family, friends or work. Write the Mails in my name (YOUR NAME). both the plain body text and html formatted body text are needed",
        "parameters": {
            "type": "object",
            "properties": {
                "reciever": {
                    "type": "string",
                    "description": "the email address of the receiver"
                },
                "subject": {
                    "type": "string",
                    "description": "the subject of the email"
                },
                "body_plain": {
                    "type": "string",
                    "description": "main email text in plain text format"
                },
                "body_html": {
                    "type": "string",
                    "description": "is the same body text but in html format."
                }
            }
        },
        "required": ["reciever", "subject", "body_plain", "body_html"]
    },
    {
        "name": "delete_unread_email",
        "description": "You can delete emails that are spam or commercial. the mail to delete is the email_number in the get_unread_emails() function",
        "parameters": {
            "type": "object",
            "properties": {
                "id_number": {
                    "type": "string",
                    "description": "the id of the email to delete"
                }
            }
        },
        "required": ["id_number"]
    },
    {
        "name": "search",
        "description": "Here you can communicate with BingGPT for websearch. In case of me wanting you to search for something, or if you can't answer my command or question, because of your cut-off date.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "the search query from you can also be the link to my given Websites for the news"
                },
                "bing_summary_response": {
                    "type": "string",
                    "description": "summary from the Bing AI after browsing the web from your given search query"
                },
                "sources": {
                    "type": "string",
                    "description": "The sources Bing AI used to give the Summary"
                }
            }
        },
        "required": ["title"]
    }
]

# sending gpt the message
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k-0613",
    messages=messages,
    functions=functions,
    function_call="auto",
)

response_message = response["choices"][0]["message"]
first_response = response_message["content"]

if first_response == None:
    print("")
else:
    print(first_response)
    assistant_input = first_response
    data_assistant = {
        "role": "assistant",
        "content": assistant_input
    }
    with open(file_name, "a") as file:
        json_data = json.dumps(data_assistant)
        json_data += "\n"
        file.write(json_data)

# checking if a function has been called by gpt
if response_message.get("function_call"):       
    function_name = response_message["function_call"]["name"]
    # checking with function has been called
    if function_name == "get_unread_emails":
        function_response = get_unread_emails()

        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )

        # instead if appending the message, it saves it into the conversations.txt file
        # data_function_response = {
        #     "role": "function",
        #     "name": function_name,
        #     "content": function_response,
        # }
    
        # with open(file_name, "a") as file:
        #     json_data = json.dumps(data_function_response)
        #     json_data += "\n"
        #     file.write(json_data)

    elif function_name == "send_email":
        arguments = json.loads(response_message["function_call"]["arguments"])
        reciever = arguments.get("reciever")
        subject = arguments.get("subject")
        body_plain = arguments.get("body_plain")
        body_html = arguments.get("body_html")
        function_response = send_email(reciever, subject, body_plain, body_html)
        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )

    elif function_name == "delete_unread_email":
        arguments = json.loads(response_message["function_call"]["arguments"])
        id_number = arguments.get("id_number")
        function_response = delete_unread_email(id_number)
        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )

    elif function_name == "search":
        arguments = json.loads(response_message["function_call"]["arguments"])
        title = arguments.get("title")
        function_response = asyncio.run(search(title))
        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )

    # sending the response from the function into gpt a second time fro the summaries, etc
    second_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=messages,
    )

    second_response_message = second_response["choices"][0]["message"]['content']

    print(second_response_message) # printing the summary out

    assistant_input = second_response_message

    data_assistant = {
        "role": "assistant",
        "content": assistant_input
    }

    with open(file_name, "a") as file:
        json_data = json.dumps(data_assistant)
        json_data += "\n"
        file.write(json_data) # also saving the summary into the same conversations.txt file
