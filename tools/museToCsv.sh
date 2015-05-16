for f in *.muse; do
	file=${f%.*}
	muse-player -f $file.muse -C $file.csv
done