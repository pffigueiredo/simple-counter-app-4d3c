from nicegui import ui
from app.database import get_session
from app.models import Counter
from datetime import datetime
from sqlmodel import select


def create() -> None:
    @ui.page("/counter")
    def page():
        # Get or create the default counter from database
        def get_or_create_counter() -> Counter:
            with get_session() as session:
                statement = select(Counter).where(Counter.name == "default_counter")
                counter = session.exec(statement).first()
                if counter is None:
                    counter = Counter(name="default_counter", value=0)
                    session.add(counter)
                    session.commit()
                    session.refresh(counter)
                return counter

        # Load initial count from database
        initial_counter = get_or_create_counter()
        initial_count = initial_counter.value

        # Create UI components
        count_label = (
            ui.label(f"Count: {initial_count}").classes("text-6xl font-bold text-center mb-8").mark("count-display")
        )

        def update_count(change: int) -> None:
            def update_db() -> int:
                with get_session() as session:
                    statement = select(Counter).where(Counter.name == "default_counter")
                    counter = session.exec(statement).first()
                    if counter is not None:
                        counter.value += change
                        counter.updated_at = datetime.utcnow()
                        session.add(counter)
                        session.commit()
                        return counter.value
                    return 0

            new_count = update_db()
            count_label.set_text(f"Count: {new_count}")

        # Create buttons with proper styling
        with ui.row().classes("gap-4 justify-center"):
            ui.button("-", on_click=lambda: update_count(-1)).classes(
                "text-3xl px-8 py-4 bg-red-500 hover:bg-red-600"
            ).mark("decrement")
            ui.button("+", on_click=lambda: update_count(1)).classes(
                "text-3xl px-8 py-4 bg-green-500 hover:bg-green-600"
            ).mark("increment")

        # Add reset button
        with ui.row().classes("justify-center mt-4"):

            def reset_count() -> None:
                def reset_db() -> None:
                    with get_session() as session:
                        statement = select(Counter).where(Counter.name == "default_counter")
                        counter = session.exec(statement).first()
                        if counter is not None:
                            counter.value = 0
                            counter.updated_at = datetime.utcnow()
                            session.add(counter)
                            session.commit()

                reset_db()
                count_label.set_text("Count: 0")

            ui.button("Reset", on_click=reset_count).classes("px-4 py-2 bg-gray-500 hover:bg-gray-600").mark("reset")
