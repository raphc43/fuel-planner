# Fuel Planner API

This project calculates optimized fuel costs along a route using OSRM and station data.

## ---------------------------- Optimzation strategy ----------------------------
1 - I did not implement CACHING, as it is an obvious way to optimize the code in production. It defeats the purpose of
    the first/fresh request speed, which is the most important part of this showcase.

2 - The code executes only one API call as specified in the document to get route (ideal).

3 - However, if the input locations are not present in the DATABASE, only then it makes the second API call.

4 - That second API call actually consists of two requests but I utilized concurrency to make it one. 
    (35%-50% faster compared to calling it seperately).

5 - Input locations are persisted in the DATABASE because location data is relatively static and reusable. 
    Storing previously resolved locations reduces unnecessary external API calls and improves performance for subsequent requests.


6 - Input format (payload):
{
    "start": "New York, NY",
    "end": "Miami, FL"
}


7 - Even for the DATABASE query of input locations, I used concurrency there to make the queries effecient (very small difference).