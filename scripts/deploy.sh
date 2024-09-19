#!/bin/bash

echo
echo "Installing gratus maximus on your cluster"
echo

CONTEXT=$(kubectl config current-context)
NS="gratusmaximus"

kubectl get namespace | grep -E "^${NS}" > /dev/null 2>&1 || {
  echo "Using context: $CONTEXT"
  echo
  echo "This script will install the following:"
  echo "- Create the ${NS} namespace"
  echo "- Create a secret for the database"
  echo "- Apply all the services files which match **/k8s.yaml"
  echo
  echo "Is this okay? (yes/no)"
  read -r answer
  if [ "$answer" != "yes" ]; then
    echo "Exiting"
    exit 1
  fi

  db_password=$(openssl rand -base64 32)

  kubectl create namespace "${NS}" || exit 1
  kubectl create secret generic db-secret --from-literal=password="${db_password}" -n "${NS}" || exit 1

  echo
  echo "Done."
  echo
}

echo
echo "Now deploying the application"
echo

find . -type f -name k8s.yaml -exec kubectl apply -f {} -n "${NS}" \;
