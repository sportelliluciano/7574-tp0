package service

import (
	"errors"
	"io"
	"math/rand"
	"time"

	log "github.com/sirupsen/logrus"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/models"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/protocol"
)

const BACKOFF_FACTOR_SECONDS = 2
const BACKOFF_DISPERSION_MS = 1000

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
	return l.sendCommand(&cmd)
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

		err = l.sendCommand(&batch)
		if err != nil {
			return err
		}
	}

	return l.sendEof()
}

func (l *LotteryService) Winners() ([]uint32, error) {
	cmd := protocol.NewWinnersCommand(l.ID)

	for i := 1; ; i++ {
		response, err := l.client.SendCommand(&cmd)
		if err != nil {
			return nil, err
		}

		if response.IsSuccess() {
			winners := protocol.NewWinnersResponse(response)
			return winners.WinnersId, nil
		} else {
			// Server doesn't have a response yet. Wait some time
			// and try again. We'll use a randomized linear backoff
			// here to wait a little longer each time.
			// The reason to use a linear backoff instead of an exponential
			// backoff is that the server *is* available but our result isn't
			// there yet, as opposed to the server being unavailable.
			backoffTime := time.Duration(rand.Int31n(BACKOFF_DISPERSION_MS))*time.Millisecond + time.Duration(i*BACKOFF_FACTOR_SECONDS)*time.Second
			log.Infof("action: winners | result: backoff | backoff_time: %.3f s | server said: `%s`", backoffTime.Seconds(), response.ErrorMessage())
			time.Sleep(backoffTime)
			log.Infof("action: winners | result: backoff-resume")
		}

	}
}

func (l *LotteryService) sendEof() error {
	cmd := protocol.NewEofCommand(l.ID)
	return l.sendCommand(&cmd)
}

func (l *LotteryService) sendCommand(cmd protocol.Command) error {
	response, err := l.client.SendCommand(cmd)
	if err != nil {
		return err
	}

	if response.IsSuccess() {
		return nil
	}

	return errors.New(response.ErrorMessage())
}
