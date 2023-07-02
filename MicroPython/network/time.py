import httpget
import ntptime
import utime
import time


# JST(日本標準時)はUTC+9時間
JP_UTC_OFFSET = 9


class TimeObj:
    def __init__(self, offset, retry):
        self.offset = offset
        self.retry = retry
        self.success = False

    def Fix(self):
        for i in range(self.retry):
            try:
                ntptime.settime()
                self.success = True
                break
            except OSError as exc:
                if exc.args[0] == 110:  # ETIMEDOUT
                    print("ETIMEDOUT. Returning False")
                    time.sleep(5)

    def GetTime(self):
        if not self.success:
            self.Fix()
        return utime.localtime(utime.mktime(utime.localtime()) + self.offset * 3600)


if __name__ == "__main__":
    # nw = httpget.Network("CENTRAL_WIFI", "centralsp")
    nw = httpget.Network("山崎孝洋のiPhone (2)", "TTu8-IUAZ-9HM5-ex9e")
    rst = nw.Connect()
    print(rst)
    print("before：%s" % str(utime.localtime()))
    tm = TimeObj(JP_UTC_OFFSET, 2)

    print("after: %s" % str(tm.GetTime()))
