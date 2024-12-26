from playwright.sync_api import sync_playwright
import shutil
import os
import time
from utils import clean_user_data, connect_phantom_wallet, is_wallet_connected  # Importing functions from utils.py

# Constants
PHANTOM_EXTENSION_PATH = r"C:\Users\Ant UI Designer\AppData\Local\Google\Chrome\User Data\Profile 16\Extensions\bfnaelmomeimhlpmgjnjophhpkkoljpa\24.30.0_0"
KAMINO_URL = "https://app.kamino.finance/"
USER_DATA_DIR = "user_data"
PHANTOM_POPUP_URL = "chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/popup.html"

PASSWORD = "2VGw8q5eVfkigXZ4yrEMYCbEoELTrRYjCorZwiYG6SNZt5rK4pCXW2BAqMFmiYjtTN6xvJLYjxCPZ7GEnYb3JBXp"  # Replace with your actual password

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

            # Check if Phantom wallet is connected, otherwise connect it
            if not is_wallet_connected(page):
                connect_phantom_wallet(page)

            # Navigate to Kamino and connect the wallet if necessary
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
