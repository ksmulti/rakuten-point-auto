import rakuten_kuji_lib as RKL

rkc = RKL.RakutenKujiCore()
rkc.Index()
rkc.GoLoginPage()
rkc.Login()
rkc.Kuji()

print("rakuten kuji end")