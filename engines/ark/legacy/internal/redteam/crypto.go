package redteam

import (
	"context"
	"github.com/polaris-owner/ARK/arkfield/internal/crypto"
)

type SignatureFailure struct{}

func (s SignatureFailure) Name() string { return "signature_failure" }
func (s SignatureFailure) Category() string { return "crypto" }

func (s SignatureFailure) Run(ctx context.Context) Result {
	env := crypto.Envelope{}
	ok := crypto.VerifyEnvelope(env)
	return Result{
		Name:   s.Name(),
		Passed: !ok,
		Severity: "critical",
		Recovery: "reject unsigned events",
	}
}
