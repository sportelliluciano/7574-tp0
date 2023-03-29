package protocol

import (
	"encoding/binary"
	"errors"
)

type StatusCode uint8

const (
	Ok    StatusCode = 0b111
	Error StatusCode = 0b110
)

type Response struct {
	status  StatusCode
	payload []byte
}

func DeserializeResponse(tag uint8, payload []byte) (*Response, error) {
	the_tag := StatusCode(tag)
	if the_tag == Ok || the_tag == Error {
		return &Response{status: the_tag, payload: payload}, nil
	}

	return nil, errors.New("invalid server response")
}

func ParseTagAndLength(data []byte) (uint8, uint16) {
	tag_and_length := binary.BigEndian.Uint16(data)
	tag := uint8(tag_and_length >> 13)
	length := tag_and_length & 0b0001_1111_1111_1111
	return tag, length
}

func (r *Response) IsSuccess() bool {
	return r.status == Ok
}

func (r *Response) ErrorMessage() string {
	if r.status == Error {
		errorMessage := string(r.payload)
		return errorMessage
	} else {
		return "success"
	}
}
