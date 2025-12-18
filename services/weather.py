import httpx
from config import OPENWEATHER_API_KEY

async def get_flood_risk(lat: float, lon: float) -> str:
    if not OPENWEATHER_API_KEY:
        return "medium"

    url = (
        f"https://api.openweathermap.org/data/3.0/onecall?"
        f"lat={lat}&lon={lon}&exclude=current,minutely,daily,alerts"
        f"&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code != 200:
            return "low"
        data = resp.json()

    total_rain = 0.0
    max_pop = 0.0
    for hour in data.get("hourly", [])[:48]:
        total_rain += hour.get("rain", {}).get("1h", 0)
        max_pop = max(max_pop, hour.get("pop", 0))

    if total_rain > 100 or max_pop > 0.8:
        return "high"
    elif total_rain > 50 or max_pop > 0.5:
        return "medium"
    else:
        return "low"