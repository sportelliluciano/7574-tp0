package protocol

type EofCommand struct {
	AgencyId uint8
}

func NewEofCommand(agencyId uint8) EofCommand {
	return EofCommand{AgencyId: agencyId}
}

func (c *EofCommand) Serialize() ([]byte, error) {
	return SerializeCommand(Eof, []byte{c.AgencyId})
}
