package service

import (
	"errors"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/models"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/protocol"
)

type LotteryService struct {
	client *common.Client
}

func NewLotteryService(client *common.Client) (*LotteryService, error) {
	return &LotteryService{client: client}, nil
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
