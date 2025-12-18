# OnWatch - Flood Risk Alert USSD Application

**OnWatch** is a life-saving USSD and app-based early warning system designed to deliver real-time flood risk alerts and emergency reporting for communities in Nigeria, Ghana, and Cameroon.

Users dial a simple USSD code to check flood risk in their area, receive personalized alerts via SMS during high-risk conditions, and — most importantly — report "I am in danger" to instantly log an emergency with location, time, and phone number for potential rescue coordination.

Built for impact.

## Features

- **Multilingual Support**  
  - Nigeria: Nigerian Pidgin  
  - Ghana: English  
  - Cameroon: French or English (user choice)

- **Real-time Flood Risk Assessment**  
  Uses OpenWeatherMap API to analyze rainfall forecast (next 48 hours) for major cities.

- **Automatic High-Risk SMS Alerts**  
  If heavy rainfall is predicted, users automatically receive a warning SMS.

- **Emergency "I am in danger" Reporting**  
  Users can report immediate danger after seeing risk level.  
  Logs: phone number, city, country, timestamp, and current risk level to database.  
  Sends confirmation SMS to user.

- **Persistent Sessions**  
  Powered by SQLite (with easy upgrade path to PostgreSQL).

- **Africa's Talking Integration**  
  Full USSD menu + SMS delivery (sandbox ready).

## Supported Countries & Cities

| Country   | Cities                  | Language(s)         |
|-----------|-------------------------|---------------------|
| Nigeria   | Lagos, Abuja            | Pidgin              |
| Ghana     | Accra, Kumasi           | English             |
| Cameroon  | Yaoundé, Douala         | French / English    |

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLModel + SQLite
- **Weather Data**: OpenWeatherMap One Call API
- **SMS & USSD**: Africa's Talking API
- **HTTP Client**: httpx (async)
- **Environment**: python-dotenv (local dev)

## Project Structure

```
onwatch/
├── main.py                    # FastAPI entry point
├── config.py                  # Environment variables
├── models.py                  # SQLModel schemas (sessions & emergencies)
├── database/
│   ├── session.py             # DB engine & session
│   └── base.py                # Table creation
├── services/
│   ├── ussd.py                # Core USSD flow logic
│   ├── weather.py             # Flood risk calculation
│   └── sms.py                 # SMS alerts via Africa's Talking
├── utils/
│   ├── constants.py           # Messages, cities, prefixes
│   └── user_session.py        # Session & emergency logging helpers
├── requirements.txt
├── .env.example
└── flood_alert.db             # Auto-created SQLite DB
```

## Setup & Local Development

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/onwatch.git
   cd onwatch
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file**
   ```bash
   cp .env.example .env
   ```
   Fill in your keys:
   ```
   OPENWEATHER_API_KEY=your_openweather_key
   AT_USERNAME=sandbox
   AT_API_KEY=your_africastalking_sandbox_key
   AT_SMS_FROM=AFRICASTKNG
   ```

4. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Expose with ngrok (for USSD testing)**
   ```bash
   ngrok http 8000
   ```
   Use the `https://xxxx.ngrok.io/ussd` URL as callback in Africa's Talking.

6. **Create USSD Channel**
   - Go to [Africa's Talking Sandbox](https://account.africastalking.com/apps/sandbox/ussd)
   - Create new channel → Paste your ngrok/deployed URL + `/ussd`
   - Get your test code (e.g., `*384*12345#`)

7. **Test!**
   - Use simulator or dial the code on a phone.


## Database

- Uses SQLite by default (`flood_alert.db`)
- Tables:
  - `ussdsession`: Tracks user flow state
  - `emergencyalert`: Logs all "I am in danger" reports

Easy to view with DB Browser for SQLite during demos.

## Future Improvements

- Add more cities & dynamic location detection
- Admin dashboard to view live emergency reports
- Integrate with national disaster agencies
- Voice alerts (Africa's Talking Airtime + Text-to-Speech)
- Support for more countries


**OnWatch** – Because every second counts when floods are coming.

Built with ❤️ for climate resilience in Africa.


