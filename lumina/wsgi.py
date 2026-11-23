"""
WSGI entry point for production deployment.
"""

from app import create_app, db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Register objects for flask shell."""
    return {
        "db": db,
    }

if __name__ == "__main__":
    app.run()
