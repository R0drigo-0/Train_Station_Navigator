# Train Stations Navigator

It's a navigation system that allows the user to find a route on a train map from a given origin and destination and selecting the criterion or preference in the selection of the route to follow.

## Search algorithms:
* **DFS**
* **BFS**
* **UCS**
* **A***

## Project structure
### CityInformation:
It contains information on all available cities, in this case it is only Lyon.

* **Lyon_smallCity:**<br>
  * **InfoVelocity.txt:** contains the information of the speed at which eachline travels. 

  * **Stations.txt:** contains information of stations, for each station, you have ID, name, line number and coordinates where it is located.

  * **Time.txt:**  is a table that shows how long it takes to get from one station to another. If the table value is zero, it means that there is no connection between two stations.

### Code:
* **SearchAlgorithm.py:** Contains the functions necessary to implement the search.
* **TestCase.py:** Contains the code to test the implementation of `Code/SearchAlgorithm.py`
* **TrainStationMap.py:** Contains two main classes.
  * **Map:** Contains all the information about the city.
  * **Path:** Stores the information about a route or set of stops.
* **utils.py:** Contains functions that help to execute `Code/SearchAlgorithm.py`

## External packages:
* **numpy**
* **math**
* **copy**
* **os**
* **unittest**