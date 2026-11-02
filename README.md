# platform-gitops

Single source of truth for what runs on the ARO cluster. Argo CD reconciles this repo every 30 seconds.

| Path | What it is | Who changes it |
|---|---|---|
| `apps/<service>/base` | Service manifests (Namespace, Deployment, Service, Route, ExternalSecret, RBAC) | Golden-path template, then the app team |
| `apps/<service>/overlays/{sit,uat}` | Per-environment image tag and config | CI (SIT) and promotion PRs (UAT) |
| `apps/<service>/overlays/preview` | Template for PR preview environments | Platform team |
| `components/guardrails` | Quota, LimitRange, NetworkPolicy shared by every namespace | Platform team |
| `spikes/<name>` | Short-lived environments (auto-merged, auto-expired) | Developer Hub "Spike environment" template |
| `argocd/` | AppProjects + ApplicationSets (bootstrapped once by the demo scripts) | Platform team |
| `catalog/` | Developer Hub catalog (groups, users, 200 components, templates) | Platform team |
| `templates/` | Developer Hub software templates | Platform team |
