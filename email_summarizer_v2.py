import os
import imaplib
import email
import re
import html2text
import urllib.parse
import logging

from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from dotenv import load_dotenv
load_dotenv()

OPEN_AI_PAT = os.environ['OPEN_AI_PAT']
IMAP_SERVER = os.getenv('IMAP_SERVER')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def remove_urls(text):
    # Remove URLs using regex pattern
    return re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

def get_text(msg):
    if msg.is_multipart():
        return get_text(msg.get_payload(0))
    else:
        payload = msg.get_payload()
        content_type = msg.get_content_type()
        if content_type == "text/html":
            payload = html2text.html2text(payload)
            payload_text = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', payload)
            return remove_urls(payload_text)
        else:
            payload_text = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', payload)
            return remove_urls(payload_text)

mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
mail.select("inbox")

status, messages = mail.select("INBOX")
num_of_messages = int(messages[0])

llm = OpenAI(
    temperature=0,
    openai_api_key=OPEN_AI_PAT,
    model_name="text-davinci-003"
)

# Load the summarization chain
chain = load_summarize_chain(llm, chain_type="refine")

for i in range(num_of_messages, num_of_messages - 3, -1):
    result, data = mail.fetch(str(i), "(RFC822)")
    raw_email = data[0][1]

    email_message = email.message_from_bytes(raw_email)
    sender = email_message['From']
    subject = email_message['Subject']

    body = get_text(email_message)

    try:
        body = body.decode()
    except:
        pass

    urls = list(set(urllib.parse.urlsplit(url) for url in re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)))

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=50,
        separators=[" ", ",", "\n"]
    )
    
    chunks = text_splitter.split_text(body)

    documents = []

    # Iterate over the chunks and create Document objects with page_content
    if len(chunks) <= 10:
        for chunk in chunks:
            document = Document(page_content=chunk)
            documents.append(document)

    if documents:
        prompt_document = Document(page_content="Summarize the following email into bullet points ordered by importance:\n")

        documents.insert(0, prompt_document)
        summary = chain(documents)
        summarized_text = summary['output_text']

        print("CHUNKS:", len(chunks))
        print("SENDER:", sender)
        print("SUBJECT:", subject)
        print("SUMMARY:\n", summarized_text)
        print("----------\n")
    else:
        print("CHUNKS:", len(chunks))
        print("SENDER:", sender)
        print("SUBJECT:", subject)
        print("----------\n")