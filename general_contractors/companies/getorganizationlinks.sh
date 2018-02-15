
for x in a e i o u y 
do
    for y in {1..1300}
    do
        curl https://nclbgc.org/search/licenseResults?licenseNumber=\&licenseName=$x\&page=$y \
                | grep "<a href=\"/search/licenseDetails?licenseNumber=[0-9]*" \
                | grep -o "licenseDetails?licenseNumber=[0-9]*" 
    done
done

