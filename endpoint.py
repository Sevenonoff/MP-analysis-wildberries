from fastapi import FastAPI, Query, HTTPException
import sqlite3
from pydantic import BaseModel
from parse import parse_wildberries, save_to_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# подтягивание данных для фильтра
@app.get("/api/products/")
def get_products(
    min_price: float = Query(None),
    max_price: float = Query(None),
    min_rating: float = Query(None),
    min_reviews: int = Query(None)
):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # фильтрациия товаров
    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if min_price is not None:
        query += " AND price >= ?"
        params.append(min_price)
    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)
    if min_rating is not None:
        query += " AND rating >= ?"
        params.append(min_rating)
    if min_reviews is not None:
        query += " AND reviews_count >= ?"
        params.append(min_reviews)

    cursor.execute(query, params)
    products = cursor.fetchall()

    result = []
    for product in products:
        result.append({
            "id": product[0],
            "name": product[1],
            "price": product[2],
            "discounted_price": product[3],
            "rating": product[4],
            "reviews_count": product[5]
        })

    # гистограмма цен
    cursor.execute("SELECT MIN(price), MAX(price) FROM products")
    r = cursor.fetchone()
    print(r)
    min_price_db, max_price_db = min_price or r[0], max_price or r[1]

    if min_price_db is None or max_price_db is None:
        price_histogram = []
    else:
        step = (max_price_db - min_price_db) / 4
        ranges = [
            f"{min_price_db:.0f}-{min_price_db + step:.0f}",
            f"{min_price_db + step:.0f}-{min_price_db + 2 * step:.0f}",
            f"{min_price_db + 2 * step:.0f}-{min_price_db + 3 * step:.0f}",
            f"{min_price_db + 3 * step:.0f}-{max_price_db:.0f}"
        ]

        price_histogram = []
        for i, price_range in enumerate(ranges):
            lower_bound = min_price_db + i * step
            upper_bound = min_price_db + (i + 1) * step
            cursor.execute("""
            SELECT COUNT(*) FROM products
            WHERE price >= ? AND price < ?
            """, (lower_bound, upper_bound))
            count = cursor.fetchone()[0]
            price_histogram.append({"price_range": price_range, "count": count})

    # скидка и рейтинг    
    rating_filter = min_rating if min_rating is not None else 0.0

    cursor.execute("""
    SELECT 
        ROUND((discounted_price - price) / price * 100, 1) AS discount_percent,
        rating
    FROM products
    WHERE rating >= ?
    """, (rating_filter,))
    discount_vs_rating = [{"discount": f"{row[0]}%", "rating": row[1]} for row in cursor.fetchall()]
    
    conn.close()

    return {
        "products": result,
        "charts_data": {
            "price_histogram": price_histogram,
            "discount_vs_rating": discount_vs_rating
        }
    }



class ParseRequest(BaseModel):
    search_query: str


# запуск парсинга
@app.post("/api/parse/")
async def parse_products(request: ParseRequest):
    search_query = request.search_query

    if not search_query:
        raise HTTPException(status_code=400, detail="Поисковый запрос не может быть пустым")

    products = parse_wildberries(search_query)

    if not products:
        raise HTTPException(status_code=404, detail="Товары не найдены")

    save_to_db(products)

    return {"message": "Парсинг завершен", "parsed_items": len(products)}