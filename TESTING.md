# Statbotic Testing

- [Statbotic Testing](#statbotic-testing)
  - [HTML validation](#html-validation)
  - [CSS validation](#css-validation)
  - [PEP8 validation](#pep8-validation)
  - [Testing user stories](#testing-user-stories)
    - [As a manager/supervisor, I can...](#as-a-managersupervisor-i-can)
  - [Notable Bugs](#notable-bugs)


The project was tested continuosly throughout development by running the app multiple times between code changes. This was to test the output from the bot, exceptions being raised correctly and the spacing/clearing of the output. I used extra code to produce more verbose exceptions to help me to catch every error, which was then removed once the workflow had been thoroughly tested. Further [user story testing](#testing-user-stories) was also completed.

## HTML validation

The [W3C Markup Validation Service](https://validator.w3.org/) was used to validate the HTML of the website. Most of the HTML was provided for me as part of the Code Institute template for this project, with a few tweaks made to update the styling.

![HTML validation](docs/testing/html.png)

*Go back to the [top](#table-of-contents)*

---

## CSS validation

The [W3C Jigsaw CSS Validation Service](https://jigsaw.w3.org/css-validator/validator) was used to validate the CSS of the website. The CSS passes with 0 errors. There are 2 warnings due to the provided code in the project template.

![CSS validation](docs/testing/css.png)

*Go back to the [top](#table-of-contents)*

---

## PEP8 validation

[PEP8 Online](http://pep8online.com) was used to validate the Python code on the site. No errors were flagged in any of the Python files.

<details><summary>run.py</summary>
<img src="docs/testing/run.png">
</details>
<details><summary>app.py</summary>
<img src="docs/testing/app.png">
</details>
<details><summary>authorise.py</summary>
<img src="docs/testing/authorise.png">
</details>
<details><summary>database.py</summary>
<img src="docs/testing/database.png">
</details>
<details><summary>date.py</summary>
<img src="docs/testing/date.png">
</details>
<details><summary>helpers_stats.py</summary>
<img src="docs/testing/helpers_stats.png">
</details>
<details><summary>helpers.py</summary>
<img src="docs/testing/helpers.png">
</details>
<details><summary>stats.py</summary>
<img src="docs/testing/stats.png">
</details>
<details><summary>title.py</summary>
<img src="docs/testing/title.png">
</details>
<details><summary>user.py</summary>
<img src="docs/testing/user.png">
</details>
<details><summary>welcome.py</summary>
<img src="docs/testing/welcome.png">
</details>

*Go back to the [top](#table-of-contents)*

---

## Testing user stories

### As a manager/supervisor, I can...

US1: **...input stats to be saved for future reference.**

| **Feature** | **Acceptance criteria** | **Test** | **Result** |
|:--|:--|:--|:--:|
| [F7](README.md#7-add-or-update-statistics) | The user should be able to input statistics and see that they are saved to the database. | - Navigate to the menu option<br>- Input stats data<br>- See confirmation message<br>- View stats to ensure it was saved |:white_check_mark:|

US2: **...view historical stats for a particular date/date range.**
US3: **...see averages when viewing saved stats.**

| **Feature** | **Acceptance criteria** | **Test** | **Result** |
|:--|:--|:--|:--:|
| [F8](README.md#8-view-statistics) | The user should be able to choose a date/date range to view historical data from the database, along with averages. | - Navigate to the menu option<br>- Enter a date range<br>- See displayed stats<br>- See averages |:white_check_mark:|

US4: **...export the data so I can use my charting software.**

| **Feature** | **Acceptance criteria** | **Test** | **Result** |
|:--|:--|:--|:--:|
| [F9](README.md#9-export-stats) | The user should be able to save and export data to a JSON file[^1]. | - Navigate to the menu option<br>- Enter a date range<br>- See confirmation message and file path |:white_check_mark:|

[^1]: The file appears not to exist on Heroku due to the [ephemeral file system](https://help.heroku.com/K1PPS2WM/why-are-my-file-uploads-missing-deleted-from-the-application). This works locally.

US5: **...login to provide some security.**

| **Feature** | **Acceptance criteria** | **Test** | **Result** |
|:--|:--|:--|:--:|
| [F2](README.md#2-login-menu)<br>[F3](README.md#3-login)<br>[F4](README.md#4-register) | The user should be able to create login credentials and then login to see the main app. | - Choose register from login menu<br>- Create a new user<br>- Choose login from login menu<br>- Login and see main menu |:white_check_mark:|

US6: **...see a friendly application to help command-line be less scary.**

| **Feature** | **Acceptance criteria** | **Test** | **Result** |
|:--|:--|:--|:--:|
| [F1](README.md#1-welcome-banner)<br>[F6](README.md#6-main-menu) | The user should feel less anxious with the help of natural language and ascii art. | - Use the app<br>- Observe spacing and ascii art<br>- Read app output |:white_check_mark:|

US7: **...navigate the application easily.**

| **Feature** | **Acceptance criteria** | **Test** | **Result** |
|:--|:--|:--|:--:|
| [F2](README.md#2-login-menu)<br>[F6](README.md#6-main-menu)<br>[F5](README.md#5-exit) | The user should be able to move around the app easily. | - Use the app<br>- Try all the menu options |:white_check_mark:|

US8: **...see feedback on my actions.**

| **Feature** | **Acceptance criteria** | **Test** | **Result** |
|:--|:--|:--|:--:|
| [F10](README.md#10-exceptions) | The user should see feedback if an incorrect input is used or data is/is not found, etc. | - Use the app<br>- Test every feature while deliberately trying to break it<br>- See relevant error messages and loops |:white_check_mark:|

## Notable Bugs

My first version (Jan 2022) of this project ran into a number of issues with the menu system in particular. These are the bugs related to that. These were all rendered irrelevant by replacing the menus with much simpler code in my second version (Jun 2022).

- Entering a number that isn't an option kicks you out of the program, when it should stay on the menu.
- Logging in after registering was returning False and kicking out of the program.
- Enter random string when asking for a date prompts the program to return "Please insert a number:".
- Typing something other than y/n at y/n questions will kick back to the menu.
- Registering will also log you in.

The menu system in the first version relied on too many booleans, making for a confusing structure and bugs that were tricky to catch and fix. The second version separates the code into more files, breaking up the workflows, simplifying the menu system, and making a much more robust app.

These are the notable bugs from V1 and V2:

| **Resolved** | **Bug** | **Fix** |
|:--:|--|--|
| :white_check_mark: | $round in the MongoDB aggregator doesn't work | Remove it and use Python instead (V1) |
| :white_check_mark: | Unbound errors when trying to run app | Rename variables to avoid conflict - [commit](https://github.com/lucywoodman/stats-bot/commit/b2807f7a01e54cbdedef7f9801dd5c38e42002f2)|
| :white_check_mark: | Date input validation not working | Add try/except with exception message - [commit](https://github.com/lucywoodman/stats-bot/commit/13bf0abc307484c0a196730809ea697f69017ea2)|
| :white_check_mark: | Incorrect message seen before screen cleared when returning to menus | Add an else to menu loops - [commit](https://github.com/lucywoodman/stats-bot/commit/13c5fac263bc61ae012b5a291df541eef9067b0f)|
| :white_check_mark: | Catchall exception raised when a non-integer is entered for stats | Add a ValueError exception with better messaging - [commit](https://github.com/lucywoodman/stats-bot/commit/451d06ef8ed3e975a78d6274c484771a0ad38407)|