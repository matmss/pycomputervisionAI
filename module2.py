import cv2
import sys
 
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
 
if __name__ == '__main__':
 
    print (minor_ver)
    #tecnicas de rastreamento
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    tracker_type = tracker_types[1]
 
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
 
    #video
    video = cv2.VideoCapture("videos/3_pessoas_3.h264")
    if not video.isOpened():
        print('Erro abertura de video')
        sys.exit()
    ok, frame = video.read()
    if not ok:
        print('Erro na leitura do video')
        sys.exit()
     
    #caixa de selecao
    bbox = (287, 23, 86, 320)
    bbox = cv2.selectROI(frame, False)
 
    #inicia rastreamento
    ok = tracker.init(frame, bbox)
 
    while True: 
        ok, frame = video.read()
        if not ok:
            break
        timer = cv2.getTickCount()
 
        #atualiza rastreamento
        ok, bbox = tracker.update(frame)
 
        #calcula FPS
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
        if ok:
            #rastreou
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            #falha
            cv2.putText(frame, "Falha no rastreamento", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        #tipo rastreamento
        cv2.putText(frame, tracker_type + " rastreamento", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
        #FPS
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        # Display result
        cv2.imshow("rastreando", frame)
 
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
