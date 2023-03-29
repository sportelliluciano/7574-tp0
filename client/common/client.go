package common

import (
	"net"
	"time"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/protocol"
	log "github.com/sirupsen/logrus"
)

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID            string
	ServerAddress string
	LoopLapse     time.Duration
	LoopPeriod    time.Duration
}

// Client Entity that encapsulates how
type Client struct {
	config ClientConfig
	conn   net.Conn
}

// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(config ClientConfig) *Client {
	client := &Client{
		config: config,
	}
	return client
}

// CreateClientSocket Initializes client socket. In case of
// failure, error is printed in stdout/stderr and exit 1
// is returned
func (c *Client) createClientSocket() error {
	conn, err := net.Dial("tcp", c.config.ServerAddress)
	if err != nil {
		log.Fatalf(
			"action: connect | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
	}
	c.conn = conn
	return nil
}

func (c *Client) SendCommand(command protocol.Command) (*protocol.Response, error) {
	c.createClientSocket()
	defer c.conn.Close()
	lotteryStream := protocol.NewLotteryStream(c.conn)
	err := lotteryStream.SendCommand(command)
	if err != nil {
		log.Infof("action: send_command | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
		return nil, err
	}

	response, err := lotteryStream.RecvResponse()
	if err != nil {
		log.Infof("action: wait_response | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
		return nil, err
	}

	return response, nil
}
