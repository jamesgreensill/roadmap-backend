In this project, you will build a simple command line interface (CLI) to fetch the recent activity of a GitHub user and display it in the terminal. This project will help you practice your programming skills, including working with APIs, handling JSON data, and building a simple CLI application.

## Requirements

The application should run from the command line, accept the GitHub username as an argument, fetch the user's recent activity using the GitHub API, and display it in the terminal. The user should be able to:

- Provide the GitHub username as an argument when running the CLI.
  ```bash
  github-activity <username>
  ```
- Fetch the recent activity of the specified GitHub user using the GitHub API. You can use the following endpoint to fetch the user's activity:
  ```
  # https://api.github.com/users/<username>/events
  # Example: https://api.github.com/users/kamranahmedse/events
  ```
- Display the fetched activity in the terminal.
  ```
  Output:
  jamesgreensill pushed 4 commits in jamesgreensill/roadmap-backend
  jamesgreensill opened 1 issue in jamesgreensill/roadmap-backend
  jamesgreensill pushed 1 commit in jamesgreensill/roadmap-backend
  jamesgreensill opened 2 issues in jamesgreensill/roadmap-backend
  jamesgreensill pushed 3 commits in jamesgreensill/roadmap-backend
  - ...
  ```
  You can [learn more about the GitHub API here](https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28).
- Handle errors gracefully, such as invalid usernames or API failures.
- Use a programming language of your choice to build this project.
- Do not use any external libraries or frameworks to fetch the GitHub activity.