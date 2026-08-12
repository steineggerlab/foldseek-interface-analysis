# Get PDB IDs whose structures were determined by NMR, 14,892
curl -s -G 'https://search.rcsb.org/rcsbsearch/v2/query' \
  --data-urlencode 'json={
    "query": {
      "type": "terminal",
      "service": "text",
      "parameters": {
        "attribute": "rcsb_entry_info.experimental_method",
        "operator": "exact_match",
        "value": "NMR"
      }
    },
    "return_type": "entry",
    "request_options": {
      "return_all_hits": true,
      "results_verbosity": "compact"
    }
  }' | jq -r '.result_set[]' > nmr_ids.txt


# Ids to lowercase, 14,892
awk '{ print tolower($0) }' nmr_ids.txt  > nmr_ids_lowercase.txt


# Retrieve ids that are in our dimerdb, 1,805
awk 'FNR==NR{split($2, words, "-"); split(words[1], hi, "DI_");name[hi[2]]=1; next}{if($1 in name){print}}' dimerpdb.source nmr_ids_lowercase.txt  > nmr_ids_inourpdb.txt

# Ids to uppercase, 1,805
awk '{ print toupper($0) }' nmr_ids_inourpdb.txt > nmr_ids_inourpdb_upper.txt

# Download mmcif files
mkdir -p mmcif
: > failed.txt
xargs -a nmr_ids_inourpdb_upper.txt -P 4 -I{} sh -c '
  f=mmcif/{}.cif.gz
  [ -s "$f" ] && exit 0
  curl -sS -f --retry 3 --retry-delay 2 -o "$f" \
    "https://files.rcsb.org/download/{}.cif.gz" \
    || { rm -f "$f"; echo {} >> failed.txt; }
'

# make foldseek db and dimerdb for each mmcif file (e.g. 1AI0db, 1AI0dimerdb)
mkdir -p dbdir/db
mkdir -p dbdir/dimerdb
for f in mmcif/*.cif.gz; do
  id=$(basename "$f" .cif.gz)          
  db="dbdir/db/${id}db"              
  dimerdb="dbdir/dimerdb/${id}dimerdb"    
  dimertmp="dbdir/dimerdb/${id}dimertmp"   
  nmrlist=dbdir/dimerdb/${id}_list.txt
  echo "== $id"
  foldseek createdb "$f" "$db" --threads 1
  foldseek createdimerdb "$db" "$dimerdb" "$dimertmp" --threads 1
  awk '{c=split($2, words, "_MODEL_"); if(c>1){split(words[2], hi,  "_"); print NR-1"\t"hi[1]"\t"hi[2]"_"hi[3]}else{print "single model"}}' "${dimerdb}.source" > "$nmrlist"
done


# Split dimerdb for each dimer (e.g.1AI0_E_F_db, 1AI0_D_L_db) - 3,950 dimers contained multiple NMR models among 5,135 dimers
LISTDIR=dbdir/dimerdb
ORIGDIR=dbdir/dimerdb
OUT=dbdir/subdb
TMP=dbdir/tmp
OFF=0
mkdir -p "$OUT" "$TMP" logs
: > logs/skipped.txt; : > logs/badkeys.txt; : > logs/failed.txt

for lf in "$LISTDIR"/*_list.txt; do
  id=$(basename "$lf" _list.txt)
  orig="$ORIGDIR/${id}dimerdb"

  nentry=$(wc -l < "${orig}.lookup")

  awk -F'\t' -v off="$OFF" -v tmp="$TMP" -v id="$id" '
    /^[0-9]+\t[0-9]+\t/ {
      k1 = $1*2 + off; k2 = k1 + 1
      f = tmp "/" id "_" $3 ".ids"
      print k1 > f; print k2 > f
      seen[$3] = 1
    }
    END { for (p in seen) print p }
  ' "$lf" | while read -r pair; do

    idf="$TMP/${id}_${pair}.ids"
    out="$OUT/${id}_${pair}_db"
    sort -n -u "$idf" -o "$idf"

    [ -s "${out}.dbtype" ] && continue 

    maxk=$(tail -1 "$idf")
    if [ "$maxk" -ge "$nentry" ] || [ "$(head -1 "$idf")" -lt 0 ]; then
      printf '%s\t%s\tmaxkey=%s\tentries=%s\n' "$id" "$pair" "$maxk" "$nentry" >> logs/badkeys.txt
      continue
    fi
    foldseek createsubdb "$idf" "$orig" "$out" -v 1
    
    for sfx in _h _ss _ca; do
      foldseek createsubdb "$idf" "${orig}${sfx}" "${out}${sfx}" -v 1
    done
  done
done


# Retrieve interfacedb and cluster with same parameter we clustered PDB interfaces
mkdir -p dbdir/interfacedb
mkdir -p dbdir/clures
SUB=dbdir/subdb
OUT=dbdir/interfacedb
CLUDIR=dbdir/clures
SCR=/mnt/scratch/sooyoung
mkdir -p "$OUT" logs/iface
: > logs/iface/failed.txt; : > logs/iface/skipped.txt

for lk in "$SUB"/*_db.lookup; do
  db=${lk%.lookup}                      # dbdir/subdb/1AI0_A_F_db
  name=$(basename "$db")                # 1AI0_A_F_db
  out="$OUT/${name%_db}_ifacedb"        # dbdir/interfacedb/1AI0_A_F_ifacedb
  clures="$CLUDIR/${name%_db}_clu"
  clutmp="$SCR/${name%_db}_tmp"
  foldseek createinterfacedb "$db" "$out" --threads 1
  foldseek easy-multimercluster "$out" "$clures" "$clutmp" --exhaustive-search -e 10000000 --lddt-threshold 0.20 --chain-tm-threshold 0 -c 0 --interface-lddt-threshold 0 --cov-mode 0 --cluster-mode 0 --max-iterations 1 --multimer-tm-threshold 0.4 --threads 6
done


# Simple statistics
cd dbdir/clures
for f in *_clu_cluster.tsv; do
  awk -F'\t' -v n="${f%_clu_cluster.tsv}" \
    '{c++; u[$1]}  END{ printf "%s\t%d\t%d\n", n, c+0, length(u) }' "$f"
done > cluster_summary.tsv


