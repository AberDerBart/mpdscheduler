package main

import (
	"errors"
	"fmt"
	"math"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/rs/zerolog/log"
	"github.com/vincent-petithory/mpdclient"
)

func listEvents(mpc *mpdclient.MPDClient, config *Config, events []*Event) ([]*Event, error) {
	log.Info().Msgf("listing %d events", len(events))
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

func cancelEvent(mpc *mpdclient.MPDClient, config *Config, events []*Event, index int) ([]*Event, error) {
	if index >= len(events) {
		return nil, errors.New(fmt.Sprintf("invalid index: %d", index))
	}

	event := events[index]

	log.Info().Msgf("canceling event #%d: %s at %v", index, event.EventType, event.Time)

	event.Cancel()

	return append(events[:index], events[index+1:]...), nil
}

func getVol(mpc *mpdclient.MPDClient) (uint, error) {
	resp := mpc.Cmd("status")
	if resp.Err != nil {
		return 0, resp.Err
	}

	for _, data := range resp.Data {
		split := strings.Split(data, ":")
		if len(split) != 2 {
			log.Warn().Msgf("could not parse mpd response: %s", data)
		}

		key := strings.Trim(split[0], " \t")
		value := strings.Trim(split[1], " \t")

		if key == "volume" {
			vol, err := strconv.Atoi(value)
			if err != nil {
				return 0, err
			}
			return uint(vol), nil
		}
	}

	return 0, errors.New("no volume given")
}

func setVol(mpc *mpdclient.MPDClient, vol uint) error {
	if vol > 100 {
		return errors.New(fmt.Sprintf("invalid volume: %d", vol))
	}
	resp := mpc.Cmd(fmt.Sprintf("setvol %d", vol))
	return resp.Err
}

var (
	fadeMutex sync.Mutex
)

func fade(mpc *mpdclient.MPDClient, duration time.Duration, volStart, volEnd uint) error {
	fadeMutex.Lock()
	defer fadeMutex.Unlock()

	if volEnd > 100 {
		return errors.New(fmt.Sprintf("invalid volume: %d", volEnd))
	}

	if volEnd > volStart {
		log.Debug().Msgf("fading in from %d to %d, duration %.0fs", volStart, volEnd, math.Ceil(duration.Seconds()))
	} else {
		log.Debug().Msgf("fading out from %d to %d, duration %.0fs", volStart, volEnd, math.Ceil(duration.Seconds()))
	}
	err := setVol(mpc, volStart)
	if err != nil {
		return err
	}

	tickFn := func(v uint) uint {
		return v + 1
	}
	if volStart > volEnd {
		tickFn = func(v uint) uint {
			return v - 1
		}
	}

	steps := int(volEnd) - int(volStart)
	if steps < 0 {
		steps = -steps
	}
	if steps == 0 {
		return nil
	}

	interval := duration.Milliseconds() / int64(steps)
	ticker := time.NewTicker(time.Duration(interval) * time.Millisecond)

	for vol := uint(volStart); vol != uint(volEnd); vol = tickFn(vol) {
		<-ticker.C
		err = setVol(mpc, vol)
	}

	ticker.Stop()

	err = setVol(mpc, volEnd)
	if err != nil {
		return err
	}

	log.Debug().Msg("fade finished")

	return nil
}

func scheduleSleep(mpc *mpdclient.MPDClient, config *Config, events []*Event, t *time.Time) ([]*Event, error) {
	log.Info().Msgf("scheduling sleep for %v", t)
	sleepEvent := Schedule(
		func() error {
			log.Info().Msg("going to sleep")
			vol, err := getVol(mpc)
			if err == nil {
				err := fade(mpc, config.fadeTime, vol, 0)
				if err != nil {
					log.Error().Err(err).Msg("failed to fade")
					return err
				}
			} else {
				log.Warn().Err(err).Msg("failed to get volume, stopping playback")
			}

			log.Debug().Msg("pausing playback")
			resp := mpc.Cmd("pause")
			if resp.Err != nil {
				log.Error().Err(resp.Err).Msg("failed to pause")
				return resp.Err
			}

			if vol > 0 {
				log.Debug().Msgf("restoring volume to %d", vol)
				err = setVol(mpc, vol)
				if err != nil {
					log.Error().Err(err).Msg("failed to set volume")
					return err
				}
			}
			return nil
		},
		t,
		"sleep",
	)
	return append(events, sleepEvent), nil
}

func scheduleAlarm(mpc *mpdclient.MPDClient, config *Config, events []*Event, t *time.Time) ([]*Event, error) {
	log.Info().Msgf("scheduling alarm for %v", t)
	sleepEvent := Schedule(
		func() error {
			log.Info().Msg("alarm")
			err := setVol(mpc, 0)
			if err != nil {
				log.Error().Err(err).Msg("failed to set volume")
				return err
			}
			resp := mpc.Cmd("play")
			if resp.Err != nil {
				log.Error().Err(resp.Err).Msg("failed to play")
				return resp.Err
			}
			err = fade(mpc, config.fadeTime, 0, config.maxVol)
			if err != nil {
				log.Error().Err(err).Msg("failed to fade")
				return err
			}
			return nil
		},
		t,
		"alarm",
	)
	return append(events, sleepEvent), nil
}
