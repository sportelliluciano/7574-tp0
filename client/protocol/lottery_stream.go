package protocol

import (
	"io"
)

type LotteryStream struct {
	stream io.ReadWriteCloser
}

func NewLotteryStream(w io.ReadWriteCloser) LotteryStream {
	return LotteryStream{stream: w}
}

func (ls *LotteryStream) SendCommand(command Command) error {
	payload, err := command.Serialize()
	if err != nil {
		return err
	}

	return ls.sendExact(payload)
}

func (ls *LotteryStream) RecvResponse() (*Response, error) {
	tag_and_length, err := ls.recvExact(2)
	if err != nil {
		return nil, err
	}

	tag, length := ParseTagAndLength(tag_and_length)
	var payload []byte
	if length > 0 {
		payload, err = ls.recvExact(int(length))
		if err != nil {
			return nil, err
		}
	}

	return DeserializeResponse(tag, payload)
}

func (ls *LotteryStream) sendExact(payload []byte) error {
	totalWritten := 0
	for lastWritten, err := ls.stream.Write(payload[totalWritten:]); totalWritten != len(payload); totalWritten += lastWritten {
		if err != nil {
			return err
		}
	}

	return nil
}

func (ls *LotteryStream) recvExact(n int) ([]byte, error) {
	data := make([]byte, n)

	totalRead := 0
	for lastRead, err := ls.stream.Read(data[totalRead:]); totalRead != n; totalRead += lastRead {
		if err != nil {
			return nil, err
		}
	}

	return data, nil
}
