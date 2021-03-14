import cv2
import numpy as np

def close_wins():
    cv2.waitKey()
    cv2.destroyAllWindows()
    
def blurring(img_path, h1, h2, w1, w2):
    img = cv2.imread(img_path, 0)
    r, c = img.shape
    
    # 做一個局部打碼區域為 1 其餘為 0 的掩模
    mask = np.zeros((r, c), dtype=np.uint8)
    #
    mask[h1:h2, w1:w2] = 1
    #cv2.imshow("mask", mask) # 把 1 暫時改大一點較看得出差異
    #close_wins()
    
    # 使用隨機數矩陣 key 對 img 加密，得到一幅和原圖同尺寸的雜點圖
    key = np.random.randint(0, 256, size=[r,c], dtype=np.uint8)
    img_xor_key = cv2.bitwise_xor(img, key)
    #cv2.imshow("img_xor_key", img_xor_key)
    #close_wins()
    
    # 取得: (1) 背景為 0 (2) 打碼區域為雜點(馬賽克) 的圖像
    with_blur_no_bg = cv2.bitwise_and(img_xor_key, mask*255)
    #cv2.imshow("with_blur_no_bg", with_blur_no_bg)
    #close_wins()
    
    # 取得: (1) 背景為原圖 (2) 打碼區域為 0 的圖像
    with_bg_no_blur = cv2.bitwise_and(img, (1-mask)*255)
    #cv2.imshow("with_bg_no_blur", with_bg_no_blur)
    #close_wins()
    
    # 綜合以上二圖(相當於做 OR 運算)，
    # 得到背景為原圖; 打碼區域為 雜點 的圖像
    result = with_blur_no_bg + with_bg_no_blur
    #cv2.imshow("blurred_img", blurred_img)
    #close_wins()
    return result

if __name__ == "__main__":
    ''' 指定圖片來源 '''
    img_path = "../res/Lena/lena_256_unif332.png"

    ''' 指定打碼範圍 '''
    h1, h2, w1, w2 = 200, 220, 190, 280

    ''' 顯示原圖 ''' 
    img = cv2.imread(img_path, 0)
    cv2.imshow("原圖", img)
    close_wins()
    
    ''' 顯示打碼後的照片 '''
    blurred_img = blurring(img_path, h1, h2, w1, w2)
    cv2.imshow("眼睛打碼後", blurred_img)
    close_wins()