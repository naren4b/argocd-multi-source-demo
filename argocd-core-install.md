# Deploy ArgoCD core with Cluster RBAC 

Open a Killerkoda play ground : https://killercoda.com/killer-shell-ckad/scenario/playground

Installation Script
----------------------------
```bash
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64

export ARGOCD_VERSION=v3.2.1 #TODO 
kubectl create namespace argocd
kubectl apply -n argocd --server-side -f https://raw.githubusercontent.com/argoproj/argo-cd/$ARGOCD_VERSION/manifests/core-install.yaml


kubectl config set-context --current --namespace=argocd # change current kube context to argocd namespace
argocd login --core
argocd admin dashboard -n argocd --address 0.0.0.0
```
