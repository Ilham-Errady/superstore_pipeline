import psycopg2
import os
from dotenv import load_dotenv

# تحميل الإعدادات من ملف .env
load_dotenv()

def create_warehouse_structure():
    try:
        # الاتصال بقاعدة البيانات باستعمال المتغيرات من .env
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()

        # الكود الكامل لتصميم المستودع (BI & ML)
        sql_commands = """
        -- 1. كاري السكيمات
        CREATE SCHEMA IF NOT EXISTS bi_schema;
        CREATE SCHEMA IF NOT EXISTS ml_schema;

        -- 2. جداول BI Schema (Star Schema)
        CREATE TABLE IF NOT EXISTS bi_schema.dim_localisation (
            loc_id SERIAL PRIMARY KEY,
            city VARCHAR(100)
        );

        CREATE TABLE IF NOT EXISTS bi_schema.dim_caracteristiques (
            carac_id SERIAL PRIMARY KEY,
            surface_m2 FLOAT,
            segment VARCHAR(50)
        );

        CREATE TABLE IF NOT EXISTS bi_schema.fact_annonce (
            annonce_id SERIAL PRIMARY KEY,
            loc_id INT REFERENCES bi_schema.dim_localisation(loc_id),
            carac_id INT REFERENCES bi_schema.dim_caracteristiques(carac_id),
            price FLOAT,
            price_per_m2 FLOAT
        );

        -- 3. جدول ML Schema (One Big Table)
        CREATE TABLE IF NOT EXISTS ml_schema.obt_avito_dataset (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100),
            surface_m2 FLOAT,
            market_segment VARCHAR(50),
            price_per_m2 FLOAT,
            price FLOAT
        );
        """
        
        cur.execute(sql_commands)
        conn.commit()
        print(f"✅ Warehouse structure created in '{os.getenv('DB_NAME')}' (Schemas: BI & ML)")

    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    create_warehouse_structure()