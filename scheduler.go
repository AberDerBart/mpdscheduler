package main

import "time"

type Event struct {
	EventType string
	Time      *time.Time
	timer     *time.Timer
	cancel    chan struct{}
}

func Schedule(f func(), t *time.Time, eventType string) *Event {

	timer := time.NewTimer(t.Sub(time.Now()))
	cancel := make(chan struct{})

	go func() {
		select {
		case <-timer.C:
			f()
		case <-cancel:
			return
		}
	}()

	return &Event{
		timer:     timer,
		cancel:    cancel,
		EventType: eventType,
		Time:      t,
	}
}

func (e *Event) Cancel() {
	e.timer.Stop()
	e.cancel <- struct{}{}
}
