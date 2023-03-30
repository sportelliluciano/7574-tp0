package main

import (
	"fmt"
	"strings"
	"time"

	"github.com/pkg/errors"
	"github.com/sirupsen/logrus"
	log "github.com/sirupsen/logrus"
	"github.com/spf13/viper"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common"
	lottery "github.com/7574-sistemas-distribuidos/docker-compose-init/client/services"
)

// InitConfig Function that uses viper library to parse configuration parameters.
// Viper is configured to read variables from both environment variables and the
// config file ./config.yaml. Environment variables takes precedence over parameters
// defined in the configuration file. If some of the variables cannot be parsed,
// an error is returned
func InitConfig() (*viper.Viper, error) {
	v := viper.New()

	// Configure viper to read env variables with the CLI_ prefix
	v.AutomaticEnv()
	v.SetEnvPrefix("cli")
	// Use a replacer to replace env variables underscores with points. This let us
	// use nested configurations in the config file and at the same time define
	// env variables for the nested configurations
	v.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

	// Add env variables supported
	v.BindEnv("id")
	v.BindEnv("server", "address")
	v.BindEnv("loop", "period")
	v.BindEnv("loop", "lapse")
	v.BindEnv("log", "level")
	v.BindEnv("betsPerBatch", "betsPerBatch")

	// Bet info
	v.BindEnv("name", "name")
	v.BindEnv("lastname", "lastName")
	v.BindEnv("idcard", "idCard")
	v.BindEnv("birthdate", "birthdate")
	v.BindEnv("betnumber", "betNumber")

	// Try to read configuration from config file. If config file
	// does not exists then ReadInConfig will fail but configuration
	// can be loaded from the environment variables so we shouldn't
	// return an error in that case
	v.SetConfigFile("./config.yaml")
	if err := v.ReadInConfig(); err != nil {
		fmt.Printf("Configuration could not be read from config file. Using env variables instead")
	}

	// Parse time.Duration variables and return an error if those variables cannot be parsed
	if _, err := time.ParseDuration(v.GetString("loop.lapse")); err != nil {
		return nil, errors.Wrapf(err, "Could not parse CLI_LOOP_LAPSE env var as time.Duration.")
	}

	if _, err := time.ParseDuration(v.GetString("loop.period")); err != nil {
		return nil, errors.Wrapf(err, "Could not parse CLI_LOOP_PERIOD env var as time.Duration.")
	}

	return v, nil
}

// InitLogger Receives the log level to be set in logrus as a string. This method
// parses the string and set the level to the logger. If the level string is not
// valid an error is returned
func InitLogger(logLevel string) error {
	level, err := logrus.ParseLevel(logLevel)
	if err != nil {
		return err
	}

	customFormatter := &logrus.TextFormatter{
		TimestampFormat: "2006-01-02 15:04:05",
		FullTimestamp:   false,
	}
	logrus.SetFormatter(customFormatter)
	logrus.SetLevel(level)
	return nil
}

// PrintConfig Print all the configuration parameters of the program.
// For debugging purposes only
func PrintConfig(v *viper.Viper) {
	logrus.Infof("action: config | result: success | client_id: %s | server_address: %s | loop_lapse: %v | loop_period: %v | log_level: %s | bets_per_batch: %s | batch_file_path: %s",
		v.GetString("id"),
		v.GetString("server.address"),
		v.GetDuration("loop.lapse"),
		v.GetDuration("loop.period"),
		v.GetString("log.level"),
		v.GetString("betsPerBatch"),
		v.GetString("batchFilePath"),
	)
}

func main() {
	v, err := InitConfig()
	if err != nil {
		log.Fatalf("%s", err)
	}

	if err := InitLogger(v.GetString("log.level")); err != nil {
		log.Fatalf("%s", err)
	}

	// Print program config with debugging purposes
	PrintConfig(v)

	clientConfig := common.ClientConfig{
		ServerAddress: v.GetString("server.address"),
		ID:            v.GetString("id"),
		LoopLapse:     v.GetDuration("loop.lapse"),
		LoopPeriod:    v.GetDuration("loop.period"),
	}

	client := common.NewClient(clientConfig)
	log.Infof("action: create_client | result: in_progress")
	lottery, err := lottery.NewLotteryService(client, uint8(v.GetUint64("id")), uint16(v.GetUint64("betsPerBatch")))
	if err != nil {
		log.Fatalf("action: create_client | result: fail | err: %v", err)
	}
	log.Infof("action: create_client | result: success")

	log.Infof("action: send_batch | result: in_progress")
	err = lottery.SendBatch(v.GetString("batchFilePath"))
	if err != nil {
		log.Infof("action: send_batch | result: fail | err: %v", err)
	}
	log.Infof("action: send_batch | result: success")
}
