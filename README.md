# Atrevrix Graphe

**This module is a future [OpenPathView](http://opv.li/) module in active developpment.**



<html>
      <strong>This document is written in Broken English</strong><br/>
      <strong>This module is still in active developpement, don't used it in production</strong><br />
      The goal of this module is to create virtual tour from a campaign of panorama taken in a hiking session. <br />
      At the end of the session, you only have the GPS position of the panorama, and it's not simple to link all panorama together to create a virtual tour. A simple way
      to resovle this problem is to take the hour of each panorama as a parameter to link them. But if you have multiples cameras or your cameras are not really precise
       (like time reset), you can't really create a "precise" tour. <br />
      The purpose of this module is to create the most precise tour with only the GPS position of each panrama. To resolv this problem, this module used Graphe and alogrithm like:
      <ul>
        <li>Breadth First Search</h1>
        <li>Dijktra</li>
      </ul>
      The main step of the resolution of this problems are:
      <ul>
        <li>1) Create node in graphe with GPS point of each panorama</li>
        <li>2) Detect near nodes between each nodes</li>
        <li>3) Detect subgraphe and merge them</li>
        <li>4) Search endpoints of the merge graphe</li>
        <li>5) Compute path between endpoints and hotpoints and reduce the graphe</li>
        <li>6) Reduce the node number (take one paramater each X meters)</li>
      </ul>
    </p>
</html>

## How to test

You can used the test.py script that used the test.json data:


```bash
./test.py
```

It will generate 6 files (graphes), one files for each step describe below:

* 01_points.json
* 02_detect_nears_panorama.json
* 03_merge_graphe.json
* 04_get_endpoints.json
* 05_reduce_path.json
* 06_reduce_nodes.json

You can visualize all this grahpe with the html file show_graphe.html. But first you have to launch a HTTP server. Python is our friend:

#### Python2

```bash
python -m SimpleHTTPServer
```

#### Python3

```bash
python3 -m http.server
```

It will launch an HTTP server on port 8000. If you go on [http://127.0.0.1:8000](127.0.0.1:8000) you will got a documentation of what does the module. But if you only want to see the result of each step:

<ul>
<li><a href="http://127.0.0.1:8000/show_graphe.html?name=01_points.json">http://127.0.0.1:8000/show_graphe.html?name=01_points.json</a><br /></li>
<li><a href="http://127.0.0.1:8000/show_graphe.html?name=02_detect_nears_panorama.json">http://127.0.0.1:8000/show_graphe.html?name=02_detect_nears_panorama.json</a><br /></li>
<li><a href="http://127.0.0.1:8000/show_graphe.html?name=03_merge_graphe.json">http://127.0.0.1:8000/show_graphe.html?name=03_merge_graphe.json</a><br /></li>
<li><a href="http://127.0.0.1:8000/show_graphe.html?name=04_get_endpoints.json">http://127.0.0.1:8000/show_graphe.html?name=04_get_endpoints.json</a><br /></li>
<li><a href="http://127.0.0.1:8000/show_graphe.html?name=05_reduce_path.json">http://127.0.0.1:8000/show_graphe.html?name=05_reduce_path.json</a><br /></li>
<li><a href="http://127.0.0.1:8000/show_graphe.html?name=06_reduce_nodes.json">http://127.0.0.1:8000/show_graphe.html?name=06_reduce_nodes.json</a><br /></li>
</ul>

<html>
    <!-- ============================= Create graphe ============================= -->
    <h2>1) Create node in graphe with GPS point of each panorama</h2>
    <p>Just create Node with Point class from yours picture/panorama.<br />
    For example, with your_data.json:</p>

</html>

```python
{
  "457": {
    "longitude": 6.458647,
    "altitude": 1751.628,
    "latitude": 44.976771
  },
  "176": {
    "longitude": 6.467963,
    "altitude": 1623.186,
    "latitude": 44.981512
  }
}
```
This code can be used to create the Graphe:

```python
with open("your_data.json", "r") as fic:
    data = json.load(fic)

graphe = Graphe("Test")
for name, gps in data.items():
    point = Point(
        x=gps["latitude"],
        y=gps["longitude"],
        z=gps["altitude"]
    )

    graphe.create_node(
        name,
        point=point
    )
```
<html>
      </pre>
    </code>
    <p>You can see the graphe: <a href="/show_graphe.html?name=01_points.json">01_points</a></p><br />
    <!-- ============================= Detect near nodes ============================= -->
    <h2>2) Detect nears nodes</h2><br />
    <p>
      To create edges between panorama, we will use a home algorithm that detect near panoras for each panoramas. It have 2 parammeters:<br>
      <ul>
        <li><strong>d</strong> = The maximum distance bewteen two node, to consider it near</li>
        <li><strong>alpha</strong> = The maximum angle between two nodes to consider it near</li>
      </ul>
      For example if we take 5 points (A, B, C, D, E)<br/>
      <img src="img/02_near_nodes_00.png" height="400" width="600"/><br />
      The next steps are run on each point. For the example, we will run it on the A point.
    </p><br />
    <h3>2.1) Detect near nodes with distance</h3>
    <p>
      The first step is to detect the nodes that are <strong>d</strong> meters from the node A.<br />
      <img src="img/02_near_nodes_01.png" height="400" width="600"><br />
      The node that are < <strong>distance</strong> are:
      <ul>
        <li>B</li>
        <li>C</li>
        <li>D</li>
      </ul>
      The nearest node (node B in our example) is take as the referential.<br />
      <img src="img/02_near_nodes_02.png" height="400" width="600"><br />
      Now we will use <strong>alpha</strong> to determine the other near panorama
    </p><br />
    <h3>2.2) Detect near panorama with alpha angle</h3><br />
    <p>
      Now we have our reference point (B), we will consider all node as near if the angle between BAX > <strong>alpha</strong>.<br />
      <img src="img/02_near_nodes_03.png" height="400" width="600"><br />
      <ul>
        <li>Has the BAC angle is <strong>alpha</strong>, we don't take it has a near panorama.</li>
        <li>But the BAD angle is > <strong>alpha</strong>, so we consider it has a near panorama.</li>
      </ul>
      <img src="img/02_near_nodes_04.png" height="400" width="600"><br />
    </p>
    <h3>2.3) Final graphe</h3>
    <p>
      If we run all previous step on each node, we will have this final graphe:<br />
      <img src="img/02_near_nodes_05.png" height="400" width="600"><br />
      And you will understan the main problem. Our tour have holes, we must fill this holes.<br/>
      <a href="/show_graphe.html?name=02_detect_nears_panorama.json">You can see the detect near panoramas with our example here!</a><br />
    </p>
    <h2>3) Detect subgraphe and merge them</h2>
    <p>
      To fill all the holes, we will:
      <ul>
        <li>Detect subgraphe with the <strong>Breadth First Search</strong> algorithm</li>
        <li>Merge all subgraphe</li>
      </ul>
      The detection of the subgraphe is a classical implementation of the <strong>Breadth First Search</strong> algorithm, so I will not describe it.<br />
      But the merge subgraphe algorithm is a home made, so I will describe it here:<br />
      So after the <strong>Breadth First Search</strong> algorithm:
      <img src="img/03_merge_graphe_00.png" height="400" width="600"><br />
      It found 3 subgraphes:<br/>
      <ul>
        <li>D, A, B, C</li>
        <li>E</li>
        <li>F, G, H</li>
      </ul>
      To merge this subpgraphe, we take a subgraphe as a referential (for the example, we will take the graphe D, A, B, C) and we found the nearest subgraphe and merge it.<br/>
      <code>
        <pre>
REF
LIST_SUBGRAPHES
WHEN LIST_SUBGRAPHES NOT EMPTY
  FOUND NEAREST SUBGRAPHE
  MERGE IT WITH REF
END
        </pre>
      </code>
      The nearest subgraphe is E, so we merge it:<br/>
      <img src="img/03_merge_graphe_01.png" height="400" width="600"><br />
      The nearest subgraphe is F, G, H, so we merge it:<br/>
      <img src="img/03_merge_graphe_02.png" height="400" width="600"><br />
      <a href="/show_graphe.html?name=03_merge_graphe.json">You can see the merge graphe with our example here!</a><br />
    </p>
    <h2>4) Search endpoints of the merge graphe</h2>
    <p>
      The actual algorithm is pretty simple, it only consider as endpoint a node that only have one edge.<br />
      <a href="/show_graphe.html?name=04_get_endpoints.json">You can see the endpoints detection with our example here!</a><br />
    </p>
    <h2>5) Compute path between endpoints and hotpoints and reduce the graphe</h3>
    <p>
      For this part, I simply used the <strong>Dijkstra alogrithm</strong> to compute the shortest path between <strong>ALL</strong> endpoints/hot point.<br />
      TODO
      <a href="/show_graphe.html?name=05_reduce_path.json">You can see the path with our example here!</a><br />
    </p>
    <h2>6) Reduce the node number (take one paramater each X meters)</h2>
    <p>
      <strong>TODO</strong>
    </p>
    <a href="/show_graphe.html?name=06_reduce_nodes.json">You can see the reduced path (15 meters) with our example here!</a><br />
</html>

