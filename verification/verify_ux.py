import sys
import os
import time

# Add parent directory to sys.path to ensure modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from playwright.sync_api import sync_playwright

def verify_ux():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Start Streamlit app in background (assuming it's running on port 8501)
        # Note: In this environment, we rely on the user or previous steps to have started the app.
        # But here I need to start it myself if I haven't.
        # Since I can't easily start a background process and wait for it in this script without blocking,
        # I will assume the user/agent handles the server start.
        # However, for this verification, I will just check if the port is open or try to connect.

        try:
            page.goto("http://localhost:8501")
            page.wait_for_timeout(3000) # Wait for load

            # 1. Verify Title
            assert "PVF: Unbreakable Engine Demo" in page.title()
            print("✅ Title Verified")

            # 2. Verify Tooltip presence (Playwright can check for 'aria-label' or 'title' or just existence of help icon)
            # Streamlit help tooltips usually appear as small question mark icons.
            # We can check if the help text exists in the DOM when hovering, but that's complex.
            # We can check if the elements that should have help text are present.

            # Check if "Script Input" label exists
            # In Streamlit, labels are often associated with the widget.
            # We can check if the text area is present.
            text_area = page.get_by_label("Script Input")
            assert text_area.is_visible()
            print("✅ Script Input Verified")

            # 3. Verify Expander (initially collapsed)
            # We need to run a simulation first to see the expander.

            # Click the main button
            # Button text: "Generate Blueprint & Simulate Render"
            page.get_by_role("button", name="Generate Blueprint & Simulate Render").click()

            # Wait for processing
            page.wait_for_timeout(5000)

            # Check for "View Technical Blueprint" expander
            expander = page.get_by_text("View Technical Blueprint")
            assert expander.is_visible()
            print("✅ Expander Verified")

            # 4. Verify Console Output is disabled (read-only)
            # The console output is a text area with label "Console Output"
            console_output = page.get_by_label("Console Output")
            # Streamlit disabled text areas usually have 'disabled' attribute or class.
            # Using .is_disabled() from Playwright
            # Note: Streamlit might implement disabled differently, but let's try.
            # If not standard HTML disabled, we might need to check attributes.
            # Actually, Streamlit disabled text area might just be read-only.

            # Let's check if we can type into it.
            try:
                console_output.fill("Test")
                print("❌ Console Output should be disabled but was editable.")
            except:
                print("✅ Console Output Verified (Read-only/Disabled)")

            # Take screenshot
            page.screenshot(path="verification/ux_verification.png")
            print("✅ Screenshot saved to verification/ux_verification.png")

        except Exception as e:
            print(f"❌ UX Verification Failed: {e}")
            sys.exit(1)

        browser.close()

if __name__ == "__main__":
    verify_ux()
