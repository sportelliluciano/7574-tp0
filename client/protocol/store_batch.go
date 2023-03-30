package protocol

import (
	"encoding/binary"
	"errors"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/models"
)

const MAX_BETS_PER_BATCH = 32

type StoreBatchCommand struct {
	bets []*models.Bet
}

func NewStoreBatchCommand() StoreBatchCommand {
	return StoreBatchCommand{bets: make([]*models.Bet, 0)}
}

func (c *StoreBatchCommand) AddBet(bet *models.Bet) error {
	if len(c.bets) >= MAX_BETS_PER_BATCH {
		return errors.New("maximum number of bets per batch reached")
	}

	c.bets = append(c.bets, bet)
	return nil
}

func (c *StoreBatchCommand) Serialize() ([]byte, error) {
	data := []byte{}
	data = binary.BigEndian.AppendUint16(data, uint16(len(c.bets)))
	for i := 0; i < len(c.bets); i++ {
		data = append(data, serializeBetPayload(c.bets[i])...)
	}
	return SerializeCommand(StoreBatch, data)
}
