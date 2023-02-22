#!/bin/bash
set -euo pipefail

dw="./datawarehouse"
tmp_dw="$(mktemp -d)"

function cleanup {
    rm -rf "$tmp_dw"
}

trap cleanup EXIT

cat << EOF > "$tmp_dw/dataset-metadata.json" 
{
    "id": "daviddavo/dao-analyzer"
}
EOF

# 1. Copy metadata files
echo "Copying metadata"
for f in "$dw"/*.txt; do
    cp "$f" "$tmp_dw""${f#"$dw"}"
done
for f in "$dw"/**/metadata.json; do
    newf=$tmp_dw${f#"$dw"}
    mkdir -p "$(dirname "$newf")"
    cp "$f" "$newf"
done

# 2. Transform arrow to csv
echo "Transforming to csv"
for f in "$dw"/**/*.arr; do
    newf=$tmp_dw${f#"$dw"}
    csvf=${newf%.arr}.csv
    mkdir -p "$(dirname "$newf")"

    # cp "$f" "$newf"
    python -c "import pandas as pd; pd.read_feather(\"$f\").to_csv(\"$csvf\")" 
    echo -n .
done
echo

update_date=$(cat "$tmp_dw/update_date.txt")
echo "Dataset size:" "$(du -hs "$tmp_dw")"
# DEBUGGING
# ( cd "$tmp_dw" && zip -9r - . ) > /tmp/kaggle.zip
# unzip -l /tmp/kaggle.zip
kaggle datasets version --dir-mode zip -p "$tmp_dw" -m "$update_date"
