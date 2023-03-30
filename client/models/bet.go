package models

import (
	"errors"
	"strconv"
	"strings"
)

const MAX_STR_LEN = 30

type Bet struct {
	Agency      uint8
	Name        string
	LastName    string
	Id          uint32
	BirthYear   uint16
	BirthMonth  uint8
	BirthDay    uint8
	NumberToBet uint16
}

func NewBet(Agency uint8, Name string, LastName string, Id uint32, DateOfBirth string, NumberToBet uint16) (*Bet, error) {
	dateParts := strings.Split(DateOfBirth, "-")
	if len(dateParts) != 3 {
		return nil, errors.New("invalid date")
	}

	year, err := strconv.ParseUint(dateParts[0], 10, 16)
	if err != nil {
		return nil, err
	}

	month, err := strconv.ParseUint(dateParts[1], 10, 8)
	if err != nil {
		return nil, err
	}

	day, err := strconv.ParseUint(dateParts[2], 10, 8)
	if err != nil {
		return nil, err
	}

	if len(Name) > MAX_STR_LEN || len(LastName) > MAX_STR_LEN {
		return nil, errors.New("max string length is 30 characters")
	}

	return &Bet{
		Agency:      Agency,
		Name:        Name,
		LastName:    LastName,
		Id:          Id,
		BirthYear:   uint16(year),
		BirthMonth:  uint8(month),
		BirthDay:    uint8(day),
		NumberToBet: NumberToBet,
	}, nil
}
