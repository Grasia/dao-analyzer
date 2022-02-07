#!/bin/bash
# set -exuo pipefail

# The goal of this script is to check if running two/three times the script
# with continuation enabled results in the same data as running it one time
dates=("2021-03-01" "2021-06-01" "2021-09-01" "2021-12-01")

generate_full () {
    local d=$1
    local p="datawarehouse-full-$d" # Building the filename

    if [ ! -d "$p" ]; then
        echo "$p" not found, running again
        ./cache_scripts/main.py -FD "$p" --block-datetime "$d" -n mainnet --skip-daohaus-names || exit 1
    else
        echo "$p" found, not running
    fi

    lastp="$p"
}

# Running for the first and the last
# These two are a "full download", so they won't be deleted between runs.
# Pretty useful if you only modify the update methods
generate_full "${dates[-1]}"
full="$lastp" # We save the full-latest to compare it later
generate_full "${dates[0]}"

generate_partial() {
    local d=$1
    local p="datawarehouse-partial-$d"

    [ -d "$p" ] && rm -r "$p" # If it exists, we delete it
    cp -r "$lastp" "$p"
    ./cache_scripts/main.py -D "$p" --block-datetime "$d" -n mainnet --skip-daohaus-names || exit 1

    lastp=$p
}

for d in "${dates[@]:1}"; do
    generate_partial "$d"
done

./scripts/datawarehouseDiff.py "$full" "$lastp"

# If there is no datawarehouse, we copy it so it can be used by the flask app
if [ ! -d "datawarehouse" ]; then
    cp -r "$full" "datawarehouse"
fi