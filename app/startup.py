from app.database import create_tables
from nicegui import ui
import app.counter


def startup() -> None:
    # this function is called before the first request
    create_tables()
    app.counter.create()

    @ui.page("/")
    def index():
        ui.label("Simple Counter App").classes("text-4xl font-bold text-center mb-8")
        ui.link("Go to Counter", "/counter").classes("text-xl text-blue-500 hover:text-blue-700 text-center block")
