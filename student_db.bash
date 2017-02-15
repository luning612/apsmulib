 for f in *2016removedlines\(anony\).txt
 do
  if [ $f \> "Feb2016removedlines\(anony\).txt" ]; then
  python student_db.py $f
  fi
 done