# custome awk.py module


class controller:

    def __init__(self, f1):
        self.m_file_data = file(f1)
        self.m_handlers = []

    def subscribe(self, o):
        self.m_handlers.append(o)

    def run(self):

        s1 = self.m_file_data.readline()
        while s1 != "":
            for o in self.m_handlers:
                o.process_lines(s1)
            s1 = self.m_file_data.readline()

        # for o in self.m_handlers:
        # o.choose()

        for o in self.m_handlers:
            o.output()

        for o in self.m_handlers:
            o.end()

    def print_results(self):
        print
        print "Results:"
        print
        for o in self.m_handlers:
            print '----------------------------------'
            print o.description()
            print '----------------------------------'
            print o.result()
