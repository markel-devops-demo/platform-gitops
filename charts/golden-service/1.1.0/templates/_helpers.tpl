{{- define "gs.name" -}}{{ required "name is required" .Values.name }}{{- end }}
{{- define "gs.replicas" -}}{{ if eq .Values.drTier "bronze" }}2{{ else }}3{{ end }}{{- end }}
{{- define "gs.labels" -}}
app: {{ include "gs.name" . }}
backstage.io/kubernetes-id: {{ include "gs.name" . }}
app.kubernetes.io/managed-by: golden-service-{{ .Chart.Version }}
{{- end }}
