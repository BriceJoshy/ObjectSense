response = requests.get(url, stream=True).raw
        # .read reads the data into a bytstream and the datatype is changes to uint8
        image = np.asarray(bytearray(response.read()), dtype="uint8")
        #  reading the image as it is without any change
        image = cv.imdecode(image, cv.IMREAD_COLOR)
        i = i + 1
        cv.imshow("url_image", image)
        cv.waitKey(0)
        cv.destroyAllWindows()