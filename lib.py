import os

def check_env_vars(required_vars: list = None):
    """Check if all required environment variables are set."""
   
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )