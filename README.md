A website for displaying information and advertisements "PRs". Created with Python using flask. 
## Usage
- ```/``` displays PRs.
- ```/admin``` is the administrator interface for managing PRs. Can be accessed by any registered user. Users with the ```admin``` role will be able to manage all PRs while users with the ```pr``` role will only be able to access their own.
- ```/users``` is the user management interface, available only for users with the ```admin``` role.
- ```/pr``` returns a list of relative links to PRs to be shown in JSON format.

### Dates
A day starts at 5:00 and ends at 5:00 the next day. This means that an end date ```%yy-%mm-%dd``` translates to ```%yy-%mm%dd+1 5:00```. The time of start dates is also set to 5:00, except for when the start day is the current day. In this case the time is set to the current time and the PR is displayed immediately. PRs are permanently removed after their end date (as soon as ```/pr``` is requested).

### Priority
The default priority is 0. If a PR has its priority set to 1, it will be the only PR shown until its end date (useful for pubs etc.).

## Running in Docker
```
git clone https://github.com/mightynerd/tvmannen
make build
make up-prod
```
***Important***: Change ```SECRET_KEY``` in ```src/config.py``` to something more secret.

See docker-compose.yml/docker-compose.prod.yml for ports, which you probably want to change. A default admin account will be created on first start (if no existing database is present). Visit ```/login``` and login with "admin" and "pass".
