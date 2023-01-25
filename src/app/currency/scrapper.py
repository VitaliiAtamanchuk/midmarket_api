from datetime import datetime

import bs4 
import httpx

from app.currency.contants import HEADERS, HEADERS


async def fetch_currency(amount: float, from_currency_code: str, to_currency_code: str):
    url = f'https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={from_currency_code}&To={to_currency_code}'
    
    async with httpx.AsyncClient() as client:
        
        response = await client.get(url, headers=HEADERS, cookies=HEADERS)
        created_at = datetime.utcnow()

        soup = bs4.BeautifulSoup(response.text, "lxml")
        amount = float(soup.select_one('.result__BigRate-sc-1bsijpp-1').get_text().split(" ")[0].replace(',', ''))

        paragraphs = soup.select('.unit-rates___StyledDiv-sc-1dk593y-0 p')
        rate = amount \
            if len(paragraphs) == 1 \
            else float(soup.select_one('.unit-rates___StyledDiv-sc-1dk593y-0 p').get_text().split(" ")[3].replace(',', ''))
    
    return {
        "rate": rate,
        "amount": amount,
        "created_at": created_at
    }
