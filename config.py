"""Application configuration management.

This module handles environment-specific configuration loading, parsing,
and management
for the application. It includes environment detection, .env file loading, and
configuration value parsing.
"""

import os
from enum import Enum
from dotenv import load_dotenv


# Define environment types
class Environment(str, Enum):
    """Application environment types.

    Defines the possible environments the application can run in:
    development, staging, production, and test.
    """

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


def get_path_fs(prefix: str) -> str:
    """
    Get the local filesystem path for the given object name.

    Args:
        object_name (str): The name of the object.

    Returns:
        str: The local filesystem path.
    """

    prefix = f".{prefix}/"
    if not os.path.exists(prefix):
        os.makedirs(prefix)

    path_root = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
    path_fs = os.path.join(path_root, prefix)
    if not os.path.exists(path_fs):
        os.makedirs(path_fs)
    return path_fs


# Determine environment
def get_environment() -> Environment:
    """
    Get the current environment.

    Returns:
        Environment: The current environment
        (development, staging, production, or test)
    """
    match os.getenv("APP_ENV", "production").lower():
        case "production" | "prod":
            return Environment.PRODUCTION
        case "staging" | "stage":
            return Environment.STAGING
        case "test":
            return Environment.TEST
        case _:
            return Environment.DEVELOPMENT


# Load appropriate .env file based on environment
def load_env_file():
    """Load environment-specific .env file."""
    env = get_environment()
    print(f"Loading environment: {env}")
    path_env = os.path.dirname(os.path.abspath(__file__))

    # Define env files in priority order
    env_files = [
        os.path.join(path_env, f".env.{env.value}.local"),
        os.path.join(path_env, f".env.{env.value}"),
        os.path.join(path_env, ".env.local"),
        os.path.join(path_env, ".env"),
    ]

    # Load the first env file that exists
    for env_file in env_files:
        if os.path.exists(env_file):
            load_dotenv(dotenv_path=env_file)
            print(f"Loaded environment from {env_file}")
            return env_file

    # Fall back to default if no env file found
    return None


ENV_FILE = load_env_file()


class Settings:
    """Application settings without using pydantic."""

    def __init__(self):
        """Initialize application settings from environment variables.

        Loads and sets all configuration values from environment variables,
        with appropriate defaults for each setting. Also applies
        environment-specific overrides based on the current environment.
        """
        # Set the environment
        self.ENVIRONMENT = get_environment()
        self.APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
        self.A2A_CLIENT = os.getenv("A2A_CLIENT", "http://localhost:8010/a2a")

        # Apply environment-specific settings
        self.apply_environment_settings()

    def apply_environment_settings(self):
        """
        Apply environment-specific settings based
        on the current environment.
        """
        env_settings = {
            Environment.DEVELOPMENT: {
                "DEBUG": True,
                "LOG_LEVEL": "DEBUG",
                "LOG_FORMAT": "console"
            },
            Environment.STAGING: {
                "DEBUG": False,
                "LOG_LEVEL": "INFO"
            },
            Environment.PRODUCTION: {
                "DEBUG": False,
                "LOG_LEVEL": "WARNING"
            },
            Environment.TEST: {
                "DEBUG": True,
                "LOG_LEVEL": "DEBUG",
                "LOG_FORMAT": "console"
            },
        }

        # Get settings for current environment
        current_env_settings = env_settings.get(self.ENVIRONMENT, {})

        # Apply settings if not explicitly set in environment variables
        for key, value in current_env_settings.items():
            env_var_name = key.upper()
            # Only override if environment variable wasn't explicitly set
            if env_var_name not in os.environ:
                setattr(self, key, value)


# Create settings instance
settings = Settings()
