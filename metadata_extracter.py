import os
import hashlib
import mimetypes
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def tree(main, depth = 0):
    if depth == 0:
        with open('data_report.csv', 'w', encoding='utf-8') as f:
            f.write("File name,File size,Last modification time,File type,File extension,File digest,File geolocation\n")

    content = list( os.walk(main, topdown=True))
    for i in range(len(content[0])):
        if i == 0 and depth == 0: #root
            print (content[0][i])
        if i == 1: #dirs
            for j in range(len(content[0][i])):
                folder = content[0][i][j]
                if content[0][2] == [] and j == len(content[0][i])-1:
                    print(depth * "|   " + "└─ " + "📁" + folder)
                else:
                    print (depth*"|   " + "├─ " + "📁" + folder)
                tree(content[0][0]+"/"+folder, depth+1)

        if i == 2: #files
            for j in range(len(content[0][i])):
                file = content[0][i][j]
                file_data = all_data(content[0][0] + "/" + file)
                with open('data_report.csv', 'a', encoding='utf-8') as f:
                    f.write(f"{file},{file_data['Size']},{file_data['Last modification time']},{file_data['File type']},{file_data['File extension']},{file_data['File digest']},{file_data['File geolocation']}\n")
                if j == len(content[0][i])-1:
                    print(depth * "|   " + "└─ " + "📄" + file + '   ', file_data)
                else:
                    print (depth*"|   " + "├─ " + "📄" + file + '   ', file_data)


def metadata(file):
    return  {'Size': os.stat(file).st_size, 'Last modification time': os.stat(file).st_mtime}

def file_digest(file, algorithm='md5'):
    match algorithm:
        case 'md5':
            hasher = hashlib.md5()
        case 'sha1':
            hasher = hashlib.sha1()
        case _:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

    with open(file, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

#print(file_digest('data/CBE_cw4_gr4_pon_TN_13_v1.pdf', 'sha1'))
#print(file_digest('data/CBE_cw4_gr4_pon_TN_13_v1.pdf', 'md5'))
#print()

def file_extension(file):
    return file.split('.')[-1].upper()

#print(file_extension('data/CBE_cw4_gr4_pon_TN_13_v1.pdf'))

# Nie ma sensu robić słownika bo jest biblioteka mimetypes
'''
def file_type(file):
    if file.endswith('.pdf'):
        return 'PDF'
    elif file.endswith('.docx'):
        return 'Word Document'
    elif file.endswith('.xlsx'):
        return 'Excel Spreadsheet'
    elif file.endswith('.pptx'):
        return 'PowerPoint Presentation'
    elif file.endswith('.jpg'):
        return 'JPEG Image'
    elif file.endswith('.png'):
        return 'PNG Image'
    elif file.endswith('.txt'):
        return 'Text File'
    elif file.endswith('.csv'):
        return 'CSV File'
    elif file.endswith('.zip'):
        return 'ZIP Archive'
    elif file.endswith('.rar'):
        return 'RAR Archive'
    elif file.endswith('.tar'):
        return 'TAR Archive'
    elif file.endswith('.gz'):
        return 'GZIP Archive'
    elif file.endswith('.7z'):
        return '7-Zip Archive'
    elif file.endswith('.mp3'):
        return 'MP3 Audio'
    elif file.endswith('.mp4'):
        return 'MP4 Video'
    elif file.endswith('.avi'):
        return 'AVI Video'
    elif file.endswith('.mkv'):
        return 'MKV Video'
    elif file.endswith('.flv'):
        return 'FLV Video'
    elif file.endswith('.mov'):
        return 'MOV Video'
    elif file.endswith('.wmv'):
        return 'WMV Video'
    elif file.endswith('.gif'):
        return 'GIF Image'
    elif file.endswith('.bmp'):
        return 'BMP Image'
    elif file.endswith('.svg'):
        return 'SVG Image'
    elif file.endswith('.html'):
        return 'HTML Document'
    elif file.endswith('.css'):
        return 'CSS File'
    elif file.endswith('.js'):
        return 'JavaScript File'
    elif file.endswith('.json'):
        return 'JSON File'
    else:
        return 'Unknown'
'''

def file_type(file):
    mime_type, encoding = mimetypes.guess_type(file)
    if mime_type:
        return mime_type
    else:
        return 'UNKNOWN'

#print(file_type('data/CBE_cw4_gr4_pon_TN_13_v1.pdf'))
#print(file_type('data/dir1/very/deep/folder/deepest_file.txt'))
#print(file_type('data/dir1/dir2/New Bitmap Image.bmp'))


def get_geolocation(file):
    def get_decimal_from_dms(dms, ref):
        degrees, minutes, seconds = dms
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if ref in ['S', 'W']:
            decimal = -decimal
        return decimal
    try:
        image = Image.open(file)
    except IOError:
        return None

    exif_data = image._getexif()
    if not exif_data:
        return None
    gps_info = {}
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag)
        if tag_name == "GPSInfo":
            for key in value:
                gps_tag = GPSTAGS.get(key)
                gps_info[gps_tag] = value[key]

    if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:
        lat = get_decimal_from_dms(gps_info['GPSLatitude'], gps_info['GPSLatitudeRef'])
        lon = get_decimal_from_dms(gps_info['GPSLongitude'], gps_info['GPSLongitudeRef'])
        return lat, lon
    return None

#print(get_geolocation('data/dir1/New folder/germany-english-garden.jpg'))

def all_data(file):
    return {'Size': os.stat(file).st_size, 'Last modification time': os.stat(file).st_mtime, 'File type': file_type(file), 'File extension': file_extension(file), 'File digest': file_digest(file), 'File geolocation': get_geolocation(file)}

print()
tree('data')
with open('report_hashes.txt', 'w', encoding='utf-8') as f:
    f.write('sha1: '+ file_digest('data_report.csv', 'sha1') + '\n')
    f.write('md5: '+ file_digest('data_report.csv', 'md5') + '\n')