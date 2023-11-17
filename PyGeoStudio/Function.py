import xml.etree.ElementTree as ET
from .BasePropertiesClass import BasePropertiesClass
import matplotlib.pyplot as plt
import numpy as np

class Function(BasePropertiesClass):
  """
  :param ID: ID of the function (must not be changed)
  :type ID: int
  :param Name: Name of the function
  :type Name: str
  :param Points: XY points to be interpolated and that defined the function
  :type Points: numpy array
  :param Function:
  :type Function:
  :param Estimate:
  :type Estimate:
  :param Types: Type of function. For example, for a function defining a water retention curve of a material, function type is ``["Material", "Hydraulic", "VolWCFun"]``.
  :type Types: list of str
  """
  parameter_type = {
    "ID" : int,
    "Name" : str,
    "Points" : list,
    "Function" : str,
    "Estimate" : str,
    "Types" : list,
  }
  my_data = ["Types"]

  def plot(self):
    """
    Plot the function data using matplotlib
    """
    fig,ax = plt.subplots()
    X = self.data["Points"][:,0]
    Y = self.data["Points"][:,1]
    ax.plot(X,Y,'r', label=self.data["Name"])
    ax.set_xlabel(self.fun_options["InputParam"])
    ax.set_ylabel(self.fun_options["OutputParam"])
    if self.fun_options["LogInput"]: ax.set_yscale('log')
    if self.fun_options["LogOutput"]: ax.set_yscale('log')
    ax.grid()
    ax.legend()
    plt.show()
    return
  
  def getXData(self):
    """
    Helper method to extract the X data of the Points attribute.

    :return: The X datapoints of the function
    :rtype: numpy array
    """
    return self.data["Points"][:,0]

  def setXData(self, values):
    """
    Helper method to set the X data of the Points attribute.
    Size must match the actual X data.

    :param values: The new X data
    :type values: numpy array or list
    """
    self.data["Points"][:,0] = values
    return

  def getYData(self):
    """
    Helper to extract the Y data of the Points attribute.

    :return: The Y datapoints of the function
    :rtype: numpy array
    """
    return self.data["Points"][:,1]

  def setYData(self, values):
    """
    Helper method to set the Y data of the Points attribute.
    Size must match the actual Y data.

    :param values: The new Y data
    :type values: numpy array or list
    """
    self.data["Points"][:,1] = values
    return

  def __initialize__(self):
    self.header = self.data["Points"][0]
    self.tags = [ x[0] for x in self.data["Points"][1:] ]
    self.data["Points"] = np.array( [ [float(x[1]),float(x[2])] for x in self.data["Points"][1:] ] )
    options = [ x.split('=') for x in self.data["Function"].split('(')[-1][:-1].split(',') ]
    self.fun_options = {x[0] : x[1] for x in options }
  
  def __deinitialize__(self):
    self.data["Points"] = [self.header] + [ [x,str(y[0]),str(y[1])] for x,y in zip(self.tags,self.data["Points"]) ]
    return
