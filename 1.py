import openai
from simplegmail import Gmail

gmail = Gmail()

openai.api_key = "YOUR-API-KEY"

messages = gmail.get_unread_inbox()

emails = []

for message in messages:
    emails.append(f"From: {message.sender}\nSubject: {message.subject}\n{message.plain}")
    message.mark_as_read()

prompt_template = """\
Pretend to be a friendly assistant / motivational coach to me, someone that you know really well. \
I have just asked if there are any noteworthy new e-mails. \
Respond providing relevant summaries and if there are any important details or followups needed for each of the e-mails without just reading them out. \
Maybe slip in a joke if possible. \
Try to be observant of all the details in the data \ to come across as observant and emotionally intelligent as you can. \
Don't ask for a followup or if they need any other help. and don't add sentences.  \
In case the emails have attachments, they are automatically saved. \
Number of new e-mails: {EMAIL_COUNT}

Emails:
{EMAILS}

Response:
"""

prompt = prompt_template.format(EMAIL_COUNT=len(emails), EMAILS="\n\n".join(emails))

response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.3,
    max_tokens=800,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
)

resp = response["choices"][0]["text"]

conversation = "You: " + resp + "\n"

with open('PATH-TO-THE-TEXT-FILE', 'a') as file:
    file.write(conversation)

with open('PATH-TO-THE-TEXT-FILE', 'r') as file:
    conversation = file.read()

print(resp)