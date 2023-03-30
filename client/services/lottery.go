package service

import (
	"errors"
	"io"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/models"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/protocol"
)

type LotteryService struct {
	client       *common.Client
	betsPerBatch uint16
	ID           uint8
}

func NewLotteryService(client *common.Client, agencyId uint8, betsPerBatch uint16) (*LotteryService, error) {
	return &LotteryService{
		client:       client,
		betsPerBatch: betsPerBatch,
		ID:           agencyId,
	}, nil
}

func (l *LotteryService) StoreBet(bet *models.Bet) error {
	cmd := protocol.NewStoreBetCommand(bet)
	response, err := l.client.SendCommand(&cmd)
	if err != nil {
		return err
	}

	if response.IsSuccess() {
		return nil
	}

	return errors.New(response.ErrorMessage())
}

func (l *LotteryService) SendBatch(path string) error {
	reader, err := NewBatchReader(l.ID, path)
	if err != nil {
		return err
	}

	defer reader.Close()

	isEof := false
	for !isEof {
		batch := protocol.NewStoreBatchCommand()
		for i := 0; i < int(l.betsPerBatch); i++ {
			bet, err := reader.Next()
			if err != nil {
				if err == io.EOF {
					isEof = true
					break
				}
				return err
			}
			err = batch.AddBet(bet)
			if err != nil {
				return err
			}
		}

		response, err := l.client.SendCommand(&batch)
		if err != nil {
			return err
		}

		if !response.IsSuccess() {
			return errors.New(response.ErrorMessage())
		}
	}
	return nil
}
