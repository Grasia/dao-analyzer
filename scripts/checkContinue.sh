#!/bin/bash
# set -exuo pipefail

# The goal of this script is to check if running two/three times the script
# with continuation enabled results in the same data as running it one time
dates=("2021-03-01" "2021-06-01" "2021-09-01" "2021-12-01")

other_args_cc="$@"

cache_scripts () {
    local d=$1
    local p="$2"
    local other_args=$3

    daoa-cache-scripts -D "$p" --block-datetime "$d" -n mainnet --skip-daohaus-names --no-ignore-errors --only-updatable $other_args_cc || exit 1
}

generate_full () {
    local d=$1
    local p="datawarehouse-full-$d" # Building the filename

    if [ ! -f "$p/version.txt" ]; then
        echo '>>>' "$p" not found, running again
        cache_scripts "$d" "$p"
    else
        if diff -w "$p/version.txt" <(daoa-cache-scripts -V); then
            echo '>>>' "$p" found and good version, not running
        else
            echo '>>>' "Version of datawarehouse and cache_scripts differ, running again"
        fi
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

    echo '>>> Running partial over' "$lastp" 'onto' "$p"
    cache_scripts "$d" "$p"

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