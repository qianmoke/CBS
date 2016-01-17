import datetime
import re

import xlwt

import awkv2

data_file = 'monipq.log.20160112'


# the time collect of pcl in server.log
class collect_pcltime:

    def __init__(self):
        self.tuxedo_log = {}
        self.data = ""
        self.time = ""
        self.time_seq = []

    def process_lines(self, line):
        try:
            if re.search("server", line):
                self.data = line
            if re.search("2015", line):
                self.time = line
                self.data = ""
            if self.data:
                array = self.data.split()
                prog_name = array[0]
                queued = array[4]
                if self.time in self.tuxedo_log.keys():
                    self.tuxedo_log[self.time].append(prog_name)
                    self.tuxedo_log[self.time].append(queued)
                else:
                    self.tuxedo_log[self.time] = []
                    self.time_seq.append(self.time)
                    self.tuxedo_log[self.time].append(prog_name)
                    self.tuxedo_log[self.time].append(queued)
            self.data = ""
        except AttributeError:
            pass
        except IndexError:
            pass

    def end(self):
        pass

    def description(self):
        return "Collection Data of Log"

    def result(self):
        s = ""
        for time in self.tuxedo_log.keys():
            # s +=str(self.tuxedo_out[time][0].split())
            # s +=str(self.tuxedo_log[time][1].split())
            data = str(self.tuxedo_log[time])
            s += str(time)
            s += " "
            s += data
            s += "\n"
        return s

    def output(self):
        workbook = xlwt.Workbook(encoding='gbk')
        sheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
        i = 0
        time_str = ""
        for time in self.time_seq:
            for j in range(0, len(self.tuxedo_log[time]) / 2):
                porg_name = self.tuxedo_log[time][j * 2]
                queued = int(self.tuxedo_log[time][j * 2 + 1])
                if queued > 10:
                    time_str = time.strip('\n')
                    time_format = "%a %b %d %H:%M:%S EAT %Y"
                    time_fin = str(datetime.datetime.strptime(time_str,
                                                              time_format))
                    sheet.write(i, 0, time_fin)
                    sheet.write(i, 1, porg_name)
                    sheet.write(i, 2, queued)
                    i += 1

        workbook.save('time.xls')


ar = awkv2.controller(data_file)
ar.subscribe(collect_pcltime())
ar.run()
ar.print_results()
