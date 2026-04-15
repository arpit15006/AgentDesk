"""
AgentDesk – AI Agent (Browser Automation)
Uses Playwright to perform IT actions via the admin panel UI.
Supports multi-step execution.
"""

import sys
import os
import asyncio
import json
import time
from playwright.async_api import async_playwright

# Fix for Playwright Node deprecation warnings (DEP0169 url.parse)
os.environ["NODE_OPTIONS"] = "--no-deprecation"

from llm_parser import parse_input

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
FRONTEND_URL = "http://localhost:3000"
STEP_DELAY_MS = 700  # Delay between steps for visual realism (human feel)


async def delay(ms: int = STEP_DELAY_MS):
    """Small delay between agent steps for realism."""
    await asyncio.sleep(ms / 1000)


# ---------------------------------------------------------------------------
# Action: Create User
# ---------------------------------------------------------------------------
async def create_user(page, email: str):
    """Navigate to create-user page and submit the form via UI."""
    print(f"\n[Agent] ---> Sub-task: Create user {email}")

    # Step 1: Navigate to create-user page
    print("[Agent] Navigating to create-user page...")
    await page.goto(f"{FRONTEND_URL}/create-user")
    await page.wait_for_load_state("networkidle")
    await delay()

    # Step 2: Type email into input field
    print(f"[Agent] Typing email: {email}")
    email_input = page.locator("[data-testid='email-input']")
    await email_input.click()
    await email_input.fill(email)
    await delay()

    # Step 3: Click create button
    print("[Agent] Clicking create button...")
    create_btn = page.locator("[data-testid='create-btn']")
    await create_btn.click()
    await delay(1500)

    # Step 4: Check for result
    print("[Agent] Verifying task completion...")
    print("[Agent] Checking for success message...")
    status = page.locator("[data-testid='create-status']")
    try:
        await status.wait_for(state="visible", timeout=5000)
        status_text = await status.text_content()
        
        if status_text and "already exists" in status_text.lower():
            print(f"[Agent] Done: User {email} already exists (not created)")
        elif status_text and "error" in status_text.lower():
            print(f"[Agent] Error: {status_text}")
        else:
            print(f"[Agent] Done: Successfully created user {email}")
    except Exception:
        print("[Agent] Warning: Could not find explicit success status, but form was submitted.")


# ---------------------------------------------------------------------------
# Action: Reset Password
# ---------------------------------------------------------------------------
async def reset_password(page, email: str):
    """Navigate to users page, find user, and click reset password via UI."""
    print(f"\n[Agent] ---> Sub-task: Reset password for {email}")

    # Step 1: Navigate to users page
    print("[Agent] Navigating to users page...")
    await page.goto(f"{FRONTEND_URL}/users")
    await page.wait_for_load_state("networkidle")
    await delay()

    # Step 2: Wait for users table to load
    print("[Agent] Waiting for users table to load...")
    table = page.locator("[data-testid='users-table']")
    try:
        await table.wait_for(state="visible", timeout=10000)
    except Exception:
        print("[Agent] Users table not found or empty.")
    await delay()

    # Step 3: Find and click reset button for the specific user
    print(f"[Agent] Looking for reset button for user: {email}...")
    reset_btn = page.locator(f"[data-testid='reset-btn-{email}']")

    try:
        await reset_btn.wait_for(state="visible", timeout=3000)
        print(f"[Agent] Found user {email}, clicking reset button...")
        await reset_btn.click()
        await delay(1500)
        
        print("[Agent] Verifying task completion...")
        print("[Agent] Checking for reset success message...")
        status = page.locator(f"[data-testid='reset-status-{email}']")
        await status.wait_for(state="visible", timeout=5000)
        print(f"[Agent] Done: Password reset successful for {email}")

    except Exception:
        print(f"[Agent] User {email} not found! Fallback triggered: creating user first...")
        # Fallback logic: Create user, then try resetting again
        await create_user(page, email)
        
        print(f"[Agent] Returning to users page to reset password for {email}...")
        await page.goto(f"{FRONTEND_URL}/users")
        await page.wait_for_load_state("networkidle")
        await delay()
        
        print(f"[Agent] Now clicking reset button for the newly created user...")
        reset_btn = page.locator(f"[data-testid='reset-btn-{email}']")
        await reset_btn.wait_for(state="visible", timeout=5000)
        await reset_btn.click()
        await delay(1500)
        
        print("[Agent] Verifying task completion...")
        print("[Agent] Checking for reset success message...")
        status = page.locator(f"[data-testid='reset-status-{email}']")
        await status.wait_for(state="visible", timeout=5000)
        print(f"[Agent] Done: Password reset successful for {email}")


# ---------------------------------------------------------------------------
# Main Agent Logic
# ---------------------------------------------------------------------------
async def run_agent(user_input: str):
    """Main agent entry point."""
    print("🤖 AgentDesk Initialized")
    print(f"[Agent] Received task: {user_input}")
    print("[Agent] Thinking... calling Groq to parse intent...")

    try:
        result = parse_input(user_input)
        tasks = result.get("tasks", [])
    except ValueError as e:
        print(f"[Agent] Failed to parse input: {e}")
        sys.exit(1)

    if not tasks:
        print("[Agent] Error: No tasks identified from input.")
        sys.exit(1)

    print(f"[Agent] Plan: Identified {len(tasks)} steps.")
    for i, t in enumerate(tasks):
        print(f"  {i+1}. {t['action'].upper()} -> {t['email']}")

    print("\n[Agent] Simulating human interaction...")
    print("[Agent] Launching browser to execute task sequence...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()

        try:
            for task in tasks:
                action = task['action']
                email = task['email']
                
                if action == "create":
                    await create_user(page, email)
                elif action == "reset":
                    await reset_password(page, email)
                else:
                    print(f"[Agent] Unknown action skipped: {action}")
            
            print("\n[Agent] Overall Task completed successfully")
        except Exception as e:
            print(f"\n[Agent] Error during automation: {e}")
        finally:
            await delay(3000)  # Keep browser open briefly to see result
            await browser.close()
            print("[Agent] Browser closed.")


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent.py \"<natural language request>\"")
        sys.exit(1)

    user_input = " ".join(sys.argv[1:])
    asyncio.run(run_agent(user_input))
