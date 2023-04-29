import sys
import json
import openai
from simplegmail import Gmail

gmail = Gmail('/Users/gokdenizgulmez/Desktop/gpt/gptgmail/Kurzbefehl_main/client_secret.json')

openai.api_key = "YOUR-API-KEY"

messages = gmail.get_unread_inbox()

input_text = sys.argv[1]

emails = []
for message in messages:
    emails.append(f"From: {message.sender}\nSubject: {message.subject}")
   
conversation = "Me: " + input_text + "\n"

with open('PATH-TO-THE-TEXT-FILE', 'a') as file:
    file.write(conversation)

with open('PATH-TO-THE-TEXT-FILE', 'r') as file:
    conversations = file.read()

prompt_template = """\
You are pretending to be a friendly assistant/motivational coach for me, someone you know well. You can answer randomly asked questions and send emails/reply's to my last unread emails. Your response is in a JSON file that includes attributes such as "mail-empf", "mail-sub", "mail-body", and "response".
For "mail-empf", only include the email address (also do not write the "<>" in your response) to send a new email to, based on the emails that have been received do not come up with a email address thats not listed here. 
For "mail-sub", provide the subject of the email to send. 
For "mail-body", provide the main text of the email to send, keeping everything in one line and use '\n' instead of pressing enter. 
For "mail-body-html", is the same main text from "mail-body" but in HTML format.
For "response", reassure me that the email has been sent and answer my question or just answer my question if i didn't want you to reply or send an email. If I ask you a question that is not related to the emails, you will only output the "response" attribute, do not send a email.
For example, If I ask you for some quick and nice stretching workouts, you will provide me with a JSON file that only has the attribute "response" (not "mail-empf", "mail-sub", "mail-body", "mail-body-html") with your answer.
You should write the email in my name, YOUR NAME. The received emails contain information such as names and email addresses, which you can use in your response.
Please include the received emails and the last conversation between the person and you in your response. 
Additionally, you can answer questions about a variety of topics, but if thats the case, then just respond with the "response" attribute. 
Try to be observant of all details in the data to come across as emotionally intelligent.
Finally, please make sure that the JSON response is in one line and ask for a follow-up or if I need any other help, and do not add extra sentences.
And do not forget, if I am just asking a question instead of wanting to sending an email, do not send an email, just answer my question.
here are the received E-Mails:
{EMAILS}

Here are also some email add that may be useful if i want to send a pedicular email to some of these people:
„work@gmail.com“ that’s my work E-Mail address.
„sis@gmail.com“ that’s the E-Mail address of my Sister.
„law@agmail.com“ that’s the E-Mail address of my lawyer.
„mom@gmail.com“ that’s the E-Mail address of my mother.

Here is the last conversation between me and you:
{CONVS}

Response:
"""

prompt = prompt_template.format(EMAILS="\n\n".join(emails), CONVS="\n".join(conversations))

response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.3,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
)

resp = response["choices"][0]["text"]

mail = "resp: " + resp + "\n"

with open('PATH-TO-THE-TEXT-FILE', 'a') as file:
    file.write(mail)

try:
    response_dict = json.loads(resp)
    res = response_dict["response"]
    print(res)
    conversation = "You: " + res + "\n"
except json.decoder.JSONDecodeError:
    print("Invalid JSON---------------------------------------: \n", resp)

with open('PATH-TO-THE-TEXT-FILE', 'a') as file:
    file.write(conversation)

if '@' in response_dict['mail-empf']:
    if response_dict["mail-sub"]: 
        if response_dict["mail-body-html"]:
            if response_dict["mail-body"]:
                params = {
                    "to": response_dict["mail-empf"],
                    "sender": "YOUR EMAIL",
                    "subject": response_dict["mail-sub"],
                    "msg_html": response_dict["mail-body-html"],
                    "msg_plain": response_dict["mail-body"],
                    "signature": True
                }
                message = gmail.send_message(**params)

                mail = "Mail: " + json.dumps(params) + "\n"

                with open('PATH-TO-THE-TEXT-FILE m.txt', 'a') as file:
                    file.write(mail)