package protocol

import (
	"encoding/binary"
	"errors"
)

type CommandTag uint8

const (
	StoreBet CommandTag = 0b001
)

type Command interface {
	Serialize() ([]byte, error)
}

func SerializeCommand(tag CommandTag, payload []byte) ([]byte, error) {
	length := len(payload)

	if length > 8190 { // 8192 - 2 (tag and length)
		return nil, errors.New("cannot serialize command: payload exceeds 8190")
	}

	tag_and_length := (uint16(tag) << 13) | uint16(length)

	data := make([]byte, 2)
	binary.BigEndian.PutUint16(data, uint16(tag_and_length))
	return append(data, payload...), nil
}
