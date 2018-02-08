# https://www2.ncdhhs.gov/dhsr/reports.htm
# Author: jfave
# Last Updated: 2/8/2018
import certifi
import urllib3

TYPE = 'type'
HEADER_FILE = 'h_file'
HEADER_FILE_KEY = 'h_file_k'
DATA_FILE = 'data'

NCDHHS_URL = 'http://www2.ncdhhs.gov/dhsr/data/'
HDR_KEY_IDX = 0
SEPARATOR_IDX = 2
HDRS_IDX = 3
SEPARATOR = '------------------'

HTTP_SUCCESS = 200

NC_LICENSED_FACILITIES = [
    { TYPE: 'adult_care_home',
      HEADER_FILE: 'ha-header.txt',
      HEADER_FILE_KEY: 'ADULT CARE HOME LISTING',
      DATA_FILE: 'ha.txt' },
    { TYPE: 'ambulatory_surgical',
      HEADER_FILE: 'as-header.txt',
      HEADER_FILE_KEY: 'AMBULATORY SURGICAL LISTING',
      DATA_FILE: 'as.txt' },
    { TYPE: 'cardiac_rehab',
      HEADER_FILE: 'crp-header.txt',
      HEADER_FILE_KEY: 'CARDIAC REHABILITATION LISTING',
      DATA_FILE: 'crp.txt' },
    { TYPE: 'family_care_home',
      HEADER_FILE: 'fch-header.txt',
      HEADER_FILE_KEY: 'FAMILY CARE HOME LISTING',
      DATA_FILE: 'fch.txt' },
    { TYPE: 'home_care_all',
      HEADER_FILE: 'hc-header.txt',
      HEADER_FILE_KEY: 'HOME CARE ALL',
      DATA_FILE: 'hc.txt' },
    { TYPE: 'hospice',
      HEADER_FILE: 'hos-header.txt',
      HEADER_FILE_KEY: 'HOSPICE LISTING',
      DATA_FILE: 'hos.txt' },
    { TYPE: 'intermed_care_mentally_retard',
      HEADER_FILE: 'icfmr-header.txt',
      HEADER_FILE_KEY: 'INTERMEDIATE CARE FACILITY / MENTALLY RETARDED DATA',
      DATA_FILE: 'icfmr.txt' },
    { TYPE: 'mental_health',
      HEADER_FILE: 'mhl-header.txt',
      HEADER_FILE_KEY: 'MENTAL HEALTH FACILITY LISTING BY COUNTY',
      DATA_FILE: 'mhl.txt' },
    { TYPE: 'nursing_homes',
      HEADER_FILE: 'nhco-header.txt',
      HEADER_FILE_KEY: 'NURSING HOME LISTING',
      DATA_FILE: 'nhco.txt' }
]

pool = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)

def ncdhhs_request(file):
    # what other kinds of exceptions are thrown when the request fails?
    res = pool.request('GET', NCDHHS_URL + file)
    if res.status != HTTP_SUCCESS:
        pass
    else:
        return res.data.decode('utf-8', 'ignore')

# Get the header file
for fac in  NC_LICENSED_FACILITIES:
    print(fac['type'] + ".csv")
    with open(fac[TYPE] + '.csv', 'w+') as outf:
        h_data = ncdhhs_request(fac[HEADER_FILE]).split('\r\n')
        lines = [line for line in h_data if line != '']
        # Check the header files to make sure it's in the expected format
        if (fac[HEADER_FILE_KEY] in lines[HDR_KEY_IDX]) and (SEPARATOR in lines[SEPARATOR_IDX]):
            outf.write(lines[HDRS_IDX] + '\n')
            # headers = lines[HDRS_IDX]
            # get the data
            # data = ncdhhs_request(fac[DATA_FILE]).split('\r\n')
            data = ncdhhs_request(fac[DATA_FILE])
            outf.write(data)
            #for row in data:
            #    print(row)
        else:
            print("ERROR:", NCDHHS_URL + fac[HEADER_FILE], "does not match expected format.")
