package main

import (
	"errors"
	"fmt"
	"os"
	"strconv"
)

type Config struct {
	host string
	port uint
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

	return &Config{
		host: envOrDefault("MPD_HOST", "localhost"),
		port: uint(port),
	}, nil
}
