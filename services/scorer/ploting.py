import numpy
import matplotlib.pyplot as plt


class CustomPloting:
    def make_plot(self, collection):
        trainPredictPlot = numpy.empty_like(collection)
        trainPredictPlot[:] = numpy.nan
        trainPredictPlot[0:len(collection)] = collection
        return trainPredictPlot


    def show_plots(self, testPredict, testY):
        plot1 = self.make_plot(testPredict)
        plot2 = self.make_plot(testY)

        plt.plot(plot1, label='predicted load')
        plt.plot(plot2, label='load')

        plt.legend()
        plt.show()