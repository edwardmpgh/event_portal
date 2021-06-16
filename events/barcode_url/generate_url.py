import barcode

from heinz_signup.settings import MEDIA_ROOT, MEDIA_URL


def get_bardoce_url(barcode_data):
    barcode_svg = barcode.get('code128', barcode_data)
    barcode_svg.save(MEDIA_ROOT + '/barcodes/' + barcode_data)

    return MEDIA_URL + '/barcodes/' + barcode_data+'.svg'

