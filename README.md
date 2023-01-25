# Run
docker-compose up --build -d
docker-compose exec backend alembic upgrade head
Default API KEY - `API_KEY`

# Example /convert 
amount - 1000
from_currency - US Dollar
to_currency - Yen

# Scrapping 
Selected the most convenient method - xe.com with html parsing.
Wise.com use cloudflare with bot management.
