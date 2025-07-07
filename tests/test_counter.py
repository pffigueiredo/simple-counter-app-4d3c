from nicegui.testing import User
from nicegui import ui


async def test_counter_initial_state(user: User) -> None:
    """Test counter starts at 0."""
    await user.open("/counter")
    await user.should_see("Count: 0")


async def test_counter_increment(user: User) -> None:
    """Test incrementing the counter."""
    await user.open("/counter")

    # Click the increment button
    user.find(marker="increment").click()
    await user.should_see("Count: 1")

    # Click increment again
    user.find(marker="increment").click()
    await user.should_see("Count: 2")


async def test_counter_decrement(user: User) -> None:
    """Test decrementing the counter."""
    await user.open("/counter")

    # First increment to have a positive count
    user.find(marker="increment").click()
    user.find(marker="increment").click()
    await user.should_see("Count: 2")

    # Now decrement
    user.find(marker="decrement").click()
    await user.should_see("Count: 1")


async def test_counter_negative_values(user: User) -> None:
    """Test counter can go negative."""
    await user.open("/counter")

    # Decrement from 0
    user.find(marker="decrement").click()
    await user.should_see("Count: -1")

    # Decrement again
    user.find(marker="decrement").click()
    await user.should_see("Count: -2")


async def test_counter_reset(user: User) -> None:
    """Test resetting the counter."""
    await user.open("/counter")

    # Increment counter
    user.find(marker="increment").click()
    user.find(marker="increment").click()
    user.find(marker="increment").click()
    await user.should_see("Count: 3")

    # Reset counter
    user.find(marker="reset").click()
    await user.should_see("Count: 0")


async def test_counter_reset_from_negative(user: User) -> None:
    """Test resetting counter from negative value."""
    await user.open("/counter")

    # Decrement counter to negative
    user.find(marker="decrement").click()
    user.find(marker="decrement").click()
    await user.should_see("Count: -2")

    # Reset counter
    user.find(marker="reset").click()
    await user.should_see("Count: 0")


async def test_counter_ui_elements_exist(user: User) -> None:
    """Test that all UI elements are present."""
    await user.open("/counter")

    # Check that increment button exists
    await user.should_see(marker="increment")

    # Check that decrement button exists
    await user.should_see(marker="decrement")

    # Check that reset button exists
    await user.should_see(marker="reset")

    # Check that count label exists
    await user.should_see("Count: 0")


async def test_index_page_navigation(user: User) -> None:
    """Test navigation from index page to counter."""
    await user.open("/")

    # Check that index page content exists
    await user.should_see("Simple Counter App")
    await user.should_see("Go to Counter")

    # Click the link to counter
    user.find(ui.link).click()
    await user.should_see("Count: 0")


async def test_counter_multiple_operations(user: User) -> None:
    """Test multiple counter operations in sequence."""
    await user.open("/counter")

    # Perform a sequence of operations
    user.find(marker="increment").click()  # 1
    user.find(marker="increment").click()  # 2
    user.find(marker="increment").click()  # 3
    await user.should_see("Count: 3")

    user.find(marker="decrement").click()  # 2
    await user.should_see("Count: 2")

    user.find(marker="decrement").click()  # 1
    user.find(marker="decrement").click()  # 0
    user.find(marker="decrement").click()  # -1
    await user.should_see("Count: -1")

    user.find(marker="increment").click()  # 0
    await user.should_see("Count: 0")
