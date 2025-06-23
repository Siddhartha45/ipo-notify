print("---script started---")
import os
import requests, smtplib, time
from datetime import datetime, date
from bs4 import BeautifulSoup
from email.message import EmailMessage
# from dotenv import load_dotenv
from zoneinfo import ZoneInfo


# load_dotenv()
#email setup
email = os.getenv("EMAIL")
app_password = os.getenv("APP_PASSWORD")
#telegram setup
bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

#nepal time and date
nepal_tz = ZoneInfo("Asia/Kathmandu")
nepal_date_today = datetime.now(nepal_tz).date()
current_nepal_time = datetime.now(nepal_tz).time()

def send_mail(message):
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = "IPO ALERT!!!"
    msg["To"] = email 
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(email, app_password)
    s.send_message(msg)
    print("----mail sent----")
    s.quit()

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, payload)
    if response.status_code == 200:
        print("Message sent to Telegram.")
    else:
        print("Failed to send message:", response.text)

url = "https://merolagani.com/"
upcoming_url = url + "Ipo.aspx?type=upcoming"
page = requests.get(upcoming_url)
soup = BeautifulSoup(page.content, "html.parser")
block = soup.find(id="ctl00_ContentPlaceHolder1_divData")
# ipos = block.find_all("div", class_="media-body")

#test data
main_data = [
    {'Symbol': 'DHEL (Daramkhola Hydro Energy Limited)', 'Fiscal Year': '081-082', 'Announcement Detail': 'Daramkhola Hydro Energy Limited is going to issue its 2,91,950.00 units of IPO shares to the foreign employment citizens of Nepal starting from 9th - 23rd Ashad, 2082', 'Announcement Date': '2025/06/15 AD (2082/03/01 BS)', 'Tags': 'NoticeIPOIssueForeign Employment', 'Agenda': '', 'Bookclose Date': '', '% Cash Dividend': '', '% Bonus Share': '', 'Right Share Ratio': '', 'Date': '2025/06/23 AD (2082/03/09 BS)', 'Venue': '', 'Time': ''},
    {'Symbol': 'JBLB (Daramkhola Hydro Energy Limited)', 'Fiscal Year': '081-082', 'Announcement Detail': 'Daramkhola Hydro Energy Limited is going to issue its 2,91,950.00 units of IPO shares to the foreign employment citizens of Nepal starting from 9th - 23rd Ashad, 2082', 'Announcement Date': '2025/06/15 AD (2082/03/01 BS)', 'Tags': 'NoticeIPOIssueForeign Employment', 'Agenda': '', 'Bookclose Date': '', '% Cash Dividend': '', '% Bonus Share': '', 'Right Share Ratio': '', 'Date': '2025/06/22 AD (2082/03/08 BS)', 'Venue': '', 'Time': ''},
    {'Symbol': 'SMPL (Daramkhola Hydro Energy Limited)', 'Fiscal Year': '081-082', 'Announcement Detail': 'Daramkhola Hydro Energy Limited is going to issue its 2,91,950.00 units of IPO shares to the foreign employment citizens of Nepal starting from 9th - 23rd Ashad, 2082', 'Announcement Date': '2025/06/15 AD (2082/03/01 BS)', 'Tags': 'NoticeIPOIssueForeign Employment', 'Agenda': '', 'Bookclose Date': '', '% Cash Dividend': '', '% Bonus Share': '', 'Right Share Ratio': '', 'Date': '2025/06/23 AD (2082/03/08 BS)', 'Venue': '', 'Time': ''},
    {'Symbol': 'LALA (Daramkhola Hydro Energy Limited)', 'Fiscal Year': '081-082', 'Announcement Detail': 'Daramkhola Hydro Energy Limited is going to issue its 2,91,950.00 units of IPO shares to the foreign employment citizens of Nepal starting from 9th - 23rd Ashad, 2082', 'Announcement Date': '2025/06/15 AD (2082/03/01 BS)', 'Tags': 'NoticeIPOIssueForeign Employment', 'Agenda': '', 'Bookclose Date': '', '% Cash Dividend': '', '% Bonus Share': '', 'Right Share Ratio': '', 'Date': '2025/06/22 AD (2082/03/08 BS)', 'Venue': '', 'Time': ''}
]

# main_data = []

# for ipo in ipos:
#     ipo_link = url + ipo.find("a")["href"]
#     page = requests.get(ipo_link)
#     soup = BeautifulSoup(page.content, "html.parser")
#     table = soup.find("table", class_="table table-hover")
#     rows = table.find_all("tr")
#     data = {}
#     for row in rows:
#         cols = row.find_all("td")
#         if len(cols) == 2:
#             key = cols[0].get_text(strip=True)
#             value = cols[1].get_text(strip=True)
#             data[key] = value
#     main_data.append(data)

unique = []     #removes duplicate ipos
seen_symbols = set()   #stores ipo symbols

for item in main_data:
    if item["Symbol"] not in seen_symbols:
        unique.append(item)
        seen_symbols.add(item["Symbol"])

for item in unique:
    symbol = item["Symbol"]
    ipo_date = datetime.strptime(str(item["Date"][:10]), "%Y/%m/%d").date()
    message = f"Apply for ipo: {symbol}. It has opened on {ipo_date}."
    while True:
        if ipo_date == nepal_date_today:
            if current_nepal_time.hour == 2 and 1 <= current_nepal_time.minute <= 59:
                print("--started--")
                send_telegram_message(bot_token, chat_id, message)
                send_mail(message)
                print("---ended----")
                break
            else:
                print("---waiting---")
            time.sleep(60)
        else:
            print("No ipo openings")
            break

