# Abstract

This Python script utilizes OpenAI's language model to summarize the content of emails fetched from an IMAP email server.

The script connects to the email server, retrieves the desired emails, processes their content, and uses the language model to generate concise summaries.

The summaries can be useful for quickly understanding the key points of the emails without reading them in detail.

The script also handles HTML content, removes URLs, and supports splitting long emails into smaller chunks for more accurate summarization.

## Things to add

- Aggregate email summarizes and send a summary at 24:00 every day
  - Either through email
  - Or through sms, email by email
- Archive emails that have been summarized
  - Or move them to an "Archived" folder?
- Make the setting up process simpler
- Make summaries into bullet points ordered by "importance"?

## Getting started

To run the provided script for email summarization using OpenAI's language model, follow these steps:

Install the required dependencies: Ensure you have Python installed on your system. Additionally, install the necessary packages by running the command pip install langchain openai-python-client html2text python-dotenv.

1. **Set up the environment variables:** Create a file named .env in the same directory as the script. Open the .env file and provide the required environment variables:

- `OPEN_AI_PAT`: Your OpenAI API key.
- `IMAP_SERVER`: The IMAP server address for your email provider.
- `EMAIL_ADDRESS`: Your email address.
- `EMAIL_PASSWORD`: Your email password.

2. **Customize the script (optional):** Review the script and make any necessary modifications. For example, you can adjust the summarization settings or modify the prompt used for summarization.

3. **Run the script:** Execute the script by running the command python script_name.py, replacing script_name.py with the actual name of the script file.

Ensure that you have a stable internet connection and access to the configured IMAP email server. The script will work for the most recent emails in your inbox, but you can adjust the range of messages to process by modifying the num_of_messages variable.

Note: Make sure to handle your API key and other sensitive information securely and avoid sharing it publicly.
