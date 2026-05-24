from pathlib import Path

from selene import browser


def close_modal():
    try:
        browser.element('#closeLargeModal').with_(timeout=0.5).click()
    except:
        pass


def path(file_name):
    return str(
        Path(__file__).parent
        .joinpath(f'resources/{file_name}')
    )