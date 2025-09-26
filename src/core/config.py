import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    PG_URL = os.getenv(
        "PG_URL",
        "postgresql://postgres.haxlclcfgqdpocvwldth:postgres@aws-1-eu-north-1.pooler.supabase.com:5432/postgres?sslmode=require",
    )

    POOL_SIZE = int(os.getenv("POOL_SIZE", 3))
    MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", 0))
    POOL_TIMEOUT = int(os.getenv("POOL_TIMEOUT", 180))

    SEED_TIMEOUT_S = int(os.getenv("SEED_TIMEOUT_S", 10))
    SEED_BATCH_SIZE = int(os.getenv("SEED_BATCH_SIZE", 5))
    SEED_BASE_COUNTRIES_SIZE = int(os.getenv("SEED_BASE_COUNTRIES_SIZE", 150))
    SEED_BASE_USERS_SIZE = int(os.getenv("SEED_BASE_USERS_SIZE", 1_000))


config = Config()
