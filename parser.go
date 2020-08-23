package main

import (
	"errors"
	"fmt"
	"regexp"
	"strconv"
	"time"

	"github.com/vincent-petithory/mpdclient"
)

const timePattern = `((?P<time>(([01]?[0-9])|(2[0-3])):[0-5]\d)|(?P<offset>\+\d+))`

var (
	offsetTimeRE   = regexp.MustCompile(`^\+(\d+)$`)
	absoluteTimeRE = regexp.MustCompile(`^([01]?\d|2[0-3]):(\d\d)$`)
)

type Command struct {
}

func parseOffsetTime(timeString string) (*time.Time, error) {
	if !offsetTimeRE.MatchString(timeString) {
		return nil, errors.New("could not parse offset time")
	}

	minuteOffset, err := strconv.ParseInt(timeString, 10, 32)
	if err != nil {
		return nil, errors.New("could not parse offset time")
	}

	timeVal := time.Now().Add(time.Duration(minuteOffset) * time.Minute)
	return &timeVal, nil
}

func parseAbsoluteTime(timeString string) (*time.Time, error) {
	match := absoluteTimeRE.FindStringSubmatch(timeString)

	if len(match) != 3 {
		return nil, errors.New("could not parse absolute time")
	}

	hour, err := strconv.Atoi(match[1])
	if err != nil {
		return nil, err
	}

	minute, err := strconv.Atoi(match[2])
	if err != nil {
		return nil, err
	}

	now := time.Now()

	timeVal := time.Date(now.Year(), now.Month(), now.Day(), hour, minute, 0, 0, now.Location())
	if timeVal.Before(now) {
		timeVal = timeVal.Add(time.Hour * 24)
	}

	return &timeVal, nil
}

func ParseTime(timeString string) (*time.Time, error) {
	timeVal, err := parseOffsetTime(timeString)
	if err == nil {
		return timeVal, nil
	}

	timeVal, err = parseAbsoluteTime(timeString)
	if err == nil {
		return timeVal, nil
	}

	return nil, errors.New("could not parse time")
}

func newArgumentCountError(got, want int) error {
	return errors.New(fmt.Sprintf("invalid number of arguemnts: got %d, expected %d", got, want))
}

func ExecCommand(mpc *mpdclient.MPDClient, events []*Event, cmd string) ([]*Event, error) {
	split := regexp.MustCompile(`\s+`).Split(cmd, -1)

	if len(split) < 1 {
		return nil, errors.New("could not parse command")
	}

	if split[0] == "alarm" {
		if len(split) != 2 {
			return nil, newArgumentCountError(len(split), 2)
		}

		t, err := ParseTime(split[1])
		if err != nil {
			return nil, err
		}

		return scheduleAlarm(mpc, events, t)
	}

	if split[0] == "sleep" {
		if len(split) != 2 {
			return nil, newArgumentCountError(len(split), 2)
		}

		t, err := ParseTime(split[1])
		if err != nil {
			return nil, err
		}

		return scheduleSleep(mpc, events, t)
	}

	if split[0] == "list" {
		if len(split) != 1 {
			return nil, newArgumentCountError(len(split), 1)
		}

		return listEvents(mpc, events)
	}

	if split[0] == "cancel" {
		if len(split) != 2 {
			return nil, newArgumentCountError(len(split), 2)
		}

		index, err := strconv.Atoi(split[1])
		if err != nil {
			return nil, errors.New(fmt.Sprintf("could not parse index: %s", split[1]))
		}
		return cancelEvent(mpc, events, index)
	}

	return events, nil
}
