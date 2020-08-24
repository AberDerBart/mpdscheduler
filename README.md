# mpdScheduler

mpdScheduler is a client for mpd that adds functionality. This is done via the mpd channel interface.

## Supported features

* sleep - lets mpd fade out and stop the playback after a specified amount of time
* alarm - lets mpd start playback fade in at a specified point in time
* list all sleep timers and alarms
* cancel scheduled sleep timers and alarms

## Compilation

Compile using the go compiler and make like this
 
    $ make

## Usage

Start the program by typing

    $ ./mpdScheduler

By setting the `MPD_HOST` and `MPD_PORT` environment variables, host and port of the corresponding mpd server can be configured.
The fade time (in seconds) can be set with the `MPDSCHEDULER_FADE_TIME` environment variable.
The volume to fade to on an alarm can be set with the `MPDSCHEDULER_MAX_VOLUME` environment variable.

Then send commands via the mpd channel "scheduler" (for example using mpc). Responses are sent on the "scheduled" channel.
The syntax is as follows:

* `sleep [timestamp]`: initializes a sleep timer for [timestamp]
* `alarm [timestamp]`: sets an alarm for [timestamp]
* `list`: returns a list of all currently scheduled tasks (sleep timers and alarms)
* `cancel [index]`: cancels the task with index [index]. The indexes are shown in the response of the list command

Any items scheduled to a time in the past are executed immediately. Timestamps can be any of the following formats:

* `+[minutes]`: a time offset to the current time
* `[HH]:[MM]`: a time the current or the next day (dependent, if the time has passed already today)

The `sleep`, `alarm` and `cancel` commands can be send on the channels with the same name as the command as well, the message then only contains the arguments.
This behaviour can be deactivated by setting the environment variable `MPDSCHEDULER_ADDITIONAL_CHANNELS` to `0`.

### Examples

Set a sleep timer in 30 minutes
    
    $ mpc sendmessage scheduler "sleep +30"
  
Set an alarm for 7:25

    $ mpc sendmessage scheduler "alarm 7:25"
    
Cancel job with index 13

    $ mpc sendmessage scheduler "cancel 13"

Set an alarm in 10 minutes (using the alarm channel):

    $ mpc sendmessage alarm +10
