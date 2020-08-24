package main

import (
	"errors"
	"fmt"
	"os"
	"strconv"
	"time"
)

type Config struct {
	host string
	port uint

	fadeTime time.Duration
	maxVol   uint

	additionalChannels bool
}

func envOrDefault(key, def string) string {
	res := os.Getenv(key)
	if res == "" {
		return def
	}
	return res
}

func ParseConfig() (*Config, error) {
	port, err := strconv.Atoi(envOrDefault("MPD_PORT", "6600"))
	if err != nil {
		return nil, err
	}
	if port < 0 || port > 65536 {
		return nil, errors.New(fmt.Sprintf("invalid port: %d", port))
	}

	fadeTime, err := strconv.Atoi(envOrDefault("MPDSCHEDULER_FADE_TIME", "30"))
	if err != nil {
		return nil, err
	}
	if fadeTime < 0 {
		return nil, errors.New(fmt.Sprintf("invalid fade time: %d", fadeTime))
	}

	maxVol, err := strconv.Atoi(envOrDefault("MPDSCHEDULER_MAX_VOLUME", "100"))
	if err != nil {
		return nil, err
	}
	if maxVol < 0 || maxVol > 65536 {
		return nil, errors.New(fmt.Sprintf("invalid volume: %d", maxVol))
	}

	additionalChannels := envOrDefault("MPDSCHEDULER_ADDITIONAL_CHANNELS", "1") == "1"

	return &Config{
		host:               envOrDefault("MPD_HOST", "localhost"),
		port:               uint(port),
		fadeTime:           time.Duration(fadeTime) * time.Second,
		maxVol:             uint(maxVol),
		additionalChannels: additionalChannels,
	}, nil
}
