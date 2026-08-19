// Command github_live_demo controls the live GitHub Actions presentation.
//
// It only invokes the authenticated GitHub CLI. Every remote dispatch requires
// an explicit confirmation, and the intentionally failing scenario runs in the
// isolated, non-blocking demo workflow.
package main

import (
	"bufio"
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"os"
	"os/exec"
	"os/signal"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"syscall"
	"time"
)

const (
	defaultRepository = "samsilveira/GC_ComplianceEmDevOps"
	defaultRef        = "main"
	officialWorkflow  = "compliance.yml"
	demoWorkflow      = "demo-compliance.yml"
)

var errOperationCanceled = errors.New("operação cancelada pelo apresentador")

type workflowRun struct {
	Conclusion   string `json:"conclusion"`
	CreatedAt    string `json:"createdAt"`
	DatabaseID   int64  `json:"databaseId"`
	DisplayTitle string `json:"displayTitle"`
	Status       string `json:"status"`
	URL          string `json:"url"`
}

type application struct {
	ctx         context.Context
	repository  string
	ref         string
	login       string
	pollTimeout time.Duration
	reader      *bufio.Reader
	stdout      io.Writer
	stderr      io.Writer
}

func main() {
	repository := flag.String(
		"repo",
		defaultRepository,
		"repositório no formato owner/name",
	)
	ref := flag.String("ref", defaultRef, "branch padrão usada nos disparos")
	pollTimeout := flag.Duration(
		"poll-timeout",
		60*time.Second,
		"tempo máximo para localizar o RUN_ID criado",
	)
	flag.Parse()

	ctx, stop := signal.NotifyContext(
		context.Background(),
		os.Interrupt,
		syscall.SIGTERM,
	)
	defer stop()

	app := &application{
		ctx:         ctx,
		repository:  *repository,
		ref:         *ref,
		pollTimeout: *pollTimeout,
		reader:      bufio.NewReader(os.Stdin),
		stdout:      os.Stdout,
		stderr:      os.Stderr,
	}

	if _, err := exec.LookPath("gh"); err != nil {
		fmt.Fprintln(app.stderr, "ERRO: GitHub CLI (gh) não encontrado no PATH.")
		os.Exit(1)
	}

	if err := app.menu(); err != nil && !errors.Is(err, context.Canceled) {
		fmt.Fprintf(app.stderr, "ERRO: %v\n", err)
		os.Exit(1)
	}
}

func (app *application) menu() error {
	for {
		app.printMenu()
		choice, err := app.readLine("Escolha uma opção: ")
		if err != nil {
			if errors.Is(err, io.EOF) {
				fmt.Fprintln(app.stdout, "\nEncerrando.")
				return nil
			}
			return err
		}

		var actionErr error
		switch strings.TrimSpace(choice) {
		case "1":
			actionErr = app.preflight()
		case "2":
			actionErr = app.dispatchOfficialPipeline()
		case "3":
			actionErr = app.dispatchDemo("policy_failure", "failure")
		case "4":
			actionErr = app.dispatchDemo("approved", "success")
		case "5":
			actionErr = app.watchExistingRun()
		case "6":
			actionErr = app.listRecentRuns()
		case "7":
			actionErr = app.downloadArtifacts()
		case "8":
			actionErr = app.openRunInBrowser()
		case "0":
			fmt.Fprintln(app.stdout, "Demonstração encerrada sem novos disparos.")
			return nil
		default:
			fmt.Fprintln(app.stderr, "Opção inválida. Use um número de 0 a 8.")
			continue
		}

		if errors.Is(actionErr, errOperationCanceled) {
			fmt.Fprintln(
				app.stdout,
				"\n[CANCELADO] Nenhum workflow foi disparado.",
			)
		} else if actionErr != nil {
			fmt.Fprintf(app.stderr, "\n[ERRO] %v\n", actionErr)
		} else {
			fmt.Fprintln(app.stdout, "\n[OK] Operação concluída.")
		}
		fmt.Fprintln(app.stdout)
	}
}

func (app *application) printMenu() {
	fmt.Fprintln(app.stdout, "============================================================")
	fmt.Fprintln(app.stdout, " Compliance em DevOps — demonstração ao vivo no GitHub")
	fmt.Fprintf(app.stdout, " Repositório: %s | Ref: %s\n", app.repository, app.ref)
	fmt.Fprintln(app.stdout, "============================================================")
	fmt.Fprintln(app.stdout, "1. Verificar pré-requisitos (sem alterar o remoto)")
	fmt.Fprintln(app.stdout, "2. Disparar pipeline oficial conforme (verde esperado)")
	fmt.Fprintln(app.stdout, "3. Disparar bloqueio controlado (vermelho esperado)")
	fmt.Fprintln(app.stdout, "4. Disparar cenário corrigido (verde esperado)")
	fmt.Fprintln(app.stdout, "5. Acompanhar uma execução existente pelo RUN_ID")
	fmt.Fprintln(app.stdout, "6. Listar execuções manuais recentes")
	fmt.Fprintln(app.stdout, "7. Baixar artefatos de uma execução")
	fmt.Fprintln(app.stdout, "8. Abrir uma execução no navegador")
	fmt.Fprintln(app.stdout, "0. Sair")
}

func (app *application) preflight() error {
	fmt.Fprintln(app.stdout, "\n[1/5] Conferindo autenticação do gh...")
	if err := app.runInteractive("auth", "status"); err != nil {
		return fmt.Errorf("autenticação do gh indisponível: %w", err)
	}

	fmt.Fprintln(app.stdout, "\n[2/5] Conferindo acesso ao repositório...")
	if err := app.runInteractive(
		"repo",
		"view",
		app.repository,
		"--json",
		"nameWithOwner,url",
	); err != nil {
		return fmt.Errorf("repositório indisponível: %w", err)
	}

	if err := app.resolveLogin(); err != nil {
		return err
	}
	fmt.Fprintf(app.stdout, "\n[3/5] Usuário autenticado: %s\n", app.login)

	fmt.Fprintln(app.stdout, "\n[4/5] Conferindo pipeline oficial...")
	if err := app.runInteractive(
		"workflow",
		"view",
		officialWorkflow,
		"--repo",
		app.repository,
	); err != nil {
		return fmt.Errorf("workflow oficial indisponível: %w", err)
	}

	fmt.Fprintln(app.stdout, "\n[5/5] Conferindo workflow isolado...")
	if err := app.runInteractive(
		"workflow",
		"view",
		demoWorkflow,
		"--repo",
		app.repository,
	); err != nil {
		return fmt.Errorf(
			"workflow de demonstração ainda não está na branch padrão: %w",
			err,
		)
	}

	fmt.Fprintln(app.stdout, "\nPré-requisitos aprovados para a demonstração.")
	return nil
}

func (app *application) dispatchOfficialPipeline() error {
	confirmed, err := app.confirm(
		"Disparar agora o Compliance Pipeline oficial na main?",
	)
	if err != nil {
		return err
	}
	if !confirmed {
		return errOperationCanceled
	}

	return app.dispatchAndWatch(
		officialWorkflow,
		nil,
		"success",
		"",
	)
}

func (app *application) dispatchDemo(scenario string, expected string) error {
	description := "cenário corrigido, com conclusão verde"
	if expected == "failure" {
		description = "bloqueio isolado, com conclusão vermelha esperada"
	}

	confirmed, err := app.confirm(
		fmt.Sprintf("Disparar agora o %s?", description),
	)
	if err != nil {
		return err
	}
	if !confirmed {
		return errOperationCanceled
	}

	demoID := fmt.Sprintf(
		"%s-%s",
		scenario,
		time.Now().UTC().Format("20060102T150405Z"),
	)
	inputs := map[string]string{
		"demo_id":  demoID,
		"scenario": scenario,
	}
	return app.dispatchAndWatch(demoWorkflow, inputs, expected, demoID)
}

func (app *application) dispatchAndWatch(
	workflow string,
	inputs map[string]string,
	expectedConclusion string,
	titleMarker string,
) error {
	if err := app.resolveLogin(); err != nil {
		return err
	}

	beforeRuns, err := app.listRuns(workflow)
	if err != nil {
		return fmt.Errorf("não foi possível listar runs antes do disparo: %w", err)
	}
	knownIDs := make(map[int64]struct{}, len(beforeRuns))
	for _, run := range beforeRuns {
		knownIDs[run.DatabaseID] = struct{}{}
	}

	arguments := []string{
		"workflow",
		"run",
		workflow,
		"--repo",
		app.repository,
		"--ref",
		app.ref,
	}
	keys := make([]string, 0, len(inputs))
	for key := range inputs {
		keys = append(keys, key)
	}
	sort.Strings(keys)
	for _, key := range keys {
		arguments = append(arguments, "--raw-field", key+"="+inputs[key])
	}

	fmt.Fprintf(app.stdout, "\nDisparando %s...\n", workflow)
	output, err := app.runCapture(arguments...)
	if output != "" {
		fmt.Fprintln(app.stdout, output)
	}
	if err != nil {
		return fmt.Errorf("falha ao disparar workflow: %w", err)
	}

	runID := parseRunIDFromOutput(output)
	if runID == 0 {
		fmt.Fprintln(app.stdout, "Aguardando o GitHub registrar o RUN_ID...")
		runID, err = app.waitForNewRun(workflow, knownIDs, titleMarker)
		if err != nil {
			return err
		}
	}

	fmt.Fprintf(
		app.stdout,
		"RUN_ID localizado: %d\nhttps://github.com/%s/actions/runs/%d\n",
		runID,
		app.repository,
		runID,
	)

	if err := app.watchRun(runID); err != nil {
		return err
	}
	run, err := app.viewRun(runID)
	if err != nil {
		return err
	}

	fmt.Fprintf(
		app.stdout,
		"Conclusão observada: %s | Esperada: %s\n",
		run.Conclusion,
		expectedConclusion,
	)
	if !matchesExpectedConclusion(run.Conclusion, expectedConclusion) {
		return fmt.Errorf(
			"conclusão inesperada: %s (esperado %s)",
			run.Conclusion,
			expectedConclusion,
		)
	}

	open, err := app.confirm("Abrir esta execução no navegador?")
	if err != nil {
		return err
	}
	if open {
		return app.runInteractive(
			"run",
			"view",
			strconv.FormatInt(runID, 10),
			"--repo",
			app.repository,
			"--web",
		)
	}
	return nil
}

func (app *application) resolveLogin() error {
	if app.login != "" {
		return nil
	}
	output, err := app.runCapture("api", "user", "--jq", ".login")
	if err != nil {
		return fmt.Errorf("não foi possível identificar o usuário autenticado: %w", err)
	}
	app.login = strings.TrimSpace(output)
	if app.login == "" {
		return errors.New("o GitHub CLI retornou um login vazio")
	}
	return nil
}

func (app *application) listRuns(workflow string) ([]workflowRun, error) {
	arguments := []string{
		"run",
		"list",
		"--repo",
		app.repository,
		"--workflow",
		workflow,
		"--event",
		"workflow_dispatch",
		"--branch",
		app.ref,
		"--limit",
		"20",
		"--json",
		"databaseId,displayTitle,status,conclusion,url,createdAt",
	}
	if app.login != "" {
		arguments = append(arguments, "--user", app.login)
	}

	output, err := app.runCapture(arguments...)
	if err != nil {
		return nil, err
	}
	var runs []workflowRun
	if err := json.Unmarshal([]byte(output), &runs); err != nil {
		return nil, fmt.Errorf("JSON inválido retornado por gh run list: %w", err)
	}
	return runs, nil
}

func (app *application) waitForNewRun(
	workflow string,
	knownIDs map[int64]struct{},
	titleMarker string,
) (int64, error) {
	deadline := time.Now().Add(app.pollTimeout)
	for time.Now().Before(deadline) {
		select {
		case <-app.ctx.Done():
			return 0, app.ctx.Err()
		case <-time.After(2 * time.Second):
		}

		runs, err := app.listRuns(workflow)
		if err != nil {
			fmt.Fprintf(app.stderr, "Aviso ao consultar runs: %v\n", err)
			continue
		}
		if runID := selectNewRun(runs, knownIDs, titleMarker); runID != 0 {
			return runID, nil
		}
	}
	return 0, fmt.Errorf(
		"RUN_ID não apareceu em %s; consulte a aba Actions antes de repetir",
		app.pollTimeout,
	)
}

func selectNewRun(
	runs []workflowRun,
	knownIDs map[int64]struct{},
	titleMarker string,
) int64 {
	var selected int64
	for _, run := range runs {
		if _, known := knownIDs[run.DatabaseID]; known {
			continue
		}
		if titleMarker != "" && !strings.Contains(run.DisplayTitle, titleMarker) {
			continue
		}
		if run.DatabaseID > selected {
			selected = run.DatabaseID
		}
	}
	return selected
}

func parseRunIDFromOutput(output string) int64 {
	pattern := regexp.MustCompile(`/actions/runs/([0-9]+)`)
	match := pattern.FindStringSubmatch(output)
	if len(match) != 2 {
		return 0
	}
	runID, err := strconv.ParseInt(match[1], 10, 64)
	if err != nil {
		return 0
	}
	return runID
}

func matchesExpectedConclusion(observed string, expected string) bool {
	return observed == expected
}

func (app *application) watchRun(runID int64) error {
	fmt.Fprintln(app.stdout, "\nAcompanhando jobs em tempo real...")
	if err := app.runInteractive(
		"run",
		"watch",
		strconv.FormatInt(runID, 10),
		"--repo",
		app.repository,
		"--compact",
		"--interval",
		"3",
	); err != nil {
		return fmt.Errorf("falha ao acompanhar o run: %w", err)
	}
	return nil
}

func (app *application) viewRun(runID int64) (workflowRun, error) {
	output, err := app.runCapture(
		"run",
		"view",
		strconv.FormatInt(runID, 10),
		"--repo",
		app.repository,
		"--json",
		"databaseId,displayTitle,status,conclusion,url,createdAt",
	)
	if err != nil {
		return workflowRun{}, fmt.Errorf("falha ao consultar conclusão: %w", err)
	}
	var run workflowRun
	if err := json.Unmarshal([]byte(output), &run); err != nil {
		return workflowRun{}, fmt.Errorf("JSON inválido em gh run view: %w", err)
	}
	return run, nil
}

func (app *application) watchExistingRun() error {
	rawID, err := app.readLine("RUN_ID que deseja acompanhar: ")
	if err != nil {
		return err
	}
	runID, err := strconv.ParseInt(strings.TrimSpace(rawID), 10, 64)
	if err != nil || runID <= 0 {
		return errors.New("RUN_ID inválido")
	}
	if err := app.watchRun(runID); err != nil {
		return err
	}
	run, err := app.viewRun(runID)
	if err != nil {
		return err
	}
	fmt.Fprintf(app.stdout, "Conclusão: %s | %s\n", run.Conclusion, run.URL)
	return nil
}

func (app *application) listRecentRuns() error {
	fmt.Fprintln(app.stdout, "\nPipeline oficial:")
	if err := app.runInteractive(
		"run",
		"list",
		"--repo",
		app.repository,
		"--workflow",
		officialWorkflow,
		"--event",
		"workflow_dispatch",
		"--limit",
		"5",
	); err != nil {
		return err
	}

	fmt.Fprintln(app.stdout, "\nDemonstração isolada:")
	if err := app.runInteractive(
		"run",
		"list",
		"--repo",
		app.repository,
		"--workflow",
		demoWorkflow,
		"--event",
		"workflow_dispatch",
		"--limit",
		"5",
	); err != nil {
		return err
	}
	return nil
}

func (app *application) downloadArtifacts() error {
	rawID, err := app.readLine("RUN_ID dos artefatos: ")
	if err != nil {
		return err
	}
	runID, err := strconv.ParseInt(strings.TrimSpace(rawID), 10, 64)
	if err != nil || runID <= 0 {
		return errors.New("RUN_ID inválido")
	}

	defaultDirectory := filepath.Join(
		"reports",
		fmt.Sprintf("github-run-%d", runID),
	)
	directory, err := app.readLine(
		fmt.Sprintf("Diretório de destino [%s]: ", defaultDirectory),
	)
	if err != nil {
		return err
	}
	directory = strings.TrimSpace(directory)
	if directory == "" {
		directory = defaultDirectory
	}

	return app.runInteractive(
		"run",
		"download",
		strconv.FormatInt(runID, 10),
		"--repo",
		app.repository,
		"--dir",
		directory,
	)
}

func (app *application) openRunInBrowser() error {
	rawID, err := app.readLine("RUN_ID que deseja abrir: ")
	if err != nil {
		return err
	}
	runID, err := strconv.ParseInt(strings.TrimSpace(rawID), 10, 64)
	if err != nil || runID <= 0 {
		return errors.New("RUN_ID inválido")
	}
	return app.runInteractive(
		"run",
		"view",
		strconv.FormatInt(runID, 10),
		"--repo",
		app.repository,
		"--web",
	)
}

func (app *application) confirm(prompt string) (bool, error) {
	answer, err := app.readLine(prompt + " [s/N]: ")
	if err != nil {
		return false, err
	}
	normalized := strings.ToLower(strings.TrimSpace(answer))
	return normalized == "s" || normalized == "sim", nil
}

func (app *application) readLine(prompt string) (string, error) {
	fmt.Fprint(app.stdout, prompt)
	line, err := app.reader.ReadString('\n')
	if err != nil && !errors.Is(err, io.EOF) {
		return "", err
	}
	if errors.Is(err, io.EOF) && line == "" {
		return "", io.EOF
	}
	return strings.TrimSpace(line), nil
}

func (app *application) runInteractive(arguments ...string) error {
	command := exec.CommandContext(app.ctx, "gh", arguments...)
	command.Stdin = os.Stdin
	command.Stdout = app.stdout
	command.Stderr = app.stderr
	return command.Run()
}

func (app *application) runCapture(arguments ...string) (string, error) {
	command := exec.CommandContext(app.ctx, "gh", arguments...)
	var stdout bytes.Buffer
	var stderr bytes.Buffer
	command.Stdout = &stdout
	command.Stderr = &stderr
	err := command.Run()
	output := strings.TrimSpace(strings.Join(
		filterEmptyStrings(stdout.String(), stderr.String()),
		"\n",
	))
	return output, err
}

func filterEmptyStrings(values ...string) []string {
	filtered := make([]string, 0, len(values))
	for _, value := range values {
		if trimmed := strings.TrimSpace(value); trimmed != "" {
			filtered = append(filtered, trimmed)
		}
	}
	return filtered
}
