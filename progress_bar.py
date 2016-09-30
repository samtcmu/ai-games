import sys
import termcolor
import time

# Usage
# with ProgressBar(100, 1) as progress_bar:
#     for i in range(100):
#         complete_task(i)
#         progress_bar.Increment()
class ProgressBar:
    def __init__(self, total_tasks, quantas=50, start_message=None, 
                 bar_color="yellow", verbose=True):
        self._total_tasks = total_tasks
        self._completed_tasks = 0 
        self._quantas = quantas
        self._quanta_size = self._total_tasks / self._quantas
        self._start_message = start_message
        self._bar_color = bar_color
        self._verbose = verbose
        self._start_time = None
        self._end_time = None

    def __enter__(self):
        self._start_time = time.clock()
        self._completed_tasks = 0

        if self._verbose:
            print self._start_message
            print "[" + ("{:^%d}" % (self._quantas,)).format("progress") + "]\n",
            print "[",

        return self

    def __exit__(self, type, value, traceback):
        self._end_time = time.clock()
        if self._verbose:
            print "]"
            print "elapsed time: %.3f s\n" % (self._end_time - self._start_time)

    def Increment(self):
        self._completed_tasks += 1
        if self._verbose and ((self._completed_tasks % self._quanta_size) == 0):
            sys.stdout.write(termcolor.colored("=", color=self._bar_color))
            sys.stdout.flush()
