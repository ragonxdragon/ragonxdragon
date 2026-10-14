<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Jack Hall, IoT and embedded systems engineer" src="assets/banner-light.svg" width="100%">
</picture>

I build connected devices and the systems behind them: ESP32 firmware that keeps reporting over cellular from rooms nobody visits, the cloud plumbing that manages it, and the Python tooling that tests and measures all of it.

Most of my production work is client firmware in private repositories. The public projects below show how I work.

**Available for contract work and full-time roles** in embedded, IoT, and industrial data.<br>
[Portfolio and case studies](https://johnragonhall.github.io) &nbsp;·&nbsp; [Email](mailto:johnragonhall@gmail.com) &nbsp;·&nbsp; [LinkedIn](https://www.linkedin.com/in/johnragonhall) &nbsp;·&nbsp; United States

## Selected work

### [twinflow](https://github.com/johnragonhall/twinflow)

A digital twin of a warehouse operation. A discrete-event model of receiving and putaway drives a simulated device fleet over MQTT, a Lean Six Sigma engine judges both the live telemetry and the model's own predictions, and an AI agent answers what-if questions with a statistical verdict instead of a paragraph. The deployment follows the Purdue model: the broker bridge is the only path between the OT and IT segments.

`Python` `MQTT` `Sparkplug B` `ISA-95` `SPC` &nbsp;·&nbsp; [Docs](https://johnragonhall.github.io/twinflow/) &nbsp;·&nbsp; v0.1.0, phase 1 in progress

### [spbconform](https://github.com/johnragonhall/spbconform)

The full Eclipse Sparkplug B v3.0.0 assertion table with a runner that checks an edge node against it. It carries all 299 testable assertions, executable checks for the 143 an in-process harness can observe, and a recorded reason for each one it cannot. Written clean-room, with zero dependencies, under MIT.

`Python` `Sparkplug B` `MQTT` `conformance testing`

### [secom-spc](https://github.com/johnragonhall/secom-spc)

Statistical process control on the UCI SECOM semiconductor dataset: I-MR charts with Nelson rules, EWMA and CUSUM, an autocorrelation check that decides whether a chart can be trusted, and a fail-prediction study on a time-ordered split that reports honestly when the data does not support a model.

`Python` `SPC` `scikit-learn` `Jupyter`

### Code samples

[Recovery ladder](https://gist.github.com/johnragonhall/40e022699158dc6cc4e20941b1def484) (C++17, boot-loop detection, no heap) &nbsp;·&nbsp; [Cellular backoff](https://gist.github.com/johnragonhall/dc041808503e7cbfaa6d99bd95b8b2a3) (C++17, full jitter and circuit breaker) &nbsp;·&nbsp; [Nelson rules checker](https://gist.github.com/johnragonhall/897b5ff8f95737c4feb72646c48edca1) (Python, stdlib only)

### Case studies

Three write-ups from client work, with names removed: [diagnosing a field upload failure](https://johnragonhall.github.io/case-studies/field-diagnostics.html), [a camera model that lifted order accuracy from 72.0% to 94.1%](https://johnragonhall.github.io/case-studies/vision-pick-audit.html), and [shipping firmware fixes to a fleet with no rollback](https://johnragonhall.github.io/case-studies/release-structure.html).

### Production firmware (private, client work)

- **Cellular RFID gateway.** ESP32 firmware on an LTE modem that reads an RFID reader over Ethernet and uploads through mbedTLS to a REST API, managed through Azure IoT Hub device twins. It ships with OTA updates, on-device self-tests, a recovery ladder for unattended sites, native unit tests, libFuzzer harnesses, and GitHub Actions workflows for provisioning, deploys, and twin changes.
- **IoT Network Check.** A site network preflight and on-device connectivity self-test: a Windows and Linux CLI plus an ESP32 library, in C++.

## Toolbox

| Area | Tools |
| --- | --- |
| Embedded | C, C++, ESP32, PlatformIO, FreeRTOS, mbedTLS, LTE modems |
| IoT and cloud | Azure IoT Hub, MQTT, Sparkplug B, ISA-95, REST APIs |
| Software | Python, TypeScript, PowerShell |
| Quality | Unit tests, fuzzing, CI gates on GitHub Actions, statistical process control |

## How I work

- **Tests first.** Every bug fix gets a regression test, and CI gates every merge.
- **Measured claims only.** A number in my docs comes from a recorded run. If it has not been measured, it says TBD.
- **Clean licensing.** Permissive licenses, clean-room code, and no copyleft in client deliverables.
- **Built for the field.** Devices fail where nobody is watching, so firmware reports its own health and recovers without a site visit.
