import cv2

cap = cv2.VideoCapture(r"C:\Users\sakb\OneDrive - Det Kongelige Akademi\Desktop\timelapse\Timelapse Aedes .mp4")
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

out = cv2.VideoWriter(r"C:\Users\sakb\OneDrive - Det Kongelige Akademi\Desktop\Three Stages\motion.avi", fourcc, 5.0, (2160,3840))
frame_id = 0 
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
frame1 = cv2.imread(r"C:\Users\sakb\OneDrive - Det Kongelige Akademi\Desktop\second monitoring framework\my_video_frame.png")

print(frame1.shape)
while cap.isOpened():
    #Image Processing
    ret, frame2 = cap.read()
    ret, frame3 = cap.read()
    blur1 = cv2.bilateralFilter(frame1,9,250,250)
    blur2 = cv2.bilateralFilter(frame2,9,250,250)
    diff = cv2.absdiff(blur1, blur2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
     
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 1000:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 1)
    cv2.drawContours(frame1, contours, -1, (255, 0, 0), 2)

    image = cv2.resize(frame1, (465,738))
    blur1 = cv2.resize(blur1, (465,738))

    diff = cv2.resize(diff, (465,738))
    gray = cv2.resize(gray, (465,738))
    thresh = cv2.resize(thresh, (465,738))
    dilated = cv2.resize(dilated, (465,738))
    #out.write(frame1)
    '''
    #Grid 
    image2 = image 
    H,W = image2.shape[:2]
    stepsize = 20
    #print(H,W)

    for i in range(0, int(H), stepsize):
        cv2.line(image2, (0,i),(W,i),(255,255,255),1)

    for j in range(0, int(W), stepsize):
        cv2.line(image2, (j,0),(j,H),(255,255,255),1)

    height = H/2 
    weight = W/2
    '''

    cv2.imshow("blur", blur1)
    #cv2.imshow("grid", image2)
    cv2.imshow("feed", cv2.resize(frame1, (465,738)))
    cv2.imshow("difference", diff)
    cv2.imshow("binary", thresh)
    cv2.imshow("dilated", dilated)

    frame1 = frame2
    ret, frame1 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
out.release()
