import python_weather
import asyncio
import smtplib, ssl, email

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import requests
import credentials



# fetch the weather data for Berlin and Jakarta
cities = ["Berlin", "Jakarta"]
weather_dict = {}
def city_forecast(city):
  response = requests.get(
          "https://community-open-weather-map.p.rapidapi.com/forecast?q="+city,
          headers={
          "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
          "X-RapidAPI-Key": credentials.rapidapi_key
        },
  )
  return response.json()
for city in cities:
  weather_dict[city] = city_forecast(city)
f = open('forecast_new.txt', 'a')
f.write(str(weather_dict) + '\n')
f.close()



subject = "Weather forecast in Berlin and Jakarta for the upcoming 14 days"
body = "Hi Lisa, this is the weather forecast for the next 14 days  "

#here you should add your email address as sender and reciever
#if you have account on gmail it will be eaasier to use it, because the server is set as smtp.gmail.com
sender_email = "email-address@domain.com"
receiver_email = "email-address@domain.com"
password = input("Type your password and press enter:")

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails
# Add body to email
message.attach(MIMEText(body, "plain"))

filename = ("forecast_new.txt") # In same directory as script

# Open text file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email
encoders.encode_base64(part)

# Add header as key/value pair to attachment part23769GeHo#%

part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
