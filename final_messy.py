import re
import os
import openai
from time import time,sleep
from uuid import uuid4
import smtplib
from email.message import EmailMessage

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


openai.api_key = open_file('openaiapikey.txt')


def gpt3_completion(prompt, engine='text-davinci-002', temp=1.0, top_p=1.0, tokens=2000, freq_pen=0.0, pres_pen=0.0, stop=['asdfasdf', 'asdasdf']):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            save_file('gpt3_logs/%s' % filename, prompt + '\n\n==========\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


def email_alert(subject, body, to):
  msg= EmailMessage()
  user = "alerts.hackathon@gmail.com"
  #account password: GoogleHackathon2021@gmail.com
  # Generated app password
  password = "kedsgdrrahkhztyq"
  msg.set_content(body)
  msg['from']=user
  msg['to'] = to
  msg['subject'] = subject
  
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login (user, password)
  server.send_message(msg)
  server.quit()

# email_alert("Fire! Fire! Fire!", "To whom it may concern, it appears there seems to be a fire on the premises.", "-@gmail.com")
# classification_label= "wheelchair"

if __name__ == '__main__':
    scenario = open_file('input.txt')
    prompt = open_file('prompt_to_email.txt').replace('<<_TOPIC_>>', scenario)
    print('\n\n==========\n\n', prompt)
    completion = gpt3_completion(prompt)
    filename = scenario.replace(' ','').lower()[0:10] + str(time()) + '.txt'
    output = scenario.strip() + '\n\nEMAIL:\n\n' + completion
    print('\n\n', completion)
    save_file('assistant_email/%s' % filename, output)
    subject = []
    email= []
    recipient= []
    # phone_number= []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip() # remove "\n" from line
            if line.startswith("Subject:"):
                subject.append(line[8:])
            if line.startswith("Email:"):
                email.append(line[6:])
            if line.startswith("Recipient:"):
                recipient.append(line[10:])
            # if line.startswith("Phone:"):
            #     phone_number.append(line[6:])
    email_alert(subject, email, recipient)
    # email_alert(subject, email, phone_number)


