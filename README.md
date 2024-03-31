# Multiple Sources for an ArgoCD Application

ref: Argo CD has the ability to specify multiple sources for a single Application. Argo CD compiles all the sources and reconciles the combined resources. 
(argocd-multi-sources)[https://argo-cd.readthedocs.io/en/stable/user-guide/multiple_sources/]

# Add Git repo

```bash
k get secrets -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
argocd login localhost:30242  --insecure # node port or 8080 port-forward

USERNAME=npanda
TOKEN=hello

# Add Template Repo
REPO_URL=https://github.com/naren4b/demo-app.git
argocd repo add ${REPO_URL} --username ${USERNAME} --password ${TOKEN}

# ADD Value Repo

REPO_URL=https://github.com/naren4b/argocd-multi-source-demo.git
argocd repo add ${REPO_URL} --username ${USERNAME} --password ${TOKEN}
```

# Deploy the App 
```bash
kubectl apply -f demo-argo-application.yaml
```
