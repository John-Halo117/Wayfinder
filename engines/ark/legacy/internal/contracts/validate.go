package contracts

import (
	"errors"

	"github.com/polaris-owner/ARK/arkfield/internal/models"
)

func ValidateEvent(e models.Event) error {
	if e.CID == "" {
		return errors.New("missing cid")
	}
	if e.StateHash == "" {
		return errors.New("missing state_hash")
	}
	if e.Sequence == 0 {
		return errors.New("invalid sequence")
	}
	return nil
}
