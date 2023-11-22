# NHL Scraper

### About

This is just a little side project to allow me to play with some NHL data.  My goal is compute statistics around players like the many advanced statistics sites out there.  However, it is not as much fun to just consume someone else's work, so I am doing it myself.

Eventually I would like to extend upon the statistics by incorporating Macnine Learning to see if I can predict some simple stats like if a player will score a goal in a game or not.

### Current state

Currently the app will query the NHL Edge API to gather a list of games for processing.  If there are not games loaded yet, it will start with 1980/1981 season.  Otherwise, it will look at the most recent game in the database and then use that game's data as the starting point for searching for newer games.  The NHL Edge API provides the next schedule date (which covers one week), so as long as that field is in the reponse, there are newer games we can process.

All these games get stored in an SQLite database.  Once all the scheduled games have been gathered, the app will query the NHL Edge API again for the game data.  Here I grab the list of players for a game, and the plays that occurred in the game.  I then build out the stats for each player, for each game and store those results in the database.

The app currently will retry processing games if there were any errors when requesting the data from the API.  In addition, it also throttles request to reduce the load on the API servers.  This throttling does cause the app to process the game data slowly.  However, this works out fine for me as I have wrapped it in a Docker container that I deploy to a home server where it can take as long as it needs without interruption.

### TODO

Here I have a general list of next items I am thinking about tackling.

- [ ] Calculate stats for players per season
- [ ] Calculate overall stats for players
- [ ] Update the logging statements to a uniformed format using the Python logging features
- [ ] Add in some environment variables for database and log locations for running in a Docker container
- [ ] Update processed game states to handle resuming processing if the app execution was interrupted

### Getting started

While I am not making this as a true "open source" project but rather just a "public source" project.  I thought I would add this section in case anyone is interested in trying it out.

First I setup a virtual environment and install the dependencies.

```sh
> virtualenv .venv
> . .venv/bin/activate
> pip install -r requirements.txt
```

Initialize the database.

```sh
> python src/init_db.py
```

Note: You can always recreate a fresh, empty database by passing the `--empty` flag to the `init_db.py` script.

```sh
> python src/init_db.py
```

Finally, you can run the script by executing the `main.py` file.

```sh
> python src/main.py
```

Note: This will take some time to run, likely measured in hours.
