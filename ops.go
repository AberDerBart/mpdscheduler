package main

import (
	"errors"
	"fmt"
	"time"

	"github.com/rs/zerolog/log"
	"github.com/vincent-petithory/mpdclient"
)

func listEvents(mpc *mpdclient.MPDClient, events []*Event) ([]*Event, error) {
	log.Info().Msgf("listing %d events\n", len(events))
	channels, err := mpc.Channels()
	if err != nil {
		return nil, err
	}

	scheduledChannelFound := false
	for _, channel := range channels {
		if channel == "scheduled" {
			scheduledChannelFound = true
		}
	}
	if !scheduledChannelFound {
		// Noone listens for the events list, so we don't have to say anything
		return events, nil
	}

	err = mpc.SendMessage("scheduled", "Scheduler queue:")
	if err != nil {
		return nil, err
	}

	for index, event := range events {
		msg := fmt.Sprintf("%d %v %s", index, event.Time, event.EventType)
		err = mpc.SendMessage("scheduled", msg)
		if err != nil {
			return nil, err
		}
	}

	return events, nil
}

func cancelEvent(mpc *mpdclient.MPDClient, events []*Event, index int) ([]*Event, error) {
	if index >= len(events) {
		return nil, errors.New(fmt.Sprintf("invalid index: %d", index))
	}

	event := events[index]

	log.Info().Msgf("canceling event #%d: %s at %v", index, event.EventType, event.Time)

	event.Cancel()

	return append(events[:index], events[index+1:]...), nil
}

func scheduleSleep(mpc *mpdclient.MPDClient, events []*Event, t *time.Time) ([]*Event, error) {
	log.Info().Msgf("scheduling sleep for %v", t)
	sleepEvent := Schedule(
		func() {
			log.Info().Msg("going to sleep")
			mpc.Cmd("stop")
		},
		t,
		"sleep",
	)
	return append(events, sleepEvent), nil
}

func scheduleAlarm(mpc *mpdclient.MPDClient, events []*Event, t *time.Time) ([]*Event, error) {
	log.Info().Msgf("scheduling alarm for %v", t)
	sleepEvent := Schedule(
		func() {
			log.Info().Msg("alarm")
			mpc.Cmd("play")
		},
		t,
		"alarm",
	)
	return append(events, sleepEvent), nil
}
