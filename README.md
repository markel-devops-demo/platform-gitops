# platform-gitops

Single source of truth for what runs on the ARO cluster. Argo CD reconciles this repo every 30 seconds.

| Path | What it is | Who changes it |
|---|---|---|
| `charts/golden-service/<version>` | The shared, versioned golden-path Helm chart (Deployment, Service, Route, RBAC, quota, network policy, optional autoscaling from 1.1.0) | Platform team (new feature = new version) |
| `apps/<service>/values.yaml` | **Onboarding record** of a template-created service: name, owner, DR tier, data class, hostname | Developer Hub template once, then PRs from the app team |
| `apps/<service>/envs/<env>.yaml` | **Release record**: chart version + image tag running in that environment | Release API (image tag) · app-team PR (chart version) |
| `apps/<service>/base` | Service manifests (Namespace, Deployment, Service, Route, ExternalSecret, RBAC) | Golden-path template, then the app team |
| `apps/<service>/overlays/{sit,uat}` | Per-environment image tag and config | Release API (SIT) and promotion PRs (UAT) |
| `apps/<service>/overlays/preview` | Template for PR preview environments | Platform team |
| `components/guardrails` | Quota, LimitRange, NetworkPolicy shared by every namespace | Platform team |
| `spikes/<name>` | Short-lived environments (auto-merged, auto-expired) | Developer Hub "Spike environment" template |
| `argocd/` | AppProjects + ApplicationSets (bootstrapped once by the demo scripts) | Platform team |
| `catalog/` | Developer Hub catalog (groups, users, 200 components, templates) | Platform team |
| `templates/` | Developer Hub software templates | Platform team |

## How a build reaches an environment

CI (any system) builds and tests, pushes the image to ACR, then makes **one call**, the release API
(`.github/workflows/release.yml`, triggered by `repository_dispatch` with `{app, version, env}`).
The platform checks the image exists, then updates the release record: SIT directly, UAT via an approval PR.
Argo CD deploys. Nobody hand-edits values files per release.
