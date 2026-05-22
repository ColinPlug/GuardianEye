import cv2

#functie die image omzet in een geblurde image binnen de bounding box
def blur_img(img_path, bounding_box):

    img = cv2.imread(img_path)

    #YOLO bounding boxes worden in x, y, w en h gezet
    x, y, w, h = bounding_box
    roi = img[y : y + h, x : x + w]

    blurred_roi = cv2.GaussianBlur(roi, (151, 151), 0)

    img[y : y + h, x : x + w] = blurred_roi

    cv2.imwrite(img_path, img)
    cv2.imshow("blurred image:", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

blur_img("./notebooks/test_blurred.jpg", [50, 20, 400, 250])
