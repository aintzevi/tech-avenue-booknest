# Tech Avenue Booknest (Workshop Version)

This repository contains a **deliberately messy, small Python web app** used for workshops about CI/CD, clean code, and architecture.

The story: this "Booknest" app has grown organically with **no clear ownership, no agreed architecture, and no standards**. Your task in the workshop is to inspect the codebase and propose improvements.

## Running the app

1. Create a virtual environment (optional but recommended).
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the app:

   ```bash
   python app.py
   ```

4. Open `http://127.0.0.1:5000/` in your browser. Try `http://127.0.0.1:5000/specials` as well.

## What to look for (for instructors)

This codebase intentionally includes:

- Hardcoded secrets, prices, and URLs
- Duplicated configuration and UI code
- Inconsistent UI styles and layout decisions
- No internal documentation or clear architecture
- A broken GitHub Actions workflow under `.github/workflows/deploy.yml`
- No environments concept – everything is treated as "production"

You can use this project to drive discussions about:

- Designing a CI/CD strategy and environments
- Introducing branching conventions and PR practices
- Refactoring towards cleaner code and clearer architecture
- Improving onboarding and documentation

