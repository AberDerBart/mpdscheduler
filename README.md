# fictional-potato

fictional-potato is a client for mpd that adds functionality. This is intended to be done via the mpd channel interface (but not yet implemented).

Thanks to GitHub for the nice name proposal.

## Supported features

* sleep - lets mpd fade out and stop the playback after a specified amount of time

## Usage

Start the program by typing

    $ python Client.py [mpdHost [mpdPort]]

If mpdPort is not given, fictional-potato will default to 6600. If mpdHost is not given, fictional-potato will read the $MPD_HOST environment variable or default to localhost, if $MPD_HOST is not set.

Then send commands via mpd channels (for example using mpc). Each feature is controlled by an individual channel.
The syntax is as follows:

* sleep: a sleep timer can be initialized by sending a timestamp on the sleep channel

### Examples

Set a sleep timer for 19:30
    
    $ mpc sendmessage sleep 19:30
  
