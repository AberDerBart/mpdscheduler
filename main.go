package main

import (
	"fmt"
	"os"
	"time"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"

	"github.com/vincent-petithory/mpdclient"
)

const schedulerChannelName = "scheduler"

func keepAlive(mpc *mpdclient.MPDClient) *time.Ticker {
	ticker := time.NewTicker(10 * time.Second)

	go func() error {
		for {
			<-ticker.C
			err := mpc.Ping()
			if err != nil {
				log.Error().Err(err).Msg("keepAlive failed")
			}
		}
	}()

	return ticker
}

func main() {
	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stdout, TimeFormat: "15:04:05"})

	config, err := ParseConfig()
	if err != nil {
		log.Error().Err(err).Msg("failed to parse config")
		os.Exit(1)
	}

	log.Info().Msgf("connecting to %s on port %d", config.host, config.port)
	mpc, err := mpdclient.Connect(config.host, config.port)
	if err != nil {
		log.Error().Err(err).Msg("failed to connect")
		os.Exit(1)
	}
	defer mpc.Close()

	err = mpc.Subscribe(schedulerChannelName)
	if err != nil {
		log.Error().Err(err).Msgf("failed to subscribe to channel %s", schedulerChannelName)
		os.Exit(1)
	}

	if config.additionalChannels {
		err = mpc.Subscribe("alarm")
		if err != nil {
			log.Error().Err(err).Msgf("failed to subscribe to channel alarm")
			os.Exit(1)
		}
		err = mpc.Subscribe("sleep")
		if err != nil {
			log.Error().Err(err).Msgf("failed to subscribe to channel sleep")
			os.Exit(1)
		}
		err = mpc.Subscribe("cancel")
		if err != nil {
			log.Error().Err(err).Msgf("failed to subscribe to channel cancel")
			os.Exit(1)
		}
	}

	log.Debug().Msgf("Listening on channel %s", schedulerChannelName)

	keepAlive(mpc)

	schedEvents := mpc.Idle("message")

	events := []*Event{}

	for {
		<-schedEvents.Ch
		msgs, err := mpc.ReadMessages()
		if err != nil {

			log.Error().Msgf("Failed to read message: %v", err)
		}

		for _, msg := range msgs {
			cmd := msg.Message
			if msg.Channel != schedulerChannelName {
				// an additional channel named after the command has been called - use the channel name as command
				cmd = fmt.Sprintf("%s %s", msg.Channel, msg.Message)
			}

			newEvents, err := ExecCommand(mpc, config, events, cmd)
			if err != nil {
				log.Warn().Str("cmd", msg.Message).Err(err).Msg("failed to execute command")
			}

			if newEvents != nil {
				events = newEvents
			}
		}
	}
}
