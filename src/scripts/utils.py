import shutil
import os

# Constants
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

def is_wallet_connected(page):
    """Check if Phantom wallet is already connected."""
    print("Checking if Phantom wallet is already connected...")
    try:
        # Check if the wallet is connected by looking for the `solana` object
        page.wait_for_function("window.solana && window.solana.publicKey", timeout=5000)
        print("Phantom wallet is already connected.")
        return True
    except:
        print("Phantom wallet is not connected.")
        return False
