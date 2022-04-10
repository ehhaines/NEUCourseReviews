from progress.bar import ChargingBar
#pip install progress

'''
str, float -> None

Creates a "loading bar" based on the input score of a given metric.
'''
def make_data_bar(measure, value):

  class ReviewBar(ChargingBar):
    
    suffix = str(value) + " " + course
  
  print(measure)
  
  bar = ReviewBar(max=100)
  for i in range(int(value * 10)):
    bar.next()
  bar.finish()

