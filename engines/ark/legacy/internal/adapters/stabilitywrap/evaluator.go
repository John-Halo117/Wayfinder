package stabilitywrap

import "github.com/polaris-owner/ARK/arkfield/internal/stability"

type Evaluator struct {
	Kernel *stability.Kernel
}

func (e Evaluator) Evaluate(observation stability.Observation) stability.Decision {
	return e.Kernel.Evaluate(observation)
}
