import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser

# Define the URL of the website to scrape
URLS = ['https://miz.org/de/kurse?filter[course_conduct_choir_leader][0]=Orchester-%20%2F%20Ensembleleitung', 'https://miz.org/de/kurse?filter[course_conduct_choir_leader][0]=Chorleitung']

def scrape_website():
    event_list = []
    for URL in URLS:
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')
    
        events = soup.find_all('div', class_='search-result-list__item')
    
        # Extract relevant information
        for event in events:
            title = event.find('h3').text
            date_span = event.find('span', class_='card-list-event__date')
            times = date_span.find_all('time')
            if len(times) >= 2:
                start_date = times[0].text.strip()
                end_date = times[1].text.strip()
            elif len(times) == 1:
                start_date = times[0].text.strip()
                end_date = times[0].text.strip()
            else: continue
            # The location is the remaining text after the second <time> element
            location = date_span.text.split('|')[-1].strip()
            link = 'miz.org'+event.find('a').get('href')

            event_data = {
                'title': title,
                'start_date': start_date,
                'end_date': end_date,
                'location': location,
                'link': link
            }

            event_list.append(event_data)

    
    return event_list

def send_newsletter(events):
    # Read configuration from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Extract email configuration
    smtp_server = config['EMAIL']['SMTP_SERVER']
    smtp_port = config['EMAIL'].getint('SMTP_PORT')
    from_email = config['EMAIL']['FROM_EMAIL']
    to_email = config['EMAIL']['TO_EMAIL']
    smtp_user = config['EMAIL']['SMTP_USER']
    smtp_password = config['EMAIL']['SMTP_PASSWORD']
    subject = 'MIZ Zusammenfassung'
    
    # Create the email content
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    body = '<h2>Dirigierkurse in den kommenden Monaten:</h2>\n\n'
    for event in events:
        if event['link']:
            #print(event['link'])
            body += f'<p><strong><a href="{event["link"]}">{event["title"]}</a></strong></p>'
        else:
            body += f'<p><strong>{event["title"]}</strong></p>'
        body += f'<p>Datum: {event["start_date"]} - {event["end_date"]}</p>\n'
        body += f'<p>Standort: {event["location"]}</p>\n'
        body += '\n'
    
    msg.attach(MIMEText(body, 'html'))
    
    # Send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

def main():
    events = scrape_website()
    if events:
        send_newsletter(events)
    else:
        print("No events found matching the filters.")

if __name__ == "__main__":
    main()
