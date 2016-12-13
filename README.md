# mpdScheduler

mpdScheduler is a client for mpd that adds functionality. This is done via the mpd channel interface.

## Supported features

* sleep - lets mpd fade out and stop the playback after a specified amount of time
* alarm - lets mpd start playback fade in at a specified point in time
* list all sleep timers and alarms
* cancel scheduled sleep timers and alarms

## Dependencies

mpdScheduler has the following dependencies:

* python-mpd2
* parse

## Usage

Start the program by typing

    $ python main.py [mpdHost [mpdPort]]

If mpdPort is not given, mpdScheduler will default to 6600. If mpdHost is not given, mpdScheduler will read the $MPD_HOST environment variable or default to localhost, if $MPD_HOST is not set.

Then send commands via the mpd channel "scheduler" (for example using mpc). Responses are sent on the "scheduled" channel.
The syntax is as follows:

* sleep [timestamp]: initializes a sleep timer for [timestamp]
* alarm [timestamp]: sets an alarm for [timestamp]
* list: returns a list of all currently scheduled tasks (sleep timers and alarms)
* cancel [index]: cancels the task with index [index]. The indexes are shown in the response of the list command

Any items scheduled to a time in the past are executed immediately. Timestamps can be any of the following formats:

* +[minutes]: a time offset to the current time
* HH:MM[:ss]: a time the current or the next day (dependent, if the time has passed already today)

### Examples

Set a sleep timer in 30 minutes
    
    $ mpc sendmessage scheduler "sleep +30"
  
Set an alarm for 7:25

    $ mpc sendmessage scheduler "alarm 7:25"
    
Cancel job with index 13

    $ mpc sendmessage scheduler "cancel 13"
