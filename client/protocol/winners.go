package protocol

import "encoding/binary"

type WinnersCommand struct {
	AgencyId uint8
}

func NewWinnersCommand(agencyId uint8) WinnersCommand {
	return WinnersCommand{AgencyId: agencyId}
}

func (c *WinnersCommand) Serialize() ([]byte, error) {
	return SerializeCommand(Winners, []byte{c.AgencyId})
}

type WinnersResponse struct {
	WinnersCount uint16
	WinnersId    []uint32
}

func NewWinnersResponse(response *Response) WinnersResponse {
	count := binary.BigEndian.Uint16(response.payload[:2])
	winners := make([]uint32, count)
	for i := uint16(0); i < count; i++ {
		winners[i] = binary.BigEndian.Uint32(response.payload[2+4*i : 2+4*(i+1)])
	}

	return WinnersResponse{
		WinnersCount: count,
		WinnersId:    winners,
	}
}
