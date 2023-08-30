from crawler.cpp import CppCrawler

# cpp=CppCrawler()
# cpp.startLogin()
# cpp.searchManzhanInfo()
# cpp.getPiaoJia()
# cpp.chosePiao()
# cpp.getGouPiaoRenInfo()
# cpp.choseGoupiaoren()
# cpp.qiangQiao()

# import sys
#
# from PyQt5.QtWidgets import QApplication, QWidget
#
# from qtui.index import Ui_Form
#
# app = QApplication(sys.argv)
# wigdt=QWidget()
# ex=Ui_Form()
# ex.setupUi(wigdt)
# wigdt.show()
# sys.exit(app.exec_())


from apscheduler.schedulers.blocking import BlockingScheduler
cpp=CppCrawler()
cpp.startLogin()
print("cpp抢票脚本")
while True:
    print("0.填写常规信息")
    print("1.直接抢票")
    print("2.定时抢票")
    print("3.退出")
    a = input("输入序号：")
    if int(a) == 0:
        cpp.searchManzhanInfo()
        cpp.getPiaoJia()
        cpp.chosePiao()
        cpp.getGouPiaoRenInfo()
        cpp.choseGoupiaoren()
    elif int(a) == 1:
        cpp.qiangQiao()
    elif int(a) == 2:
        m = input("输入时间：(格式为2020-03-12 12:00:00):")
        scheduler = BlockingScheduler()
        scheduler.add_job(cpp.qiangQiao, 'date', run_date=m)
        scheduler.start()
    else:
        print("退出")
        break

