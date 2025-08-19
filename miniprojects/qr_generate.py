#generate a qr codecusing python
import qrcode
data = "kushal shah"

qr = qrcode.make(data)
qr.save("qrcode.png")

print("qr code generated")