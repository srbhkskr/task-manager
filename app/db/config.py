import os

# Database connection string, ideally from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost/task_manager_db")

