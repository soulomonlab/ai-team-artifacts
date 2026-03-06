K8s Security Baseline (MVP)

1) PodSecurity
- Enforce PodSecurity admission controller.
- Profiles:
  - prod namespaces: "restricted"
  - staging: "baseline"
  - dev: "privileged" (only if necessary)
- How to label namespaces:
  kubectl label ns production pod-security.kubernetes.io/enforce=restricted
  kubectl label ns production pod-security.kubernetes.io/enforce-version=v1.25

2) Resource Quotas & LimitRange
- Provide example LimitRange and ResourceQuota manifests.

3) SecurityContext recommendations
- runAsNonRoot: true
- runAsUser > 1000
- readOnlyRootFilesystem: true where possible
- allowPrivilegeEscalation: false

4) Admission Controllers / Policies
- Enable: PodSecurity, NodeRestriction, EventRateLimit (if supported)
- OPA/Gatekeeper optional for policy enforcement (future)

5) Image Security
- Use immutable tags; enable image scanning in registry (ECR/GCR).
- Block images with known critical vulnerabilities via admission webhook (future).

6) Health checks
- All Deployment manifests must include liveness and readiness probes.

7) RBAC
- Least privilege for service accounts.

8) Network Policies
- Default deny ingress/egress in prod namespaces; explicit allow rules per app.

Example manifests and a minimal adoptable manifest are in output/config/k8s_examples.yaml
