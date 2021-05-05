#! /bin/bash

file_path="${1}"
base_name=$(basename "${file_path}")
dir_name=$(dirname "${file_path}")
file_name="${base_name%.*}"
file_ext="${base_name#*.}"
shift

echo "file_path=${file_path}"
echo "base_name=${base_name}"
echo "dir_name=${dir_name}"
echo "file_name=${file_name}"
echo "file_ext=${file_ext}"

input_file_name=${file_path}
scaffolds_file_name=${dir_name}/${file_name}-scaffolds.${file_ext}
contigs_file_name=${dir_name}/${file_name}-contigs.${file_ext}

if test -f "${scaffolds_file_name}"; then
  echo "found scaffolds file"
  input_file_name=${scaffolds_file_name}
elif test -f "${contigs_file_name}"; then
  echo "found contigs file"
  input_file_name=${contigs_file_name}
fi

echo "input_file_name=${input_file_name}"
prokka "${input_file_name}" "$@"