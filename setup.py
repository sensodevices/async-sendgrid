import setuptools

import async_sendgrid

setuptools.setup(
    name='async-sendgrid',
    version=async_sendgrid.__version__,
    description='SendGrid simple async client based on httpx',
    packages=['async-sendgrid'],
    install_requires=[
        "httpx>=0.21",
    ],
    author_email='saltytimofey@gmail.com',
)
