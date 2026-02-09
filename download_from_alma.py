import requests
from tqdm import tqdm

S = requests.Session()

S.cookies['mod_auth_openidc_session'] = '7934a2d8-96c2-468e-bc9c-23648adebcdf'

filenames = [
'2024.1.01182.S_uid___A001_X3788_X9ea4.ADMIT.tgz',
'2024.1.01182.S_uid___A001_X3788_X9ea4.QA2_report.tgz',
'calibrated_final.tgz',
]

root = 'https://bulk.cv.nrao.edu/almadata/proprietary/2024.1.01182.S/X9ea4/'

for filename in filenames:
    with open(filename, 'wb') as fh:
        response = S.get(f'{root}/{filename}', stream=True)

        for chunk in tqdm(response.iter_content(chunk_size=8192)):
            if chunk:
                fh.write(chunk)
