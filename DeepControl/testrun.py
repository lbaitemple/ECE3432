from CarFile import CarDataFile
import cv2

a=CarDataFile(dfile='data/output_6.csv')
key = 32
print(a.len)
for i in range(a.len):
    a.display(i, cmd=key)
    key = cv2.waitKey(0) & 0xFF
    # & 0xFF == ord('q')
    #    print(key)
    if (key == ord('q')):
        break
    elif (key == ord('s')):
        a.display(i, cmd=key, nfile='data.csv')
        break
'''
for i in range(a.len):
    a.display(i,cmd=key)
    key = cv2.waitKey(0) & 0xFF
    if (key == ord('q')):
        break

a.saverecord(nfile='goodcsv')
'''

#a = CarDataFile(dfile='data.csv')
#key = 32
#print(a.len)
#for i in range(a.len):
#    a.display_pred(i)
#    a.display(i, key)
#    key = cv2.waitKey(0) & 0xFF
          #& 0xFF == ord('q')
#    print(key)
##    if (key == ord('q')):
#        break

#print(a.badindx)
#a.saverecord()

'''
[0, 1, 2, 3, 4, 5, 6, 13, 14, 15, 16, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115]

'''