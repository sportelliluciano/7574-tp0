package service

import (
	"encoding/csv"
	"errors"
	"os"
	"strconv"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/models"
)

type BatchReader struct {
	agencyId uint8
	fd       *os.File
	reader   *csv.Reader
}

func NewBatchReader(agencyId uint8, path string) (*BatchReader, error) {
	fd, err := os.Open(path)
	if err != nil {
		return nil, err
	}

	reader := csv.NewReader(fd)
	return &BatchReader{agencyId: agencyId, fd: fd, reader: reader}, nil
}

func (br *BatchReader) Close() {
	br.fd.Close()
}

func (br *BatchReader) Next() (*models.Bet, error) {
	record, err := br.reader.Read()
	if err != nil {
		return nil, err
	}

	// Santiago Lionel,Lorca,30904465,1999-03-17,2201
	if len(record) != 5 {
		return nil, errors.New("invalid record: not enough fields in row")
	}

	name := record[0]
	lastName := record[1]
	id, err := strconv.Atoi(record[2])
	if err != nil {
		return nil, errors.New("invalid record: bad id")
	}
	dob := record[3]
	numberToBet, err := strconv.Atoi(record[4])
	if err != nil {
		return nil, errors.New("invalid record: bad number to bet")
	}

	return models.NewBet(br.agencyId, name, lastName, uint32(id), dob, uint16(numberToBet))
}
