# Async-Sendgrid

SendGrid simple async client based on httpx.

# Installation

```bash
pip install async-sendgrid
```

# Usage

```python
import async_sendgrid
from sendgrid.helpers.mail import Content, Email, Mail, To
import os

API_KEY = os.environ.get('API_KEY')

from_email = Email("test@example.com")
to_email = To("test@example.com")
subject = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
content = Content("text/plain", "Sed varius ligula ac urna vehicula ultrices. Nunc ut dolor sem.")
mail = Mail(from_email, to_email, subject, content)

data = {
    "personalizations": [
        {
            "to": [{"email": "test@example.com"}],
            "subject": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        }
    ],
    "from": {"email": "test@example.com"},
    "content": [
        {
            "type": "text/plain",
            "value": "Sed varius ligula ac urna vehicula ultrices. Nunc ut dolor sem."
        }
    ],
}


# Send email with context manager

async with async_sendgrid.AsyncClient(api_key=API_KEY) as client:
    response1 = await client.send(data)
    response2 = await client.send(mail)

# Send email without context manager

client = async_sendgrid.AsyncClient(api_key=API_KEY)
await client.open()
response1 = await client.send(data)
response2 = await client.send(mail)
await client.close()

```
