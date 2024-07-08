set -e

SEARCH_KEY=$(yq -r '.servers[0].url' openapi.yaml)
FIRST_UPSTREAM=$(jq -r '."'$SEARCH_KEY'"[0].upstream_name' records.json)


echo "Searching for location data in $SEARCH_KEY"
echo "First upstream is $FIRST_UPSTREAM"

echo "Generating Upstreams based on records.json"
python generate_upstreams.py --records-file records.json --key $SEARCH_KEY --output-file .staging/upstreams.yaml 

echo "Generating Route by Header Plugin"
python generate-route-by-header-plugin.py --records-file records.json --key $SEARCH_KEY --output-file .staging/route-by-header.yaml 

echo "Convertung OpenAPI to Kong"
cat openapi.yaml | deck file openapi2kong -o .staging/kong.yaml

echo "Merging Upstreams to Kong state file"
deck file merge .staging/kong.yaml .staging/upstreams.yaml -o .staging/final-kong.yaml

echo "Adding Plugins to Kong state file"
cat .staging/final-kong.yaml | deck file add-plugins plugins/request-transformer-advanced.yaml .staging/route-by-header.yaml -o .staging/final-kong.yaml

echo "Patching Service host to $FIRST_UPSTREAM"
cat .staging/final-kong.yaml | deck file patch --selector="$..services[0]" --value='host:"'$FIRST_UPSTREAM'"' -o .staging/final-kong.yaml

echo "Adding location based paths to Kong state file"
yq eval -i '
.services[].routes[].paths |= . + map(sub("^~", "~/(?<location>eu|us|ch)"))
' .staging/final-kong.yaml


