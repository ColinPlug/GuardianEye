import cv2

img = cv2.imread("./test.jpg")

blurred_img = cv2.GaussianBlur(img, (151, 151), 0)

cv2.imwrite('test_blurred.jpg', blurred_img)

cv2.imshow('Origineel', img)
cv2.imshow('Geblurd', blurred_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
