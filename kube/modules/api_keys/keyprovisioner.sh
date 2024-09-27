kubectl version
echo
echo

gratus_pod="$(kubectl get pods -l 'app.kubernetes.io/name=maximus' -o jsonpath='{.items[*].metadata.name}' | cut -d' ' -f1)"
echo "Found maximus pod: ${gratus_pod}"
echo

for kname in $(echo ${KEYS});
do
    echo "Provisioning key: ${kname}"
    key="$(kubectl exec "${gratus_pod}" -- ./scripts/assert_key.py -n "${kname}")"
    kubectl create secret generic "${kname}" --from-literal=key="${key}" --dry-run=client -o yaml | kubectl apply -f -
done

echo
echo "Done provisioning keys"
exit 0
