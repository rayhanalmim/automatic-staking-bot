from playwright.sync_api import sync_playwright
import shutil
import os
import time

# Constants
PHANTOM_EXTENSION_PATH = r"C:\Users\Ant UI Designer\AppData\Local\Google\Chrome\User Data\Profile 16\Extensions\bfnaelmomeimhlpmgjnjophhpkkoljpa\24.30.0_0"
KAMINO_URL = "https://app.kamino.finance/"
USER_DATA_DIR = "user_data"
PHANTOM_POPUP_URL = "chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/popup.html"

PASSWORD = "2VGw8q5eVfkigXZ4yrEMYCbEoELTrRYjCorZwiYG6SNZt5rK4pCXW2BAqMFmiYjtTN6xvJLYjxCPZ7GEnYb3JBXp"  # Replace with your actual password


def clean_user_data():
    """Clean up the persistent user data directory to avoid browser context corruption."""
    if os.path.exists(USER_DATA_DIR):
        shutil.rmtree(USER_DATA_DIR)

def connect_phantom_wallet(page):
    """Function to connect Phantom wallet."""
    print("Connecting Phantom wallet...")

    try:
        # Navigate to the Phantom popup page
        page.goto(PHANTOM_POPUP_URL, wait_until="domcontentloaded")

        # Wait for the password field to appear
        page.wait_for_selector("input[type='password']", timeout=10000)

        print("Password field found, filling it with the provided password...")
        # Fill the password field
        page.fill("input[type='password']", PASSWORD)

        # Click the "Unlock" button
        page.click("button[type='submit']")
        print("Phantom wallet unlocked successfully.")
    except Exception as e:
        print(f"Error connecting Phantom wallet: {e}")
        raise

def navigate_to_kamino(page):
    """Function to navigate to Kamino and connect Phantom wallet."""
    print("Navigating to Kamino...")
    try:
        page.goto(KAMINO_URL, wait_until="domcontentloaded")

        # Wait for the Kamino app to load
        page.wait_for_selector("body", timeout=10000)
        print("Kamino page loaded.")

        # Connect Phantom wallet to Kamino
        print("Connecting Phantom wallet to Kamino...")
        page.evaluate("""
            () => {
                const provider = window.solana;
                if (provider && provider.isPhantom) {
                    provider.connect();
                    console.log("Connected Phantom wallet to Kamino");
                } else {
                    console.error("Phantom wallet not detected.");
                }
            }
        """)
        # Wait for wallet connection
        page.wait_for_function("window.solana && window.solana.publicKey", timeout=15000)
        print("Successfully connected Phantom wallet to Kamino.")
    except Exception as e:
        print(f"Error navigating to Kamino: {e}")
        raise

def main():
    with sync_playwright() as p:
        try:
            # Launch browser with Phantom extension
            browser = p.chromium.launch_persistent_context(
                user_data_dir="user_data",  # Persistent context to retain Phantom wallet session
                headless=False,
                args=[
                    f"--disable-extensions-except={PHANTOM_EXTENSION_PATH}",
                    f"--load-extension={PHANTOM_EXTENSION_PATH}",
                    "--start-maximized",
                ],
            )

            # Open a new page
            page = browser.pages[0] if browser.pages else browser.new_page()

            # Set viewport size
            page.set_viewport_size({"width": 1920, "height": 1080})

            # Connect Phantom wallet and navigate to Kamino
            connect_phantom_wallet(page)
            navigate_to_kamino(page)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Keep the browser open for inspection or close it after a delay
            print("Automation completed. Keeping the browser open for inspection.")
            time.sleep(300)
            browser.close()

if __name__ == "__main__":
    main()
