SERVER=$1 #"https://edge-1-control-plane:6443"
cat<<EOF | kubectl apply  -n argocd -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: 'demo-app'
spec:
  destination:
    server: $SERVER
    namespace: default
  source:
    path: sample-app
    repoURL: https://github.com/naren4b/demo-app.git
    targetRevision: HEAD  
  project: default
EOF

