package protocol

import (
	"encoding/binary"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/models"
)

type StoreBetCommand struct {
	bet *models.Bet
}

func NewStoreBetCommand(bet *models.Bet) StoreBetCommand {
	return StoreBetCommand{bet: bet}
}

func (c *StoreBetCommand) Serialize() ([]byte, error) {
	return SerializeCommand(StoreBet, serializeBetPayload(c.bet))
}

func serializeBetPayload(bet *models.Bet) []byte {
	data := []byte{bet.Agency}
	data = binary.BigEndian.AppendUint16(data, uint16(bet.NumberToBet))
	data = binary.BigEndian.AppendUint32(data, uint32(bet.Id))
	data = binary.BigEndian.AppendUint16(data, uint16(bet.BirthYear))
	data = append(data, byte(bet.BirthMonth), byte(bet.BirthDay))

	// NUL-terminated UTF8 strings
	name := append([]byte(bet.Name), byte(0))
	lastName := append([]byte(bet.LastName), byte(0))
	return append(append(data, name...), lastName...)
}
