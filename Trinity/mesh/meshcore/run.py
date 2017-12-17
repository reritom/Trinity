from spark import Spark

red = Spark(origin="1113564", destination="theend", mode="explorer")

red.addAction("GET_DATA")
red.addAction("REBOOT")
red.showSpark()
