# Run
- docker-compose up --build -d
- docker-compose exec backend alembic upgrade head
- Default API KEY - `API_KEY`

# Scrapping 
Selected the most convenient method - xe.com with html parsing.
Wise.com use cloudflare with bot management.

# Architecture
Ideally architecture would be Event-driven, but taking into account short deadline the basic chosen.
