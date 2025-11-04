# How to Contribute to DB Reborn

Hello! We're thrilled that you're interested in contributing to DB Reborn. Every contribution is welcome! This document provides a set of guidelines to help you contribute to the project.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Help?

There are many ways to contribute, and not all of them involve writing code.

*   **Reporting Bugs:** If you find a problem, let us know!
*   **Suggesting Enhancements:** Have an idea for a new feature or an improvement to the interface? We'd love to hear it.
*   **Writing Documentation:** Documentation can always be improved.
*   **Contributing Code:** Fixing a bug or implementing a new feature.

## How to Report a Bug

Good bug reports are extremely helpful. Follow the steps below to ensure your report is as clear as possible.

1.  **Check if the bug has already been reported:** Search the [Issues](https://github.com/rfm-code-dev/DB-Reborn/issues ) section on GitHub to see if someone has already reported the same problem.

2.  **Be as detailed as possible:** Create a new "Issue" and include the following information:
    *   **A clear and descriptive title:** E.g., "App crashes when converting a JSON file with no bones."
    *   **DB Reborn Version:** E.g., v1.0.
    *   **Operating System:** E.g., Windows 11, Ubuntu 22.04.
    *   **Steps to reproduce the error:** Describe exactly what you did to make the error happen. E.g., "1. Opened the app. 2. Selected the `test.json` file. 3. Clicked Convert. 4. The app closed."
    *   **What did you expect to happen?** E.g., "I expected to see an error message saying the file was invalid."
    *   **What actually happened?** E.g., "The application closed unexpectedly with no message."
    *   **Attachments:** If possible, attach the DragonBones `.json` file that caused the problem. This helps us test and debug much faster!

## How to Suggest an Enhancement

1.  Create a new "Issue" on GitHub.
2.  Use a clear title, like "Suggestion: Add an animation preview in the UI."
3.  Describe your idea in detail. Explain the problem it solves and how you imagine the feature should work.

## How to Contribute Code

If you want to fix a bug or implement a new feature, please follow these steps:

1.  **Fork the repository:** Click the "Fork" button in the top-right corner of the project page to create a copy of the repository in your own GitHub account.

2.  **Clone your fork:**
    ```bash
    git clone https://github.com/rfm-code-dev/DB-Reborn.git
    ```

3.  **Create a new Branch:** Create a specific branch for your change. Use a descriptive name.
    ```bash
    git checkout -b my-awesome-fix
    ```

4.  **Make your changes:** Write your code, fix the bug, or implement the new feature.

5.  **Commit your changes:** Use clear commit messages.
    ```bash
    git add .
    git commit -m "Feat: Add support for shear interpolation"
    ```

6.  **Push your changes to your fork:**
    ```bash
    git push origin my-awesome-fix
    ```

7.  **Open a Pull Request (PR ):**
    *   Go to your fork's page on GitHub.
    *   Click the "Compare & pull request" button.
    *   In the PR title and description, clearly explain what you did and why. If your PR fixes an existing Issue, mention its number (e.g., `Fixes #42`).

Wait for your code to be reviewed. We may ask for some changes before merging your work into the main project.

Thank you for your contribution!
