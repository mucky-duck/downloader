import requests
import sys
import time


def DownloadFile(url, directory) :
    localFilename = url.split('/')[-1]
    with open(directory + '/' + localFilename, 'wb') as f:
        start = time.time()
        r = requests.get(url, stream=True)
        content_length = int(r.headers.get('content-length'))
        if content_length is None:
            f.write(r.content)
        else:
            dl = 0
            for chunk in r.iter_content(chunk_size=content_length/100):
                dl += len(chunk)
                if chunk:
                    f.write(chunk)
                progress = (50 * dl / content_length)
                byte_speed = dl / (time.time() - start)
                kbps_speed = byte_speed / 1024
                mbps_speed = kbps_speed / 1024
                downloaded = float(dl) / (1024 * 1024)
                file_size = float(content_length) / (1024 * 1024)
                if byte_speed > 0:
                    eta = (content_length - dl) / byte_speed
                else:
                    eta = 0
                output = "\r[%s%s] %.1f Mbps: %.1fMb Of %.1fMb" %('=' * progress, ' ' * (50-progress), mbps_speed, downloaded, file_size)
                output += " time left: %02d:%02d" %divmod(eta, 60)
                sys.stdout.write(output)

                print ''

    return (time.time() - start)


def main() :
    if len(sys.argv) > 1 :
        url = sys.argv[1]
    else :
        url = raw_input("Enter the URL : ")
    directory = raw_input("Where would you want to save the file ?")

    time_elapsed = DownloadFile(url, directory)
    print "Download complete..."
    print "Time Elapsed: %02d:%02d" %divmod(time_elapsed, 60)


if __name__ == "__main__" :
    main()
