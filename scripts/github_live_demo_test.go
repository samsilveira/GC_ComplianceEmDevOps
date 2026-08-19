package main

import (
	"bufio"
	"bytes"
	"errors"
	"testing"
)

func TestParseRunIDFromOutput(t *testing.T) {
	t.Parallel()

	output := "https://github.com/example/project/actions/runs/32212377152"
	if got := parseRunIDFromOutput(output); got != 32212377152 {
		t.Fatalf("parseRunIDFromOutput() = %d, want 32212377152", got)
	}
}

func TestParseRunIDFromOutputWithoutURL(t *testing.T) {
	t.Parallel()

	if got := parseRunIDFromOutput("dispatch accepted"); got != 0 {
		t.Fatalf("parseRunIDFromOutput() = %d, want 0", got)
	}
}

func TestSelectNewRunUsesMarkerAndNewestID(t *testing.T) {
	t.Parallel()

	runs := []workflowRun{
		{DatabaseID: 10, DisplayTitle: "old"},
		{DatabaseID: 11, DisplayTitle: "DEMO session-1"},
		{DatabaseID: 13, DisplayTitle: "another session"},
		{DatabaseID: 12, DisplayTitle: "DEMO session-1"},
	}
	known := map[int64]struct{}{10: {}}

	if got := selectNewRun(runs, known, "session-1"); got != 12 {
		t.Fatalf("selectNewRun() = %d, want 12", got)
	}
}

func TestSelectNewRunIgnoresKnownRuns(t *testing.T) {
	t.Parallel()

	runs := []workflowRun{{DatabaseID: 20, DisplayTitle: "DEMO"}}
	known := map[int64]struct{}{20: {}}

	if got := selectNewRun(runs, known, "DEMO"); got != 0 {
		t.Fatalf("selectNewRun() = %d, want 0", got)
	}
}

func TestMatchesExpectedConclusion(t *testing.T) {
	t.Parallel()

	if !matchesExpectedConclusion("failure", "failure") {
		t.Fatal("expected matching failure conclusions")
	}
	if matchesExpectedConclusion("success", "failure") {
		t.Fatal("different conclusions must not match")
	}
}

func TestDecliningDispatchReturnsControlledCancellation(t *testing.T) {
	t.Parallel()

	input := bytes.NewBufferString("n\n")
	output := &bytes.Buffer{}
	app := &application{
		reader: bufio.NewReader(input),
		stdout: output,
	}

	if err := app.dispatchOfficialPipeline(); !errors.Is(err, errOperationCanceled) {
		t.Fatalf("dispatchOfficialPipeline() = %v, want controlled cancellation", err)
	}
}

func TestMenuShowsCancellationWithoutError(t *testing.T) {
	t.Parallel()

	input := bytes.NewBufferString("2\nn\n0\n")
	output := &bytes.Buffer{}
	app := &application{
		reader: bufio.NewReader(input),
		stdout: output,
		stderr: output,
	}

	if err := app.menu(); err != nil {
		t.Fatalf("menu() = %v, want nil", err)
	}
	if !bytes.Contains(output.Bytes(), []byte("[CANCELADO]")) {
		t.Fatalf("output = %q, want cancellation marker", output.String())
	}
	if bytes.Contains(output.Bytes(), []byte("[ERRO]")) {
		t.Fatalf("output = %q, cancellation must not be an error", output.String())
	}
}
