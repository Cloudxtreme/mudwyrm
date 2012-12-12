# Mudwyrm

Mudwyrm is an extensible HTML5/Websocket MUD client written and scripted in Python.

It's split into three packages:
  - [`mudwyrm`](https://github.com/voidseeker/mudwyrm) - web server built with [Pyramid](http://www.pylonsproject.org/) framework.
    Deals with user authentication, serves UI and user content to the browser.
    Also contains simple HTML5 script editor based on [Ace](http://ace.ajax.org/).
  - [`mudwyrm_engine`](https://github.com/voidseeker/mudwyrm_engine) - websocket server.
    The core component. Acts as a proxy between game (MUD) servers and websocket clients running on the users' browsers. Executes the user scripts. Uses [gevent](http://www.gevent.org/).
  - [`mudwyrm_users`](https://github.com/voidseeker/mudwyrm_users) - user content collection.
    Each user has a separate module inside this package that contains their scripts, data and UI files (HTML/CSS/JS that gets sent to the browser).
    With this, every user can not only have their own scripts for the game they play, but also fully customize the interface they see.

Although it does work, Mudwyrm is far from being finished and hasn't been developed since 2010, and I hope to get back to it in the future, but for now, here's the code.

## Features

  - **Thin client.**
    Due to the fact that the server acts as a proxy between the client (the webpage in the browser) and the MUD server, almost all the client does is display the data that comes from the server and send back the user input.
    This can make for a better user experience when playing on mobile devices, as it reduces hardware requirements (due to the client not having to parse text and execute scripts) while potentially improving the responsiveness (the server machine usually has better connection to the MUD server with lower latency than a mobile phone would if it had been connecting to the MUD directly).

  - **Multiuser support.**
    One server can handle multiple clients, and each user can have several games they are playing - the server keeps the files and settings for every game setup separately.

  - **Python scripting.**

  - **Customizable UI.**
    Users can fully customize the page by providing their own HTML/CSS files and writing JS plugins (like a health meter or a Canvas map of an area around the player).

  - **Built-in script editor** based on [Ace](http://ace.ajax.org/) lets the users edit their scripts and UI files right in the browser.

## Screenshots

![Game selection menu](https://dl.dropbox.com/u/4321724/mudwyrm/game-menu.png)
![Connecting to MUD](https://dl.dropbox.com/u/4321724/mudwyrm/connecting-to-mud.png)
![Gameplay 1](https://dl.dropbox.com/u/4321724/mudwyrm/gameplay-1.png)
![Gameplay 2](https://dl.dropbox.com/u/4321724/mudwyrm/gameplay-2.png)
![Code editor](https://dl.dropbox.com/u/4321724/mudwyrm/editor.png)

## Installation

Put all three packages in the same directory:

    $ git clone https://github.com/voidseeker/mudwyrm.git
    $ git clone https://github.com/voidseeker/mudwyrm_engine.git
    $ git clone https://github.com/voidseeker/mudwyrm_users.git

Install each of them in development mode:

    $ cd mudwyrm
    $ python setup.py develop
    $ cd ../mudwyrm_engine
    $ python setup.py develop
    $ cd ../mudwyrm_users
    $ python setup.py develop

Run the web server:

    $ cd ../mudwyrm
    $ pserve development.ini

Start the websocket server:

    $ cd ../mudwyrm_engine
    $ gunicorn -c config.py mudwyrm_engine:app

Alternatively, launch both servers at once with foreman:

    $ cd ../mudwyrm
    $ foreman start

Finally, open http://localhost:6543/ in the browser to play.
Log in as 'admin' with the password 'admin' to access the example scripts and UI that are provided within `mudwyrm_users` package.

## License

Copyright 2010 Shamil Fattakhov.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.