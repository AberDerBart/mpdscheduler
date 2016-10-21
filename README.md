# fictional-potato

fictional-potato is a client for mpd that adds functionality. This is intended to be done via the mpd channel interface (but not yet implemented).

Thanks to GitHub for the nice name proposal.

## Supported features

* sleep - lets mpd fade out and stop the playback after a specified amount of time

## Usage

Start the program by typing

    $ python Client.py [mpdHost [mpdPort]]

Then send commands via mpd channels (for example using mpc). Each feature is controlled by an individual channel.
The syntax is as follows:

* sleep: a sleep timer can be initialized by sending a timestamp on the sleep channel

### Examples

Set a sleep timer for 19:30
    
    $ mpc sendmessage sleep 19:30
  
