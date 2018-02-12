
for x in a e i o u y 
do
    for y in {1..600}
    do
        curl https://nclbgc.org/search/qualifierResults?qualifierName=$x\&page=$y \
                | grep "<a href=\"/search/qualifierDetails" \
                | grep -o "qualifierDetails?key=[0-9a-zA-Z]*&amp;licenseNumber=[0-9]*" 
    done
done

