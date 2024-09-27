kubectl version

echo
echo
echo

gratus_pod="$(kubectl get pods -l 'app.kubernetes.io/name=gratus' -o jsonpath='{.items[*].metadata.name}' | cut -d' ' -f1)"
echo "Found Gratus pod: ${gratus_pod}"
echo

for kname in "${KEYS}";
do
    echo "Provisioning key: ${kname}"
done
# kubectl exec "${gratus_pod}" -- ./scripts/assert_key.py -n aaa

echo
echo
echo "Done provisioning keys"
exit 0
