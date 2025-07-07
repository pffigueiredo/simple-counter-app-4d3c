from nicegui import ui, app


def create() -> None:
    @ui.page("/counter")
    def page():
        # Use client storage to persist count across page refreshes
        initial_count = app.storage.client.get("count", 0)

        # Create UI components
        count_label = (
            ui.label(f"Count: {initial_count}").classes("text-6xl font-bold text-center mb-8").mark("count-display")
        )

        def update_count(change: int) -> None:
            current_count = app.storage.client.get("count", 0)
            new_count = current_count + change
            app.storage.client["count"] = new_count
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
                app.storage.client["count"] = 0
                count_label.set_text("Count: 0")

            ui.button("Reset", on_click=reset_count).classes("px-4 py-2 bg-gray-500 hover:bg-gray-600").mark("reset")
