#generate a qr codecusing python
import qrcode
data = "kushal shah"

qr = qrcode.make(data)
qr.save(f"E:/kushal/git/BCA/miniprojects/{data}.png")

print("qr code generated")