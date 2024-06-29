# COMMUPOOL
#### Video Demo:  https://youtu.be/HkKI2FdVDDY
## Intro:
CommuPool is a web-based application running on Python via Flask in the back-end as well as Javascript on the front-end and SQLite for data management. The purpose of the app is to match commuters together and make carpooling easier for the trips we make going to and from work. The way the matching is done is according to a combination of three factors: the postal code where the user lives, the postal code where the user works, the time at which they commute to their workplace, and the time at which they commute back home.

<br>

## Foundation:
- Flask
- SQLite3
- Javascript

<br>

As for the structure of the application, the foundation borrows much to PS8’s ”Finance” and mostly relies on three files:

- commute.py which contains the routing logic, data handling and the database queries.
- Helpers.py include the different service functions being uses recurrently throughout the application.
- Commute.db includes the references to the database and its tables.

<br>

Additionally, as per Flask’s specifications, the template folder contains the different views for the different section of the app.

<br>
<br>

### Python modules:
- CS50 SQL
- Flask (redirect, render_template, request, session)
- Flask_session (session)
- werkzeug.security (check_password_hash, generate_password_hash)
- werkzeug.datastructures (ImmutableMultiDict)

<br>
<br>

## Data architecture:

The database is composed of 4 tables:

- Users: referencing each user and their credentials, their home postal code and their workplace postal code.
- Postal_Codes: Contains a non-exhaustive list of Canadian Postal Codes converted from an existing CSV file.
- Commute_Days: Tracks the days on which each user is actually commuting.
- Commuting_Times: Keep a record of each user’s commenting times inbound and outbound.

<br>
<br>

## Use case:

The first interface of the application is the login page, on which the user will land by default as it is currently defined as the root page. From there, they can either log in (if they have an account) or register as a new user. After a new user registers, they will have to actually log-in in order to access their profile.

The profile page allows a user a set up or update their home and workplace addresses’ postal code, as well as the days they usually they commute and the times for inbound and outbound travel. This is still a bare MVP at the moment and some compromises were made to keep deadline. Some future developments would include a module for vehicle information (specifically, the number of seats available which could condition a maximum capacity feature and allow the app to manage carpooling request more accurately).

The other half of the application at the moment consistent of an overview of potential carpooling ”buddies” for the user… These are matched to the user by the app according to the corresponding postal codes (for home and workplace addresses) and commuting schedules (times and days) between users. Again, some enhancement task would be to allow users to switch between a ”driver” and a ””rider” view in their account.
<br>
<br>

## Sanity checks:


As another piece of legacy from PS8’s Finance, the application is able handle some erroneous user situations, such as:


- Erroneous/unknown password
- Erroneous/unknown username
- Pre-existing username (at sign-up)
- Pre-existing inconsistent password confirmation (at sign-up)