from google_images_download import google_images_download


def get_img_url(img_name):
    # creating object
    response = google_images_download.googleimagesdownload()

    query = img_name + " icon"

    # keywords is the search query
    # format is the image file format
    # limit is the number of images to be downloaded
    # print urs is to print the image file url
    # size is the image size which can
    # be specified manually ("large, medium, icon")
    # aspect ratio denotes the height width ratio
    # of images to download. ("tall, square, wide, panoramic")
    arguments = {"keywords": query,
                 "limit": 1,
                 "print_urls": True,
                 }
    try:
        response.download(arguments)
        # Handling File NotFound Error
    except Exception as e:
        print("ERROR")
        print(e)


if __name__ == '__main__':
    get_img_url("Google Chrome")
