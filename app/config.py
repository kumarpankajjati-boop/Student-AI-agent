"""Settings loader (Day 7): reads values from the .env file using pydantic-settings.

Every value has a safe default, so the project also runs without a .env file.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./students.db"

    # Which AI model answers questions: "ollama" (local, offline) or "gemini" (cloud)
    llm_provider: str = "ollama"

    # Local model (Day 10)
    ollama_model: str = "llama3.2"
    ollama_base_url: str = "http://127.0.0.1:11434"

    # Cloud model (Day 3 to 5). Key comes from Google AI Studio and lives ONLY in .env
    gemini_model: str = "gemini-2.5-flash"
    google_api_key: str = ""

    # Logging (Day 2)
    log_file: str = "logs/app.log"

    # Insert sample students on startup if the table is empty (handy for a live demo)
    seed_demo_data: bool = False

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
