# mpdScheduler

mpdScheduler is a client for mpd that adds functionality. This is intended to be done via the mpd channel interface (but not yet implemented).

## Supported features

* sleep - lets mpd fade out and stop the playback after a specified amount of time

## Usage

Start the program by typing

    $ python main.py [mpdHost [mpdPort]]

If mpdPort is not given, fictional-potato will default to 6600. If mpdHost is not given, fictional-potato will read the $MPD_HOST environment variable or default to localhost, if $MPD_HOST is not set.

Then send commands via the mpd channel "scheduler" (for example using mpc). Responses are sent on the "scheduled" channel.
The syntax is as follows:

* sleep: a sleep timer can be initialized by sending a timestamp on the sleep channel
* alarm: an alarm can be set by sending a timestamp on the alarm channel
* list: returns a list of all currently scheduled items
* cancel: any scheduled job can be canceled by sending the corresponding index on the cancel channel

Any items scheduled to a time in the past are executed immediately. Timestamps can be any of the following formats:

* +[minutes]: a time offset to the current time
* HH:MM[:ss]: a time the current or the next day (dependent, if the time has passed already today)
* dd/mm/yyyy HH:MM[:ss]: a date and time

### Examples

Set a sleep timer in 30 minutes
    
    $ mpc sendmessage scheduler "sleep +30"
  
Set an alarm for 7:25

    $ mpc sendmessage scheduler "alarm 7:25"
